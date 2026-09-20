# Scenario Maker prompt-behavior evaluation rubric

## Authority and scope

This Phase 1 suite implements the 16-case portfolio approved in [issue #16](https://github.com/lfelipegg/scenario-maker-skill/issues/16#issuecomment-5746288781), using the settled boundaries in [#17](https://github.com/lfelipegg/scenario-maker-skill/issues/17#issuecomment-5746449221), [#18](https://github.com/lfelipegg/scenario-maker-skill/issues/18#issuecomment-5746540497), [#19](https://github.com/lfelipegg/scenario-maker-skill/issues/19#issuecomment-5746665421), [#20](https://github.com/lfelipegg/scenario-maker-skill/issues/20#issuecomment-5746782536), and [#21](https://github.com/lfelipegg/scenario-maker-skill/issues/21#issuecomment-5746874984). It evaluates observable prompt-writing behavior and requested files, not rendered image or video quality.

The fixed starting revision is `5fcc3d0eded83c6a9aaf472a1dc8d5ce24011d9d`. Baseline failures are valid evidence. Phase 1 accepts a reviewed case set and honest, complete baseline capture; it does not require the fixed revision to satisfy future behavior.

The generating session MUST receive the case request and its declared fixtures, but MUST NOT receive this rubric, criteria, expected judgments, prior outputs, or reviewer notes.

## Concrete portfolio

Cases appear in this exact order in `evals/cases.jsonl`.

| Case | Approved behavior | Concrete mapping | Scheduled criteria |
| --- | --- | --- | --- |
| 01 | SDXL tags only, no negative prompt | Greenhouse on a cliff; one unlabeled comma-separated prompt | Routing/output P2; SDXL profile P4 |
| 02 | Adapt supplied scene to Krea 2 | Red teapot image-left of white cup; preserve the complete supplied still life | Routing P2; preservation P3; Krea 2 profile P4 |
| 03 | Revise only jacket color | Yellow denim jacket becomes red; all other facts retained | Routing P2; revision preservation P3 |
| 04 | Character design only | Adult lighthouse keeper with fixed anatomy, clothing, and equipment; no scene treatment | Character scope and preservation P3 |
| 05 | Empty courtyard with no people | Empty courtyard plus scoped exclusions; no unsolicited negative field | Routing P2; exclusion handling P5 |
| 06 | Exact required lettering `OPEN` | Bakery sign centered above door; literal presence and semantic binding checked separately | Exact text and preservation P3 |
| 07 | Four composition variants | Fixed cube/sphere/sign scene; only composition may vary | Count, distinctness, and preservation P6 |
| 08 | Expand within an explicit word limit | Rowboat brief; complete output limited to 55 words | Output/limit P2; preservation P3 |
| 09 | Critique without replacement | Critique a vague prompt; no rewrite or variants | Critique routing P2 |
| 10 | Compare SDXL and Krea 2 prompts | Labeled analysis of two supplied prompts; no merged third prompt | Comparison routing P2; profile analysis P4 |
| 11 | Illustrious plus Danbooru and local lookup | Confirm `grey_hair` with the existing local lookup script; do not read raw CSV or expand related tags | Illustrious migration P4; tag/lookup evidence P5 |
| 12 | Pony profile preservation | Positive-only safe anime Pony prompt with fixed subject and scene | Preservation P3; profile migration P4 |
| 13 | NoobAI profile preservation | Positive-only space-normalized NoobAI prompt with fixed subject and action | Preservation P3; profile migration P4 |
| 14 | Existing Wan text-to-video route | One cohesive paragraph with subject, environment, camera motion, progression, and style | Routing P2; preservation P3 |
| 15 | Existing image-to-video route | Fixed synthetic source image; preserve first-frame content and add only requested motion | Routing P2; preservation P3 |
| 16 | Clothing-fragment wildcard export | Four clothing-only lines at `outputs/clothing-fragments.txt`, plus truthful external report | Export, fragment compatibility, and report P6 |

Existing-profile/route criteria are eligible for the original-baseline no-regression set immediately when all three original attempts pass; their scheduled repair phase does not postpone that protection. An inconsistent baseline remains an existing failure until its criterion's repair phase, rather than blocking unrelated earlier phases. No H3, Wan 2.2, Flux, Qwen, automatic skill-discovery, or other later Phase 7 case substitutes for these existing routes.

## Fixed fixture

`evals/fixtures/case15-geometric-source.png` is a deterministic 128 × 80 RGBA PNG authored from flat geometric raster primitives. It depicts pale-cyan sky above blue water, a red-hulled sailboat with a dark mast, a yellow right sail and white left sail, a white cloud in the upper right, and three pale horizontal ripple marks. It contains no generated or private material.

SHA-256: `96d3453296fdd1239b21aeda140412632b643d96cb3980986739da4470bd8ded`

Any byte change to this fixture creates a new cohort. Case 15 reviewers judge the actual visible fixture, not only this description.

## Case and criterion contract

Each JSONL record has this schema:

- `id`, `title`, and exact `request`
- `fixtures`: paths relative to `evals/fixtures`
- `operation`, `task`, `scope`, and `target_profile`
- `required_details` and `prohibited_changes`
- `output_contract`
- `criteria`, each with globally unique `id`, `description`, `method`, `check`, `severity`, `mandatory_phase`, and `decision_url`

`severity: hard` represents an acceptance requirement when due. `severity: advisory` records quality or preference and never compensates for a hard failure. `mandatory_phase` is criterion-granular: routing/output P2, preservation P3, named still-image profiles/migration P4, constraint/tag handling P5, controlled variants/export P6, and later additions P7. Trace evidence uses P1. Existing accepted behavior is protected through the original-baseline no-regression set independently of the scheduled repair phase.

## Mechanical methods

Mechanical evaluation is deliberately narrow:

- `exact_text` checks literal presence only. It does not prove that text is bound to the correct sign, subject, or relationship; a separate maintainer criterion covers that meaning.
- `word_limit` tokenizes the entire final output on Unicode whitespace. Case 08 declares a maximum of 55 tokens and requests prompt-only output, so labels or commentary consume the same limit.
- `numbered_count` counts numbered entries at line starts. It does not establish semantic distinctness.
- `export` resolves the declared path under the attempt workspace, counts nonblank physical lines, rejects blank entries and exact duplicate lines, and verifies the expected line count. It does not establish that a line is clothing-only or insertion-compatible.
- `trace_policy` inspects captured observable tool calls and actions against the evaluator's local-tool allowlist. It does not prove every request-specific constraint or claim that the shell is sandboxed. Unknown event formats, incomplete capture, or ambiguous shell commands yield `not-run`, never a pass. Case 11 separately requires human review of actual lookup evidence; spelling presence alone is not confirmation.

No keyword-absence proxy may award semantic exclusion, preservation, style, subject binding, relationship, profile fidelity, controlled-variant distinctness, or fragment compatibility. Exact-output equality is not appropriate for free-form prompts.

## Human review

The maintainer is the final semantic reviewer. Semantic criteria begin unfilled. A generator, automated evaluator, or model review MUST NOT grant semantic acceptance.

Reviewer decisions are append-only JSONL records with:

```text
{case_id, attempt, criterion_id, state, human:true, reviewer:"human:<stable-id>", reviewed_at, evidence}
```

`state` is exactly `passed`, `failed`, or `not-run`. Only an explicitly human-approved review entry may pass a `method: maintainer` criterion. Evidence should briefly identify the relevant output or artifact detail. Missing review is `not-run`; it is never inferred from mechanical success.

`reviewed_at` must include a timezone; evidence must be nonempty. The evaluator rejects malformed, duplicate, unknown-criterion, and non-human review entries. Leave the generated pending template unsubmitted until actual review; its null fields are not approvals.

For advisory style comparisons, record preference, tie, or abstention in reviewer evidence without converting preference into a hard pass. The suite does not evaluate rendered media.

## Three-attempt reporting and acceptance

Run exactly three attempts for every case and revision. Retain errors, timeouts, missing outputs, and unsuccessful outputs; never select the best attempts or silently replace one. A complete baseline has 16 × 3 = 48 attempts.

Report per case and criterion as counts across all three attempts, not as a single aggregate. Mixed results remain explicit, for example `passed 2 / failed 1 / not-run 0`. A normal completed output may still be scored when another execution component failed, if its raw evidence is complete enough for that criterion. Execution errors and trace completeness remain separate.

At Phase 1, acceptance requires the reviewable portfolio and complete, honest evidence rather than prompt success. For later phases, each applicable hard criterion due by that phase must pass all three candidate repetitions; `failed` or `not-run` blocks that criterion. Future-phase criteria remain visible but do not block an earlier phase.

The **original baseline no-regression set** consists only of checks that pass all three attempts in the first immutable 48-attempt baseline. Those checks remain protected even if a later baseline rerun varies. Checks passing only one or two baseline attempts are recorded as existing mixed failures with their scheduled repair phase; zero-pass checks are recorded failures. Such baseline inconsistency does not by itself block an unrelated phase, but a hard requirement must pass every repetition when its repair phase is due. Newly accepted hard requirements join the protected set as their phases complete.

## Raw evidence and immutability

For each attempt, the capture runner creates:

```text
results-or-baseline-root/
  cohort/
    case-id/
      attempt-N/
        attempt.json
        output.txt          # when normal output exists
        trace.jsonl         # raw OMP JSONL events
        stderr.txt
        ...captured generated files...
```

`attempt.json` records:

```text
{case_id, attempt, revision,
 execution:{status:'completed'|'error'|'timeout'|'not-run', exit_code},
 raw:{output:'output.txt'|null, trace:'trace.jsonl', stderr:'stderr.txt'},
 trace_complete,
 artifacts:[{path, stored_path, sha256, bytes}]}
```

The raw attempt directory is immutable after capture. Evaluator scores, human reviews, anonymous label maps, summaries, and corrections belong outside it. Preserve raw JSONL OMP events and captured requested files. Record full revision, actual OMP version, requested and observable resolved model identity, `high` reasoning, exposed settings, command, tool availability, permissions, instruction/fixture/config provenance, date, and unavailable metadata. Unknown values remain `unknown`. Redaction or incomplete traces must be declared and cannot be represented as byte-complete evidence.

A changed case, criterion, fixture, environment, or capture mechanism creates a new cohort. Never overwrite the original Phase 1 baseline or present unlike cohorts as controlled comparisons.

## Reproduction procedure

1. Have the maintainer review `evals/cases.jsonl`, this rubric, and the fixture before any baseline model call.
2. Use fresh, isolated workspaces and sessions for each case, revision, and repetition. Load only the selected Scenario Maker revision and its applicable references. Hold instructions, fixture bytes, settings, tools, and permissions constant.
3. Permit local Danbooru lookup for case 11, fixture inspection for case 15, and the requested fixture-local file write for case 16. Do not permit web research, other skills, delegation, model switching, or image/video generation. Do not provide this rubric to the generator.
4. Capture the fixed baseline with `python3 evals/run_baseline.py --out evals/baseline/<new-cohort>`. The runner owns the fixed revision and 16 × 3 schedule; do not add unsupported flags. A development `--smoke` capture is one separate smoke attempt and is never acceptance evidence.
5. Evaluate into a separate directory with `python3 evals/evaluate.py --cases evals/cases.jsonl --results evals/baseline/<cohort> --out evals/results/<new-review-dir> [--reviews PATH]`. Mechanical checks never fill semantic judgments.
6. Confirm all 48 attempt manifests and raw evidence references exist, record limitations, then freeze the cohort. Do not run or fabricate missing human review.

Reference environment from the decision: OMP observed `18.2.6`, requested model `openai-codex/gpt-6-astra`, explicit reasoning `high`. Record the actual values at execution; the requested model name is not proof of an immutable provider snapshot.

### Capture boundary

`run_baseline.py` only captures the fixed baseline; it does not implement a candidate comparison. It refuses an existing output directory. Default scheduling submits cases in portfolio order, repetitions 1–3, with at most three fresh OMP processes in flight and a 300-second limit per attempt. Errors and timeouts are retained without replacement.

Each attempt uses a separate temporary workspace outside this repository, an explicit selected-skill path exported from the fixed revision, and independent fixture/cache paths. Selected source files are read-only hardlinks to one per-cohort snapshot; CSVs are not recopied for each attempt. Only requested generated text artifacts are copied back. Raw source content is recoverable through the fixed revision and `selected-skill-files.json` hashes.

`omp-config.json` disables discovery, external research surfaces, automatic retries/model fallback, compaction, advisor, memory, title generation, and media generation. CLI flags expose only local `read`, `grep`, `glob`, `bash`, and `write`. This is a controlled tool/prompt policy, **not an OS filesystem/network sandbox**. The capture extension replaces inherited system instructions with the exact `generator-system.txt` contents; it does not load the rubric or future prompt policies.

`context.jsonl` records the effective system prompt, selected model, reasoning, active tools, and allowlisted client-visible provider request body fields (including actual instructions, tools, and input). Credentials and headers are not captured. The body may use incremental provider context within one attempt; raw OMP events retain the local message/tool history. Hidden provider instructions, immutable snapshot identity, seed, and fingerprint remain unavailable. `partial-output.txt`, when present without a completed response, is retained but is not a normal final output.

The manifest records the actual host/model request, command, scheduling, deadline, environment, source/fixture/evaluator hashes, and limitations. Run a separate `--smoke` capture to verify JSON events, effective context isolation, output extraction, and file capture before baseline use. Smoke evidence is never one of the 48 portfolio attempts.

## Later paired cohorts

A complete candidate comparison contains 96 attempts: three fixed-baseline and three candidate attempts for each of the same 16 cases. Rerun the fixed revision alongside every candidate under the same recorded environment, interleave baseline and candidate execution, and preserve case/repetition identity.

Present paired outputs to the maintainer under anonymous randomized labels. Randomize labels without breaking the case/repetition pair; store the label mapping separately from review cards and raw attempt directories. Do not invent a candidate side for the baseline-only cohort. Record scheduling and every environment difference. Latency and cost remain advisory.
