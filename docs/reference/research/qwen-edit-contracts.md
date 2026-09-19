# Qwen image-editing preservation contracts

**Research question.** Which exact Qwen image-editing models/versions and official instructions support the requested editing route, and what must a prompt communicate about requested changes, preserved content, reference inputs, visible text, and relationships?

**Source retrieval date:** 2026-09-19

## Executive answer

The verified open-weight local editing route is **not “Qwen” generically**. Qwen publishes three distinct edit checkpoints:

- `Qwen/Qwen-Image-Edit` (August 2025) is a **single-image** editor loaded with `QwenImageEditPipeline`.
- `Qwen/Qwen-Image-Edit-2509` is a **one-to-three-image** editor (one to three is the officially stated optimal range) loaded with `QwenImageEditPlusPipeline`; it adds stronger person, product, and text consistency plus ControlNet-style image conditions.
- `Qwen/Qwen-Image-Edit-2511` is the current checkpoint linked as “Edit” by the official repository and uses the same `QwenImageEditPlusPipeline`; Qwen describes it as reducing image drift and further improving character and multi-person consistency.

Those identities and interfaces are independently visible in the official model cards: [original, revision `ac7f…`](https://huggingface.co/Qwen/Qwen-Image-Edit/blob/ac7f9318f633fc4b5778c59367c8128225f1e3de/README.md), [2509, revision `d396…`](https://huggingface.co/Qwen/Qwen-Image-Edit-2509/blob/d3968ef930e841f4c73640fb8afa3b306a78167e/README.md), and [2511, revision `6f3c…`](https://huggingface.co/Qwen/Qwen-Image-Edit-2511/blob/6f3ccc0b56e431dc6a0c2b2039706d7d26f22cb9/README.md). The official repository currently points its Edit link to `2511` ([repository README at `6b5e…`](https://github.com/QwenLM/Qwen-Image/blob/6b5e1f5cec987d404be5ac6657db3b9aacb56a89/README.md)).

Qwen’s own edit-prompt enhancer makes the preservation contract concrete: say **what operation to perform, on which target, with which source/reference image, and what must stay unchanged**; quote exact visible text; and state spatial, stylistic, and functional relationships rather than relying on an implicit “use this reference.” The enhancer is an optional Qwen-VL-Max rewriting layer, not the image editor itself ([official `prompt_utils.py`](https://github.com/QwenLM/Qwen-Image/blob/6b5e1f5cec987d404be5ac6657db3b9aacb56a89/src/examples/tools/prompt_utils.py)).

`Qwen-Image-2.0` is a later **unified hosted generation-and-editing model**, and the official blog demonstrates both single- and two-image edits. However, the official repository provides only a Qwen Chat link for 2.0, not a checkpoint identifier or local Diffusers quick start. It therefore cannot presently be treated as the same verified local route as the three `Qwen-Image-Edit*` checkpoints ([official 2.0 announcement](https://qwen.ai/blog?id=qwen-image-2.0), [repository announcement](https://github.com/QwenLM/Qwen-Image/blob/6b5e1f5cec987d404be5ac6657db3b9aacb56a89/README.md)).

## Exact model and interface distinctions

| Exact identity | Verified input route | Officially stated distinction | What this establishes |
|---|---|---|---|
| `Qwen/Qwen-Image-Edit` | `QwenImageEditPipeline`; one PIL image; the card example uses `true_cfg_scale=4.0`, blank-space negative prompt, and 50 steps | Original edit-specific 20B model; semantic and appearance editing; Chinese/English text addition, deletion, and modification | A supported local single-image route, but not a multi-image route. The main repository explicitly labels it “Only Support Single Image Input” and recommends 2509 instead for both single and multiple inputs ([official README](https://github.com/QwenLM/Qwen-Image/blob/6b5e1f5cec987d404be5ac6657db3b9aacb56a89/README.md)). |
| `Qwen/Qwen-Image-Edit-2509` | `QwenImageEditPlusPipeline`; `image` is a list; card example uses `true_cfg_scale=4.0`, `guidance_scale=1.0`, blank-space negative prompt, and 40 steps | Multi-image editing trained through image concatenation; person+person, person+product, and person+scene; official optimum is 1–3 inputs; improved facial identity, product identity, and text consistency; native depth/edge/keypoint conditions | The first verified open-weight multi-reference edit route. Its “1–3” statement is an optimal range, not a hard API cardinality proven by the card ([official 2509 card](https://huggingface.co/Qwen/Qwen-Image-Edit-2509/blob/d3968ef930e841f4c73640fb8afa3b306a78167e/README.md)). |
| `Qwen/Qwen-Image-Edit-2511` | `QwenImageEditPlusPipeline`; list of images; the official quick start uses the same displayed controls as 2509 | Enhanced over 2509: less image drift, stronger character consistency, better multi-person fusion, integrated selected LoRA capabilities, industrial-design editing, and geometric reasoning | The newest documented open edit checkpoint and the best-supported default candidate when consistency matters, but “better” is Qwen’s release claim, not proof for Scenario Maker outputs ([official 2511 card](https://huggingface.co/Qwen/Qwen-Image-Edit-2511/blob/6f3ccc0b56e431dc6a0c2b2039706d7d26f22cb9/README.md); [official release post](https://qwen.ai/blog?id=qwen-image-edit-2511)). |
| `Qwen-Image-2.0` (no public checkpoint ID established by the reviewed sources) | Qwen Chat is linked; the blog shows image-to-image and two-image examples | Unified generation and editing in one model, native 2K, up to 1k-token instructions, improved text rendering and photorealism | Verified product capability, but **not** a verified local model/profile identity or Diffusers contract. It should remain separately named until Qwen publishes the target identifier and integration instructions ([official 2.0 post](https://qwen.ai/blog?id=qwen-image-2.0)). |

`Qwen/Qwen-Image` and `Qwen/Qwen-Image-2512` are text-to-image checkpoints in the official quick start, not substitutes for the named edit checkpoints. Their new-scene prompt enhancer (`prompt_utils_2512.py`) categorizes and expands portraits, text-containing images, and general images; that generation-oriented expansion contract is different from the direct edit instructions below ([official README](https://github.com/QwenLM/Qwen-Image/blob/6b5e1f5cec987d404be5ac6657db3b9aacb56a89/README.md), [generation prompt utility](https://github.com/QwenLM/Qwen-Image/blob/6b5e1f5cec987d404be5ac6657db3b9aacb56a89/src/examples/tools/prompt_utils_2512.py)).

## Verified native editing prompt contract

The following is evidence from Qwen’s edit-prompt enhancer and editing documentation, not a claim that phrasing alone guarantees preservation.

### 1. Requested change: operation, target, and attributes

The official enhancer says an edit prompt should be **direct and specific**. For add/delete/replace work, it treats the complete instruction as: task type, target entity, position, quantity, and relevant attributes. If the request is vague, it adds the minimum sufficient category, color, size, orientation, or position. Replacement is expressed explicitly as “Replace Y with X,” with X’s key visual features ([official edit enhancer](https://github.com/QwenLM/Qwen-Image/blob/6b5e1f5cec987d404be5ac6657db3b9aacb56a89/src/examples/tools/prompt_utils.py)).

A prompt-writing contract can therefore represent:

> **Operation** + **target in the editable image** + **requested result** + **location/quantity/attributes when material**.

This is native editing guidance. It is narrower than a new-scene prompt that redescribes every visual detail.

### 2. Preserved content: scope it to the kind of edit

Qwen distinguishes two editing modes:

- **Appearance editing** adds, removes, or modifies a localized element and calls for all other image regions to remain completely unchanged.
- **Semantic editing** permits broad pixel changes (for example, style transfer, viewpoint rotation, or IP creation) while retaining semantic consistency.

That distinction appears in the original model card and launch post ([official original card](https://huggingface.co/Qwen/Qwen-Image-Edit/blob/ac7f9318f633fc4b5778c59367c8128225f1e3de/README.md), [official launch post](https://qwenlm.github.io/blog/qwen-image-edit/)). A blanket “preserve everything” clause conflicts with transformations that necessarily alter pose, viewpoint, or style. The preservation instruction must match the edit class.

For people, Qwen’s enhancer explicitly names the identity-bearing fields to preserve: **ethnicity, gender, age, hairstyle, expression, outfit, and other core visual consistency**. If one of those is intentionally changed, the unchanged remainder should be named. Qwen’s own example changes a hat while keeping the smile, short hair, and gray jacket unchanged. Expression, beauty, and makeup changes should be natural and subtle rather than exaggerated ([official edit enhancer](https://github.com/QwenLM/Qwen-Image/blob/6b5e1f5cec987d404be5ac6657db3b9aacb56a89/src/examples/tools/prompt_utils.py)).

For 2509, Qwen separately claims improved preservation of facial identity and product identity; for 2511 it claims further preservation of identity and visual characteristics, including multi-person group-photo fusion ([2509 introduction](https://github.com/QwenLM/Qwen-Image/blob/6b5e1f5cec987d404be5ac6657db3b9aacb56a89/Qwen-Image-Edit-2509.md), [2511 card](https://huggingface.co/Qwen/Qwen-Image-Edit-2511/blob/6f3ccc0b56e431dc6a0c2b2039706d7d26f22cb9/README.md)). These are capability claims, not a reason to omit preservation language.

### 3. Reference inputs: assign each image a role

For multi-image work, the official enhancer requires the rewritten prompt to identify **which image’s element is modified**. Its examples use numbered references such as “picture 1” and “picture 2”; style-reference tasks must describe the reference’s relevant color, composition, texture, lighting, and artistic style while preserving the source image’s visual content ([official edit enhancer](https://github.com/QwenLM/Qwen-Image/blob/6b5e1f5cec987d404be5ac6657db3b9aacb56a89/src/examples/tools/prompt_utils.py)).

The official 2509/2511 pipeline examples pass an **ordered list** in `image=[image1, image2]`. The example prompt describes which bear is on the left and right, but does not literally say “image 1/image 2”; Qwen’s SGLang example does (“girl in Figure 1 … capybara in Figure 2”) ([official repository quick start and SGLang example](https://github.com/QwenLM/Qwen-Image/blob/6b5e1f5cec987d404be5ac6657db3b9aacb56a89/README.md)). The safe prompt contract is therefore to bind roles explicitly:

> **Image 1 is the editable base/background; image 2 supplies the subject/style/object/condition; perform X; preserve Y from image 1 and Z from image 2.**

Qwen-Image-2.0’s official two-image example follows the same principle at much greater detail: it names the person and clothing from each image, chooses image 2’s wall as the shared background, and states the subjects’ spacing, posture, lighting, lens, and desired absence of compositing seams. Its cross-dimensional example is even more explicit: image 1 is the city-photo base, its real buildings/streets/vehicles/people must not change, and three instances of image 2’s cartoon character receive distinct positions around a building ([official 2.0 post](https://qwen.ai/blog?id=qwen-image-2.0)).

**Interface caveat:** the open 2509/2511 editor accepts a list, but the repository helper `polish_edit_prompt(prompt, img)` sends a one-element image list to Qwen-VL-Max. The embedded system prompt discusses multi-image tasks, yet the published helper signature does not expose multiple images. Multi-image prompt construction and multi-image prompt-enhancement execution should not be conflated ([official helper implementation](https://github.com/QwenLM/Qwen-Image/blob/6b5e1f5cec987d404be5ac6657db3b9aacb56a89/src/examples/tools/prompt_utils.py)).

### 4. Visible text: quote the exact old/new text and preserve orthography

Qwen’s edit enhancer requires all text content to be enclosed in English double quotes, kept in its original language, and kept with its original capitalization. Adding text is treated as replacement of a selected visual region; replacement instructions should identify old and new strings where the old string is known. Position, color, layout, and font are carried through **when the user requires them**, rather than invented automatically ([official edit enhancer](https://github.com/QwenLM/Qwen-Image/blob/6b5e1f5cec987d404be5ac6657db3b9aacb56a89/src/examples/tools/prompt_utils.py)).

The original model’s official claim is Chinese/English text addition, deletion, and modification while preserving the original font, size, and style. The 2509 release adds editing of font type, color, and material ([original launch post](https://qwenlm.github.io/blog/qwen-image-edit/), [2509 introduction](https://github.com/QwenLM/Qwen-Image/blob/6b5e1f5cec987d404be5ac6657db3b9aacb56a89/Qwen-Image-Edit-2509.md)). Thus a preservation-aware text edit should communicate:

> Replace exact visible text **"OLD"** with **"NEW"** at the identified carrier/location; preserve capitalization/language and all unrequested typography, layout, carrier material, and surrounding content.

Qwen also documents a practical limit: an obscure Chinese calligraphy character failed in one pass; the team used bounding boxes and chained, progressively narrower edits until correct. This supports localized selection and iterative correction as an option, not a promise of one-pass transcription accuracy ([official original edit guide](https://github.com/QwenLM/Qwen-Image/blob/6b5e1f5cec987d404be5ac6657db3b9aacb56a89/Qwen-Image-Edit.md)).

### 5. Relationships: state them as constraints, not inferred decoration

Qwen’s enhancer requires additions to fit the input scene’s logic and style, asks style references to be decomposed into relevant visual characteristics, and asks multi-image prompts to identify the edited/source element. The official examples make relationships explicit: left/right placement and mutual facing, the subject/background source, subjects’ distance and lean, matching lighting/perspective, and the relationship between inserted content and the unchanged base ([official edit enhancer](https://github.com/QwenLM/Qwen-Image/blob/6b5e1f5cec987d404be5ac6657db3b9aacb56a89/src/examples/tools/prompt_utils.py), [2509 quick start](https://huggingface.co/Qwen/Qwen-Image-Edit-2509/blob/d3968ef930e841f4c73640fb8afa3b306a78167e/README.md), [2.0 examples](https://qwen.ai/blog?id=qwen-image-2.0)).

For prompt writing, the useful relationship fields are:

- source ownership: which image supplies the base, subject, background, style, pose/control map, object, or text carrier;
- spatial relation: left/right, foreground/background, distance, overlap, gaze/facing, contact, or attachment;
- visual integration: scale, viewpoint, lighting, shadow/reflection, palette, texture, and perspective where needed;
- preservation boundary: which source traits and which base regions must remain unchanged.

This is a synthesis of the official rules and examples. It is a **recommended schema**, not a Qwen-published JSON format.

## Prompt rewriting is a separate optional stage

The repository warns that original Qwen-Image-Edit results can become unstable without prompt rewriting and strongly recommends rewriting for stability. Its advanced usage uses `polish_edit_prompt`, which sends the image plus instruction to `qwen-vl-max-latest`, expects JSON containing `Rewritten`, and then supplies that text to the edit model ([official README](https://github.com/QwenLM/Qwen-Image/blob/6b5e1f5cec987d404be5ac6657db3b9aacb56a89/README.md), [official helper](https://github.com/QwenLM/Qwen-Image/blob/6b5e1f5cec987d404be5ac6657db3b9aacb56a89/src/examples/tools/prompt_utils.py)).

This establishes two different components:

1. **Prompt writer/enhancer:** Qwen-VL-Max inspects image plus request and returns a rewritten instruction.
2. **Image editor:** a `Qwen-Image-Edit*` checkpoint consumes input image(s) plus prompt.

Scenario Maker writes prompts and does not execute generation. It may adopt the documented instruction shape without implying that it runs either Qwen-VL-Max or the diffusion editor. Any future UI/API toggle that actually invokes the official enhancer is a separate product and credential decision.

## Recommended Scenario Maker output contract (derived, not mandated)

A preservation-aware edit prompt can use this order:

1. **Inputs and roles:** “Use image 1 as …; image 2 as …”.
2. **Operation and target:** add/delete/replace/transform/restyle X at Y.
3. **Requested result:** exact appearance, quantity, and location only where material.
4. **Preserve:** identity traits, base regions, composition, typography, or source traits that are not meant to change.
5. **Relationships/integration:** positions, scale, contact, gaze, lighting, perspective, reflections/shadows, and style-source traits needed for coherence.
6. **Visible text:** exact quoted old/new strings with language, capitalization, carrier, and only requested typographic changes.

This order is a maintainable synthesis, not official syntax. A concise request already containing these facts should remain concise; Qwen’s enhancer itself says to preserve a clear instruction and refine only its grammar.

## Decisive evidence

- Qwen itself marks original Edit as single-image and 2509/2511 as Plus-pipeline multi-image editors; 2509 states the 1–3 optimum and 2511 is the repository’s current Edit link.
- Qwen’s edit enhancer explicitly defines operation/target specificity, human identity preservation fields, exact quoted visible text, source-image identification, style-reference decomposition, and scene-relationship logic.
- Qwen’s launch materials distinguish localized appearance preservation from semantic consistency, so preservation cannot be a single universal phrase.
- Qwen-Image-2.0 has demonstrated hosted editing but no exact public checkpoint/local interface in the reviewed first-party sources.

## Maintainer choices left open

Research does not decide:

- whether a future profile targets `2509`, `2511`, hosted `Qwen-Image-2.0`, or exposes several exact targets;
- whether prompt rewriting is direct rules-based writing, an optional Qwen-VL-Max call, or omitted;
- whether the product accepts one, two, or three references and how it labels their roles;
- whether preservation fields are free text or structured inputs;
- whether ControlNet-style maps are admitted as references and how their role is represented;
- whether defaults such as 40 steps and CFG values belong in any execution layer (they are interface examples, not prompt prose);
- whether text corrections are emitted as one edit or a proposed chained workflow.

## Uncertainties and unsupported claims

- The reviewed first-party sources do not publish a `Qwen-Image-2.0` Hugging Face/ModelScope checkpoint ID or local Diffusers invocation. Generic “Qwen 2.0 local edit” support would be unsupported.
- The sources do not guarantee perfect identity, background, text, relationship, or pixel preservation. They report improvements and showcases; no Scenario Maker-specific rendered evaluation was performed.
- The 2509 card says 1–3 images are optimal, but does not specify a hard maximum accepted by every serving implementation.
- The published prompt enhancer’s multi-image rules exceed its single-`img` helper interface; behavior for enhancing multiple references through that helper is not established.
- Qwen’s public examples do not define a machine-readable preservation schema or a canonical required clause order.
- The original model card claims Chinese/English text editing; the reviewed sources do not establish an exhaustive language matrix for 2509, 2511, or 2.0 editing.
