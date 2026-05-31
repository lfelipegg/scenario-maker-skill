# Character Generator

Use `scripts/character_generator.py` when the user asks for original characters, character prompt fragments, randomized character batches, or attribute-controlled character profiles.

## CLI

Run from the `scenario-maker` skill root:

```bash
python3 scripts/character_generator.py --count 1
python3 scripts/character_generator.py --seed 7 --count 3
python3 scripts/character_generator.py --gender female --hair-color black --bangs parted --hair-style "high ponytail" --hair-length long --body-type athletic --clothes hoodie
python3 scripts/character_generator.py --format json
python3 scripts/character_generator.py --list-options
```

Supported formats:

- `both`: default; prints `Danbooru:` and `Prose:` for each character.
- `danbooru`: prints comma-separated tags only.
- `prose`: prints natural-language descriptions only.
- `json`: prints selected groups plus rendered `danbooru` and `prose`.

## Groups

The generator chooses from these grouped character fields:

- `gender`
- `hair_color`
- `bangs`
- `hair_style`
- `hair_length`
- `breast_size`
- `skin_color`
- `tanline`
- `body_type`
- `clothes`

Friendly overrides are accepted per group, such as `black`, `parted`, `long`, `athletic`, and `hoodie`. Use `--list-options` to inspect the current canonical keys, tags, aliases, and revealing opt-in markers.

## Output Ordering

Danbooru tags are rendered in this order:

`gender`, `hair_color`, `hair_length`, `bangs`, `hair_style`, `breast_size`, `skin_color`, `tanline`, `body_type`, `clothes`

The order follows common tag-group structure: subject count and adult presentation first, then hair, body, skin/tanline, build, and attire. Combine generated tags with model-specific prompt profiles from `references/model-prompts.md` when the user names Pony, Illustrious, NoobAI, or SDXL.

## Safety Defaults

- Characters are adult-presenting by default.
- Female characters include one breast-size tag by default.
- Male and nonbinary characters omit breast size.
- `--breast-size` with a non-female gender exits with an error.
- Minor-coded overrides such as `child`, `loli`, `shota`, `schoolgirl`, and `schoolboy` are rejected.
- Revealing tanline or clothing options require `--allow-revealing`; random defaults exclude those options.

## Examples

Danbooru-only character for Illustrious:

```bash
python3 scripts/character_generator.py --format danbooru --gender female --hair-color white --hair-length long --bangs blunt --hair-style twin_braids --skin-color pale --body-type petite --clothes dress
```

Deterministic batch for prompt exploration:

```bash
python3 scripts/character_generator.py --seed 42 --count 5 --format json
```
