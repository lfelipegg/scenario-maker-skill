# MiniMax H3 (Native Local)

This profile supplies compatible prompt-authoring defaults only after the task, scene, permissions, and output have been resolved. Follow [Output Contracts](../output-contracts.md) for response shape and explicit-format precedence, [Constraints and Revisions](../constraints-and-revisions.md) for preservation, scope, and invention permissions, and [Video Prompts](../video-prompts.md) for shared temporal semantics. This profile does not broaden those permissions.

## Identity, Routes, and Deliverable

Supported prompt-writing routes are limited to the ordinary native local ComfyUI paths below:

- **H3 Ref2VA — reference video generation/editing:** `H3-Base-Ref2VA` through `MiniMaxH3ReferenceToVideo`.
- **H3 FL2VA — first-frame video:** `H3-Base-FL2VA` through `MiniMaxH3ImageToVideo`, with one actual opening image. Despite the checkpoint family name, this selected one-image task uses the official **I2VA** opening-anchor form, not the two-image FL2VA task prefix.
- **H3 Ref2VA — frame-derived still edit:** `H3-Base-Ref2VA` reference generation, followed downstream by separate extraction of the first generated frame.

Do not silently substitute hosted `MiniMax-H3`, `MiniMax-H3-Max`, older Hailuo models, another checkpoint, or adjacent text-only, continuation, last-frame, interpolation, guide-chain, ControlNet, mask, turbo, Context-IR, or 2K-regeneration workflows. Generic guidance is acceptable when identity is immaterial; clarify before an identity-dependent adaptation or capability claim.

Return **prompt text for later execution**, not workflow JSON, API payloads, sampler/install settings, generated media, or an extracted frame. Prompt authoring can use inspectable media or sufficiently clear descriptions/transcripts. Never claim unseen or unheard details were inspected. Actual source-dependent execution still requires the correctly connected media; a description or textual label does not connect conditioning.

## Language, Detail, and Output

- Default to **English** and **Medium** detail (about 150 tokens) for every supported route. Very Short (about 75) and Long (about 300+) are approximate guides, not quotas or model limits. Required content outranks a soft guide; never pad sparse input.
- Preserve visible text and supplied dialogue or lyrics in their original language, spelling, case, and punctuation unless translation or revision is authorized.
- Explicit format, language, length, multiplicity, and output instructions override presentation defaults when compatible. Preserve reference bindings and temporal meaning in the requested shape. Do not add notes, settings, variants, or a prompt package.
- Default video intent is one shot. Preserve explicitly requested cuts, shot order, actor/action bindings, overlap, timing, pace, and audio continuity. Do not invent cuts or timestamps to fill sections. Natural-language timing does not set frame count, execution duration, or frame-accurate scheduling.
- Leave camera behavior unspecified when the user leaves it unspecified. Preserve requested movement or fixed framing; clarify genuinely incompatible camera or framing locks rather than weakening them.
- The structures below form **one pasteable text prompt**. Their sections are not separate ComfyUI properties and are not parser requirements.

## Native References and Conditioning

The native Ref2VA node exposes up to 9 reference images, 3 reference videos, and 3 standalone reference audios. Each reference video has a separate index-paired soundtrack input. These are per-category socket maxima; do not import hosted aggregate file/duration limits or claim unlimited practical capacity.

Bind labels to **connected, consumed order**, not upload order or a universal socket-number convention:

- Images use `<Picture N>`; videos use `<Video N>`; audio uses its own `<Audio N>` counter.
- Presentation proceeds through images, then each video with its connected soundtrack audio label before that video, then standalone audio. Missing inputs create no labels.
- A soundtrack participates in audio numbering, so `<Video 1>` need not pair with `<Audio 1>`. Sound in a video is not automatically extracted or reused; its soundtrack must be separately connected and assigned a role.
- `<Subject N>` denotes reusable content, not an input slot. One asset may define several subjects, and several assets may define one subject.

Assign only named roles: identity, appearance, clothing, composition, motion, camera, style, source-video editing, audio reuse, or audio reference. An appearance source does not donate its background, pose, dialogue, or soundtrack. Clarify material role conflicts rather than choosing silently.

