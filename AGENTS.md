# funfact engineering guidance

<!-- ecc-engineering-defaults:start -->
## Engineering defaults
For coding work, read [.engineering/defaults.md](.engineering/defaults.md).
These are shared fallback conventions; the existing project owner, nested instructions,
skills, model choices, domain contracts and stronger verification/release gates remain authoritative.
No hooks, permissions, MCP services or background automation are installed by this guidance.

### Project adaptation
Legacy Django sources live in `funfacts/`. Discover the supported Python/Django versions before setup. Use synthetic records and an isolated database; review scraper network effects before executing scripts. No verified test command is recorded yet.
<!-- ecc-engineering-defaults:end -->
