# Prompt Types

## Prompt Package

Default output is a compact package, not a long explanation:

- Ready prompt: the strongest prompt to paste into the generator.
- Variants: 2-4 alternatives when the user asks for options, a batch, or a broad idea.
- Negative prompt: include when useful for image generation or when requested.
- Format notes: include only if they help the user use the prompt immediately.
- Saved wildcard files: list paths and line counts when files were written.

Do not add tutorials, process narration, or hidden reasoning unless the user asks.

## Visible-Only Rule

Prefer details that can appear in an image or video:

- subject appearance, pose, action, wardrobe, props
- environment, weather, era, architecture, landscape
- lighting, color palette, contrast, shadows
- camera framing, lens feel, angle, composition
- visible atmosphere such as fog, rain, dust, sparks, reflections

Avoid internal thoughts, backstory, hidden motivation, smells, sound, lore, and unverifiable emotions. Convert emotions into visible cues, such as posture, expression, lighting, gesture, or environment.

## Output Formats

### Normal Version

Natural descriptive prose in full sentences. Use for general prompts, text-to-image, and cinematic scene descriptions.

Include subject, setting, visible action, composition, lighting, and atmosphere.

### Tag Version

Comma-separated visual phrases. Use for models or workflows that respond well to keyword prompts.

Example shape:

`astronaut, red desert, sandstone arches, sunset lighting, dust storm, long shadows, cinematic composition, wide shot`

### Danbooru Version

Comma-separated lower_snake_case tags for anime or imageboard-trained models.

Use common tag-style vocabulary and visual tags only:

`1girl, silver_hair, red_eyes, long_hair, military_uniform, standing, sunset, battlefield, dramatic_lighting`

## Length Targets

- Very Short: about 75 tokens, 1-2 sentences, default for fast image generation.
- Medium: about 150 tokens, 4-6 sentences, balanced detail and usability.
- Long: about 300+ tokens, 8+ sentences, useful for complex scenes and worldbuilding.
- Explicit limit: obey the user's token or word limit over the defaults.

If the requested format is Tag or Danbooru, keep the same level of detail but express it as tags instead of prose.

## Scenario Types

### Normal

Balanced scene description for general creative use.

### Text-to-Image

Optimize for a single frame. Prioritize visible clarity, composition, lighting, colors, subject placement, and camera framing.

Useful image prompt elements:

- wide shot, close-up, low angle, overhead view
- backlighting, rim light, volumetric fog, soft window light
- symmetrical composition, shallow depth of field, cinematic shadows

### Negative Prompts

Keep negative prompts concise. Target common generation failures and user exclusions:

`blurry, low detail, distorted anatomy, extra fingers, text, watermark, logo, overexposed, underexposed`

For stylized prompts, adapt the negatives to the medium. Avoid negating important requested elements.
