// Credential Access over fictional records supplied on stdin.
// This specimen never opens credential stores, files, sockets or processes.
// A secret is an inert fixture label. Deferred lease cleanup is observable.
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"os"
	"sort"
	"strconv"
	"strings"
	"unicode/utf8"
)

const TACTIC = "Credential Access"
const TACTIC_ID = "TA0006"
const MAX_INPUT = 65536
const MAX_RECORDS = 32
const MAX_OPERATIONS = 128

type ModelError struct {
	Code  string `json:"code"`
	Field string `json:"field"`
}

func (e *ModelError) Error() string {
	return e.Code + ":" + e.Field
}

func problem(code string, field string) error {
	return &ModelError{Code: code, Field: field}
}

func objectValue(value any, field string) (map[string]any, error) {
	result, ok := value.(map[string]any)
	if !ok {
		return nil, problem("OBJECT_REQUIRED", field)
	}
	return result, nil
}

func listValue(value any, field string, maximum int) ([]any, error) {
	result, ok := value.([]any)
	if !ok {
		return nil, problem("LIST_REQUIRED", field)
	}
	if len(result) > maximum {
		return nil, problem("LIMIT", field)
	}
	return result, nil
}

func textValue(value any, field string) (string, error) {
	result, ok := value.(string)
	if !ok {
		return "", problem("TEXT_REQUIRED", field)
	}
	if utf8.RuneCountInString(result) < 1 || utf8.RuneCountInString(result) > 80 {
		return "", problem("TEXT_LENGTH", field)
	}
	for _, character := range result {
		if character < 32 {
			return "", problem("CONTROL_CHARACTER", field)
		}
	}
	return result, nil
}

func integerValue(value any, field string, maximum int) (int, error) {
	number, ok := value.(json.Number)
	if !ok {
		return 0, problem("INTEGER_REQUIRED", field)
	}
	parsed, err := strconv.ParseInt(string(number), 10, 32)
	if err != nil {
		return 0, problem("INTEGER_REQUIRED", field)
	}
	if parsed < 0 || parsed > int64(maximum) {
		return 0, problem("INTEGER_RANGE", field)
	}
	return int(parsed), nil
}

func booleanValue(value any, field string) (bool, error) {
	result, ok := value.(bool)
	if !ok {
		return false, problem("BOOLEAN_REQUIRED", field)
	}
	return result, nil
}

func withDefault(object map[string]any, key string, fallback any) any {
	value, exists := object[key]
	if exists {
		return value
	}
	return fallback
}

func fields(object map[string]any, permitted string, field string) error {
	allowed := strings.Fields(permitted)
	unknown := []string{}
	for key := range object {
		found := false
		for _, name := range allowed {
			if key == name {
				found = true
				break
			}
		}
		if !found {
			unknown = append(unknown, key)
		}
	}
	sort.Strings(unknown)
	if len(unknown) != 0 {
		return problem("UNKNOWN_FIELD", field+"."+unknown[0])
	}
	return nil
}

type CredentialRecord struct {
	Name     string
	Account  string
	Secret   string
	Expires  int
	Version  int
	Disabled bool
}

func parseRecord(value any) (*CredentialRecord, error) {
	object, err := objectValue(value, "record")
	if err != nil {
		return nil, err
	}
	if err = fields(object, "name account secret expires disabled", "record"); err != nil {
		return nil, err
	}
	name, err := textValue(object["name"], "name")
	if err != nil {
		return nil, err
	}
	account, err := textValue(object["account"], "account")
	if err != nil {
		return nil, err
	}
	secret, err := textValue(object["secret"], "secret")
	if err != nil {
		return nil, err
	}
	if !strings.HasPrefix(secret, "fixture:") {
		return nil, problem("SYNTHETIC_SECRET_REQUIRED", "secret")
	}
	expires, err := integerValue(withDefault(object, "expires", json.Number("1000")), "expires", 10000)
	if err != nil {
		return nil, err
	}
	disabled, err := booleanValue(withDefault(object, "disabled", false), "disabled")
	if err != nil {
		return nil, err
	}
	return &CredentialRecord{
		Name: name,
		Account: account,
		Secret: secret,
		Expires: expires,
		Version: 0,
		Disabled: disabled,
	}, nil
}

func (record *CredentialRecord) publicView() map[string]any {
	return map[string]any{
		"name": record.Name,
		"account": record.Account,
		"secret": "[synthetic-redacted]",
		"expires": record.Expires,
		"version": record.Version,
		"disabled": record.Disabled,
	}
}

