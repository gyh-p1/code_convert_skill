// Collection from fictional documents embedded in JSON input.
// Paths are virtual keys. No filesystem, process or network API is used.
// Iterator disposal, UTF-8 byte quotas and rollback are observable semantics.
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.Json;
using System.Text.Json.Nodes;

namespace CollectionLab;

public sealed class ModelError : Exception
{
    public string Code { get; }
    public string Field { get; }

    public ModelError(string code, string field) : base(code)
    {
        Code = code;
        Field = field;
    }

    public JsonObject AsJson()
    {
        return new JsonObject
        {
            ["code"] = Code,
            ["field"] = Field,
        };
    }
}

public static class Input
{
    public static JsonObject Object(JsonNode? value, string field)
    {
        if (value is not JsonObject result)
        {
            throw new ModelError("OBJECT_REQUIRED", field);
        }
        return result;
    }

    public static JsonArray Array(JsonNode? value, string field, int maximum)
    {
        if (value is not JsonArray result)
        {
            throw new ModelError("LIST_REQUIRED", field);
        }
        if (result.Count > maximum)
        {
            throw new ModelError("LIMIT", field);
        }
        return result;
    }

    public static string Text(JsonNode? value, string field, int maximum = 80)
    {
        if (value is not JsonValue scalar || !scalar.TryGetValue<string>(out var text))
        {
            throw new ModelError("TEXT_REQUIRED", field);
        }
        if (text.Length == 0 || text.EnumerateRunes().Count() > maximum)
        {
            throw new ModelError("TEXT_LENGTH", field);
        }
        if (text.Any(character => character < 32))
        {
            throw new ModelError("CONTROL_CHARACTER", field);
        }
        return text;
    }

    public static int Integer(JsonNode? value, string field, int minimum, int maximum)
    {
        if (value is not JsonValue scalar || !scalar.TryGetValue<int>(out var number))
        {
            throw new ModelError("INTEGER_REQUIRED", field);
        }
        if (number < minimum || number > maximum)
        {
            throw new ModelError("INTEGER_RANGE", field);
        }
        return number;
    }

    public static bool Boolean(JsonNode? value, string field)
    {
        if (value is not JsonValue scalar || !scalar.TryGetValue<bool>(out var result))
        {
            throw new ModelError("BOOLEAN_REQUIRED", field);
        }
        return result;
    }

    public static void Fields(JsonObject value, string allowed, string field)
    {
        var names = allowed.Split(' ').ToHashSet(StringComparer.Ordinal);
        var unknown = value.Select(pair => pair.Key)
            .Where(key => !names.Contains(key))
            .OrderBy(key => key, StringComparer.Ordinal)
            .FirstOrDefault();
        if (unknown is not null)
        {
            throw new ModelError("UNKNOWN_FIELD", field + "." + unknown);
        }
    }

    public static JsonNode? Default(JsonObject value, string key, JsonNode fallback)
    {
        return value.ContainsKey(key) ? value[key] : fallback;
    }

    public static string VirtualPath(JsonNode? value)
    {
        var path = Text(value, "path", 160);
        if (!path.StartsWith("/lab/", StringComparison.Ordinal))
        {
            throw new ModelError("VIRTUAL_ROOT", "path");
        }
        var segments = path.Split('/').Skip(1);
        if (path.Contains('\\') || segments.Any(part => part is "" or "." or ".."))
        {
            throw new ModelError("VIRTUAL_PATH", "path");
        }
        return path;
    }
}

public sealed record VirtualDocument(
    string Path,
    string Owner,
    string Text,
    string Category,
    bool Readable,
    int Revision)
{
    public int ByteLength => Encoding.UTF8.GetByteCount(Text);

    public static VirtualDocument FromInput(JsonNode? node)
    {
        var value = Input.Object(node, "document");
        Input.Fields(value, "path owner text category readable revision", "document");
        return new VirtualDocument(
            Input.VirtualPath(value["path"]),
            Input.Text(Input.Default(value, "owner", JsonValue.Create("lab-user")!), "owner"),
            Input.Text(value["text"], "text", 4096),
            Input.Text(Input.Default(value, "category", JsonValue.Create("note")!), "category"),
            Input.Boolean(Input.Default(value, "readable", JsonValue.Create(true)!), "readable"),
            Input.Integer(Input.Default(value, "revision", JsonValue.Create(0)!), "revision", 0, 1000)
        );
    }

    public JsonObject AsJson()
    {
        return new JsonObject
        {
            ["path"] = Path,
            ["owner"] = Owner,
            ["text"] = Text,
            ["category"] = Category,
            ["readable"] = Readable,
            ["revision"] = Revision,
            ["bytes"] = ByteLength,
        };
    }
}