A connected socket or textual label does not prove active media conditioning. Image/video latent references depend on the video VAE; audio latent references depend on the audio VAE; tokenizer audio labels are not the audio signal. Known inactive conditioning, excess references, or required content beyond a consumed/truncated video segment requires clarification—not silent dropping or a capability promise. Native video references may be truncated to the target frame count and cropped to the valid frame grid; very short videos may be rejected. Unknown graph/runtime details remain unknown.

## Ref2VA Structure and Relationship Semantics

Reference generation, source-video editing, and frame-derived still editing use these sections in order:

1. `subject_definitions`
2. `summary`
3. `retention_analysis`
4. `detailed_description`
5. `overall_soundscape`
6. `non_diegetic_music`

Use task prefixes only for relationships actually present. Within the selected routes, `keyframe completion`, `reference generation`, `video editing`, `audio reuse`, and `audio reference` describe assigned roles and may be joined with ` + ` when needed. The official guide uses `keyframe completion` when an image supplies an edited keyframe; in a frame-derived still edit this is reference-guided prompt intent, not an FL2VA hard anchor or native still-image editing. For a source-video edit, begin the summary body `The target video is an edited version of <Video N>.`, replacing N with the actual consumed label of the edited source, not always 1. An image edit is not `video editing` merely because Ref2VA outputs video, and a video used only for motion, camera, or style is `reference generation`. Other prefixes in the publisher's wider guide do not add adjacent routes to this profile.

Visible-content relationship markers are `fully_preserved`, `partially_preserved`, `attribute_transfer`, and `weak_reference`. Audio markers are `fully_copy`, `partially_copy`, `reference`, and `weak_reference`. They express scoped intent, not pixel identity, waveform equality, timing, lettering, edit fidelity, or generated-quality guarantees. A marker applies only to the role defined for that label: `fully_preserved` on an identity source does not copy its pose, background, or other unassigned properties.

Audio needs an explicit role. Distinguish direct signal reuse from timbre, delivery, style, rhythm, dialogue/lyric-content, or sound-texture reference. Do not import source dialogue for a timbre-only request. Preserve supplied words and language for reuse or requested reperformance; mark unintelligible spans `[unclear]` rather than inventing them. Do not create a visible speaker for a vocal cue that exists only inside reused music. Keep referenced subjects and speaker IDs stable.

Audio sections are authored only when requested or supplied as intended target content. Otherwise write `Unspecified`; this does not request silence. Use `N/A` only with its explicitly declared meaning, such as requested complete silence in `overall_soundscape` or no non-diegetic music in `non_diegetic_music`.

## Ref2VA Full-Reference Generation

Use role-bound images, videos, and audio to synthesize a target video. Communicate only supplied or authorized subjects, relationships, appearance, setting, composition, motion, camera, style, and sound. Preserve rosters, exclusions, locked details, and exact lettering. Transfer only the named properties from each supplemental reference.

**Example source:** Picture 1 supplies Mira's appearance and red coat; Video 1 supplies walking motion only; its separately connected soundtrack is Audio 1 but is not requested; standalone Audio 2 supplies a dry alto timbre and delivery for the exact line `门还开着。`; Mira walks past a sign that must read `Open late!`; camera is unspecified.

```text
subject_definitions:
<Subject 1> is Mira, whose identity, appearance, and red coat come from <Picture 1> and whose walking motion comes from <Video 1>.
<Audio 2> is the voice-timbre and delivery reference for <Subject 1> (S1); its signal and original words are not copied.

summary:
[reference generation + audio reference] The target video shows <Subject 1> walking past a sign reading "Open late!" while <Audio 2> guides only her voice timbre and delivery.

retention_analysis:
<Subject 1> (appears in [Shot 1]): fully_preserved - Mira's identity, appearance, and red coat from <Picture 1> are retained, while only the walking motion is transferred from <Video 1>.
<Audio 2>: reference - its dry alto timbre and delivery guide Mira's supplied line without copying the signal or source words.

detailed_description:
[Shot 1] <Subject 1> (S1), preserving Mira's appearance and red coat from <Picture 1>, walks with the motion referenced from <Video 1> past a sign displaying the exact words "Open late!" She says in the dry alto timbre and delivery referenced from <Audio 2>, <d>[Chinese] 门还开着。</d> No visual, dialogue, background, camera behavior, or soundtrack is taken from <Video 1> beyond its assigned walking-motion role.

overall_soundscape:
Unspecified

non_diegetic_music:
Unspecified
```