type Lease struct {
	Name   string
	Closed bool
	Buffer []byte
}

type CredentialVault struct {
	Records map[string]*CredentialRecord
	Tick    int
	Active  int
	Closed  int
	Audit   []map[string]any
}

func newVault(values any) (*CredentialVault, error) {
	items, err := listValue(values, "records", MAX_RECORDS)
	if err != nil {
		return nil, err
	}
	vault := &CredentialVault{
		Records: map[string]*CredentialRecord{},
		Audit: []map[string]any{},
	}
	for _, item := range items {
		record, err := parseRecord(item)
		if err != nil {
			return nil, err
		}
		if _, exists := vault.Records[record.Name]; exists {
			return nil, problem("DUPLICATE_RECORD", "name")
		}
		vault.Records[record.Name] = record
	}
	return vault, nil
}

func (vault *CredentialVault) recordEvent(action string, name string) {
	vault.Audit = append(vault.Audit, map[string]any{
		"action": action,
		"name": name,
		"tick": vault.Tick,
	})
}

func (vault *CredentialVault) find(value any) (*CredentialRecord, error) {
	name, err := textValue(value, "name")
	if err != nil {
		return nil, err
	}
	record, exists := vault.Records[name]
	if !exists {
		return nil, problem("RECORD_NOT_FOUND", "name")
	}
	return record, nil
}

func (vault *CredentialVault) acquire(record *CredentialRecord) (*Lease, error) {
	if record.Disabled {
		return nil, problem("RECORD_DISABLED", "name")
	}
	if vault.Tick >= record.Expires {
		return nil, problem("RECORD_EXPIRED", "name")
	}
	vault.Active++
	vault.recordEvent("acquire", record.Name)
	return &Lease{Name: record.Name, Buffer: []byte(record.Secret)}, nil
}

func (vault *CredentialVault) release(lease *Lease) {
	if lease.Closed {
		return
	}
	for index := range lease.Buffer {
		lease.Buffer[index] = 0
	}
	lease.Buffer = nil
	lease.Closed = true
	vault.Active--
	vault.Closed++
	vault.recordEvent("release", lease.Name)
}

// Cleanup changes virtual counters; this is not a secure-erasure guarantee.
func (vault *CredentialVault) inspect(operation map[string]any) (any, error) {
	record, err := vault.find(operation["name"])
	if err != nil {
		return nil, err
	}
	fail, err := booleanValue(withDefault(operation, "fail", false), "fail")
	if err != nil {
		return nil, err
	}
	lease, err := vault.acquire(record)
	if err != nil {
		return nil, err
	}
	defer vault.release(lease)
	if fail {
		return nil, problem("INJECTED_FAILURE", "lease")
	}
	vault.recordEvent("inspect", record.Name)
	return map[string]any{
		"record": record.publicView(),
		"synthetic_bytes": len(lease.Buffer),
	}, nil
}

func (vault *CredentialVault) compare(operation map[string]any) (any, error) {
	record, err := vault.find(operation["name"])
	if err != nil {
		return nil, err
	}
	candidate, err := textValue(operation["candidate"], "candidate")
	if err != nil {
		return nil, err
	}
	if !strings.HasPrefix(candidate, "fixture:") {
		return nil, problem("SYNTHETIC_SECRET_REQUIRED", "candidate")
	}
	lease, err := vault.acquire(record)
	if err != nil {
		return nil, err
	}
	defer vault.release(lease)
	matched := bytes.Equal(lease.Buffer, []byte(candidate))
	vault.recordEvent("compare", record.Name)
	return map[string]any{"matched": matched}, nil
}

func (vault *CredentialVault) rotate(operation map[string]any) (any, error) {
	record, err := vault.find(operation["name"])
	if err != nil {
		return nil, err
	}
	secret, err := textValue(operation["secret"], "secret")
	if err != nil {
		return nil, err
	}
	if !strings.HasPrefix(secret, "fixture:") {
		return nil, problem("SYNTHETIC_SECRET_REQUIRED", "secret")
	}
	expected, err := integerValue(operation["expected"], "expected", 10000)
	if err != nil {
		return nil, err
	}
	if expected != record.Version {
		return nil, problem("VERSION_CONFLICT", "expected")
	}
	record.Secret = secret
	record.Version++
	vault.recordEvent("rotate", record.Name)
	return map[string]any{"version": record.Version}, nil
}

