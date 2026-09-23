# Model-Specific Image Prompt Profiles

Use this reference only when the user explicitly names a supported image model or a clear alias. Read `routing.md` and `output-contracts.md` first. Otherwise use generic task guidance without claiming model-specific adaptation.

## Model Detection

- SDXL: `sdxl`, `stable diffusion xl`, `stable-diffusion-xl`, `stable diffusion xlarge`
- Pony: `pony`, `pony diffusion`, `pony diffusion v6`, `pdxl`
- Illustrious: `illustrious`, `illustrious xl`, `illustrious-xl`, `ilxl`
- NoobAI: `noobai`, `noob ai`, `noobai xl`, `noobai-xl`, `nai noob`, `noob v-pred`

For multiple named models, follow the requested operation and output: prompt-writing requests get one prompt per target with minimal labels; comparisons remain analysis. An explicit shared-prompt request gets one compatible prompt or a clarification, never a silent split.

## Presentation Defaults

`output-contracts.md` owns response shape and precedence. The profiles below supply only compatible, unspecified defaults. Explicit prose, tag style, normalization, and prefix exclusions override these presentation preferences; they are not hard model input requirements.

For a single prompt-writing request, return only the finished prompt. Negative-prompt sections apply only when a negative is requested. Model-note sections supply information only for requested notes or relevant analysis, never unsolicited additions. Preserve user-specified content, length, exclusions, and safety constraints.

## SDXL

Best fit: natural descriptive prose for general image generation.

Positive prompt:

- Use a concise natural-language scene description, usually 1-3 sentences.
- Put the main subject, action, setting, composition, lighting, and style in clear prose.
- Prefer concrete visual terms over long tag stacks.
- Include camera/framing terms when useful: `close-up`, `wide shot`, `low angle`, `shallow depth of field`, `cinematic lighting`.
- Do not use Pony score tags or anime-board quality stacks unless the user explicitly asks for a tag workflow.

Negative prompt:

- Keep concise and failure-focused.
- Good defaults: `blurry, low detail, distorted anatomy, extra fingers, bad hands, text, watermark, logo, overexposed, underexposed`.
- Adapt negatives to the requested medium; avoid negating requested elements.

When model notes or relevant analysis are requested:

- Mention that SDXL often benefits from clear prompt wording and a separate negative prompt.
- Mention limitations only when relevant: text rendering, complex layouts, hands/faces at small sizes, and exact spatial relations can be unreliable.

Example shape:

`A weathered ranger stands on a mossy stone bridge in a misty pine forest, holding a lantern that casts warm light across wet leaves. Wide shot, soft dawn fog, realistic fantasy concept art, detailed textures, cinematic composition.`

## Pony

Best fit: comma-separated tag prompts using Pony's score/source/rating dialect.

Positive prompt:

- Start with score tags, then source/rating, then subject and visual tags.
- Default safe prefix: `score_9, score_8_up, score_7_up, source_anime, rating_safe`.
- Choose one source tag that matches the request: `source_anime`, `source_cartoon`, `source_pony`, `source_furry`, or another source tag the user provides.
- Use `rating_safe` by default unless the user requests another allowed rating.
- Use comma-separated tags and short visual phrases.
- Avoid generic SD quality boilerplate such as `masterpiece` and `best quality`.
- Avoid prose paragraphs unless the user explicitly asks.

Negative prompt:

- Good defaults: `score_6, score_5, score_4, low quality, bad anatomy, bad hands, extra fingers, text, watermark, signature`.
- Do not put `masterpiece`, `best quality`, or the selected source/rating tags in the negative prompt.

When model notes or relevant analysis are requested:

- Say which source and rating tag were chosen if that helps immediate use.
- Keep notes brief; describe Pony's default tag dialect without presenting it as a hard input requirement.

Example shape:

`score_9, score_8_up, score_7_up, source_anime, rating_safe, 1girl, silver hair, red eyes, long coat, standing on a rainy rooftop, neon city, looking at viewer, dramatic rim light, night, detailed background`

## Illustrious