public sealed class VirtualRepository
{
    public SortedDictionary<string, VirtualDocument> Documents { get; } =
        new(StringComparer.Ordinal);
    public int ActiveReaders { get; private set; }
    public int ClosedReaders { get; private set; }
    public JsonArray Audit { get; } = new();

    public VirtualRepository(JsonNode? values)
    {
        foreach (var value in Input.Array(values, "documents", 32))
        {
            var document = VirtualDocument.FromInput(value);
            if (!Documents.TryAdd(document.Path, document))
            {
                throw new ModelError("DUPLICATE_PATH", "path");
            }
        }
    }

    public IEnumerable<VirtualDocument> ReadCandidates(string category)
    {
        ActiveReaders++;
        Audit.Add(new JsonObject { ["event"] = "open_reader" });
        try
        {
            foreach (var document in Documents.Values)
            {
                if (category != "*" && document.Category != category)
                {
                    continue;
                }
                yield return document;
            }
        }
        finally
        {
            ActiveReaders--;
            ClosedReaders++;
            Audit.Add(new JsonObject { ["event"] = "close_reader" });
        }
    }

    public VirtualDocument Find(JsonNode? value)
    {
        var path = Input.VirtualPath(value);
        if (!Documents.TryGetValue(path, out var document))
        {
            throw new ModelError("DOCUMENT_NOT_FOUND", "path");
        }
        return document;
    }

    public JsonObject Export()
    {
        var documents = new JsonArray();
        foreach (var document in Documents.Values)
        {
            documents.Add(document.AsJson());
        }
        return new JsonObject
        {
            ["documents"] = documents,
            ["active_readers"] = ActiveReaders,
            ["closed_readers"] = ClosedReaders,
            ["audit"] = Audit.DeepClone(),
        };
    }
}

public sealed class CollectionSession
{
    public VirtualRepository Repository { get; }
    public SortedDictionary<string, VirtualDocument> Staged { get; private set; } =
        new(StringComparer.Ordinal);
    public JsonArray Outcomes { get; } = new();
    public int Quota { get; }
    public int Generation { get; private set; }

    public CollectionSession(VirtualRepository repository, int quota)
    {
        Repository = repository;
        Quota = quota;
    }

    public int TotalBytes()
    {
        return Staged.Values.Sum(document => document.ByteLength);
    }

    public void Stage(VirtualDocument document, bool replace)
    {
        if (!document.Readable)
        {
            throw new ModelError("READ_DENIED", "path");
        }
        var existingBytes = 0;
        if (Staged.TryGetValue(document.Path, out var old))
        {
            if (!replace)
            {
                throw new ModelError("ALREADY_STAGED", "path");
            }
            existingBytes = old.ByteLength;
        }
        if (TotalBytes() - existingBytes + document.ByteLength > Quota)
        {
            throw new ModelError("QUOTA_EXCEEDED", "quota");
        }
        Staged[document.Path] = document;
        Generation++;
    }

    public JsonObject Collect(JsonObject value)
    {
        Input.Fields(value, "op category limit atomic replace fail_after", "operation");
        var category = Input.Text(
            Input.Default(value, "category", JsonValue.Create("*")!), "category"
        );
        var limit = Input.Integer(
            Input.Default(value, "limit", JsonValue.Create(32)!), "limit", 0, 32
        );
        var atomic = Input.Boolean(
            Input.Default(value, "atomic", JsonValue.Create(true)!), "atomic"
        );
        var replace = Input.Boolean(
            Input.Default(value, "replace", JsonValue.Create(false)!), "replace"
        );
        int? failAfter = value["fail_after"] is null ? null :
            Input.Integer(value["fail_after"], "fail_after", 1, 32);
        var before = new SortedDictionary<string, VirtualDocument>(Staged, StringComparer.Ordinal);
        var beforeGeneration = Generation;
        var collected = new JsonArray();
        try
        {
            if (limit > 0)
            {
                foreach (var document in Repository.ReadCandidates(category))
                {
                    Stage(document, replace);
                    collected.Add(document.Path);
                    if (collected.Count == failAfter)
                    {
                        throw new ModelError("INJECTED_FAILURE", "collection");
                    }
                    if (collected.Count == limit)
                    {
                        break;
                    }
                }
            }
        }
        catch (ModelError)
        {
            if (atomic)
            {
                Staged = before;
                Generation = beforeGeneration;
            }
            throw;
        }
        return new JsonObject { ["collected"] = collected, ["bytes"] = TotalBytes() };
    }

    public JsonObject Manifest()
    {
        var entries = new JsonArray();
        foreach (var document in Staged.Values)
        {
            entries.Add(new JsonObject
            {
                ["path"] = document.Path,
                ["owner"] = document.Owner,
                ["bytes"] = document.ByteLength,
                ["revision"] = document.Revision,
                ["category"] = document.Category,
            });
        }
        return new JsonObject
        {
            ["entries"] = entries,
            ["bytes"] = TotalBytes(),
            ["generation"] = Generation,
        };
    }

