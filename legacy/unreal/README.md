# unreal/ — TODO

Stub. Nothing else here yet, on purpose.

Unreal is a **later** track, not a parallel one. It does not start until Unity has run A→E on a real project and the core doctrine has proven out.

## When it starts, the two things that differ from Unity

- **Integration via MCP**, not Unity batchmode / `AssetDatabase`. The agent reaches Unreal through an MCP server.
- **The membrane sits in a different place.** Unreal's AI-hostile layer is Blueprints (binary visual scripts — not text, not diffable, worse than Unity's `.meta` problem) plus UBT modules and the C++ build graph.

Everything in `core/` should carry over unchanged. Everything that names `AssetDatabase` or `.meta` will not — that's the point of keeping core engine-agnostic.