Best fit: Danbooru-style anime tags with quality and composition tags.

Positive prompt:

- Use comma-separated Danbooru-style tags by default.
- Start with quality/style guidance, then subject count, character traits, pose/action, setting, lighting, and composition.
- Good quality starters: `masterpiece, best quality, highres, absurdres`.
- Use common tag vocabulary, usually lower_snake_case for canonical Danbooru tags.
- Keep composition tags restrained: `close-up`, `upper_body`, `full_body`, `cowboy_shot`, `looking_at_viewer`, `dynamic_angle`.
- Natural-language fragments are acceptable only when a detail has no clean tag equivalent.
- Do not use Pony score/source/rating tags unless the user explicitly asks for Pony.

Negative prompt:

- Good defaults: `worst quality, low quality, normal quality, lowres, bad anatomy, bad hands, extra digits, fewer digits, text, watermark, signature`.
- Add style-specific exclusions only when relevant.

When model notes or relevant analysis are requested:

- Mention Danbooru-style tag ordering when useful.
- If the user requested a known character, include character/source tags when known; do not invent uncertain canonical tags.

Example shape:

`masterpiece, best quality, highres, 1girl, solo, long_hair, blue_eyes, hooded_cloak, forest_path, holding_lantern, night, moonlight, fog, looking_at_viewer, cowboy_shot, dramatic_lighting`

## NoobAI

Best fit: ordered tag prompts in NoobAI's normalized tag style.

Positive prompt:

- Use comma-separated tags and short visual phrases.
- Start with quality/model preference tags, then subject, identity/source if known, traits, action, setting, lighting, and composition.
- Good quality starters: `masterpiece, best quality, very awa, newest`.
- `very awa` is optional; include it when the user wants stronger anime/aesthetic polish, omit it for strict neutral tag conversion.
- Normalize tags with spaces instead of underscores: use `long hair`, not `long_hair`.
- Escape parentheses in character/source tags: `hakurei reimu \(touhou\)`.
- Keep tags visible and concrete. Do not add lore, relationships, or hidden personality traits.
- Do not use Pony score/source/rating tags unless the user explicitly asks for Pony.

Negative prompt:

- Good defaults: `worst quality, low quality, lowres, bad anatomy, bad hands, extra digits, fewer digits, text, watermark, signature, jpeg artifacts`.
- Use spaces instead of underscores in the negative prompt too.

When model notes or relevant analysis are requested:

- Mention that tags were normalized with spaces and escaped parentheses when applicable.
- If a requested character/source tag is uncertain, use a descriptive identity phrase instead of fabricating a canonical tag.

Example shape:

`masterpiece, best quality, very awa, newest, 1girl, solo, white hair, golden eyes, black sailor uniform, standing in a ruined classroom, broken windows, sunset light, dust particles, looking at viewer, upper body`

## Wildcards With Named Models

When creating wildcard files for a named supported model, apply the requested format first. Otherwise use these compatible presentation defaults:

- Each full-prompt line uses the selected model's default dialect.
- Pony lines should start with the score/source/rating prefix.
- Illustrious lines should use lower_snake_case Danbooru-style tags.
- NoobAI lines should use spaces instead of underscores and escape parentheses when needed.
- SDXL lines should be compact natural-language prompts.

## Source Notes

Research basis: Stability AI SDXL, Pony Diffusion V6 XL, Illustrious XL, and NoobAI XL model cards and the NoobAI manual. These notes are practical prompting defaults, not hard model settings.

- SDXL: https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0
- Pony: https://huggingface.co/LyliaEngine/Pony_Diffusion_V6_XL
- Illustrious: https://huggingface.co/OnomaAIResearch/Illustrious-xl-early-release-v0 and https://huggingface.co/OnomaAIResearch/Illustrious-XL-v1.0
- NoobAI: https://huggingface.co/Laxhar/noobai-XL-1.1 and https://huggingface.co/Laxhar/noobai-XL-Vpred-1.0
- NoobAI manual: https://files.catbox.moe/vciz3c.pdf
