# Domain docs

## Layout

Single-context: root `CONTEXT.md` and `docs/adr/`. Create these lazily when terms or qualifying decisions are resolved; do not scaffold empty files or directories.

## Before exploring

- Read root `CONTEXT.md` for domain vocabulary.
- If a root `CONTEXT-MAP.md` is introduced later, follow it to the relevant contexts instead.
- Read ADRs that touch the work in `docs/adr/`; in a multi-context layout, also check context-specific ADRs.
- If these files do not exist, proceed silently. Do not flag their absence or propose creating them upfront.

## Use the glossary's vocabulary

Use canonical names from `CONTEXT.md` in issues, proposals, hypotheses, and tests. Avoid rejected synonyms. Reconsider invented terms or note genuine gaps for domain-modeling. The glossary contains no implementation details.

## Flag ADR conflicts

Surface proposals that contradict an existing ADR rather than silently overriding it. Record new ADRs only for hard-to-reverse, surprising decisions with real trade-offs.
