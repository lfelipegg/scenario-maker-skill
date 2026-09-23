---
name: scenario-maker
description: Use when creating, refining, critiquing, or batching prompts for AI image and video generation, including character profiles, text-to-image, text-to-video, image-to-video, ComfyUI wildcards, prompt variants, tag prompts, Danbooru tags, negative prompts, Wan video prompts, and model-aware prompts for SDXL, Illustrious, NoobAI, or Pony.
---

# Scenario Maker

## Overview

Write visual prompts for AI image and video models. Turn rough ideas into ready prompts, requested analysis, variants, tags, negative prompts, and ComfyUI wildcard files. Prompt writing never invokes image/video generation.

## Reference Selection

- Read `references/routing.md` and `references/output-contracts.md` first for every request: infer the request's independent fields and apply the requested output shape before model defaults.
- Read `references/model-prompts.md` when the request names SDXL, Stable Diffusion XL, Illustrious/ILXL, NoobAI, Pony/Pony Diffusion, or another alias listed there.
- Read `references/prompt-types.md` for prose/tag syntax, length targets, negative prompts, and visible-only rules.
- Read `references/danbooru-tags.md` for Danbooru Version, Danbooru tags, tag validation, alias lookup, or related-tag expansion.
- Read `references/video-prompts.md` for text-to-video, image-to-video, and Wan video prompts.
- Read `references/wildcards.md` before creating ComfyUI wildcard `.txt` files.
- Read `references/characters.md` when creating original characters, character profiles, character prompt fragments, or randomized character batches.

## Workflow

1. Infer Operation, Task, Scope, Target, and Output independently using `references/routing.md`; do not ask the user to fill out a schema.
2. Extract the scene description, locked details, requested changes, format, length, count, and save path.
3. Apply `references/output-contracts.md` and the operation/scope permissions in `references/routing.md`. Resolve genuine incompatibilities before writing. Defaults may complete permitted local details, not introduce independent props, actions, or events into a supplied scene.
4. Keep prompts observable: describe appearance, environment, lighting, motion, camera behavior, weather, composition, and visible atmosphere. Avoid hidden thoughts, backstory, smells, lore, or internal emotions unless the user explicitly asks.
5. If a supported target model is explicitly named, use `references/model-prompts.md` for compatible, unspecified defaults. Explicit formatting overrides profile presentation preferences, not required scene content or verified hard input requirements.
6. For Danbooru Version requests, use `scripts/danbooru_lookup.py` to validate uncertain tags, resolve aliases, and find related tags instead of reading the raw CSV files.
7. For randomized character requests, use `scripts/character_generator.py` and follow `references/characters.md`.
8. Return only the requested artifact: a finished prompt for a single prompt-writing request, analysis for a critique/comparison, or the requested pair, variants, or batch. Do not add unsolicited notes, labels, negatives, or alternatives.
9. When wildcard batches are requested, create newline-separated `.txt` files automatically under `./wildcards` unless the user provides another path.

## Default Choices

- Output format: Normal Version when neither an explicit format nor a named model's compatible default selects another dialect.
- Length: Very Short unless the user requests Medium, Long, or an explicit token limit.
- Task: infer still image, image editing, text-to-video, or image-to-video independently of the operation, scope, target, and output. An existing image does not by itself imply video.
- Model coverage: use generic image/video guidance unless the user names Wan or a supported image model. Use Wan rules for Wan video prompts. Use `references/model-prompts.md` for SDXL, Illustrious, NoobAI, or Pony image prompts. Do not guess a model when none is named.
- Wildcard count: if a wildcard request omits a count, create 10 lines per requested file.

## Output Rules

- Follow `references/output-contracts.md` for output shape, multiplicity, and precedence.
- Respect user-specified token limits and formats.
- For Tag Version, use comma-separated visual phrases; exact lettering and relationships may remain literal.
- For Danbooru Version, use canonical tags where possible and minimal fidelity-preserving literal/relational phrases where necessary. Canonical-only constraints forbid that fallback; clarify if no faithful expression exists.
- For video prompts, include subject motion, environmental motion, camera motion, atmosphere, and stylization.
- For Wan prompt writing, use one cohesive cinematic paragraph unless explicitly requested otherwise.
- A model's tag/prose dialect is a default, not permission to override the requested output format or add model notes.
- For wildcard files with a named supported model, use its compatible dialect defaults unless the user specifies another format.
- For wildcard files, report saved paths and line counts after writing them.

## When To Ask

Ask a concise question only when proceeding would likely produce the wrong artifact, such as:

- The user says "continue this image" but no image or image description is available.
- The user requests saved wildcard files outside the current workspace and no writable path is clear.
- The user asks for a specific unsupported model format whose constraints are unknown and materially affect the prompt.
- Required content cannot fit the requested hard constraints after removing redundancy and optional invention.
- The requested artifact conflicts with a verified requirement of the exact model/task/interface. A preferred dialect or uncertain rendering quality alone does not justify interrupting.
