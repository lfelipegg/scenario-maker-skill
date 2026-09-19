# MiniMax H3 reference, first-frame, and frame-extraction workflows

**Question.** What official model/version/interface does the maintainer's “MiniMax H3” mean, and which verified contracts support full-reference prompting, first-frame prompting, and a video-to-first-frame image-editing workflow?

**Source retrieval date:** 2026-09-19

## Executive answer

“MiniMax H3” is now a verifiable first-party model identity, not shorthand that must be mapped to Hailuo 02 or Hailuo 2.3. MiniMax announced it on 2026-07-31 as a general-purpose multimodal generation model; the hosted API model identifier is `MiniMax-H3`, and the V2 OpenAPI description also calls the service “Hailuo-03.” MiniMax H3 is distinct from `MiniMax-H3-Max` (a faster fal.ai-post-trained variant) and from the earlier `MiniMax-Hailuo-02` and `MiniMax-Hailuo-2.3` model families. The hosted creation interface is `POST https://api.minimax.io/v2/video_generation`; it produces asynchronous **video** tasks, not still images ([launch post](https://www.minimax.io/blog/minimax-h3), [model release notes](https://platform.minimax.io/docs/release-notes/models.md), [V2 create contract](https://platform.minimax.io/docs/api-reference/video-generation-v2-create.md), [API overview](https://platform.minimax.io/docs/api-reference/api-overview)).

There are two different H3 input contracts that must not be collapsed:

1. **First-/last-frame generation (FL2VA/I2VA)** uses H3-Base-FL2VA. A `first_frame` is the actual opening frame at 0.00 seconds and anchors its composition and content; the official prompt guide says identity, clothing, colors, key objects, and spatial relationships should remain consistent. This mode is for animating forward from a supplied frame, not for replacing that frame with an edited still ([base prompt guide, commit-pinned](https://github.com/MiniMax-AI/MiniMax-H3/blob/1ce88e916de7c15b63cbaf347642503f9bc21d3d/.agents/skills/h3-prompt-writing/references/base-en.txt), [V2 API roles](https://platform.minimax.io/docs/api-reference/video-generation-v2-create.md)).
2. **Full-reference generation/editing (Ref2VA)** uses H3-Base-Ref2VA. Images, videos, and audio are references rather than hard frame anchors. Natural-language instructions can assign appearance, motion, camera, style, voice, source-video editing, continuation, or audio reuse/reference relationships. MiniMax’s official full-reference rewrite guide is real and defines six sections, but it is a prompt-authoring guide—not six independently required API fields. The API still accepts one required text item plus typed media items and roles ([official H3 repository](https://github.com/MiniMax-AI/MiniMax-H3), [full-reference guide, commit-pinned](https://github.com/MiniMax-AI/MiniMax-H3/blob/1ce88e916de7c15b63cbaf347642503f9bc21d3d/.agents/skills/h3-prompt-writing/references/ref-en.txt), [V2 create contract](https://platform.minimax.io/docs/api-reference/video-generation-v2-create.md)).

A “generate/edit video, then extract its first frame as a still” flow is technically a downstream workflow, not a native H3 still-image or image-editing contract. The verified H3 task returns an MP4 URL and declares `modality: video`; MiniMax documents no H3 endpoint that returns a still image or extracted frame. If the source image is sent as `first_frame`, extracting frame zero should recover the anchored source state, not a newly edited version. If an edited-looking still is wanted, a reference-image or reference-video edit can generate a new video and a separate media tool can extract its first output frame, but preservation, exact edit fidelity, and still-image quality are not guaranteed by the cited API. MiniMax’s separate `image-01` image-to-image endpoint only documents portrait/character subject reference and should not be presented as a general H3 image editor ([query/result contract](https://platform.minimax.io/docs/api-reference/video-generation-v2-query.md), [Image-to-Image API](https://platform.minimax.io/docs/api-reference/image-generation-i2i.md)).

## 1. Model, version, and interface identity

### Verified identities

| Name | Verified meaning | Interface/output |
| --- | --- | --- |
| `MiniMax-H3` | MiniMax’s 2026-07-31 open-weight general-purpose multimodal video model; accepts text, images, video, and audio and generates video with native stereo audio. | Hosted V2 API and hosted apps; open H3-Base checkpoints for local/self-hosted use. Hosted output supports 768P/2K and 4–15 seconds. |
| Hailuo-03 | Name in the V2 OpenAPI `info.description` for the MiniMax H3 service. It is not the request’s `model` value. | The request model enum is `MiniMax-H3` or `MiniMax-H3-Max`. |
| `MiniMax-H3-Max` | Separate fast variant jointly released with fal.ai and post-trained from H3. | Same hosted `content[]` protocol; 480P/768P, 5–15 seconds, no 2K. |
| H3-Base-FL2VA | Open H3 base checkpoint for text-to-audio-video and optional first/last-frame conditioning. | Local/self-hosted generation at a 768-pixel short edge. |
| H3-Base-Ref2VA | Separate open H3 base checkpoint for multimodal reference-to-audio-video. | Local/self-hosted reference generation/editing at a 768-pixel short edge. |
| `MiniMax-Hailuo-02`, `MiniMax-Hailuo-2.3` | Earlier Hailuo video model families, listed separately in MiniMax release notes and legacy API documentation. | Legacy task endpoints; not aliases for `MiniMax-H3`. |

Evidence: MiniMax’s [launch post](https://www.minimax.io/blog/minimax-h3) names H3, its release date, its multimodal context, native stereo audio, 15-second duration, and up-to-2K video output. The [current video guide](https://platform.minimax.io/docs/guides/video-generation.md) and [V2 OpenAPI](https://platform.minimax.io/docs/api-reference/video-generation-v2-create.md) give the exact API model enums and distinguish H3 from H3 Max. The [official repository model table](https://github.com/MiniMax-AI/MiniMax-H3) names the two open H3-Base checkpoints and their tasks. MiniMax’s [release notes](https://platform.minimax.io/docs/release-notes/models.md) list H3, Hailuo 2.3, and Hailuo 02 as separate releases.

### Hosted versus local boundaries

The hosted global endpoint is `POST https://api.minimax.io/v2/video_generation`. It accepts a required `model`, `content[]`, `resolution`, and integer `duration`; every request must contain one non-empty text item. Tasks are asynchronous and resolve through the shared query endpoint to `content.url`, an MP4, with `modality: video` ([create](https://platform.minimax.io/docs/api-reference/video-generation-v2-create.md), [query](https://platform.minimax.io/docs/api-reference/video-generation-v2-query.md)). Hailuo AI and MiniMax Design are hosted app surfaces, not local runtimes ([official repository](https://github.com/MiniMax-AI/MiniMax-H3)).

The open release contains H3-Base-FL2VA and H3-Base-Ref2VA. MiniMax documents local ComfyUI workflows and self-hosted SGLang/vLLM paths. The two checkpoint families are not interchangeable. The open release does **not** include the hosted H3-Context-IR preprocessing system or H3-Regenerate-2K; local H3-Base therefore does not reproduce the full hosted 2K pipeline ([MiniMax local-deployment guide](https://platform.minimax.io/docs/guides/local-deploy-h3.md), [official repository](https://github.com/MiniMax-AI/MiniMax-H3)).

## 2. Full-reference prompting: verified six-section guide

### Provenance

The named guide is verifiable in the first-party `MiniMax-AI/MiniMax-H3` repository. The repository README explicitly says its portable `h3-prompt-writing` skill ships `ref-en.txt` for “full-reference (Ref2VA) mode.” The corresponding skill instructs writers to follow six sections in exact order. GitHub history shows the file was added in commit [`1ce88e9`](https://github.com/MiniMax-AI/MiniMax-H3/commit/1ce88e916de7c15b63cbaf347642503f9bc21d3d) on 2026-08-07; the evidence used here is the immutable [commit-pinned guide](https://github.com/MiniMax-AI/MiniMax-H3/blob/1ce88e916de7c15b63cbaf347642503f9bc21d3d/.agents/skills/h3-prompt-writing/references/ref-en.txt), not an inferred community template.

The six sections are:

1. `subject_definitions`
2. `summary`
3. `retention_analysis`
4. `detailed_description`
5. `overall_soundscape`
6. `non_diegetic_music`

The guide defines four reference-label families: `<Subject N>` for reusable visible content; `<Picture N>` for a concrete target/keyframe/composition anchor; `<Video N>` for whole-video editing, continuation, or temporal structure; and `<Audio N>` for copied or referenced audio. It also defines explicit retention markers such as `fully_preserved`, `partially_preserved`, `attribute_transfer`, and `weak_reference`, plus separate audio markers. These are authoring semantics in the prompt text ([full-reference guide](https://github.com/MiniMax-AI/MiniMax-H3/blob/1ce88e916de7c15b63cbaf347642503f9bc21d3d/.agents/skills/h3-prompt-writing/references/ref-en.txt)).

### Contract boundary

The six-section format is strongly supported as MiniMax’s official Ref2VA prompt-writing format, and the repository’s Full 2K Ref2VA example shows H3-Context-IR producing that structure. It is **not** the wire schema of `POST /v2/video_generation`: the wire schema requires a text `content` item and uses media roles `reference_image`, `reference_video`, and `reference_audio`. Therefore:

- The six-section shape is appropriate when Scenario Maker intentionally emits an H3 full-reference rewrite.
- It should not be imposed on H3 text-only or first-/last-frame prompts; the official base guide gives those modes a different three-field structure.
- It should not be represented as API validation. The API sees text, not six typed JSON properties.
- The hosted optional [`POST /v2/h3_context_ir`](https://platform.minimax.io/docs/api-reference/video-generation-v2-h3-context-ir.md) can produce an enhanced prompt, but MiniMax says that implementation is hosted and not open sourced; it does not itself create a video.

### Reference-input limits and incompatibility

The hosted Ref2VA contract accepts up to 9 reference images, 3 reference videos, and 3 reference audio clips, with at most 12 mixed files. Video and audio clips are 2–15 seconds each and each modality’s total clip duration is at most 15 seconds. Critically, reference roles and first-/last-frame roles are mutually exclusive in one request. A request cannot combine `reference_image`/`reference_video`/`reference_audio` with `first_frame`/`last_frame` ([V2 create contract](https://platform.minimax.io/docs/api-reference/video-generation-v2-create.md)).

## 3. First-frame prompting: what is controlled, preserved, and changed

The API calls this image-to-video. One image with `role: first_frame`—or one image with the role omitted—selects the first-frame scenario. The input image determines aspect ratio and causes `ratio` to be treated as `adaptive`. MiniMax says first/last-frame mode controls the opening or ending frame and brings a specific frame to life ([video guide](https://platform.minimax.io/docs/guides/video-generation.md), [V2 create contract](https://platform.minimax.io/docs/api-reference/video-generation-v2-create.md)).

The official [base prompt guide](https://github.com/MiniMax-AI/MiniMax-H3/blob/1ce88e916de7c15b63cbaf347642503f9bc21d3d/.agents/skills/h3-prompt-writing/references/base-en.txt) is more precise:

- I2VA begins with the fixed alignment statement that `<Picture 1>` is fully referenced at 0.00 seconds.
- `<Picture 1>` is the actual first frame of `[Shot 1]`.
- The prompt should establish the image’s style, subjects, composition, and scene anchors, then develop action forward.
- Character identity, clothing, colors, key objects, and spatial relationships should remain consistent.
- The recommended progression is “first-frame anchor → action onset → continuous development → result or reaction.”

Accordingly, the verified first-frame contract supports changes **after** the anchored opening: subject motion, camera movement, focus changes, evolving physical effects, state changes, dialogue, sound, and music. MiniMax’s own API example asks the video to pull focus to the background and add more ramen steam while supplying the source image as `first_frame`; its Context-IR example describes those effects developing through the clip rather than rewriting the 0.00-second image ([H3-Context-IR example](https://platform.minimax.io/docs/api-reference/video-generation-v2-h3-context-ir.md)).

It does not establish a contract for changing the anchored frame’s clothes, identity, layout, object inventory, or appearance at time zero. Those edits conflict with the official instruction to fully reference the actual first frame and preserve its anchors. A prompt writer may describe later transformations, but should not promise that `first_frame` is a general image-editing input.

## 4. Video/reference editing and extracting a first-frame still

### What is native

H3 natively accepts reference video in Ref2VA. MiniMax describes generalized reference and editing in natural language, and its official Ref2VA example treats a source video as directly edited while preserving its framing, lighting, setting, subject identity, and background, adding new lip motion/dialogue and reusing/reference-mixing audio ([launch post](https://www.minimax.io/blog/minimax-h3), [official repository’s Full 2K Ref2VA case](https://github.com/MiniMax-AI/MiniMax-H3), [full-reference guide](https://github.com/MiniMax-AI/MiniMax-H3/blob/1ce88e916de7c15b63cbaf347642503f9bc21d3d/.agents/skills/h3-prompt-writing/references/ref-en.txt)). Reference relationships are natural-language instructions, so “fully preserved,” “partially preserved,” or “attribute transfer” communicates intent; it is not a pixel-level guarantee.

The hosted V2 API only exposes `reference_video` as a reference-scenario role, not a separate editing operation or deterministic preservation parameter. Local H3 uses the Ref2VA checkpoint for video-to-video/reference editing. ComfyUI also documents control-video and masked video-inpainting workflows, but these are ComfyUI workflow capabilities around the open model and should not be mistaken for the hosted API contract ([ComfyUI H3 guide](https://docs.comfy.org/tutorials/video/minimax/minimax-h3), [MiniMax local-deployment guide](https://platform.minimax.io/docs/guides/local-deploy-h3.md)).

### What is a workaround

The following pipeline is possible in principle but is not a native H3 image endpoint:

1. Submit a Ref2VA request using an image or source video as reference, with natural-language edit and retention instructions.
2. Receive the generated MP4.
3. Use a separate media decoder/extraction tool to decode the first output frame and save it as a still image.

Only steps 1–2 are H3 generation. Step 3 is ordinary post-processing, absent from the MiniMax H3 API contract. The API returns a time-limited video URL and `modality: video`; it does not return PNG/JPEG frames ([query contract](https://platform.minimax.io/docs/api-reference/video-generation-v2-query.md)). No generation or extraction was executed for this research ticket, so this report is not quality proof.

Two materially different cases must be named correctly:

- **Input as `first_frame`:** the first output frame is supposed to be the supplied anchor. Extracting it is effectively recovering the original/anchored frame, not obtaining a newly edited still. Changes are expected to develop after 0.00 seconds.
- **Input as `reference_image` or `reference_video`:** H3 is free to synthesize a new first output frame according to reference and editing instructions. Extracting that frame can yield a changed still, but exact source preservation, requested edit fidelity, temporal stability at the first frame, and still-image quality are unverified and not guaranteed by MiniMax’s API schema.

The first-/last-frame and reference roles cannot be mixed in the hosted request. Therefore there is no verified hosted request that both hard-locks an input as `first_frame` and simultaneously treats the same request as a Ref2VA edit ([V2 create contract](https://platform.minimax.io/docs/api-reference/video-generation-v2-create.md)).

### Separate image API is not an H3 substitute

MiniMax’s hosted image endpoint uses model `image-01` (and its documented enum also lists `image-01-live`), not H3. Its image-to-image contract currently defines `subject_reference` only for `type: character` and recommends a single front-facing portrait. That is evidence for character subject reference, not a documented general-purpose arbitrary image editor, and it should not be substituted for an unverified H3 still-image contract ([Image-to-Image API](https://platform.minimax.io/docs/api-reference/image-generation-i2i.md)).

## 5. Decisive evidence

1. **Identity:** MiniMax’s 2026-07-31 launch and release notes explicitly name MiniMax H3; current OpenAPI requires `model: MiniMax-H3` and labels the V2 API Hailuo-03.
2. **Two base families:** The first-party repository publishes separate FL2VA and Ref2VA checkpoints with different supported tasks.
3. **Six-section guide:** The official repository’s commit-pinned `ref-en.txt` literally names “Full-Reference Mode Rewrite Output Format Guide” and enumerates six ordered sections.
4. **First-frame semantics:** The official commit-pinned base guide says the source picture is the actual first frame at 0.00 seconds and specifies what should remain consistent.
5. **Wire contract:** The V2 API makes first-/last-frame and reference roles mutually exclusive and returns asynchronous video output.
6. **No native still output:** The query schema labels successful generation output `modality: video` and returns an MP4 URL; no first-frame extraction/still response is documented.
7. **Hosted/local split:** MiniMax states H3-Context-IR and H3-Regenerate-2K are not in the open release; H3-Base FL2VA/Ref2VA can be local/self-hosted.

## 6. Implications and options (not product decisions)

- Scenario Maker can expose **H3 base/keyframe prompting** and **H3 full-reference prompting** as separate output contracts. The former follows the three-field base guide; the latter follows the verified six-section guide.
- A first-frame prompt can accurately promise “start from/animate this frame,” while a reference prompt can express “preserve/change/transfer these attributes.” Calling both “image editing” would erase a meaningful model contract.
- If a still deliverable is desired from H3, an option is to label it explicitly as **Ref2VA video generation plus external first-frame extraction**, with a warning that this is a workaround and not H3 still-image generation.
- If fidelity to the original at 0.00 seconds is the priority, `first_frame` is the verified route, but it works against editing that exact frame. If changing the still is the priority, `reference_image`/`reference_video` leaves room for changes but weakens exact frame preservation.
- Hosted integration can use `MiniMax-H3` and optional hosted Context-IR/2K services. Local support needs an explicit FL2VA-versus-Ref2VA checkpoint choice and should not claim hosted Context-IR or native 2K regeneration.
- Any future product wording should keep `MiniMax-H3-Max` and prior Hailuo versions separate until a deliberate model-target decision is made.

## 7. Uncertainties and unsupported claims

- MiniMax documents semantic preservation/editing behavior but does not publish a deterministic fidelity threshold for source-video edits or reference-image changes. “Fully preserved” is prompt intent, not an API guarantee.
- The official first-frame guide says the input is the actual first frame, but the reviewed sources do not specify whether an encoded output’s decoded first frame is pixel-identical to the uploaded image. Do not promise byte- or pixel-level identity.
- The reviewed official MiniMax sources do not document a native H3 still-image output, “return first frame” option, or supported frame-extraction command.
- No official evidence was found that a first-frame-conditioned request can edit the 0.00-second frame while retaining first-frame semantics. The verified semantics point the other way.
- ComfyUI’s multiframe guides, control video, masks, and video inpainting broaden local workflows, but they are not evidence that the hosted H3 API accepts those controls or returns still images.
- The six-section guide is official repository guidance, but the API does not validate that textual layout. H3-Context-IR may emit it for Ref2VA; clients may also author it themselves.
- The guide file’s first recorded commit is attributed to “Copilot App” and is unsigned. Its first-party provenance rests on publication in the official MiniMax-AI repository and the repository README/skill explicitly adopting it, not on a signed release artifact.

## 8. Searches performed

Primary-source discovery covered MiniMax’s H3 launch post, release notes, model/API overview, V2 create/query/Context-IR contracts, video and local-deployment guides, image-to-image contract, the official `MiniMax-AI/MiniMax-H3` repository and commit history, and the official ComfyUI H3 documentation linked by MiniMax. Searches for an official H3 still-image or first-frame-extraction endpoint returned only the video-generation and image-to-video documentation; no first-party H3 still/extraction contract was located as of the retrieval date.
