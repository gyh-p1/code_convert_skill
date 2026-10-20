# Offline Exfiltration model using an in-memory sink and caller-supplied text.
# No files, URLs, sockets, processes, external destinations or host data are used.
# PowerShell byte-array pipeline behavior and finally cleanup are intentional.

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$script:TACTIC = 'Exfiltration'
$script:TACTIC_ID = 'TA0010'
$script:MAX_INPUT = 65536
$script:MAX_PAYLOAD = 4096

class ModelError : System.Exception {
    [string] $Code
    [string] $Field

    ModelError([string] $code, [string] $field) : base($code) {
        $this.Code = $code
        $this.Field = $field
    }
}

function Fail-Model {
    param([string] $Code, [string] $Field)
    throw [ModelError]::new($Code, $Field)
}

function Get-ObjectValue {
    param($Value, [string] $Field)
    if ($Value -isnot [System.Collections.IDictionary]) {
        Fail-Model 'OBJECT_REQUIRED' $Field
    }
    return $Value
}

function Get-ListValue {
    param($Value, [string] $Field, [int] $Maximum)
    if ($Value -isnot [array]) {
        Fail-Model 'LIST_REQUIRED' $Field
    }
    if ($Value.Count -gt $Maximum) {
        Fail-Model 'LIMIT' $Field
    }
    return ,$Value
}

function Get-TextValue {
    param($Value, [string] $Field, [int] $Maximum = 80, [bool] $AllowEmpty = $false)
    if ($Value -isnot [string]) {
        Fail-Model 'TEXT_REQUIRED' $Field
    }
    if ((-not $AllowEmpty -and $Value.Length -eq 0) -or $Value.Length -gt $Maximum) {
        Fail-Model 'TEXT_LENGTH' $Field
    }
    return $Value
}

function Get-IntegerValue {
    param($Value, [string] $Field, [int] $Minimum, [int] $Maximum)
    if ($Value -isnot [int] -and $Value -isnot [long]) {
        Fail-Model 'INTEGER_REQUIRED' $Field
    }
    if ($Value -lt $Minimum -or $Value -gt $Maximum) {
        Fail-Model 'INTEGER_RANGE' $Field
    }
    return [int]$Value
}

function Get-BooleanValue {
    param($Value, [string] $Field)
    if ($Value -isnot [bool]) {
        Fail-Model 'BOOLEAN_REQUIRED' $Field
    }
    return $Value
}

function Get-Field {
    param([System.Collections.IDictionary] $Value, [string] $Key, $Default = $null)
    if ($Value.Contains($Key)) {
        return ,$Value[$Key]
    }
    return ,$Default
}

function Assert-Fields {
    param([System.Collections.IDictionary] $Value, [string[]] $Allowed, [string] $Field)
    $unknown = [System.Collections.Generic.List[string]]::new()
    foreach ($key in $Value.Keys) {
        if ($Allowed -cnotcontains $key) {
            $unknown.Add($key)
        }
    }
    $unknown.Sort([System.StringComparer]::Ordinal)
    if ($unknown.Count -ne 0) {
        Fail-Model 'UNKNOWN_FIELD' ($Field + '.' + $unknown[0])
    }
}

function Get-Bytes {
    param([string] $Text)
    $encoder = [System.Text.UTF8Encoding]::new($false, $true)
    try {
        [byte[]]$data = $encoder.GetBytes($Text)
    }
    catch [System.Text.EncoderFallbackException] {
        Fail-Model 'UNENCODABLE_TEXT' 'text'
    }
    if ($data.Length -gt $script:MAX_PAYLOAD) {
        Fail-Model 'PAYLOAD_LIMIT' 'text'
    }
    return ,$data
}

function Get-Hex {
    param([byte[]] $Data)
    return [System.Convert]::ToHexString($Data).ToLowerInvariant()
}

function Get-Digest {
    param([byte[]] $Data)
    $algorithm = [System.Security.Cryptography.SHA256]::Create()
    try {
        return Get-Hex ($algorithm.ComputeHash($Data))
    }
    finally {
        $algorithm.Dispose()
    }
}

function Copy-Bytes {
    param([byte[]] $Data)
    $copy = [byte[]]::new($Data.Length)
    [System.Array]::Copy($Data, $copy, $Data.Length)
    return ,$copy
}

