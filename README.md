# Scenario Maker

Scenario Maker is an agent skill for writing, refining, critiquing, and batching prompts for AI image and video workflows. It turns rough ideas or existing prompts into model-aware descriptions while preserving the details you want to keep.

**It writes prompts; it does not generate images or videos.** Use the resulting text in your image or video generation tool.

## What it can do

- Create or expand scene descriptions, character designs, clothing descriptions, and isolated assets.
- Adapt prompts for SDXL, local Krea 2 RAW/Turbo, Illustrious, NoobAI, and Pony Diffusion V6 XL.
- Write text-to-video and image-to-video prompts, including Wan prompts.
- Convert between natural-language prose, general tag prompts, and Danbooru-style tags.
- Revise specific details without changing the rest of a prompt.
- Critique prompts or compare model-specific approaches without silently rewriting them.
- Produce requested negative prompts, controlled variants, exploratory variants, and randomized character batches.
- Save ComfyUI wildcard batches as newline-separated `.txt` files.

## Getting started

1. Make this directory available to an assistant that supports agent skills, using that application's skill installation or discovery mechanism. Keep `SKILL.md`, `references/`, `scripts/`, and `docs/` together so the skill can access its supporting instructions and lookup data.
2. Ask the assistant to use **scenario-maker**, then describe what you want. The entry point is [SKILL.md](SKILL.md); invocation syntax depends on the application hosting the skill.
3. Copy the returned prompt into your generation workflow, or use the saved wildcard files in your wildcard setup.

Start with an ordinary-language request:

```text
Use scenario-maker to write an SDXL prompt for an abandoned greenhouse
filled with blue fog. Use natural-language prose, under 60 words.
```

You do not need to fill out a schema. When useful, include:

- **Task:** still image, image editing, text-to-video, or image-to-video.
- **Scope:** full scene, character design, clothing, or isolated asset.
- **Target:** the exact model or checkpoint, if known.
- **Output:** prose, tags, positive/negative pair, variants, critique, or files.
- **Constraints:** required details, exclusions, exact lettering, length, and what may change.

For image-to-video requests, provide the starting image or describe it. Naming a model selects prompt-writing guidance; it does not establish that a particular interface supports a task or control.

## Formats and defaults

| Format | What you get |
| --- | --- |
| **Normal Version** | Natural-language prose. |
| **Tag Version** | Comma-separated visual phrases. |
| **Danbooru Version** | Canonical tags where possible, with minimal literal or relational phrases when needed to preserve required meaning. |

For strictly canonical Danbooru output, say **canonical-only**. If canonical tags cannot faithfully express a required detail, the assistant asks how to resolve the conflict rather than dropping it.

Your explicit format and length take precedence over model presentation defaults. Without a named model or explicit format, the skill uses Normal Version. The default length is Very Short unless a selected profile supplies another default; local Krea 2 defaults to Medium.

A single prompt-writing request returns the prompt only. Ask explicitly for explanations, negative prompts, alternatives, or a positive/negative pair. Critique and comparison requests return analysis rather than an unsolicited rewrite.

## Controlling changes

Supplied facts and **locked details** remain protected: subject counts, colors, relationships, exclusions, and exact visible text should survive adaptation and revision unless you authorize a change.

| Mode | Allowed changes |
| --- | --- |
| **Preserve** | Reword or reorganize without introducing new visual facts. Default for adaptation and revision. |
| **Balanced** | Fill unspecified local details without adding independent subjects, props, actions, or events. Default for creation and expansion. |
| **Explore** | Add compatible ideas within the requested scope; additional subjects require an open roster or explicit permission. |

Modes do not broaden the request. A clothing description does not become a full scene, and “change only the jacket color” still permits only that change, even in Explore mode.

## Example requests

### Adapt an existing prompt

```text
Use scenario-maker to adapt this for Illustrious in Danbooru Version.
Preserve both subjects, their clothing colors, and the exact sign text
"Open late!". Do not add props or a background:
[paste the source prompt]
```

### Make a targeted revision

```text
Revise this prompt: change only the jacket from yellow to red.
Keep the hair, pose, setting, and all other details unchanged:
[paste the source prompt]
```

### Write a video prompt

```text
Write a Wan image-to-video prompt from this starting frame:
a small sailboat on calm water beneath an overcast sky.
Let the boat drift slowly left as the camera stays fixed.
Preserve the lighting and add no other boats.
```

### Create controlled variants

```text
Create four controlled variants of this SDXL prompt, changing only
the lighting. Keep the subject, clothing, pose, and setting fixed:
[paste the source prompt]
```

### Request analysis instead of a rewrite

```text
Critique this prompt for unclear subject relationships and conflicting
visual instructions. Do not rewrite it:
[paste the prompt]
```

### Save a wildcard batch

```text
Create 20 full-prompt SDXL wildcard entries for abandoned botanical
interiors. Use Balanced mode and natural-language prose.
Save them to ./wildcards/botanical-interiors.txt.
```

## ComfyUI wildcard files

Each non-empty line is one selectable prompt or fragment. Files contain no Markdown fences, numbering, or explanatory text.

- **Full-prompt wildcard entries** are complete prompts, including applicable model-specific prefixes.
- **Fragment wildcard entries** are partial descriptions intended for insertion into a larger prompt, without repeated model boilerplate.
- The default destination is `./wildcards` relative to the assistant's current working directory, unless you provide another path.
- If no count is specified, the skill creates **10 entries per requested file**.
- After saving, the assistant reports the file paths and line counts.

To request modular files, name the roles explicitly, such as clothing, settings, or lighting. See [wildcard guidance](references/wildcards.md) for the file contract.

## Repository guide

- [SKILL.md](SKILL.md): skill entry point, workflow, and defaults.
- [references/](references/): model profiles, prompt formats, video guidance, preservation rules, character guidance, and wildcard conventions.
- [scripts/](scripts/): utilities for Danbooru tag lookup/indexing and randomized character generation.
- [docs/](docs/): supporting documentation and tag data.
- [wildcards/](wildcards/): existing wildcard files.
- [tests/](tests/): utility tests.
- [evals/](evals/): prompt-behavior evaluation cases, tooling, and results.

For detailed behavior, start with [output contracts](references/output-contracts.md), [constraints and revisions](references/constraints-and-revisions.md), and the [model profile index](references/model-prompts.md).