Here `<Audio 1>` is absent from the prompt because the connected video soundtrack has no requested target role; `<Audio 2>` keeps its consumed-order label. The generation prompt communicates relationships but does not connect or execute the sources.

## Ref2VA Source-Video Editing

Identify the source video being edited, every authorized change, and the content to preserve. Do not silently reuse, replace, remove, or invent its soundtrack. Clear edits apply locally; unaffected protected content remains protected.

**Example source:** Video 1 is the edited source. Change only Ana's green scarf to blue; preserve Ana, Ben, their positions, actions, café, framing, lighting, and the exact sign `Open late!`. Its separately connected Audio 1 is reused unchanged. No camera change is requested.

```text
subject_definitions:
<Video 1> is the source video for the target video edit.
<Subject 1> is Ana in <Video 1>, including her identity and clothing; only her green scarf is to change to blue.
<Subject 2> is Ben in <Video 1>, preserved without change.
<Audio 1> is the synchronized soundtrack of <Video 1> and is reused as the target video's complete final audio track.

summary:
[video editing + audio reuse] The target video is an edited version of <Video 1>. Only <Subject 1>'s green scarf becomes blue; all other specified visual content and <Audio 1> are retained.

retention_analysis:
<Video 1> (source composition, action, framing, lighting, setting, and timing): fully_preserved - the café, Ana and Ben's positions and actions, and the sign reading "Open late!" remain unchanged.
<Subject 1> (appears throughout): partially_preserved - Ana's identity and all clothing remain as in <Video 1>, except her green scarf is blue.
<Subject 2> (appears throughout): fully_preserved - Ben remains unchanged.
<Audio 1>: fully_copy - <Audio 1> is reused as the complete final audio track.

detailed_description:
The target keeps <Video 1>'s existing visual style.
[Shot 1] Follow <Video 1>'s original shot, composition, actions, framing, lighting, café setting, camera behavior, and timing. Preserve <Subject 1> and <Subject 2>, their positions and relationships, and the exact sign text "Open late!" Change only <Subject 1>'s scarf from green to blue from the first output frame onward. Reuse <Audio 1> unchanged; add no dialogue, sound, music, camera change, or other visual alteration.

overall_soundscape:
The ambience and physical sounds in <Audio 1> are directly reused as part of the complete copied soundtrack.

non_diegetic_music:
Any audience-only music present in <Audio 1> is directly reused as part of the complete copied soundtrack; add none.
```

## FL2VA First-Frame Video

For the default structured output, the selected local path uses one actual opening image and begins with the official I2VA anchor:

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.
```

After one blank line, write `integrated_multimodal_description`, `overall_soundscape`, and `non_diegetic_music`. The image is the actual 0.00-second opening: preserve its starting identity, clothing, colors, objects, composition, and relationships, then express authorized motion or transformation forward from it. Do not rebuild the image as an invented scene.

Bare “animate this” requires asking what should change or move; motion is not compulsory, and an explicit still hold is valid. Separate subject motion, environmental motion, temporal transformation, and camera behavior. “Only the curtain moves” does not permit blinking, gestures, lighting drift, sound, or a camera move. A later red-to-blue coat transition preserves red at the opening. A request for the anchored opening itself to already be blue conflicts with this route and requires clarification rather than route substitution or source rewriting.

**Example source:** The opening image contains a woman in a red coat beside a closed curtain and a sign reading `Open late!`. Only the curtain may move gently; framing is locked; audio intent is unspecified.

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] Preserve <Picture 1> as the opening state, including the woman's identity, red coat, still pose, position, the closed curtain, the locked framing and lighting, and the sign displaying the exact words "Open late!" The camera remains fixed. Only the curtain begins to move gently; the woman, her clothing, the sign, all other objects, and the lighting remain still and unchanged.

overall_soundscape: Unspecified

non_diegetic_music: Unspecified
```

Explicitly requested multi-shot intent is allowed: preserve supplied cuts, order, overlap, timing, and audio continuity without inventing timestamps or promising scheduler precision.

## Ref2VA Frame-Derived Still Editing

This route means reference-guided video generation followed by downstream extraction of the **first generated output frame**. It is not native still-image editing, generation is not extraction, and Scenario Maker performs neither.

