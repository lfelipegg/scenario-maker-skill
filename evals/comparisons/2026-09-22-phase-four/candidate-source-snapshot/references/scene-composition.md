# Scene Composition

Use after [Request Routing](routing.md) and before model-facing wording. A scene description is the visible content to communicate, not a model dialect or a required output schema. Keep it internal unless the user asks to see it; do not expose planning JSON or add a planning section to a prompt-only response.

## Extract Before Expressing

Read the brief, supplied prompt, and any available source image together. Identify only what applies:

- Subjects and their attributes, including counts and which attributes belong to which subject.
- Actions and spatial relationships: who does what, with which object, and where.
- Setting and composition, including placement, framing, and requested perspective.
- Visual treatment: style, palette, lighting, and materials.
- Required visible text, with its exact spelling, case, punctuation, and the object that carries it.
- Locked details, other supplied facts and necessary implications, permitted changes, and exclusions.

Missing fields remain unspecified until the operation, scope, and invention mode permit completion. These categories are not a checklist to fill. Do not infer active rain from a wet street, add equipment from an occupation, or import scenery from a model example. Separate supplied content from optional inventions so the latter can be removed without losing the former.

Apply [Constraints and Revisions](constraints-and-revisions.md) to decide what may change. Infer these permissions from ordinary language; do not require the user to supply a schema or choose a mode when the default is sufficient.

## Operations

| Operation | Work on the scene description |
| --- | --- |
| **Create** | Construct from the brief, retaining every supplied fact. Complete only unspecified, permitted details; Balanced by default. |
| **Expand** | Add compatible detail within the existing content and scope; Balanced by default. More words do not require more objects or events. |
| **Adapt** | Keep the scene; change its model-facing expression. Preserve by default, even if another dialect favors different compositions or vocabulary. |
| **Revise** | Change the requested attributes or relationships, preserving everything else. Preserve by default; permission is local to the requested change. |
| **Critique** | Identify problems and explain relevant trade-offs. Suggestions are not permission to apply them; do not silently replace the prompt. |

For compound requests, apply each permission locally. “Adapt and invent background details” opens the background while preserving the subjects. “Adapt, Explore” does not by itself authorize new scene content. A comparison remains analysis unless prompts are also requested.

## Express in the Requested Dialect

Once content and permissions are resolved, apply [Output Contracts](output-contracts.md), [Prompt Types](prompt-types.md), and the applicable model or task reference. Model profiles determine compatible expression, not a different scene. Task templates describe relevant fields, not mandatory invention.

- Preserve subject counts, colors, props, actions, spatial relationships, and required lettering across prose, generic tags, and model-specific tags.
- Preserve relationships explicitly. Listing two objects separately does not establish which is left of the other or who holds what.
- Grouped canonical attributes may express an unambiguous single-subject association; do not turn every attribute group into prose. Use the minimal literal or relational fallback permitted by the output contract when tags cannot carry required meaning.
- Keep exclusions effective in the requested artifact without adding an unsolicited negative-prompt section. Do not turn an excluded object into positive scene content or negate a required element.
- Length defaults are targets, not quotas. Prefer a complete sparse prompt over invented padding. For hard limits, remove redundancy and optional invention before considering a clarification.

## Final Fidelity Check

Compare the final artifact with the source and the locally authorized changes, not merely with its intermediate wording. Check subject/attribute binding, counts, props, actions, relationships, exact lettering and its carrier, exclusions, and locked details. Reject additions outside the permitted mode or scope. In a narrow revision, the requested difference should be the only scene change; in an adaptation, there should be no scene change.

Keep this check internal. Return the requested prompt, analysis, pair, or batch shape without unsolicited explanations or alternative outputs.
