# FLUX family generation and editing contracts

Source retrieval date: 2026-09-19

## Question

Which exact official models and versions could the requested **Flux**, **Flux Klein**, and **Flux Klein Edit** routes mean, and what generation versus editing prompt contracts do Black Forest Labs' primary sources support?

## Executive answer

1. **`Flux` is not an exact model identity.** Black Forest Labs (BFL) publishes multiple, materially different image families and variants under that name. Its current image documentation recommends **FLUX.2** for new text-to-image work, while its official FLUX.1 repository still lists `FLUX.1 [schnell]`, `FLUX.1 [dev]`, `FLUX.1 Krea [dev]`, and task-specific FLUX.1 checkpoints such as `FLUX.1 Kontext [dev]` for editing. A route named only `Flux` therefore needs a human choice of family, checkpoint/service tier, and interface; research cannot map it uniquely. ([FLUX.2 text-to-image docs](https://docs.bfl.ai/flux_2/flux2_text_to_image), [official FLUX.1 repository/model table](https://github.com/black-forest-labs/flux))
2. **The exact current family name behind “Flux Klein” is `FLUX.2 [klein]`.** It is a family, not one checkpoint. BFL lists distilled 4B and 9B models, undistilled Base 4B and Base 9B models, and a 9B KV-cache variant; BFL also publishes quantized builds. ([official FLUX.2 inference repository](https://github.com/black-forest-labs/flux2), [BFL Klein announcement](https://bfl.ai/blog/flux2-klein-towards-interactive-visual-intelligence))
3. **No distinct BFL checkpoint or API endpoint named “FLUX.2 Klein Edit” was found.** The decisive first-party evidence says Klein unifies text-to-image, single-reference editing, and multi-reference editing in one model. The official API uses the same `/v1/flux-2-klein-4b` or `/v1/flux-2-klein-9b` endpoint and request schema for generation and editing; adding `input_image` fields changes the workflow. “Flux Klein Edit” is therefore supported as a **product route/mode over a Klein checkpoint**, not as an official model identity. ([BFL Klein announcement](https://bfl.ai/blog/flux2-klein-towards-interactive-visual-intelligence), [4B API reference](https://docs.bfl.ai/api-reference/models/generate-or-edit-an-image-with-flux2-%5Bklein%5D-4b), [9B API reference](https://docs.bfl.ai/api-reference/models/generate-or-edit-an-image-with-flux2-%5Bklein%5D-9b))
4. **One editing-optimized checkpoint does exist, but it is not an edit-only model:** `FLUX.2 [klein] 9B KV`. BFL describes it as the 9B model with cached reference-image key/value projections for faster editing, and the repository's model table still marks it capable of text-to-image, single-reference editing, and multi-reference editing. It must not be silently equated with a generic “Klein Edit” route. ([BFL KV-cache guide](https://github.com/black-forest-labs/flux2/blob/main/docs/flux2_klein_kv_cache.md), [official FLUX.2 model table](https://github.com/black-forest-labs/flux2#model-overview))

## Exact identities and version distinctions

| Candidate | Official identifier / alias | Distillation and intended use | Generation/edit support | Availability and license |
| --- | --- | --- | --- | --- |
| FLUX.2 Klein 4B | HF `black-forest-labs/FLUX.2-klein-4B`; local CLI `flux.2-klein-4b`; API `/v1/flux-2-klein-4b` | Step- and guidance-distilled; official reference parameters are 4 steps and guidance 1.0 | T2I, single-reference edit, multi-reference edit in one checkpoint | Local weights and API; Apache-2.0 |
| FLUX.2 Klein 9B | HF `black-forest-labs/FLUX.2-klein-9B`; local CLI `flux.2-klein-9b`; API `/v1/flux-2-klein-9b` | Step- and guidance-distilled; 4 steps and guidance 1.0 | T2I, single-reference edit, multi-reference edit in one checkpoint | Local weights and API; FLUX Non-Commercial License for open weights |
| FLUX.2 Klein 9B KV | HF `black-forest-labs/FLUX.2-klein-9B-kv`; local CLI `flux.2-klein-9b-kv`; API preview is described as a 9B KV-cached serving variant | Same 4-step/guidance-distilled contract, with reference-token KV caching | Same three tasks; optimized especially for reference-image editing | Local weights; non-commercial open-weight license. BFL documents `/v1/flux-2-klein-9b-preview` as the latest KV-cached API variant, while `/v1/flux-2-klein-9b` is the fixed endpoint |
| FLUX.2 Klein Base 4B | HF `black-forest-labs/FLUX.2-klein-base-4B`; local CLI `flux.2-klein-base-4b` | Undistilled; reference defaults 50 steps and guidance 4.0; intended for fine-tuning/custom pipelines and higher diversity | T2I and single-/multi-reference editing | Local only, not public API; Apache-2.0 |
| FLUX.2 Klein Base 9B | HF `black-forest-labs/FLUX.2-klein-base-9B`; local CLI `flux.2-klein-base-9b` | Undistilled; reference defaults 50 steps and guidance 4.0; intended for research/fine-tuning/customization | T2I and single-/multi-reference editing | Local only, not public API; FLUX Non-Commercial License |
| FLUX.2 dev | HF `black-forest-labs/FLUX.2-dev`; local CLI `flux.2-dev` | 32B open-weight FLUX.2 development model; 50-step/guidance-4 defaults in BFL's reference registry | T2I and single-/multi-reference editing | Local; FLUX Non-Commercial License |

The identifiers, default/fixed parameters, and repository IDs above come directly from BFL's [`FLUX2_MODEL_INFO` registry](https://github.com/black-forest-labs/flux2/blob/main/src/flux2/util.py). The capability and license matrix comes from the [official FLUX.2 repository model overview](https://github.com/black-forest-labs/flux2#model-overview). The Base variants are explicitly not served by the public API, according to the [FLUX.2 overview](https://docs.bfl.ai/flux_2/flux2_overview#flux2-klein-models).

BFL additionally announces FP8 and NVFP4 quantizations of all Klein variants. Those are deployment formats of the named variants, not new generation/edit prompt contracts; selecting one remains a hardware/runtime decision. ([BFL Klein announcement, “Quantized versions”](https://bfl.ai/blog/flux2-klein-towards-interactive-visual-intelligence#quantized-versions))

### Why the generic `Flux` identity remains open

BFL's present FLUX.2 family includes `[klein]`, `[pro]`, `[flex]`, `[max]`, and `[dev]`, with different interfaces and controls. Its overview calls `[dev]` the local-development option and recommends `[pro]`/`[max]`/`[flex]`/`[klein]` for different hosted purposes. ([FLUX.2 overview](https://docs.bfl.ai/flux_2/flux2_overview)) Separately, BFL's FLUX.1 repository retains generation checkpoints (`FLUX.1 [schnell]`, `FLUX.1 [dev]`, `FLUX.1 Krea [dev]`) and specialized editing/conditioning checkpoints (`Kontext`, Fill, Canny, Depth, Redux). ([official FLUX.1 repository](https://github.com/black-forest-labs/flux)) Consequently:

- “Flux” cannot safely alias `FLUX.1 [dev]`, `FLUX.2 [dev]`, any hosted Pro model, or Klein without an explicit product decision.
- For a **current local unified generation/editing** route, `FLUX.2 [dev]` is a documented candidate, but its size/license and the smaller Klein choices are materially different.
- If “Flux” was intended to mean a **legacy FLUX.1 text-to-image** route, the exact `[schnell]`, `[dev]`, or Krea checkpoint still must be named; those are not aliases of one another.

## Prompt contract

### Text-to-image generation

BFL documents a natural-language instruction contract rather than tag-only syntax. Its prompt guide recommends a clear subject first, then action/state, mood/context, and only visual details that improve the requested image. A useful optional structure is image type/subject, location, style, camera settings, lighting, colors, effect, and supporting elements; it is an aid, not a required schema. FLUX.2 supports prompts up to 32K tokens, but BFL explicitly advises starting short and adding only effective detail. ([BFL prompt-building guide](https://docs.bfl.ai/guides/prompting_unified_building))

The hosted FLUX.2 documentation supports ordinary text and JSON-structured prompt text, direct quoted text for typography, and hexadecimal color descriptions. These are prompt forms, not separate output tasks. ([FLUX.2 text-to-image examples](https://docs.bfl.ai/flux_2/flux2_text_to_image))

Klein specifically does **not** receive BFL's hosted automatic prompt upsampling: “what you write is what you get,” so BFL advises descriptive prompts. ([technical prompting guide](https://docs.bfl.ai/guides/prompting_unified_technical#prompt-upsampling), [FLUX.2 overview](https://docs.bfl.ai/flux_2/flux2_overview#flux2-klein-models)) The official local CLI nevertheless exposes optional `upsample_prompt_mode=local|openrouter|none`; that is a wrapper-side facility using another model/service, not an intrinsic Klein checkpoint or hosted Klein API field. ([official CLI source](https://github.com/black-forest-labs/flux2/blob/main/scripts/cli.py))

### Single-reference editing

The model input becomes an editing request when a reference image accompanies the prompt. The wording should state the target change and explicitly state what must remain the same. BFL's guide gives patterns such as changing one attribute while retaining pose, composition, texture, or “everything else”; vague instructions such as “make it better” are discouraged. ([single-reference editing guide](https://docs.bfl.ai/guides/prompting_editing_single_reference#writing-effective-single-reference-prompts))

This preservation language is an **instruction**, not an API-strength slider or deterministic guarantee. The specific Klein API schema exposes no edit-strength/denoise-strength field. ([Klein 4B API schema](https://docs.bfl.ai/api-reference/models/generate-or-edit-an-image-with-flux2-%5Bklein%5D-4b))

### Multi-reference editing

For multiple inputs, BFL instructs callers to identify each source by position (`image 1`, `image 2`, and so on), assign each source a role, state the target composition, and name what should be preserved. Its examples separately identify the subject, scene, material/style, and layout sources. ([multi-reference editing guide](https://docs.bfl.ai/guides/prompting_editing_multi_reference))

The Klein hosted contract accepts `input_image` through `input_image_4`, so its specific limit is four references. The broader FLUX.2 editing page's eight-API/ten-playground statement applies to other variants; BFL's comparison table and Klein schema narrow Klein to four. ([Klein 9B API schema](https://docs.bfl.ai/api-reference/models/generate-or-edit-an-image-with-flux2-%5Bklein%5D-9b), [FLUX.2 comparison table](https://docs.bfl.ai/flux_2/flux2_overview#which-model-to-choose)) BFL's local CLI accepts a list of input-image paths, but the examined first-party source does not publish a maximum for local Klein inference; do not inherit the API limit or claim unlimited local references without runtime-specific evidence. ([official CLI source](https://github.com/black-forest-labs/flux2/blob/main/scripts/cli.py))

### Negative prompts

BFL says most FLUX models do not support negative prompts and recommends positive replacement descriptions (for example, describe “empty pathways” instead of “no crowds”). The Klein API and BFL local CLI expose no `negative_prompt` field. A Scenario Maker contract should therefore produce positive visual instructions rather than inventing a separate negative-prompt channel for these official interfaces. ([BFL technical prompting guide](https://docs.bfl.ai/guides/prompting_unified_technical#working-without-negative-prompts), [Klein API schema](https://docs.bfl.ai/api-reference/models/generate-or-edit-an-image-with-flux2-%5Bklein%5D-4b), [official CLI configuration](https://github.com/black-forest-labs/flux2/blob/main/scripts/cli.py))

## Interface-specific controls and supported workflows

| Interface | Generation versus editing switch | Relevant controls | Important limits/distinctions |
| --- | --- | --- | --- |
| BFL Klein API | Same model endpoint; omit image fields for T2I, supply `input_image`…`input_image_4` for editing/reference generation | Required `prompt`; optional seed, width, height, safety tolerance, output format, webhook fields | No negative prompt, guidance, steps, edit strength, or prompt-upsample field in the Klein schema; at most four image inputs. 4B and 9B are separate endpoints; 9B also has preview versus fixed endpoints |
| BFL local reference CLI | Same checkpoint/path; an empty `input_images` list is T2I, one or more paths supply edit references | prompt, seed, width, height, input images, optional output-size match to one reference, steps, guidance, and wrapper prompt-upsample mode | Distilled Klein fixes 4 steps/guidance 1.0; Base defaults to 50/4.0 and does not mark them fixed. The CLI provides no negative-prompt or edit-strength control |
| Diffusers | Same `Flux2KleinPipeline`; image input(s) invoke the image-conditioned path | Pipeline/runtime controls include prompt, dimensions, generator seed, steps, and guidance as supported by the chosen variant | BFL model cards show 4-step/guidance-1 distilled usage and 50-step/guidance-4 Base usage. Exact installed Diffusers version remains an integration choice ([4B model card](https://huggingface.co/black-forest-labs/FLUX.2-klein-4B), [Base 4B model card](https://huggingface.co/black-forest-labs/FLUX.2-klein-base-4B)) |
| ComfyUI | Workflow topology supplies no image or one/multiple images to the same model family | Node/sampler controls depend on the chosen Base/distilled workflow | Comfy's official templates separately demonstrate 4B/9B, Base/distilled, T2I/edit workflows, but the “Image Edit” template names are workflow names rather than evidence of edit-only BFL checkpoints ([ComfyUI Klein guide](https://docs.comfy.org/tutorials/flux/flux-2-klein)) |

BFL's own repository is the strongest supported local workflow: install the `flux2` project and run its interactive CLI for both text-to-image and one-/multi-image editing. It has explicit aliases for the five Klein checkpoints plus 9B KV and FLUX.2 dev. ([official repository local instructions](https://github.com/black-forest-labs/flux2#local-installation), [model registry](https://github.com/black-forest-labs/flux2/blob/main/src/flux2/util.py)) BFL model cards also explicitly name Diffusers and ComfyUI as supported runtimes. ([4B model card](https://huggingface.co/black-forest-labs/FLUX.2-klein-4B), [9B model card](https://huggingface.co/black-forest-labs/FLUX.2-klein-9B))

## Decisive evidence on “Klein Edit”

The conclusion that “Klein Edit” is a mode/route label rather than a distinct official edit checkpoint rests on converging primary evidence:

- BFL says Klein has “unified generation and editing” in a “single model.” ([announcement](https://bfl.ai/blog/flux2-klein-towards-interactive-visual-intelligence))
- BFL's repository capability table gives every listed Klein checkpoint T2I, single-reference edit, and multi-reference edit capability; none is named `Edit`. ([model table](https://github.com/black-forest-labs/flux2#model-overview))
- BFL's API titles the same endpoints “Generate or edit,” using optional image inputs in one schema. ([4B endpoint](https://docs.bfl.ai/api-reference/models/generate-or-edit-an-image-with-flux2-%5Bklein%5D-4b), [9B endpoint](https://docs.bfl.ai/api-reference/models/generate-or-edit-an-image-with-flux2-%5Bklein%5D-9b))
- BFL's local CLI encodes zero or more image references into the same denoising path and does not select a separate edit model. ([CLI source](https://github.com/black-forest-labs/flux2/blob/main/scripts/cli.py))
- The 9B KV model is genuinely a distinct checkpoint optimized for reference-image performance, but BFL still lists all Klein capabilities for it. ([KV-cache guide](https://github.com/black-forest-labs/flux2/blob/main/docs/flux2_klein_kv_cache.md))

## Implications and options (not product decisions)

- The product may expose separate **Klein Generate** and **Klein Edit** routes for UX clarity while routing both to one explicitly selected Klein checkpoint. The edit route would require at least one image and emit preservation-aware edit instructions; the generation route would not accept edit references.
- A shared prompt core can cover generation and editing, but the edit mode needs additional structured facts: ordered references and their roles, requested changes, and explicit invariants/preservations.
- A local-first default still requires choosing **4B versus 9B**, **distilled versus Base**, precision/quantization, and license posture. BFL's sources support all as real choices; they do not make the product decision.
- If edit latency with repeated/multiple references dominates and the license/hardware fit, 9B KV is an available option. Its optimization does not justify renaming it “Klein Edit” or assuming it is the desired default.
- The generic Flux route should be versioned in product configuration or display text (for example, a selected exact model ID), not bound permanently to an unqualified family nickname.

## Uncertainties and unsupported claims

- The maintainer's words **Flux**, **Flux Klein**, and **Flux Klein Edit** do not identify an exact checkpoint, parameter count, service tier, or local runtime. Only the second phrase identifies the Klein family; none selects 4B/9B, distilled/Base/KV, or quantization.
- No first-party BFL artifact examined defines `Flux Klein Edit` as a model, checkpoint, or API alias. Search also found no such entry in BFL's official model inventory. This is evidence of absence in the current official surfaces, not a guarantee that no third-party UI uses that label.
- The official docs do not establish generated-image quality for Scenario Maker's use cases. Model-card examples and workflow templates demonstrate supported invocation shapes, not acceptance-test results.
- Prompt preservation instructions improve intent clarity but are not a contractual pixel-level guarantee.
- API and repository interfaces can evolve. The 9B preview endpoint deliberately receives newer weights than the fixed endpoint, so reproducible behavior requires the fixed endpoint or a pinned local artifact. ([preview endpoint policy](https://docs.bfl.ai/flux_2/flux2_overview#preview-endpoints))
- The exact local hardware fit depends on precision/runtime. BFL reports roughly 13 GB for 4B and 29 GB for 9B BF16 model-card configurations, while quantized workflows have different footprints; no deployment target was selected here. ([4B card](https://huggingface.co/black-forest-labs/FLUX.2-klein-4B), [9B card](https://huggingface.co/black-forest-labs/FLUX.2-klein-9B))

## Human choices still required

1. What exact checkpoint/service should the generic **Flux** route name: a FLUX.1 generation checkpoint, FLUX.2 dev, a hosted FLUX.2 tier, or something else?
2. Should local Klein target 4B or 9B, and distilled, Base, or 9B KV?
3. Is commercial local deployment required? That materially separates Apache-2.0 4B choices from non-commercial 9B/dev open weights.
4. Should hosted deployments use the fixed 9B endpoint for stability or the moving 9B preview/KV-backed endpoint for latest performance?
5. Which runtime is in scope—BFL CLI/reference code, Diffusers, ComfyUI, or an API adapter—and which version/quantization must be pinned?
6. Should the user-facing “Klein Edit” route support one reference only or expose Klein's four-image hosted contract and ordered per-image roles from the start?
