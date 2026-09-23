# Video Prompts

Use this reference for text-to-video, image-to-video, and Wan-style prompts.

Read `routing.md`, `output-contracts.md`, [Scene Composition](scene-composition.md), and [Constraints and Revisions](constraints-and-revisions.md) first. These task fields do not change a critique/comparison into prompt writing, authorize video generation, or expand operation and scope permissions. Explicit output formatting overrides presentation defaults below.

## Core Video Fields

The following are available video-description fields, not required slots or permission to invent:

- subject: who or what appears
- scene: where the action happens
- subject motion: what the subject does over time
- environmental motion: weather, particles, crowds, water, lights, fabric, smoke
- camera motion: how the camera moves
- progression: how the scene changes from start to end
- atmosphere and style: visual mood, medium, realism, genre

Express only fields supplied by the user or permitted by the resolved operation, mode, and scope. A model or video template does not authorize missing motion, camera movement, atmosphere, supporting objects, events, or scene content.

Keep video prompts visual. Avoid dialogue, music, sound effects, inner thoughts, and invisible story context unless explicitly requested. If supplied nonvisual information needs a visible rendering, use only supplied cues or cues that the resolved permissions allow.

## Text-to-Video

Use when the video is generated from text alone. Describe the permitted initial content and its authorized changes over time. Do not invent a “full” initial scene or motion merely to populate the format.

Conditional structure:

`[Supplied/permitted initial content]. [Supplied/permitted motion or progression]. [Supplied/permitted camera, style, lighting, or atmosphere].`

Include pace such as slow, smooth, handheld, fast, drifting, or dramatic only when it was supplied or pace may be chosen within the resolved permissions.

## Image-to-Video

Use when an uploaded image or existing image is the first frame.

- Preserve all content established by the source first frame—including subjects, identity, counts, appearance, objects, text, relationships, composition, setting, style, and exclusions—unless the user locally authorizes a change.
- Describe only the motion or change supplied or permitted after that frame. Preserve the rest; do not make static content disappear merely because it is not moving.
- Do not infer active weather, off-frame causes, new objects, or other details from a plausible reading of the frame.
- If no image or description is available, ask for the image or a short description before writing a specific i2v prompt.

Conditional structure:

`Starting from the provided image, [preserved visible content]. [Supplied/permitted motion or change]. [Supplied/permitted camera, lighting, or atmosphere change].`

## Wan Video Format

Use for Wan, Wan-style, or when the user asks for a cinematic single-paragraph video prompt.

Wan prompts should be one cohesive paragraph. Within that paragraph, order only the fields the user supplied or the resolved permissions allow, which may include:

- subject
- scene
- subject and environmental motion
- camera language
- visual atmosphere
- stylization

This ordering is presentation guidance, not a requirement to fill every field. Do not split Wan output into shot lists unless the user asks. Keep the permitted content direct, cinematic, and ready to paste.

Example shape when every depicted field is authorized:

`[Established subject and scene]. [Authorized subject or environmental motion]. [Authorized camera movement and progression]. [Authorized style, lighting, or atmosphere].`

## Camera Language

Use precise camera terms when camera treatment is supplied or may be chosen within the resolved permissions:

- close-up, medium shot, wide shot, extreme wide shot
- low angle, high angle, overhead, eye-level
- tracking shot, dolly in, dolly out, orbit shot, crane shot
- handheld, stabilized, slow push-in, pullback, aerial shot
- rack focus, shallow depth of field, parallax, reveal

Use only a few authorized camera terms per prompt. Too many directions can make the prompt muddy.

## Video Variants

When variants are requested, vary only a dimension the user opened to variation, such as:

- camera motion
- pacing
- lighting change
- subject action
- environment motion
- stylization

Keep protected content and first-frame content unchanged across variants. Vary one meaningful authorized dimension at a time, and keep variants compatible with the same core idea unless the user asks for broad exploration.