    public JsonObject Dispatch(JsonNode? node)
    {
        var value = Input.Object(node, "operation");
        var operation = Input.Text(value["op"], "op");
        switch (operation)
        {
            case "collect":
                return Collect(value);
            case "manifest":
                Input.Fields(value, "op", "operation");
                return Manifest();
            case "inspect":
                Input.Fields(value, "op path", "operation");
                var document = Repository.Find(value["path"]);
                if (!document.Readable)
                {
                    throw new ModelError("READ_DENIED", "path");
                }
                return document.AsJson();
            case "remove":
                Input.Fields(value, "op path", "operation");
                var path = Input.VirtualPath(value["path"]);
                if (!Staged.Remove(path))
                {
                    throw new ModelError("NOT_STAGED", "path");
                }
                Generation++;
                return new JsonObject { ["removed"] = path };
            case "clear":
                Input.Fields(value, "op", "operation");
                var count = Staged.Count;
                Staged.Clear();
                Generation++;
                return new JsonObject { ["removed"] = count };
            default:
                throw new ModelError("UNKNOWN_OPERATION", "op");
        }
    }

    public void Run(JsonNode? values)
    {
        var operations = Input.Array(values, "operations", 64);
        for (var index = 0; index < operations.Count; index++)
        {
            try
            {
                var result = Dispatch(operations[index]);
                Outcomes.Add(new JsonObject
                {
                    ["index"] = index,
                    ["ok"] = true,
                    ["result"] = result,
                });
            }
            catch (ModelError error)
            {
                Outcomes.Add(new JsonObject
                {
                    ["index"] = index,
                    ["ok"] = false,
                    ["error"] = error.AsJson(),
                });
            }
        }
    }

    public JsonObject Report()
    {
        return new JsonObject
        {
            ["tactic"] = "Collection",
            ["tactic_id"] = "TA0009",
            ["simulation"] = true,
            ["outcomes"] = Outcomes.DeepClone(),
            ["state"] = new JsonObject
            {
                ["manifest"] = Manifest(),
                ["repository"] = Repository.Export(),
                ["quota"] = Quota,
            },
        };
    }
}

public static class Program
{
    public const int MAX_INPUT = 65536;

    public static JsonObject Simulate(JsonNode? node)
    {
        var value = Input.Object(node, "input");
        Input.Fields(value, "documents operations quota", "input");
        var repository = new VirtualRepository(value["documents"]);
        var quota = Input.Integer(
            Input.Default(value, "quota", JsonValue.Create(16384)!), "quota", 0, 65536
        );
        var session = new CollectionSession(repository, quota);
        session.Run(value["operations"]);
        return session.Report();
    }

    public static JsonNode? ReadDocument()
    {
        using var input = Console.OpenStandardInput();
        using var buffer = new MemoryStream();
        var block = new byte[1024];
        while (buffer.Length <= MAX_INPUT)
        {
            var count = input.Read(block, 0, (int)Math.Min(block.Length, MAX_INPUT + 1 - buffer.Length));
            if (count == 0)
            {
                break;
            }
            buffer.Write(block, 0, count);
        }
        if (buffer.Length > MAX_INPUT)
        {
            throw new ModelError("INPUT_TOO_LARGE", "input");
        }
        string text;
        try
        {
            text = new UTF8Encoding(false, true).GetString(buffer.ToArray());
        }
        catch (DecoderFallbackException)
        {
            throw new ModelError("INVALID_UTF8", "input");
        }
        try
        {
            using var parsed = JsonDocument.Parse(text);
            CheckKeys(parsed.RootElement);
            return JsonNode.Parse(text);
        }
        catch (JsonException)
        {
            throw new ModelError("INVALID_JSON", "input");
        }
    }

    public static void CheckKeys(JsonElement element)
    {
        if (element.ValueKind == JsonValueKind.Object)
        {
            var names = new HashSet<string>(StringComparer.Ordinal);
            foreach (var property in element.EnumerateObject())
            {
                if (!names.Add(property.Name))
                {
                    throw new ModelError("DUPLICATE_JSON_KEY", property.Name);
                }
                CheckKeys(property.Value);
            }
        }
        else if (element.ValueKind == JsonValueKind.Array)
        {
            foreach (var child in element.EnumerateArray())
            {
                CheckKeys(child);
            }
        }
    }

    public static int Main()
    {
        JsonObject result;
        var exitCode = 0;
        try
        {
            result = Simulate(ReadDocument());
        }
        catch (ModelError error)
        {
            result = new JsonObject
            {
                ["simulation"] = true,
                ["error"] = error.AsJson(),
            };
            exitCode = 2;
        }
        var bytes = Encoding.UTF8.GetBytes(result.ToJsonString() + "\n");
        using var output = Console.OpenStandardOutput();
        output.Write(bytes);
        return exitCode;
    }
}