function Get-Chunk {
    param([byte[]] $Data, [int] $Index, [int] $Size)
    $start = $Index * $Size
    if ($start -ge $Data.Length) {
        return ,([byte[]]::new(0))
    }
    $length = [Math]::Min($Size, $Data.Length - $start)
    $result = [byte[]]::new($length)
    [System.Array]::Copy($Data, $start, $result, 0, $length)
    return ,$result
}

function New-Transfer {
    param([System.Collections.IDictionary] $Document)
    $text = Get-TextValue (Get-Field $Document 'text') 'text' 4096 $true
    $size = Get-IntegerValue (Get-Field $Document 'chunk_size' 4) 'chunk_size' 1 256
    [byte[]]$data = Get-Bytes $text
    $total = [int][Math]::Ceiling($data.Length / [double]$size)
    return @{
        Data = $data
        Size = $size
        Total = $total
        Digest = Get-Digest $data
        Packets = [System.Collections.Generic.Dictionary[int, byte[]]]::new()
        Attempts = 0
        Duplicates = 0
        ActiveBuffers = 0
        ClosedBuffers = 0
        Committed = $false
        Cancelled = $false
        Audit = [System.Collections.Generic.List[object]]::new()
    }
}

function Add-Event {
    param([hashtable] $Transfer, [string] $Action, [int] $Index = -1)
    $Transfer.Audit.Add(@{
        action = $Action
        index = $Index
        attempts = $Transfer.Attempts
    })
}

function Assert-Open {
    param([hashtable] $Transfer)
    if ($Transfer.Cancelled) {
        Fail-Model 'TRANSFER_CANCELLED' 'transfer'
    }
    if ($Transfer.Committed) {
        Fail-Model 'TRANSFER_COMMITTED' 'transfer'
    }
}

function Receive-Packet {
    param([hashtable] $Transfer, [int] $Index, [byte[]] $Data)
    if ($Transfer.Packets.ContainsKey($Index)) {
        $old = Get-Hex $Transfer.Packets[$Index]
        $new = Get-Hex $Data
        if ($old -cne $new) {
            Fail-Model 'PACKET_CONFLICT' 'index'
        }
        $Transfer.Duplicates++
        Add-Event $Transfer 'duplicate' $Index
        return $false
    }
    $Transfer.Packets.Add($Index, (Copy-Bytes $Data))
    Add-Event $Transfer 'receive' $Index
    return $true
}

function Send-Packet {
    param([hashtable] $Transfer, [int] $Index, [bool] $Corrupt, [bool] $Fail)
    Assert-Open $Transfer
    [byte[]]$buffer = Get-Chunk $Transfer.Data $Index $Transfer.Size
    $Transfer.ActiveBuffers++
    $Transfer.Attempts++
    Add-Event $Transfer 'open_buffer' $Index
    try {
        if ($Fail) {
            Fail-Model 'INJECTED_FAILURE' 'buffer'
        }
        if ($Corrupt -and $buffer.Length -gt 0) {
            $buffer[0] = $buffer[0] -bxor 1
        }
        $accepted = Receive-Packet $Transfer $Index $buffer
        return @{ index = $Index; accepted = $accepted; bytes = $buffer.Length }
    }
    finally {
        [System.Array]::Clear($buffer, 0, $buffer.Length)
        $Transfer.ActiveBuffers--
        $Transfer.ClosedBuffers++
        Add-Event $Transfer 'close_buffer' $Index
    }
}

function Get-Missing {
    param([hashtable] $Transfer)
    $result = [System.Collections.Generic.List[int]]::new()
    for ($index = 0; $index -lt $Transfer.Total; $index++) {
        if (-not $Transfer.Packets.ContainsKey($index)) {
            $result.Add($index)
        }
    }
    return ,($result.ToArray())
}

function Join-Packets {
    param([hashtable] $Transfer)
    $result = [System.Collections.Generic.List[byte]]::new()
    for ($index = 0; $index -lt $Transfer.Total; $index++) {
        if (-not $Transfer.Packets.ContainsKey($index)) {
            Fail-Model 'MISSING_PACKET' 'packets'
        }
        $result.AddRange($Transfer.Packets[$index])
    }
    return ,($result.ToArray())
}

