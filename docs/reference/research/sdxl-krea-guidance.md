# Official SDXL and Krea 2 local prompting contracts

**Ticket:** [#11 — Research official SDXL and Krea 2 local prompting contracts](https://github.com/lfelipegg/scenario-maker-skill/issues/11)  
**Source retrieval date:** 2026-09-19  
**Scope:** Primary-source research for prompt-writing behavior in the first local-image milestone. This note does not choose product defaults, implement profiles, or establish generated-image quality.

## Question

What do official SDXL and Krea 2 sources establish about prompt language, detail levels, ordering, negative prompts, text and relationship expression, and interface-specific syntax for local workflows?

## Executive finding

The sources support two deliberately modest contracts:

- **SDXL 1.0 Base** accepts ordinary text prompts and was explicitly marketed as producing complex images from only a few words; its official examples are compact natural-language phrases. Neither the model card nor the paper prescribes a required sentence structure, component order, comma-tag dialect, quality-token stack, or universal negative prompt. Negative prompting and dual-encoder prompts are supported by specific inference interfaces, notably Diffusers, rather than being a required textual grammar of the checkpoint ([Stability AI announcement](https://stability.ai/news-updates/stable-diffusion-sdxl-1-announcement); [fixed-revision model card](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/blob/462165984030d82259a11f4367a4eed129e94a7b/README.md); [Diffusers SDXL API](https://huggingface.co/docs/diffusers/v0.40.0/en/api/pipelines/stable_diffusion/stable_diffusion_xl)).
- **Open Krea 2 RAW/Turbo** officially recommends natural language. Its repository guide says long, detailed prompts yield the best results while minimal prompting can still produce high quality; these are recommendations and capability claims, not parser requirements. Krea's optional expansion prompt produces one cohesive paragraph, preserves user details and spatial relationships, groups each subject with its attributes/actions, and quotes requested visible text. The open reference CLI accepts one positive prompt and exposes no negative-prompt argument; Turbo's recommended CFG is `0.0`, and the reference sampler skips the unconditional/negative branch when CFG is disabled ([fixed-revision prompting guide](https://github.com/krea-ai/krea-2/blob/db3984fbc6e13b34c0064990fc2d95ac64d00058/docs/prompting.md); [expansion prompt](https://github.com/krea-ai/krea-2/blob/db3984fbc6e13b34c0064990fc2d95ac64d00058/docs/expansion.txt); [README](https://github.com/krea-ai/krea-2/blob/db3984fbc6e13b34c0064990fc2d95ac64d00058/README.md); [CLI](https://github.com/krea-ai/krea-2/blob/db3984fbc6e13b34c0064990fc2d95ac64d00058/inference.py); [sampler](https://github.com/krea-ai/krea-2/blob/db3984fbc6e13b34c0064990fc2d95ac64d00058/sampling.py)).

Accordingly, a **compact phrase-oriented SDXL option** and a **descriptive Krea 2 option** are both source-compatible product options, but the evidence does not make either shape mandatory. In particular, Krea 2 also has official minimal-prompt and hosted exploratory workflows, while SDXL accepts descriptive prompts as plain strings. Those choices remain product decisions.

## Identities and interfaces must stay separate

| Name in a user request or UI | Established identity | Relevant interface contract |
| --- | --- | --- |
| **SDXL 1.0 Base** | `stabilityai/stable-diffusion-xl-base-1.0`, a Stability AI latent-diffusion checkpoint with OpenCLIP ViT-bigG and CLIP ViT-L text encoders. It can run alone or feed the separate `stable-diffusion-xl-refiner-1.0` ([model card](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/blob/462165984030d82259a11f4367a4eed129e94a7b/README.md); [paper §2.1](https://arxiv.org/html/2307.01952#S2.SS1)). | A checkpoint does not define ComfyUI punctuation or weighting syntax. Diffusers exposes `prompt`, optional `prompt_2`, `negative_prompt`, and optional `negative_prompt_2` ([Diffusers API](https://huggingface.co/docs/diffusers/v0.40.0/en/api/pipelines/stable_diffusion/stable_diffusion_xl#diffusers.StableDiffusionXLPipeline.__call__)). |
| **Krea 2 RAW (open)** | `krea/Krea-2-Raw`; the undistilled base checkpoint, recommended for training/fine-tuning rather than the default fast inference path ([official repository](https://github.com/krea-ai/krea-2/blob/db3984fbc6e13b34c0064990fc2d95ac64d00058/README.md); [official model card](https://huggingface.co/krea/Krea-2-Raw)). | Reference CLI name `oss_raw`; README recommendation: 52 steps and CFG 3.5, trained up to 1K ([README usage](https://github.com/krea-ai/krea-2/blob/db3984fbc6e13b34c0064990fc2d95ac64d00058/README.md#raw-oss_raw)). |
| **Krea 2 Turbo (open)** | `krea/Krea-2-Turbo`; an eight-step distilled checkpoint whose model card names RAW as its base model ([official repository](https://github.com/krea-ai/krea-2/blob/db3984fbc6e13b34c0064990fc2d95ac64d00058/README.md); [official model card](https://huggingface.co/krea/Krea-2-Turbo)). | Reference CLI name `oss_turbo`; README recommendation: 8 steps, CFG `0.0`, `mu=1.15`, 1K–2K output ([README usage](https://github.com/krea-ai/krea-2/blob/db3984fbc6e13b34c0064990fc2d95ac64d00058/README.md#turbo-oss_turbo)). ComfyUI's official local template documents prompt enhancement as a workflow toggle, not an intrinsic model input ([local workflow guide](https://docs.comfy.org/tutorials/image/krea/krea-2)). |
| **Krea 2 hosted models** | Current Krea product docs name **Medium, Large, and Medium Turbo**; the hosted image node likewise exposes those names ([Krea user guide](https://www.krea.ai/docs/user-guide/features/krea-2); [ComfyUI partner-node contract](https://docs.comfy.org/built-in-nodes/Krea2ImageNode)). | Hosted-only controls include Creativity, Generative Sliders, moodboards, and style references. These must not be described as text syntax or assumed to exist in a bare local checkpoint workflow ([Krea user guide](https://www.krea.ai/docs/user-guide/features/krea-2)). |

Krea says the open checkpoints are “the same models that power” hosted generation, but its current public pages expose different variant sets (open RAW/Turbo versus hosted Medium/Large/Medium Turbo) and provide no public one-to-one mapping among those names ([Krea user guide, Open source](https://www.krea.ai/docs/user-guide/features/krea-2#open-source)). A local profile should therefore identify RAW or Turbo explicitly rather than silently equating either checkpoint with hosted Medium or Large.

## SDXL 1.0: what the sources establish

### Prompt language and detail

- Stability AI says SDXL 1.0 needs “only a few words” for complex, detailed images and no longer needs qualifier terms such as `masterpiece` merely to obtain high quality ([announcement, “More intelligent with simpler language”](https://stability.ai/news-updates/stable-diffusion-sdxl-1-announcement)). This supports a compact preset and argues against mandatory quality boilerplate.
- The fixed model card demonstrates plain, compact English such as `An astronaut riding a green horse` and `A majestic lion jumping from a big stone at night` ([model-card examples](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/blob/462165984030d82259a11f4367a4eed129e94a7b/README.md#-diffusers)). First-party Diffusers documentation also demonstrates a comma-separated descriptive phrase, `Astronaut in a jungle, cold color palette, muted colors, detailed, 8k` ([Diffusers text-to-image example](https://huggingface.co/docs/diffusers/v0.40.0/en/using-diffusers/sdxl#text-to-image)). Thus both compact sentences and phrase lists are evidenced inputs; neither is an exclusive dialect.
- No reviewed Stability AI source says SDXL prompts must be 1–3 sentences, must be “natural prose,” or must place subject/action/setting/composition/lighting/style in a fixed sequence. Such organization can be a product heuristic, but it should be labeled a recommendation rather than a model requirement.

### Ordering, weighting, and dual encoders

- The model has two text encoders ([model card](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/blob/462165984030d82259a11f4367a4eed129e94a7b/README.md#model-description); [paper §2.1](https://arxiv.org/html/2307.01952#S2.SS1)). Diffusers normally sends the same `prompt` to both, but permits a distinct `prompt_2`; the same split exists for negative prompts ([Diffusers API parameters](https://huggingface.co/docs/diffusers/v0.40.0/en/api/pipelines/stable_diffusion/stable_diffusion_xl#diffusers.StableDiffusionXLPipeline.__call__)). This is an interface capability, not evidence for a visible prompt-ordering rule.
- Diffusers supports precomputed prompt embeddings “e.g. prompt weighting,” but does not define parenthesis syntax as part of the SDXL model ([Diffusers API, `prompt_embeds`](https://huggingface.co/docs/diffusers/v0.40.0/en/api/pipelines/stable_diffusion/stable_diffusion_xl#diffusers.StableDiffusionXLPipeline.__call__)). ComfyUI's official basic guide documents `(golden hour:1.2)` and phrase-list advice specifically under **SD1.5** ([ComfyUI basic text-to-image guide](https://docs.comfy.org/tutorials/basic/text-to-image#4-start-experimenting)); that node/UI convention must not be presented as an official SDXL checkpoint grammar.

### Negative prompts

- The SDXL model card's base-only and base-plus-refiner examples do not supply a negative prompt ([model card](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/blob/462165984030d82259a11f4367a4eed129e94a7b/README.md#-diffusers)). A negative prompt is therefore not shown as required for valid inference.
- Diffusers exposes optional `negative_prompt` and `negative_prompt_2`; it documents them as text the generation should not follow and says they are ignored when classifier-free guidance is not active (`guidance_scale < 1`) ([Diffusers API](https://huggingface.co/docs/diffusers/v0.40.0/en/api/pipelines/stable_diffusion/stable_diffusion_xl#diffusers.StableDiffusionXLPipeline.__call__)). This establishes support, not a recommended universal list.
- None of the reviewed SDXL primary sources endorses a fixed negative string such as `bad hands, extra fingers, watermark`, nor the rule “always include a separate negative prompt.” A failure-focused negative field can remain an optional workflow feature, but its contents are not an official SDXL preset.

### Visible text and spatial relationships

- The model card states that SDXL 1.0 “cannot render legible text” and struggles with difficult compositionality such as `A red cube on top of a blue sphere` ([model-card limitations](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/blob/462165984030d82259a11f4367a4eed129e94a7b/README.md#limitations)). This is the clearest technical limitation for local use.
- The launch announcement makes a more optimistic marketing claim that SDXL can generate hard concepts including text and a woman in the background chasing a dog in the foreground ([announcement](https://stability.ai/news-updates/stable-diffusion-sdxl-1-announcement)). That does not override the model card's explicit limitations or prove reliable typography/relationship adherence. A prompt writer may state relationships plainly, but should not promise exact realization.
- No official SDXL source reviewed specifies quote marks around requested text or another typography syntax.

## Krea 2: what the sources establish

### Prompt language and minimal versus detailed prompts

- The official open-repository guide **recommends** natural-language prompts. It says long, detailed prompts yield the best results, while the model is capable of high-quality images with minimal prompt engineering ([prompting guide](https://github.com/krea-ai/krea-2/blob/db3984fbc6e13b34c0064990fc2d95ac64d00058/docs/prompting.md)). “Recommend” and “capable” make these guidance/capability statements, not hard parser constraints.
- The examples span a short phrase (`immense rocket launch exhaust as seen from extremely close up`), long comma-delimited descriptions, and multi-sentence paragraphs ([prompting guide examples](https://github.com/krea-ai/krea-2/blob/db3984fbc6e13b34c0064990fc2d95ac64d00058/docs/prompting.md#examples)). “Natural language” therefore does not mean “sentences only,” and commas are evidenced without becoming a required tag grammar.
- Krea's hosted-product guide recommends starting vague for broad aesthetic exploration, then narrowing the prompt ([Krea team deep dive](https://www.krea.ai/blog/krea-2-deep-dive-walkthrough#start-vague-let-the-model-explore)). This is not a contradiction with the open guide's “long detailed prompts yield best results”: the hosted article optimizes for exploration/diversity, while the repository statement describes result quality. A product may expose minimal and detailed modes, but the sources do not select one universal default.

### Optional expansion prompt and ordering

The guide links [`docs/expansion.txt`](https://github.com/krea-ai/krea-2/blob/db3984fbc6e13b34c0064990fc2d95ac64d00058/docs/expansion.txt) as an optional system prompt for an LLM “of your choice.” It is not model-side hidden syntax and is not required to run Krea 2.

That expansion prompt's visible-output contract is:

1. preserve original subjects, actions, colors, and spatial relationships;
2. group each subject with its own attributes and actions, using grounded phrasing for pose, interaction, and layout;
3. choose style, medium, framing, and lighting internally;
4. return one cohesive paragraph, not bullets/JSON/Markdown;
5. avoid invented objects and unsupported specificity;
6. lightly polish an already detailed prompt instead of expanding it heavily; and
7. preserve a user-requested medium ([expansion prompt](https://github.com/krea-ai/krea-2/blob/db3984fbc6e13b34c0064990fc2d95ac64d00058/docs/expansion.txt)).

This is the strongest first-party evidence for a **descriptive expansion option** and for relationship-aware phrasing. It does **not** prescribe a strict clause order such as subject → action → setting → style, and its “rules strictly” language governs the helper LLM, not the Krea 2 model parser.

### Visible text

- The repository guide recommends putting words to be rendered in quotes ([prompting guide](https://github.com/krea-ai/krea-2/blob/db3984fbc6e13b34c0064990fc2d95ac64d00058/docs/prompting.md)).
- The expansion prompt repeats that convention: specify the exact requested text and wrap it in quotes ([expansion prompt, rule 4](https://github.com/krea-ai/krea-2/blob/db3984fbc6e13b34c0064990fc2d95ac64d00058/docs/expansion.txt)).

This supports quote-wrapping as an official recommendation. The sources do not quantify spelling reliability or guarantee rendered text.

### Negative prompts in the open local path

- The reference CLI has one positional `prompt` and no negative-prompt option ([`inference.py`](https://github.com/krea-ai/krea-2/blob/db3984fbc6e13b34c0064990fc2d95ac64d00058/inference.py)). The README examples likewise provide only a positive prompt ([README usage](https://github.com/krea-ai/krea-2/blob/db3984fbc6e13b34c0064990fc2d95ac64d00058/README.md#usage)).
- The lower-level sampler does accept `negative_prompts`; when none are provided it uses empty strings. It only encodes/uses that branch when `guidance > 0` ([`sampling.py`](https://github.com/krea-ai/krea-2/blob/db3984fbc6e13b34c0064990fc2d95ac64d00058/sampling.py)).
- The official Turbo invocation sets `--cfg 0.0`, so the reference sampler skips negative/unconditional conditioning on that recommended path ([README Turbo invocation](https://github.com/krea-ai/krea-2/blob/db3984fbc6e13b34c0064990fc2d95ac64d00058/README.md#turbo-oss_turbo); [`sampling.py`](https://github.com/krea-ai/krea-2/blob/db3984fbc6e13b34c0064990fc2d95ac64d00058/sampling.py)). RAW's recommended CFG 3.5 can technically use the sampler's negative branch, but the public CLI does not expose it and the prompting guide gives no negative-prompt recommendations.

Therefore, an always-present Krea 2 negative-prompt package is not established by the official local reference workflow. Whether another ComfyUI graph exposes a negative condition is a property of that graph/node stack, not permission to import an SDXL negative preset into Krea 2.

## ComfyUI and hosted controls are not model prompt syntax

- ComfyUI's official **local Krea 2 Turbo** template exposes a user prompt, `prompt_enhance`, an LLM token limit, resolution, seed, and LoRA controls. Its documented default enables prompt enhancement; this is workflow behavior around the model, not evidence that the checkpoint expands prompts itself ([ComfyUI local Krea 2 guide](https://docs.comfy.org/tutorials/image/krea/krea-2#workflow-controls)).
- The hosted Krea/ComfyUI partner node accepts a required prompt plus model, aspect ratio, resolution, creativity, seed, optional moodboard, and style references ([Krea2ImageNode contract](https://docs.comfy.org/built-in-nodes/Krea2ImageNode)). Krea's own hosted docs define Creativity modes (`Raw`, `Low`, `Medium`, `High`) as degrees of expansion and separately define Generative Sliders as controls that shape interpretation “without rewriting” the prompt ([Krea user guide](https://www.krea.ai/docs/user-guide/features/krea-2#creativity); [Generative Sliders](https://www.krea.ai/docs/user-guide/features/krea-2#generative-sliders)). These hosted controls do not establish syntax for open RAW/Turbo.
- ComfyUI's generic positive/negative conditioning sockets, prompt weighting notation, subgraphs, and LLM enhancement are adapter/workflow features. Profiles should mention them only when the target interface is known.

## Decisive evidence by design question

| Question | What is established | What is not established |
| --- | --- | --- |
| SDXL language | Plain text; few words can suffice; compact phrases and comma descriptions are official examples. | A mandatory prose style, tag dialect, or fixed component order. |
| SDXL detail | Compact prompts are explicitly supported. Descriptive strings are valid. | A first-party optimum token count or mandatory 1–3 sentence length. |
| SDXL negatives | Diffusers supports optional negative inputs under CFG. | A mandatory negative prompt or official default negative list. |
| SDXL text/relations | Text and hard compositional relations are explicitly unreliable in the model card. | Quote syntax or a guarantee that relationship wording will be obeyed. |
| Krea 2 language | Natural language is recommended; examples include phrases, comma descriptions, and paragraphs. | Sentence-only input, tags-only input, or a rigid clause order. |
| Krea 2 detail | Long detailed prompts are recommended for best results; minimal prompting remains supported; hosted exploration recommends starting vague. | One universally correct/default detail level. |
| Krea 2 expansion | Optional helper yields one cohesive paragraph and preserves details/relationships/medium. | A required preprocessor or intrinsic checkpoint behavior. |
| Krea 2 negatives | Lower-level RAW-capable sampler supports them under positive CFG; open CLI does not expose them; recommended Turbo CFG disables the branch. | An official Krea 2 negative-prompt vocabulary or a reason to copy SDXL negatives. |
| Krea 2 text | Exact visible words should be quoted. | Guaranteed typography accuracy. |
| Interface syntax | Diffusers, ComfyUI workflows, and hosted Krea expose different controls. | A portable syntax/control set shared by all interfaces. |

## Implications and open implementation options (not decisions)

1. **SDXL profile shape:** a compact ordinary-English/phrase option is directly supported. A more descriptive option can also be offered, but should be framed as an editorial organization heuristic, not “the SDXL-required format.”
2. **Krea 2 detail modes:** a minimal/direct option and a detailed/expanded option both have first-party support. If expansion is offered, Krea's published expansion prompt provides a defensible behavior contract: faithfulness, grouped subject relationships, one paragraph, quoted requested text, restrained invention, and medium preservation.
3. **Negative-field policy:** SDXL can expose an optional negative field when the target workflow supports CFG. Krea 2 Turbo's reference path provides strong reason not to assume one; RAW and third-party/local graphs require interface-aware treatment.
4. **Syntax boundaries:** parenthetical weights, dual-encoder splits, LoRA trigger words, LLM expansion toggles, Creativity, sliders, moodboards, and reference-image strengths should be modeled as named-interface features, not folded into a universal prompt string.
5. **Capability notes:** SDXL typography and exact complex relations should carry a limitation note. Krea 2 can recommend quoted exact text and grounded relationship wording without promising adherence.
6. **Model selector labels:** local Krea choices can safely say `Krea 2 RAW` and `Krea 2 Turbo`. Hosted `Medium`, `Large`, and `Medium Turbo` should remain separate labels until Krea publishes a one-to-one checkpoint mapping.

## Uncertainties and unsupported claims

- No first-party SDXL prompt-style document found in the reviewed official sources prescribes component ordering, prose length, comma semantics, weight notation, or a stock negative prompt.
- The Stability announcement's optimistic text/spatial examples conflict in emphasis with the model card's explicit text/compositionality limitations. No reliability rate resolves that tension.
- Krea's phrase “long detailed prompts yield best results” is not accompanied by a benchmark, token range, ablation, or definition of “best.”
- Krea does not publish a one-to-one identity mapping between open RAW/Turbo and hosted Medium/Large/Medium Turbo in the reviewed sources.
- The official open Krea code has a lower-level negative-prompt parameter, but the reference CLI and prompt guide do not define a user-facing negative workflow. Third-party or future ComfyUI graphs may differ.
- Krea's hosted style-reference limits differ by surface (the Krea web guide says up to four, while current ComfyUI partner-node docs say up to ten). This reinforces that hosted adapter behavior is version/interface specific and irrelevant to the bare text contract.
- No generated-image experiments were conducted; this report establishes documentary support, not empirical prompt quality.

## Primary sources

All sources were retrieved on 2026-09-19.

### Krea 2

- [Official repository README, fixed revision `db3984f`](https://github.com/krea-ai/krea-2/blob/db3984fbc6e13b34c0064990fc2d95ac64d00058/README.md)
- [Official prompting guide, fixed revision](https://github.com/krea-ai/krea-2/blob/db3984fbc6e13b34c0064990fc2d95ac64d00058/docs/prompting.md)
- [Official expansion system prompt, fixed revision](https://github.com/krea-ai/krea-2/blob/db3984fbc6e13b34c0064990fc2d95ac64d00058/docs/expansion.txt)
- [Official reference CLI, fixed revision](https://github.com/krea-ai/krea-2/blob/db3984fbc6e13b34c0064990fc2d95ac64d00058/inference.py)
- [Official reference sampler, fixed revision](https://github.com/krea-ai/krea-2/blob/db3984fbc6e13b34c0064990fc2d95ac64d00058/sampling.py)
- [Krea 2 RAW official model card](https://huggingface.co/krea/Krea-2-Raw)
- [Krea 2 Turbo official model card](https://huggingface.co/krea/Krea-2-Turbo)
- [Krea hosted Krea 2 user guide](https://www.krea.ai/docs/user-guide/features/krea-2)
- [Krea Team hosted exploration/prompting deep dive](https://www.krea.ai/blog/krea-2-deep-dive-walkthrough)
- [ComfyUI official local Krea 2 workflow guide](https://docs.comfy.org/tutorials/image/krea/krea-2)
- [ComfyUI official hosted Krea 2 node contract](https://docs.comfy.org/built-in-nodes/Krea2ImageNode)

### SDXL

- [Stability AI SDXL 1.0 Base model card, fixed revision `4621659`](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/blob/462165984030d82259a11f4367a4eed129e94a7b/README.md)
- [Stability AI SDXL 1.0 announcement](https://stability.ai/news-updates/stable-diffusion-sdxl-1-announcement)
- [SDXL technical report, arXiv:2307.01952v1](https://arxiv.org/html/2307.01952)
- [Hugging Face Diffusers SDXL guide, v0.40.0](https://huggingface.co/docs/diffusers/v0.40.0/en/using-diffusers/sdxl)
- [Hugging Face Diffusers SDXL pipeline API, v0.40.0](https://huggingface.co/docs/diffusers/v0.40.0/en/api/pipelines/stable_diffusion/stable_diffusion_xl)
- [ComfyUI official basic text-to-image guide (used only to delimit UI/SD1.5 syntax from SDXL)](https://docs.comfy.org/tutorials/basic/text-to-image)
