# Project instructions for AI contributors

These instructions apply to every AI assistant and coding agent working in this
repository, including Codex, Claude, Cursor, Antigravity, and similar tools.

## Documentation requires approval

Do not create a new documentation file or other non-code work product without
the user's explicit approval. This includes Markdown or text documentation,
plans, reports, design notes, summaries, and similar prose artifacts. A request
to change code does not imply approval to create supporting documentation.

An agent may edit an existing documentation file when the user explicitly asks
for that edit or when it is a necessary part of an approved documentation
change. Preserve upstream license texts, legal notices, and attributed documents
unless the user explicitly requests a compatible change.

## Report issues discovered during development

When development reveals a confirmed project defect, regression, limitation,
or blocker, automatically create a GitHub issue in `tuxpepe1893/davidmono`.
Do not wait for separate permission to report it.

Before creating the issue, search the repository's existing issues to avoid a
duplicate. If a matching issue exists, add the new evidence there instead. A
new issue must:

- use a specific title;
- describe the observed and expected behavior;
- include reproduction steps, affected files or versions, and relevant error
  output when available;
- explain its effect on development or users;
- record any investigation or workaround already attempted;
- mention `@tuxpepe1893` and ask the repository owner to inspect it; and
- omit credentials, private data, access tokens, and other secrets.

Do not file an issue for an ordinary in-progress edit that is immediately
resolved as part of the requested change. File one when the finding remains a
distinct defect, risk, or follow-up concern for the project.

## Attribute AI contributions

Every commit containing work materially produced by an AI assistant must
include one `Co-authored-by` trailer for each assistant used. Use the
assistant's documented or configured attribution identity and name the product
or agent, such as Codex, Claude, Cursor, or Antigravity. Preserve existing
trailers and never add the same co-author twice.

For Codex, append this exact trailer once:

```text
Co-authored-by: Codex <noreply@openai.com>
```

When the exact underlying model is known and is not already part of the
documented co-author identity, also add it to the commit message as a separate
trailer, for example:

```text
AI-model: GPT-5.6 Sol
```

Contributors must still review and understand AI-assisted changes before
committing or opening a pull request.