function Complete-Transfer {
    param([hashtable] $Transfer)
    Assert-Open $Transfer
    [byte[]]$joined = Join-Packets $Transfer
    $digest = Get-Digest $joined
    if ($digest -cne $Transfer.Digest) {
        Fail-Model 'DIGEST_MISMATCH' 'packets'
    }
    $Transfer.Committed = $true
    Add-Event $Transfer 'commit'
    return @{ committed = $true; bytes = $joined.Length; sha256 = $digest }
}

function Remove-Packet {
    param([hashtable] $Transfer, [int] $Index)
    Assert-Open $Transfer
    $removed = $Transfer.Packets.Remove($Index)
    Add-Event $Transfer 'remove' $Index
    return @{ removed = $removed; index = $Index }
}

function Stop-Transfer {
    param([hashtable] $Transfer)
    Assert-Open $Transfer
    $count = $Transfer.Packets.Count
    $Transfer.Packets.Clear()
    $Transfer.Cancelled = $true
    Add-Event $Transfer 'cancel'
    return @{ cancelled = $true; removed = $count }
}

function Get-Status {
    param([hashtable] $Transfer)
    [int[]]$missing = Get-Missing $Transfer
    return @{
        total_chunks = $Transfer.Total
        received_chunks = $Transfer.Packets.Count
        missing = $missing
        attempts = $Transfer.Attempts
        duplicates = $Transfer.Duplicates
        active_buffers = $Transfer.ActiveBuffers
        closed_buffers = $Transfer.ClosedBuffers
        committed = $Transfer.Committed
        cancelled = $Transfer.Cancelled
    }
}

function Get-PacketStatistics {
    param([hashtable] $Transfer)
    $totalBytes = 0
    $minimum = $null
    $maximum = 0
    foreach ($packet in $Transfer.Packets.Values) {
        $totalBytes += $packet.Length
        if ($null -eq $minimum -or $packet.Length -lt $minimum) {
            $minimum = $packet.Length
        }
        if ($packet.Length -gt $maximum) {
            $maximum = $packet.Length
        }
    }
    return @{
        received_bytes = $totalBytes
        minimum_chunk = $minimum
        maximum_chunk = $maximum
        remaining_bytes = $Transfer.Data.Length - $totalBytes
        complete = ($Transfer.Packets.Count -eq $Transfer.Total)
    }
}

function Export-Transfer {
    param([hashtable] $Transfer)
    $packets = [System.Collections.Generic.List[object]]::new()
    for ($index = 0; $index -lt $Transfer.Total; $index++) {
        if ($Transfer.Packets.ContainsKey($index)) {
            $data = $Transfer.Packets[$index]
            $packets.Add(@{
                index = $index
                hex = Get-Hex $data
                bytes = $data.Length
            })
        }
    }
    $audit = [System.Collections.Generic.List[object]]::new()
    foreach ($event in $Transfer.Audit) {
        $audit.Add($event.Clone())
    }
    return @{
        status = Get-Status $Transfer
        packet_statistics = Get-PacketStatistics $Transfer
        packets = $packets.ToArray()
        input_bytes = $Transfer.Data.Length
        sha256 = $Transfer.Digest
        audit = $audit.ToArray()
    }
}

function Invoke-SendAll {
    param([hashtable] $Transfer, [System.Collections.IDictionary] $Operation)
    Assert-Fields $Operation @('op', 'fail_after') 'operation'
    Assert-Open $Transfer
    $failAfter = Get-Field $Operation 'fail_after'
    if ($null -ne $failAfter) {
        $failAfter = Get-IntegerValue $failAfter 'fail_after' 1 4096
    }
    $sent = [System.Collections.Generic.List[object]]::new()
    [int[]]$missing = Get-Missing $Transfer
    foreach ($index in $missing) {
        $fail = ($null -ne $failAfter -and $sent.Count + 1 -eq $failAfter)
        $sent.Add((Send-Packet $Transfer $index $false $fail))
    }
    return @{ sent = $sent.ToArray() }
}

