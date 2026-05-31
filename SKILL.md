---
name: scenario-maker
description: Use when creating, refining, critiquing, or batching prompts for AI image and video generation, including text-to-image, text-to-video, image-to-video, ComfyUI wildcards, prompt variants, tag prompts, Danbooru tags, negative prompts, Wan video prompts, and model-aware prompts for SDXL, Illustrious, NoobAI, or Pony.
---

# Scenario Maker

## Overview

Build visual prompt packages for AI image and video models. The skill turns rough ideas into ready prompts, variants, tags, negative prompts, and ComfyUI wildcard files while keeping outputs focused on visible, generateable details.

## Reference Selection

- Read `references/model-prompts.md` when the request names SDXL, Stable Diffusion XL, Illustrious/ILXL, NoobAI, Pony/Pony Diffusion, or another alias listed there.
- Read `references/prompt-types.md` for output formats, length targets, prompt packages, tag prompts, Danbooru tags, negative prompts, and visible-only rules.
- Read `references/danbooru-tags.md` for Danbooru Version, Danbooru tags, tag validation, alias lookup, or related-tag expansion.
- Read `references/video-prompts.md` for text-to-video, image-to-video, and Wan video prompts.
- Read `references/wildcards.md` before creating ComfyUI wildcard `.txt` files.

## Workflow

1. Identify the request type: normal prompt, tag prompt, Danbooru tags, text-to-image, text-to-video, image-to-video, Wan video, model-aware image prompt, negative prompt, critique, variants, or wildcard batch.
2. Extract subject, setting, action, style, lighting, composition, mood, constraints, target model, length, count, and save path.
3. Fill missing details with sensible visual defaults. Ask only when the target medium, source-image intent, safety constraints, or save location is genuinely ambiguous.
4. Keep prompts observable: describe appearance, environment, lighting, motion, camera behavior, weather, composition, and visible atmosphere. Avoid hidden thoughts, backstory, smells, lore, or internal emotions unless the user explicitly asks.
5. If a supported target model is explicitly named, apply its profile from `references/model-prompts.md`. The model profile overrides generic Normal, Tag, and Danbooru defaults only for that model-targeted request.
6. For Danbooru Version requests, use `scripts/danbooru_lookup.py` to validate uncertain tags, resolve aliases, and find related tags instead of reading the raw CSV files.
7. Return a prompt package by default: ready prompt first, then variants or supporting fields only when useful. For supported model requests, use `Positive prompt`, `Negative prompt` when useful, and compact `Model notes`.
8. When wildcard batches are requested, create newline-separated `.txt` files automatically under `./wildcards` unless the user provides another path.

## Default Choices

- Output format: Normal Version unless the user asks for Tag Version or Danbooru Version.
- Length: Very Short unless the user requests Medium, Long, or an explicit token limit.
- Scenario type: infer from the request; use text-to-image for single-frame image generation, text-to-video for video from text, and image-to-video when an existing image is the starting frame.
- Model coverage: use generic image/video guidance unless the user names Wan or a supported image model. Use Wan rules for Wan video prompts. Use `references/model-prompts.md` for SDXL, Illustrious, NoobAI, or Pony image prompts. Do not guess a model when none is named.
- Wildcard count: if a wildcard request omits a count, create 10 lines per requested file.

## Output Rules

- Put the strongest ready-to-paste prompt first.
- Respect user-specified token limits and formats.
- For Tag Version, use comma-separated visual phrases, not sentences.
- For Danbooru Version, use comma-separated lower_snake_case tags and prefer validated lookup results for uncertain tags.
- For video prompts, include subject motion, environmental motion, camera motion, atmosphere, and stylization.
- For Wan prompts, produce a single cohesive cinematic paragraph unless the user asks for multiple variants.
- For supported model prompts, follow the selected model's tag/prose dialect and include only compact actionable model notes.
- For wildcard files with a named supported model, each line should use that model's dialect.
- For wildcard files, report saved paths and line counts after writing them.

## When To Ask

Ask a concise question only when proceeding would likely produce the wrong artifact, such as:

- The user says "continue this image" but no image or image description is available.
- The user requests saved wildcard files outside the current workspace and no writable path is clear.
- The user asks for a specific unsupported model format whose constraints are unknown and materially affect the prompt.