Identify an image or video reference as the visual edit base and scope every supplemental reference. For a video base, enough source/target information must identify the intended opening image; clarify an ambiguous moment instead of selecting or extracting a frame. The complete requested still edit must exist in the first output frame. Do not describe a later transition as satisfying the still. Leave later motion, camera behavior, and whole-clip stillness unspecified unless supplied or authorized. If the required state exists only later while the requested deliverable is the first frame, clarify rather than moving the extraction point or dropping the event. Do not use the FL2VA hard first-frame anchor to edit that same anchored frame.

**Example source:** Picture 1 shows a hand holding a yellow mug labeled `MORNING` above a wooden table. Change only the mug to cobalt blue and preserve the hand, table, framing, lighting, and exact label; later motion and audio are irrelevant.

```text
subject_definitions:
<Picture 1> is the visual edit base for the first generated output frame, showing a hand holding a yellow mug labeled "MORNING" above a wooden table.
<Subject 1> is the mug and holding hand from <Picture 1>; only the mug color changes.

summary:
[keyframe completion] The first generated output frame is an edited still based on <Picture 1>, with only <Subject 1>'s mug changed from yellow to cobalt blue.

retention_analysis:
<Picture 1> ([Shot 1] edited opening keyframe): partially_preserved - its hand, table, framing, lighting, composition, and exact "MORNING" label are retained while the mug color changes.
<Subject 1> (appears in [Shot 1]): partially_preserved - the same mug and hand are retained, with only the mug's yellow surface changed to cobalt blue.

detailed_description:
[Shot 1] The first generated output frame already shows the complete edit: the same hand holds the same mug in the composition, framing, and lighting of <Picture 1>, but the mug is cobalt blue. Preserve the wooden table and the mug's exact visible label "MORNING" without alteration. Later motion and camera behavior are unspecified.

overall_soundscape:
Unspecified

non_diegetic_music:
Unspecified
```

## Negatives and Optional Enhancement

Do not add automatic negatives or a stock blacklist. The inspected native templates route positive conditioning to `BasicGuider` and expose no separate negative-text path. If a requested negative is intended for this selected path, explain that it is not consumed and clarify the intended use. Clearly requested standalone negative text may be returned without claiming execution support. Never silently fold it into the positive prompt. Scene exclusions remain binding authored instructions; never negate required text, intentional style or blur, stillness, or authorized motion.

After the pasteable prompt, briefly offer optional in-chat enhancement only when the requested output format permits. Suppress the offer for “prompt only” or equivalent restrictions. Do not emit a second version automatically. Enhance only after the user requests it, preserving task, scope, invention permissions, source evidence, role bindings, and locks. This is an in-chat rewrite—not external Context-IR, a hosted service, checkpoint behavior, generation, or extraction.

## Primary Sources

- [Official full-reference prompt guide, fixed revision](https://github.com/MiniMax-AI/MiniMax-H3/blob/1ce88e916de7c15b63cbaf347642503f9bc21d3d/.agents/skills/h3-prompt-writing/references/ref-en.txt)
- [Official base/I2VA prompt guide, fixed revision](https://github.com/MiniMax-AI/MiniMax-H3/blob/1ce88e916de7c15b63cbaf347642503f9bc21d3d/.agents/skills/h3-prompt-writing/references/base-en.txt)
- [Native H3 ComfyUI nodes, fixed revision](https://github.com/Comfy-Org/ComfyUI/blob/5ba116a40f1944f64e2e4a8ace826656e6293bf4/comfy_extras/nodes_minimax_h3.py)
- [Native H3 tokenizer, fixed revision](https://github.com/Comfy-Org/ComfyUI/blob/5ba116a40f1944f64e2e4a8ace826656e6293bf4/comfy/text_encoders/minimax.py)
- [Native I2V workflow template, fixed revision](https://github.com/Comfy-Org/workflow_templates/blob/371a7b7171bbd11e9cc92ef615ba5ad223d7e5b4/templates/video_minimax_h3_i2v.json)
- [Native R2V workflow template, fixed revision](https://github.com/Comfy-Org/workflow_templates/blob/371a7b7171bbd11e9cc92ef615ba5ad223d7e5b4/templates/video_minimax_h3_r2v.json)
- [BasicGuider implementation, fixed revision](https://github.com/Comfy-Org/ComfyUI/blob/5ba116a40f1944f64e2e4a8ace826656e6293bf4/comfy_extras/nodes_custom_sampler.py#L792-L816)
