# Request Routing

Route each request by inferring independent fields from ordinary language. These fields are internal reasoning aids, not a schema the user must fill out or see.

## Routing Fields

- **Operation** — `create`, `expand`, `adapt`, `revise`, or `critique`. A comparison remains analysis across the named prompts, targets, or approaches; do not turn it into prompt writing unless the user also asks for prompts.
- **Task** — `still image`, `image editing`, `text-to-video`, or `image-to-video`. The task describes what the prompt is for, independently of model wording or interface controls.
- **Scope** — `full scene`, `character design`, `clothing`, or `isolated asset`. Character and clothing scopes are content boundaries, not models or tasks.
- **Target** — the named model or checkpoint profile, if any. Never infer a specific target from a style, scope, or task.
- **Output** — `prompt only`, `positive/negative pair`, `variants`, `file`, or the requested analysis. Preserve an explicit count, format, file scope, and analysis shape.

Infer all fields together, then apply the instructions for each without allowing one field to replace another. For example, adapting clothing for a named checkpoint is still a clothing-scope adaptation; it is not automatically a character-generation task.

## Content and Capability Boundaries

Preserve supplied facts, relationships, exclusions, and locked details through expansion, adaptation, revision, and variation. Formatting permission is not permission to alter required scene content. Infer the task and scope from the request, but do not invent a target or claim unsupported model, task, or interface capabilities.

Prompt writing never invokes image or video generation. A request to create an image or video within this skill means writing the appropriate prompt unless the user explicitly requests a separate generation capability outside this skill.

## Unknown or Ambiguous Targets

With no target, use generic guidance for the resolved task and do not guess a model. An unknown or ambiguous name may use generic guidance only when its identity is immaterial to the requested artifact.

Ask a concise clarifying question before claiming model-specific adaptation, syntax, task support, or interface behavior when that claim depends on the unresolved identity. Do not ask merely because a model may render a requested detail unreliably; rendering uncertainty does not make the routing ambiguous.

## Routing Boundaries

- “Expand this character outfit for a still image” → `expand` + `still image` + `clothing` + no target + `prompt only` unless another output is requested.
- “Critique this SDXL prompt” → `critique` + the prompt's task and scope when discernible + `SDXL` + requested analysis; return critique, not a replacement prompt.
- “Compare this prompt in SDXL and Krea 2” → comparison analysis for two targets; do not silently produce prompts or generation results.
- “Adapt this starting frame for Wan image-to-video” → `adapt` + `image-to-video` + the described scope + `Wan` + the requested output.
- “Make a character for Pony” → character scope and Pony target; character is neither the model nor the task. Clarify the task only if the distinction materially changes the artifact.
- “Use Aurora syntax” when Aurora's identity is unresolved → clarify if syntax depends on which Aurora is meant; proceed generically only when the requested result does not depend on that identity.

After routing, apply [Prompt Types](prompt-types.md) for prompt syntax and general task conventions, plus the named model or video reference when the resolved target or task requires it. Apply [Output Contracts](output-contracts.md) to determine the returned artifact's shape.
