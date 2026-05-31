# Video Prompts

Use this reference for text-to-video, image-to-video, and Wan-style prompts.

## Core Video Fields

Strong video prompts include:

- subject: who or what appears
- scene: where the action happens
- subject motion: what the subject does over time
- environmental motion: weather, particles, crowds, water, lights, fabric, smoke
- camera motion: how the camera moves
- progression: how the scene changes from start to end
- atmosphere and style: visual mood, medium, realism, genre

Keep video prompts visual. Avoid dialogue, music, sound effects, inner thoughts, and invisible story context unless explicitly requested.

## Text-to-Video

Use when the video is generated from text alone. Describe the full initial scene and how it moves.

Good structure:

`[Subject] in [scene]. [Subject motion] while [environmental motion]. The camera [camera motion], revealing [progression]. [Style], [lighting], [atmosphere].`

Include a clear pace such as slow, smooth, handheld, fast, drifting, or dramatic when it affects the result.

## Image-to-Video

Use when an uploaded image or existing image is the first frame.

- Preserve the source image's subject, composition, style, and identity unless the user asks for changes.
- Focus on what begins moving after the still frame.
- Avoid inventing details about the source image if it is not described or visible.
- If no image or description is available, ask for the image or a short description before writing a specific i2v prompt.

Good structure:

`Starting from the provided image, [preserved subject/scene] begins to [motion]. [Environment] moves with [visible change]. The camera [camera motion] while [lighting/atmosphere] shifts subtly.`

## Wan Video Format

Use for Wan, Wan-style, or when the user asks for a cinematic single-paragraph video prompt.

Wan prompts should be one cohesive paragraph containing:

- subject
- scene
- subject and environmental motion
- camera language
- visual atmosphere
- stylization

Do not split Wan output into shot lists unless the user asks. Keep it direct, cinematic, and ready to paste.

Example shape:

`A lone warrior walks through a snow-covered mountain pass as wind drives sheets of snow across the landscape. The camera begins with a low-angle tracking shot before slowly rising into an aerial orbit, revealing towering peaks beneath a storm-filled sky. Photorealistic cinematic style, dramatic lighting, slow-motion snow particles.`

## Camera Language

Use precise camera terms when helpful:

- close-up, medium shot, wide shot, extreme wide shot
- low angle, high angle, overhead, eye-level
- tracking shot, dolly in, dolly out, orbit shot, crane shot
- handheld, stabilized, slow push-in, pullback, aerial shot
- rack focus, shallow depth of field, parallax, reveal

Use only a few camera terms per prompt. Too many directions can make the prompt muddy.

## Video Variants

When giving variants, vary one meaningful dimension at a time:

- camera motion
- pacing
- lighting change
- subject action
- environment motion
- stylization

Keep variants compatible with the same core idea unless the user asks for broad exploration.
