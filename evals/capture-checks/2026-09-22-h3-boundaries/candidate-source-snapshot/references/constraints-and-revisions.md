# Constraints and Revisions

Apply these rules to the scene description before rendering model-facing wording. They implement the [resolved invention and preservation decision](https://github.com/lfelipegg/scenario-maker-skill/issues/17#issuecomment-5746449221). See [Scene Composition](scene-composition.md) for the workflow and [Output Contracts](output-contracts.md) for dialect, response shape, and genuine incompatibilities.

## Permission Boundaries

Modes grant permission **within the operation and scope**; they never override either. Supplied facts, necessary implications, exclusions, and locked details remain protected even when not explicitly labeled “locked.”

| Mode | Permitted invention |
| --- | --- |
| **Preserve** | Reword, reorganize, remove redundancy, and make necessary implications explicit. No new visual facts. A sparse result is valid; missing optional detail is not a reason to ask. |
| **Balanced** | Fill unspecified appearance, material, or other local details of the requested content. No new independent subjects, props, actions, or events. Complete lighting only where the scope permits presentation details and without introducing new scene facts. |
| **Explore** | Add compatible, in-scope ideas and props. Add subjects only if the brief leaves the roster open or explicitly authorizes additions. Never replace supplied facts merely because Explore was requested. |

Create and expand default to Balanced. Adaptation and revision default to Preserve: adapt changes expression, while revision changes only what was requested. A vague improvement request or a mode name does not release protected details. Critique identifies problems without applying suggested changes.

Explicit additional permissions apply only to their named dimensions. “Adapt and invent background details” allows background invention, not a different subject. “Change only the jacket to red; Explore” still changes only the jacket color.

## What Must Survive

Preserve meaning, not incidental prompt wording. Protect supplied counts, colors, props, actions, spatial relationships, exclusions, and required visible text. Required lettering retains exact spelling, case, and punctuation, as well as its binding to the correct object. Normalizing tag separators must not normalize lettering.

A plausible explanation, stereotype, or common association is not a necessary implication. A wet street does not establish active rain or nighttime; an occupation does not establish equipment or a setting. A model's example, tag ordering, preferred composition, or length target does not authorize such additions.

For adaptation or revision of a previously generated prompt, that supplied prompt is now the source to preserve, including details originally invented. Do not discard those details because they were absent from an earlier brief.

A clear later instruction may change a previously locked detail without saying “unlock.” Apply that permission locally; the replacement becomes the detail preserved thereafter. For example, after “the jacket is locked yellow,” “change only the jacket to red” replaces that color, not the hair, pose, props, or background. Simultaneously requiring incompatible colors is a conflict, not a later replacement.

## Scope Boundaries

| Scope | Permitted content |
| --- | --- |
| **Full scene** | Scene content within the selected mode and protected facts. |
| **Character design** | Appearance, anatomy, clothing, and equipment within the mode. No unsolicited pose, expression, action, setting, camera, or lighting treatment. Equipment is not automatically authorized by the character's role. |
| **Clothing** | Garment design, not an invented wearer or surrounding scene. |
| **Isolated asset** | The asset, not supporting objects or an added scene. |

Explicitly supplied or requested presentation details remain allowed and protected. A narrow scope is not permission to delete a requested pose, expression, lighting treatment, or background. Explore cannot expand a clothing or character-design request into a full scene.

## Ambiguity and Conflicts

Keep unresolved source ambiguity when it can be faithfully expressed. Do not choose an interpretation merely to make the prompt more specific. Ask when the requested artifact requires a choice that the source does not establish, or when the intended revision is genuinely unclear.

Examples:

- A supplied “figure beside a bank” can retain “bank” during a prose revision that does not touch the setting. If a requested conversion requires choosing a financial building or a riverbank, clarify rather than deciding silently.
- “Expand this wet street, Preserve” may remain sparse. Do not ask for optional weather, time, or extra objects merely to fill a template.
- If required content cannot fit a hard length or format limit, remove redundancy and optional invention first. If still impossible, identify the conflict and ask which constraint may be relaxed. Do not silently omit content, exceed the limit, or change the format.
- Simultaneous incompatible instructions require clarification. Required `OPEN` lettering plus a limit too short to include it is not permission to abbreviate or drop the text.

Rendering uncertainty alone is not a conflict: preserve requested content without interrupting merely because the model might render it poorly.

## Boundary Examples

- **“Expand a coat design” — Balanced:** may choose unspecified fabric or stitching; no wearer, umbrella, or street.
- **“Create a witch character” — Balanced:** may invent unspecified hair and clothing; no automatic staff, familiar, or cottage. Explore may add compatible equipment, but not an unsolicited scene.
- **“Two women at a table” — Explore:** no added waiter without permission. **“Design a bustling market”** leaves the roster open.
- **“Adapt this scene to tags” — Preserve:** retain the same subjects, their attributes and relationships, and exact lettering; use the output contract's permitted fidelity-preserving expressions rather than changing the scene to fit convenient tags.