func (vault *CredentialVault) export() map[string]any {
	names := []string{}
	for name := range vault.Records {
		names = append(names, name)
	}
	sort.Strings(names)
	records := []any{}
	for _, name := range names {
		records = append(records, vault.Records[name].publicView())
	}
	return map[string]any{
		"records": records,
		"tick": vault.Tick,
		"active_leases": vault.Active,
		"closed_leases": vault.Closed,
		"audit": vault.Audit,
	}
}

var OP_FIELDS = map[string]string{
	"inspect": "op name fail",
	"compare": "op name candidate",
	"rotate": "op name secret expected",
	"disable": "op name disabled",
	"advance": "op delta",
	"catalog": "op",
}

func (vault *CredentialVault) dispatch(value any) (any, error) {
	operation, err := objectValue(value, "operation")
	if err != nil {
		return nil, err
	}
	kind, err := textValue(operation["op"], "op")
	if err != nil {
		return nil, err
	}
	permitted, exists := OP_FIELDS[kind]
	if !exists {
		return nil, problem("UNKNOWN_OPERATION", "op")
	}
	if err = fields(operation, permitted, "operation"); err != nil {
		return nil, err
	}
	switch kind {
	case "inspect":
		return vault.inspect(operation)
	case "compare":
		return vault.compare(operation)
	case "rotate":
		return vault.rotate(operation)
	case "catalog":
		return vault.export(), nil
	case "disable":
		record, err := vault.find(operation["name"])
		if err != nil {
			return nil, err
		}
		disabled, err := booleanValue(operation["disabled"], "disabled")
		if err != nil {
			return nil, err
		}
		record.Disabled = disabled
		vault.recordEvent("disable", record.Name)
		return map[string]any{"disabled": disabled}, nil
	default:
		delta, err := integerValue(operation["delta"], "delta", 10000)
		if err != nil {
			return nil, err
		}
		if vault.Tick + delta > 10000 {
			return nil, problem("INTEGER_RANGE", "tick")
		}
		vault.Tick += delta
		return map[string]any{"tick": vault.Tick}, nil
	}
}

func simulate(value any) (any, error) {
	document, err := objectValue(value, "input")
	if err != nil {
		return nil, err
	}
	if err = fields(document, "records operations", "input"); err != nil {
		return nil, err
	}
	vault, err := newVault(withDefault(document, "records", []any{}))
	if err != nil {
		return nil, err
	}
	operations, err := listValue(document["operations"], "operations", MAX_OPERATIONS)
	if err != nil {
		return nil, err
	}
	outcomes := []any{}
	for index, operation := range operations {
		result, err := vault.dispatch(operation)
		if err != nil {
			outcomes = append(outcomes, map[string]any{
				"index": index, "ok": false, "error": err,
			})
		} else {
			// Serialize a snapshot so subsequent mutation cannot change old observations.
			encoded, marshalErr := json.Marshal(result)
			if marshalErr != nil {
				return nil, problem("SERIALIZATION", "result")
			}
			outcomes = append(outcomes, map[string]any{
				"index": index, "ok": true, "result": json.RawMessage(encoded),
			})
		}
	}
	return map[string]any{
		"tactic": TACTIC,
		"tactic_id": TACTIC_ID,
		"simulation": true,
		"outcomes": outcomes,
		"state": vault.export(),
	}, nil
}

func readDocument() (any, error) {
	raw, err := io.ReadAll(io.LimitReader(os.Stdin, MAX_INPUT + 1))
	if err != nil {
		return nil, problem("INPUT_READ", "input")
	}
	if len(raw) > MAX_INPUT {
		return nil, problem("INPUT_TOO_LARGE", "input")
	}
	if !utf8.Valid(raw) {
		return nil, problem("INVALID_UTF8", "input")
	}
	decoder := json.NewDecoder(bytes.NewReader(raw))
	decoder.UseNumber()
	var value any
	if err := decoder.Decode(&value); err != nil {
		return nil, problem("INVALID_JSON", "input")
	}
	var trailing any
	if decoder.Decode(&trailing) != io.EOF {
		return nil, problem("INVALID_JSON", "input")
	}
	return value, nil
}

func run() int {
	value, err := readDocument()
	var result any
	if err == nil {
		result, err = simulate(value)
	}
	code := 0
	if err != nil {
		result = map[string]any{"simulation": true, "error": err}
		code = 2
	}
	encoded, encodeErr := json.Marshal(result)
	if encodeErr != nil {
		fmt.Fprintln(os.Stderr, "SERIALIZATION")
		return 3
	}
	if _, err := fmt.Fprintln(os.Stdout, string(encoded)); err != nil {
		return 3
	}
	return code
}

func main() {
	os.Exit(run())
}
