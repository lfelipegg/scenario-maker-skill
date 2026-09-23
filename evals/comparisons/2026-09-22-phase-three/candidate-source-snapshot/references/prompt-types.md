# Prompt Types

## Output Contract

Read `output-contracts.md` before choosing the response shape. A single prompt-writing request returns only the finished prompt. Negatives, notes, alternatives, and wrappers are not added just because they might be useful. Critiques, comparisons, requested pairs, and batches retain their requested shape.
Apply [Scene Composition](scene-composition.md) for the model-neutral content workflow and [Constraints and Revisions](constraints-and-revisions.md) for operation, mode, scope, preservation, and conflict rules.

The formats below describe prompt syntax, not permission to replace analysis with a prompt or expand the requested scope. Explicit formatting takes precedence over compatible model presentation defaults.
Examples below illustrate syntax or vocabulary only; they do not authorize their subjects, actions, settings, camera, lighting, or atmosphere in another request.

## Visible-Only Rule

Use these categories to express content authorized by [Scene Composition](scene-composition.md) and [Constraints and Revisions](constraints-and-revisions.md), not as a checklist of details to invent:

- subject appearance, pose, action, wardrobe, props
- environment, weather, era, architecture, landscape
- lighting, color palette, contrast, shadows
- camera framing, lens feel, angle, composition
- visible atmosphere such as fog, rain, dust, sparks, reflections

Visibility alone does not authorize a new fact. Scope and operation still govern which categories are available: character design does not acquire unsolicited pose, expression, action, setting, camera, or lighting; clothing does not acquire a wearer; and an isolated asset does not acquire supporting objects or a scene. Explicitly supplied presentation remains allowed and protected.

Avoid internal thoughts, backstory, hidden motivation, smells, sound, lore, and unverifiable emotions. Express an emotion through visible cues only when those cues were supplied or may be chosen under the resolved operation, mode, and scope; do not invent posture, expression, lighting, gesture, or environment merely to make an emotion visible.

## Output Formats

### Normal Version

Natural descriptive prose in full sentences. Use for general prompts, text-to-image, and cinematic scene descriptions.

For a full scene, express the requested subject, setting, action, composition, lighting, and atmosphere where supplied or permitted. Do not invent missing categories merely to complete this list. Character, clothing, and isolated-asset scopes do not acquire a full scene merely because the output is prose.

### Tag Version

Comma-separated visual phrases. Use for models or workflows that respond well to keyword prompts.

Preserve exact quoted lettering and explicit relationships as visual phrases; a tag-style request does not require canonical vocabulary.

Example shape:

`astronaut, red desert, sandstone arches, sunset lighting, dust storm, long shadows, cinematic composition, wide shot`

### Danbooru Version

Use comma-separated canonical lower_snake_case tags where possible for anime or imageboard-trained models. Follow `output-contracts.md` for minimal literal/relational phrases when needed for fidelity. Those phrases are not canonical tags; do not normalize exact visible lettering. If the user explicitly requires canonical-only tags and no faithful expression exists, clarify rather than silently dropping content.

Example tag-style vocabulary (validate uncertain canonical spellings with the local lookup):

`1girl, silver_hair, red_eyes, long_hair, military_uniform, standing, sunset, battlefield, dramatic_lighting`

## Length Targets

- Very Short: about 75 tokens, 1-2 sentences, default for fast image generation.
- Medium: about 150 tokens, 4-6 sentences, balanced detail and usability.
- Long: about 300+ tokens, 8+ sentences, useful for complex scenes and worldbuilding.
- Explicit limit: obey the user's token or word limit over the defaults.

These are approximate presentation targets, not quotas. Stop when the requested content is fully expressed; do not add props, actions, setting details, or weather just to reach a default length.

For Tag or Danbooru Version, express the same requested detail in the applicable format, retaining the literal/relational exceptions above. Sentence-count defaults apply to prose, not tag lists.

## Scenario Types

### Normal

General scene description. Content permission comes from the resolved operation, invention mode, and scope, not this scenario-type label.

### Text-to-Image

Optimize permitted content for a single frame. Give priority to supplied or permitted visible clarity, composition, lighting, colors, subject placement, and camera framing without filling absent categories.

When the relevant presentation dimension is supplied or permitted, useful image-prompt vocabulary includes:

- wide shot, close-up, low angle, overhead view
- backlighting, rim light, volumetric fog, soft window light
- symmetrical composition, shallow depth of field, cinematic shadows

### Negative Prompts

When a negative prompt is requested, keep it concise. Target relevant generation failures and user exclusions; do not add a negative field to a positive-only request:

`blurry, low detail, distorted anatomy, extra fingers, text, watermark, logo, overexposed, underexposed`

For stylized prompts, adapt the negatives to the medium. Avoid negating important requested elements.