function Invoke-Operation {
    param([hashtable] $Transfer, $Raw)
    $operation = Get-ObjectValue $Raw 'operation'
    $kind = Get-TextValue (Get-Field $operation 'op') 'op'
    switch -CaseSensitive ($kind) {
        'send_all' {
            return Invoke-SendAll $Transfer $operation
        }
        'send' {
            Assert-Fields $operation @('op', 'index', 'corrupt', 'fail') 'operation'
            $index = Get-IntegerValue (Get-Field $operation 'index') 'index' 0 ($Transfer.Total - 1)
            $corrupt = Get-BooleanValue (Get-Field $operation 'corrupt' $false) 'corrupt'
            $fail = Get-BooleanValue (Get-Field $operation 'fail' $false) 'fail'
            return Send-Packet $Transfer $index $corrupt $fail
        }
        'remove' {
            Assert-Fields $operation @('op', 'index') 'operation'
            $index = Get-IntegerValue (Get-Field $operation 'index') 'index' 0 ($Transfer.Total - 1)
            return Remove-Packet $Transfer $index
        }
        'commit' {
            Assert-Fields $operation @('op') 'operation'
            return Complete-Transfer $Transfer
        }
        'cancel' {
            Assert-Fields $operation @('op') 'operation'
            return Stop-Transfer $Transfer
        }
        'status' {
            Assert-Fields $operation @('op') 'operation'
            return Get-Status $Transfer
        }
        default {
            Fail-Model 'UNKNOWN_OPERATION' 'op'
        }
    }
}

function Invoke-Simulation {
    param($Raw)
    $document = Get-ObjectValue $Raw 'input'
    Assert-Fields $document @('text', 'chunk_size', 'operations') 'input'
    $transfer = New-Transfer $document
    $operations = Get-ListValue (Get-Field $document 'operations') 'operations' 128
    $outcomes = [System.Collections.Generic.List[object]]::new()
    for ($index = 0; $index -lt $operations.Count; $index++) {
        try {
            $result = Invoke-Operation $transfer $operations[$index]
            $outcomes.Add(@{
                index = $index
                ok = $true
                result = $result
            })
        }
        catch [ModelError] {
            $outcomes.Add(@{
                index = $index
                ok = $false
                error = @{
                    code = $_.Exception.Code
                    field = $_.Exception.Field
                }
            })
        }
    }
    return @{
        tactic = $script:TACTIC
        tactic_id = $script:TACTIC_ID
        simulation = $true
        outcomes = $outcomes.ToArray()
        state = Export-Transfer $transfer
    }
}

function Read-Document {
    $inputStream = [Console]::OpenStandardInput()
    $memory = [System.IO.MemoryStream]::new()
    $buffer = [byte[]]::new(1024)
    try {
        while ($memory.Length -le $script:MAX_INPUT) {
            $remaining = $script:MAX_INPUT + 1 - $memory.Length
            $count = $inputStream.Read($buffer, 0, [Math]::Min($buffer.Length, $remaining))
            if ($count -eq 0) {
                break
            }
            $memory.Write($buffer, 0, $count)
        }
        if ($memory.Length -gt $script:MAX_INPUT) {
            Fail-Model 'INPUT_TOO_LARGE' 'input'
        }
        $encoding = [System.Text.UTF8Encoding]::new($false, $true)
        try {
            $text = $encoding.GetString($memory.ToArray())
        }
        catch [System.Text.DecoderFallbackException] {
            Fail-Model 'INVALID_UTF8' 'input'
        }
    }
    finally {
        $memory.Dispose()
    }
    try {
        return ConvertFrom-Json -InputObject $text -AsHashtable -NoEnumerate -Depth 64
    }
    catch {
        Fail-Model 'INVALID_JSON' 'input'
    }
}

function Write-Document {
    param($Document)
    $text = ConvertTo-Json -InputObject $Document -Depth 64 -Compress
    $encoding = [System.Text.UTF8Encoding]::new($false)
    [byte[]]$bytes = $encoding.GetBytes($text + "`n")
    $outputStream = [Console]::OpenStandardOutput()
    $outputStream.Write($bytes, 0, $bytes.Length)
    $outputStream.Flush()
}

$exitCode = 0
try {
    $result = Invoke-Simulation (Read-Document)
}
catch [ModelError] {
    $result = @{
        simulation = $true
        error = @{
            code = $_.Exception.Code
            field = $_.Exception.Field
        }
    }
    $exitCode = 2
}
Write-Document $result
exit $exitCode
