# Wan text-to-video and image-to-video contracts

**Question.** What exact official Wan models/versions and task-specific prompting rules should inform distinct text-to-video (T2V) and image-to-video (I2V) routes?

**Source retrieval date:** 2026-09-19

## Executive finding

Wan does not have one stable, universal “cinematic paragraph” contract. The official guidance gives the two routes different semantic jobs:

- **T2V constructs the shot:** entity + scene + motion, optionally expanded with appearance, environment, lighting, framing, lens/camera movement, and style. The official prompt formula and Wan2.2 prompt extender both treat these as scene-defining inputs ([Alibaba Cloud prompt guide, “Prompt formulas”](https://www.alibabacloud.com/help/en/model-studio/text-to-video-prompt#d28c8c82af3pz); [Wan2.2 T2V extender instructions](https://github.com/Wan-Video/Wan2.2/blob/main/wan/utils/system_prompt.py)).
- **I2V animates a supplied frame:** the image already defines entity, scene, and style, so the official formula is **motion + camera movement**. Wan2.2’s I2V extender explicitly removes static descriptions already visible in the image and preserves or expands dynamic content ([Alibaba Cloud prompt guide, “Image-to-video formula”](https://www.alibabacloud.com/help/en/model-studio/text-to-video-prompt#d28c8c82af3pz); [Wan2.2 I2V extender instructions](https://github.com/Wan-Video/Wan2.2/blob/main/wan/utils/system_prompt.py)).

Accordingly, Scenario Maker can support distinct prompt-writing contracts without choosing an inference implementation. It must not promise source identity, exact temporal obedience, or output quality: the official sources specify conditioning and recommended prompt structure, not guarantees of fidelity.

## Official model and interface landscape

### Open-weight/local Wan

The current first-party open repository is **Wan2.2**. It publishes three relevant checkpoints ([Wan2.2 repository, model table](https://github.com/Wan-Video/Wan2.2#model-download)):

| Official checkpoint | Task identity | Published interface facts |
|---|---|---|
| [`Wan-AI/Wan2.2-T2V-A14B`](https://huggingface.co/Wan-AI/Wan2.2-T2V-A14B) | Dedicated T2V MoE model | 480P and 720P; its model card says it generates 5-second videos. Official CLI task: `t2v-A14B`. |
| [`Wan-AI/Wan2.2-I2V-A14B`](https://huggingface.co/Wan-AI/Wan2.2-I2V-A14B) | Dedicated I2V MoE model | 480P and 720P; requires an input image in the official CLI; output aspect ratio follows the input image. Official CLI task: `i2v-A14B`. |
| [`Wan-AI/Wan2.2-TI2V-5B`](https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B) | Unified dense T2V + I2V model | 720P at 24 fps; official examples use `1280*704` or `704*1280`; passing `--image` selects I2V and omitting it selects T2V. Official CLI task: `ti2v-5B`. The model card gives 24 GB VRAM (RTX 4090) as its example single-GPU configuration. |

The official repository also links separate first-party **Diffusers-format** artifacts for all three models, so “Wan2.2” alone does not identify checkpoint packaging or runtime interface ([Wan2.2 release/integration notice](https://github.com/Wan-Video/Wan2.2#latest-news)).

**Older but materially different local option.** Wan2.1 remains relevant only if local resource constraints drive the choice: it publishes `Wan2.1-T2V-1.3B` (480P recommended; the repository reports 8.19 GB VRAM), `Wan2.1-T2V-14B`, and separate 14B I2V checkpoints for 480P and 720P. There is no first-party Wan2.1 1.3B I2V checkpoint in its model table ([Wan2.1 repository, model table and notes](https://github.com/Wan-Video/Wan2.1#model-download)). Thus “use the small Wan model for both routes” is unsupported by the official open checkpoint matrix.

### Hosted Alibaba Cloud Wan

Hosted model names and protocols are a separate product surface and must not be treated as aliases for the open checkpoints:

- The current dedicated hosted T2V API documents `wan2.7-t2v` and the dated `wan2.7-t2v-2026-06-12`; it requires a text prompt, accepts Chinese or English up to 5,000 characters, and exposes 720P/1080P and 2–15 second outputs ([Wan2.7 T2V API reference](https://www.alibabacloud.com/help/en/model-studio/text-to-video-api-reference)).
- The current hosted I2V API examples use dated `wan2.7-i2v-2026-04-25`. Its unified `media` array distinguishes `first_frame`, `last_frame`, `driving_audio`, and `first_clip`, and supports only documented combinations for first-frame generation, first/last-frame generation, and continuation. The prompt is optional and accepts up to 5,000 characters ([Wan2.7 I2V API reference](https://www.alibabacloud.com/help/en/model-studio/image-to-video-general-api-reference)).
- The legacy I2V protocol covers Wan2.1–2.6 and uses a required `img_url`; the current docs recommend Wan2.7 instead. Its aliases, limits, duration, resolution, audio, and shot controls vary by model ([legacy first-frame I2V API reference](https://www.alibabacloud.com/help/en/model-studio/legacy-image-to-video-api-reference)).

There is a live-documentation inconsistency worth preserving as an uncertainty: the T2V user guide retrieved on this date leads with `wan3.0-video`, while the linked API reference is titled Wan2.7 and says its new protocol supports only Wan2.7 ([T2V user guide](https://www.alibabacloud.com/help/en/model-studio/text-to-video-guide); [T2V API reference](https://www.alibabacloud.com/help/en/model-studio/text-to-video-api-reference)). A model selector should therefore pin an exact documented model ID and interface rather than infer “latest Wan.”

## T2V prompt-writing contract: construct the scene and its evolution

### Evidence-backed fields

The official basic formula is **Entity + Scene + Motion**. Its advanced form adds detailed entity and scene descriptions, motion amplitude/speed/effect, aesthetic controls, and stylization ([official prompt guide](https://www.alibabacloud.com/help/en/model-studio/text-to-video-prompt#d28c8c82af3pz)). This supports the following route fields:

1. **Entity/subject:** what exists and its visually relevant appearance.
2. **Scene/environment:** foreground, background, place, time, and environmental state.
3. **Motion:** concrete subject actions plus moving environmental elements; qualify speed and intensity where useful.
4. **Temporal progression:** order action as a short evolution (“first …, then …, finally …”) when the result depends on change over time. Wan2.2’s official extender instructs the rewriting model to explain how an action unfolds and, when appropriate, add motion to background elements such as drifting clouds or wind-blown leaves ([Wan2.2 T2V system prompt](https://github.com/Wan-Video/Wan2.2/blob/main/wan/utils/system_prompt.py)).
5. **Camera/aesthetic controls:** shot size, angle, composition, lens, lighting, color, and camera movement. The guide distinguishes camera moves by effect and lists explicit terms such as push-in, pull-out, tracking, orbit, and fixed camera ([official advanced formula and camera guidance](https://www.alibabacloud.com/help/en/model-studio/text-to-video-prompt#d28c8c82af3pz)).
6. **Style:** include it when the user asks for one. Wan2.2’s official extender specifically says not to invent a style absent from the original prompt and to avoid cinematic-aesthetic additions when those conflict with a non-photoreal style such as 2D illustration ([Wan2.2 T2V system prompt](https://github.com/Wan-Video/Wan2.2/blob/main/wan/utils/system_prompt.py)).

**Research-derived prompt shape (not an official mandatory syntax):** `subject/appearance + environment/state + ordered subject and environmental motion + camera/framing + lighting/style`. This is a field ordering inferred from the official dimensions; the sources do not require headings, commas, or one paragraph.

### Scene changes and multiple shots

Do not silently encode a multi-shot narrative as one ordinary shot. For hosted Wan2.7, the official multi-shot formula is **overall description + shot number + timestamp + shot content**. The prompt itself controls shot structure; the guide says Wan2.7 no longer uses `shot_type`, and “Generate single shot.” is the documented way to request one continuous shot ([official multi-shot formula](https://www.alibabacloud.com/help/en/model-studio/text-to-video-prompt#d28c8c82af3pz)). This is version-specific hosted guidance, not a proven hard syntax for open Wan2.2.

For a single shot, temporal/environmental change should be described as motion inside the shot (for example, clouds gather while the subject turns and the camera pulls back), not as disconnected scene inventory. The official guide advises against very long or complex action sequences and rapid scene changes within one clip ([official “What not to prompt” table](https://www.alibabacloud.com/help/en/model-studio/text-to-video-prompt#d88b150354e2)).

## I2V prompt-writing contract: preserve the source frame as the visual anchor

### Reference requirement and semantics

A dedicated I2V route requires an image reference. In open Wan2.2, `i2v-A14B` asserts that an image path is present; the CLI describes `--image` as the image from which to generate video and says output aspect ratio follows that image ([official Wan2.2 generation interface](https://github.com/Wan-Video/Wan2.2/blob/main/generate.py); [I2V model card](https://huggingface.co/Wan-AI/Wan2.2-I2V-A14B)). In hosted Wan2.7, a first-frame route requires a `media` entry whose type is `first_frame`; other media combinations mean different tasks ([Wan2.7 I2V API reference, media combinations](https://www.alibabacloud.com/help/en/model-studio/image-to-video-general-api-reference)).

The prompt guide states that the image defines **entity, scene, and style**, and reduces the I2V formula to **Motion + Camera movement** ([official I2V formula](https://www.alibabacloud.com/help/en/model-studio/text-to-video-prompt#d28c8c82af3pz)). Wan2.2’s official I2V extender adds operational detail: retain the prompt’s dynamic parts and main-subject action; infer a subject from the image if the input is only an action; condense an overlong action; add reasonable motion detail to an underspecified action; retain camera motion; and remove static descriptions of content already visible in the frame ([Wan2.2 I2V system prompt](https://github.com/Wan-Video/Wan2.2/blob/main/wan/utils/system_prompt.py)).

This makes “preservation” a prompt-authoring discipline, not a guaranteed generation outcome:

- Treat source appearance, composition, scene, and style as authoritative defaults; do not gratuitously redescribe or contradict them.
- Describe **what begins moving**, **how it changes over time**, and **how strongly/quickly**.
- Describe environmental motion only when requested or useful (wind lifts fabric, reflections ripple, light changes); do not replace the frame with a new scene by default.
- State camera behavior explicitly, including `fixed camera` when preservation of composition matters. The official guide explicitly offers that phrase ([official I2V formula](https://www.alibabacloud.com/help/en/model-studio/text-to-video-prompt#d28c8c82af3pz)).
- Use a short chronological chain for action progression rather than rebuilding the full scene description.

**Research-derived prompt shape (not an official mandatory syntax):** `subject motion and progression + environmental changes + camera movement`. The image itself is a separate required input, not prose to be serialized into the prompt.

No cited first-party source promises exact identity, geometry, wardrobe, background, or pixel preservation across generated frames. Scenario Maker should therefore say that the source frame anchors those properties, not that the model will preserve them perfectly.

## Hard requirements versus recommendations and examples

| Status | Evidence |
|---|---|
| **Hard interface requirement (open I2V-A14B):** provide an image. | `generate.py` asserts it for `i2v-A14B` ([source](https://github.com/Wan-Video/Wan2.2/blob/main/generate.py)). |
| **Hard interface requirement (hosted Wan2.7 T2V):** prompt required; Chinese/English; up to 5,000 characters. | Current API schema ([source](https://www.alibabacloud.com/help/en/model-studio/text-to-video-api-reference)). |
| **Hard interface requirement (hosted Wan2.7 I2V):** valid typed media combination; prompt optional and up to 5,000 characters. | Current API schema ([source](https://www.alibabacloud.com/help/en/model-studio/image-to-video-general-api-reference)). |
| **Hard open-CLI video constraint:** `frame_num` must be `4n+1`; task-specific sizes are validated. | Wan2.2 argument parser and validation ([source](https://github.com/Wan-Video/Wan2.2/blob/main/generate.py)). This is inference configuration, not prompt grammar. |
| **Official recommendation:** enable Wan2.2 prompt extension because it can enrich details and improve quality. | Wan2.2 model cards/README ([source](https://github.com/Wan-Video/Wan2.2#using-prompt-extention)). It is optional (`--use_prompt_extend`). |
| **Prompt-extender output contract, not base-model limit:** T2V rewrite is 60–200 words; I2V rewrite is at most 100 words and dynamic-only. | Wan2.2 system prompts ([source](https://github.com/Wan-Video/Wan2.2/blob/main/wan/utils/system_prompt.py)). These constraints govern the bundled Qwen/DashScope rewriting instructions; official direct-generation examples do not establish them as hard model-token limits. |
| **Examples, not mandatory syntax:** cinematic prefix lists and long descriptive paragraphs in the model cards. | Example prompts in [`generate.py`](https://github.com/Wan-Video/Wan2.2/blob/main/generate.py) and model cards. The official formulas define dimensions, not a required prose template. |

Prompt extension is itself task-specific. Wan2.2 routes T2V through a text LLM (`qwen-plus` or local Qwen Instruct) and I2V through a vision-language model (`qwen-vl-max` or local Qwen2.5-VL) that receives the source image. The unified TI2V checkpoint chooses T2V versus I2V extender instructions according to whether a visual-language path/image is used ([Wan2.2 prompt-extension implementation](https://github.com/Wan-Video/Wan2.2/blob/main/wan/utils/prompt_extend.py); [Wan2.2 README](https://github.com/Wan-Video/Wan2.2#using-prompt-extention)). This is decisive evidence that one blind text-only rewrite is not the official design for both tasks.

## Implications and options for Scenario Maker

These are implementation options supported by the evidence, not product decisions:

1. **Separate route schemas.** T2V can collect subject, scene, subject motion, environmental motion/change, temporal order, camera, lighting/composition, and style. I2V can require a source image at execution time and collect subject motion, environmental change, temporal order, and camera behavior while treating visible source details as inherited.
2. **Pin model identity in the output contract.** Possible explicit targets are open `Wan2.2-T2V-A14B` / `Wan2.2-I2V-A14B`; unified local `Wan2.2-TI2V-5B`; older resource-oriented Wan2.1 variants; or hosted dated Wan2.7 IDs. “Wan” by itself is not precise enough.
3. **Keep prompt generation independent from inference configuration.** Frame count, resolution, duration, source media, and hosted protocol fields can be surfaced as metadata/options rather than embedded as unstructured prompt prose.
4. **Use a visual-aware rewrite path for I2V if automatic expansion is offered.** The first-party implementation uses the source image for I2V extension; a text-only expander cannot follow the official instruction to remove static details already visible in that image.
5. **Expose single-shot versus multi-shot only where the selected version supports a documented contract.** Hosted Wan2.7 uses natural-language shot structure; open Wan2.2 sources cited here do not document an equivalent hard multi-shot syntax.
6. **Avoid fidelity promises.** Report “source-anchored I2V prompt” rather than “preserves the image,” unless later generation evaluation establishes a narrower observable claim.

## Maintainer choices still open

- Which exact target comes first: open Wan2.2 dedicated A14B checkpoints, unified TI2V-5B, older Wan2.1 for lower local VRAM, or hosted Wan2.7?
- If local, is 24 GB-class hardware available for TI2V-5B, and is the much larger A14B path acceptable? The official sources do not provide a small first-party I2V counterpart to Wan2.1 T2V-1.3B.
- Should “Wan T2V/I2V” output only prompts, or also structured inference metadata (checkpoint ID, image requirement, aspect/resolution, frame count/duration)?
- Should automatic prompt extension be replicated by Scenario Maker, left to Wan’s optional extender, or disabled to avoid two successive rewrites?
- For hosted targets, should aliases (which may move) or dated IDs (which pin behavior) be emitted, and which deployment region/protocol is in scope?
- Are multi-shot, first-and-last-frame, continuation, audio, and reference-to-video future separate routes? Official Wan2.7 treats them as distinct media contracts; folding them into ordinary first-frame I2V would erase required inputs.

## Limitations and unsupported claims

- This is source research, not generated-video evaluation. It provides no proof of image quality, motion quality, prompt adherence, or preservation fidelity.
- The open Wan2.2 system prompts are instructions for the optional prompt-extension model. They are strong evidence of the publisher’s task-specific rewrite policy, but not a formal specification of the diffusion model’s tokenizer or a guarantee that direct prompts outside those lengths fail.
- Hosted documentation is mutable and region-specific. On the retrieval date, the T2V guide and linked API reference expose inconsistent leading versions (`wan3.0-video` versus Wan2.7). Exact availability must be checked when a hosted target is selected.
- The cited sources do not establish that all third-party ComfyUI nodes, wrappers, quantizations, LoRAs, or Diffusers versions accept identical fields or reproduce first-party behavior.
- No official source reviewed here supports the claim that a single generic cinematic paragraph is optimal for both T2V and I2V; the strongest primary evidence says the opposite.
