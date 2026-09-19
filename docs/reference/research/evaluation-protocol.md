# Minimal reproducible prompt-behavior evaluation protocol

**Research question.** What primary-source evaluation practices are sufficient to compare Scenario Maker at revision [`5fcc3d0`](https://github.com/lfelipegg/scenario-maker-skill/tree/5fcc3d0eded83c6a9aaf472a1dc8d5ce24011d9d) with later revisions without building a large framework or claiming better rendered images?

**Scope.** This note evaluates the skill's observable prompt-writing behavior: activation, traceable process, final text, and requested text/file artifacts. It does not evaluate an image or video generator, and a favorable result is not evidence of better rendered images.

## Findings from primary sources

1. OpenAI defines a skill eval as **prompt → captured run (trace and artifacts) → a small set of checks → a comparable score**. Its first-party worked example recommends defining success before changing the skill, keeping must-pass checks small, starting with a targeted prompt set, preserving `codex exec --json` JSONL, using deterministic checks where possible, and a structured rubric where rules fall short.[^eval-skills]
2. Skill selection itself is behavior worth testing. Codex can activate a skill explicitly or implicitly; implicit selection depends on the skill description.[^build-skills] The eval-skills example therefore includes explicit, implicit, contextual, and negative-control prompts, and says a small set of 10–20 prompts can expose early regressions.[^eval-skills]
3. OpenAI says generative output is variable and traditional deterministic tests alone are insufficient. Its evaluation guidance recommends task-specific tests, logging everything, automation where possible, and calibrating automated scoring with human feedback. It also says comparisons/classifications are generally more reliable judge tasks than open-ended generation.[^eval-best-practices]
4. The same guidance distinguishes metric-based, human, and model-judge evaluation. It calls human judgment highest quality but slow and subject to disagreement; recommends randomized, blinded comparison for human review; and warns that model judges have position and verbosity biases. It recommends pairwise or pass/fail judgments, clear rubrics, and validating judge agreement against human labels.[^eval-best-practices]
5. For Codex specifically, `codex exec` is the documented non-interactive surface and `--json` emits newline-delimited events, one per state change.[^codex-cli] The eval-skills guide says command executions appear in `item.*` events and token usage in `turn.completed`; it recommends retaining the JSONL so failed checks remain explainable.[^eval-skills]
6. Reproducibility is conditional. OpenAI documents Chat Completions as nondeterministic by default. A fixed `seed` plus identical request parameters gives only **mostly** deterministic output; `system_fingerprint` can reveal some backend changes.[^advanced-usage] OpenAI separately warns that prompting behavior can change between model snapshots and recommends pinned versions plus evals.[^api-overview] Model pages describe snapshots as the way to lock a model version when one is available.[^model-snapshot]
7. Current OpenAI dataset tooling separates exact string checks, semantic similarity, model grading, and executable checks, and treats expert annotations as the most valuable source for subjective ground truth.[^datasets] However, OpenAI has announced that its hosted Evals platform becomes read-only on October 31, 2026 and shuts down on November 30, 2026.[^eval-best-practices] A minimal repository-owned record format should therefore not depend on that hosted product.

## Decisive evidence for this ticket

The sources support a small, local comparison rather than a benchmark framework:

- keep the case set small and behavior-specific;
- run the same cases against both revisions;
- preserve raw traces, final outputs, artifacts, and known execution provenance;
- apply deterministic checks only to mechanically decidable contracts;
- send semantic prompt quality to blinded, criterion-level human comparison (or a separately versioned model judge calibrated to humans);
- repeat runs because output is variable, while making the repeat count and acceptance policy explicit maintainer decisions.

They do **not** support treating one run, exact text equality, a mutable model alias, or an unrecorded judge score as proof that one revision is better.

## Recommended minimal protocol

The following is a recommendation derived from the evidence above, not an already implemented feature.

### 1. Freeze the comparison unit

For each comparison, record a run manifest once and execute every case from the same clean fixture under both:

- baseline: `5fcc3d0eded83c6a9aaf472a1dc8d5ce24011d9d`;
- candidate: the full commit SHA under review.

Hold the case text, fixture, surrounding instructions, available skills/tools, runner version, requested model, model settings, permissions, and network/search mode constant. Prefer a pinned model snapshot where the interface exposes one. Use the same scorer/rubric version for both revisions. If any item cannot be held constant or observed, record it as `null`/`unknown`; do not imply exact replay.

A sufficient small suite should cover distinct contracts rather than many paraphrases:

- explicit invocation;
- implicit in-scope invocation;
- an adjacent negative control that should not invoke Scenario Maker;
- default normal image prompt;
- requested Tag and Danbooru formats;
- an explicitly supported model profile;
- text-to-video and image-to-video behavior;
- a request with a hard length/format constraint;
- a genuinely ambiguous request that should ask rather than guess;
- a wildcard/file-output request if file-writing behavior is in scope.

This mirrors OpenAI's explicit/implicit/contextual/negative-control pattern and its recommendation to grow coverage from real failures rather than enumerate every wording.[^eval-skills]

### 2. Use one case record and one result record

JSON Lines is sufficient; no database or service is required. Keep prompts and outputs as exact strings, not summaries.

```json
{"schema":"scenario-maker-eval-case/v1","case_id":"tag-001","purpose":"requested tag syntax and visible constraints","user_prompt":"Use $scenario-maker to write a Tag Version ...","fixture":"fixtures/empty-workspace","expected_activation":true,"deterministic":[{"id":"tag-shape","rule":"comma-separated phrases; no prose-only response"},{"id":"required-terms","rule":"contains user-specified subject and exclusion"}],"qualitative":["faithfulness to requested scene","visual observability","composition and lighting usefulness","absence of contradictory details"]}
```

```json
{"schema":"scenario-maker-eval-result/v1","comparison_id":"2026-09-19-a","case_id":"tag-001","revision":"5fcc3d0eded83c6a9aaf472a1dc8d5ce24011d9d","repeat":1,"started_at":"<RFC3339>","runner":{"surface":"codex exec --json","version":"<exact or unknown>"},"model":{"requested":"<id>","resolved_snapshot":"<id or unknown>","provider":"<id or unknown>","settings":{"reasoning_effort":"<value or unknown>","verbosity":"<value or unknown>","temperature":"<value or unknown>","top_p":"<value or unknown>","seed":"<value or unavailable>","system_fingerprint":"<value or unavailable>"}},"environment":{"os":"<value>","available_skills_hash":"<digest or unknown>","instructions_hash":"<digest or unknown>","fixture_hash":"<digest>","config_hash":"<digest or unknown>","sandbox":"<value>","approval_policy":"<value>","web_search":"<value>"},"exit_code":0,"raw":{"trace_jsonl":"artifacts/...trace.jsonl","stderr":"artifacts/...stderr.txt","final_output":"artifacts/...output.txt","artifacts_manifest":"artifacts/...files.json"},"deterministic_results":[{"id":"tag-shape","pass":true,"evidence":"<short exact observation>"}],"qualitative_review":{"rubric_version":"v1","presentation":"blinded-pairwise","reviewer_kind":"human","judgment":"A|B|tie|abstain","criterion_notes":{}},"errors":[]}
```

The manifest or each result should additionally record the case-set revision/hash, evaluation code revision/hash, candidate and baseline worktree cleanliness, locale/time zone, CLI command with secrets removed, and the number/scheduling of repeats. Store an artifact manifest with relative path, byte count, and cryptographic digest for every created file. Never store credentials.

### 3. Preserve raw evidence before scoring

For each run:

1. Save `codex exec --json` stdout byte-for-byte as the raw JSONL trace.
2. Save stderr and exit code separately.
3. Extract, but do not replace, the final response with a convenient text copy.
4. Save created/modified artifact contents or a manifest plus digests.
5. Score only after capture; keep per-check evidence so a person can audit the result.

This follows OpenAI's recommendation to grade what actually happened from structured events and retain the trace for debugging.[^eval-skills] A Codex JSONL trace is an observable client trace, not necessarily the complete raw provider request or hidden platform state; label it accordingly.

### 4. Separate deterministic contracts from qualitative judgments

Use deterministic checks for properties with one mechanically correct answer:

- process exit and parseable JSONL;
- expected activation/tool event when the trace exposes it;
- required output heading or requested field presence;
- requested Tag/Danbooru delimiter and basic syntax;
- explicit word/token limit using a declared counter;
- required literal user constraints or forbidden literal exclusions;
- expected file path, line count, and no writes outside an allow-list;
- no image/video generation tool call when the task is prompt writing only.

Do not use exact-output equality for free-form prompts. Do not turn semantic questions such as “cinematic,” “model-appropriate,” “visually coherent,” or “useful” into brittle keyword proxies.

Use criterion-level qualitative review for:

- fidelity to the user's subject, exclusions, and intent;
- conversion of hidden/internal concepts into observable details;
- clarity of subject, setting, action, composition, lighting, and atmosphere;
- appropriateness of a named model's prompt dialect;
- video motion and camera coherence;
- whether negative prompts contradict requested content;
- whether assumptions or clarification behavior are sensible;
- concision and ready-to-paste usefulness.

For revision comparison, show baseline and candidate outputs side-by-side under randomized anonymous labels and ask for `A`, `B`, `tie`, or `abstain` **for each criterion**, plus a short evidence note. Randomized/blinded pairwise review is directly aligned with OpenAI's human-eval guidance; a tie/abstain avoids forced claims.[^eval-best-practices] If an LLM judge is used, pin and record its model/settings and rubric, counterbalance A/B order to expose position bias, retain its raw response, and first measure agreement against human annotations.[^eval-best-practices]

### 5. Treat variability as data, not noise to hide

Run both revisions the same maintainer-selected number of times per case. Preserve every attempt, including failures and timeouts; never select the most attractive sample. Pair comparisons by case and repeat, and interleave or randomize revision order so time-correlated service changes do not systematically favor one side.

Report, without inventing a universal threshold:

- deterministic pass count over total attempts, per check and per case;
- number of cases with mixed outcomes across repeats;
- pairwise qualitative wins/losses/ties/abstentions, per criterion;
- reviewer disagreements where more than one reviewer is used;
- errors/timeouts separately from scored outputs;
- changes in requested/resolved model or `system_fingerprint`, when exposed.

OpenAI establishes that model output varies and that seed-based replay is only mostly deterministic; it does not prescribe a repeat count or acceptance threshold for this skill.[^eval-best-practices][^advanced-usage] Therefore repeat count, reviewer count, and acceptance thresholds remain explicit maintainer choices.

### 6. Make only bounded claims

A defensible result is phrased like:

> Under the recorded Codex/model/configuration, candidate `<sha>` passed `<x>/<n>` deterministic checks versus baseline `<y>/<n>`. Blinded reviewers preferred the candidate on `<criteria/cases>`, preferred the baseline on `<criteria/cases>`, and tied or abstained on `<criteria/cases>`. Results varied on `<cases>`. No generators were run, so this comparison says nothing about rendered-image or rendered-video quality.

Avoid “reproducible” without qualification when the resolved model snapshot, effective settings, trace inputs, or backend fingerprint are missing. Say “repeatable case definition with incomplete replay provenance” instead.

## Limitations and unsupported claims

- **No render-quality evidence.** The evaluated artifact is a written prompt. Without holding a named generator/checkpoint, sampler, seed, scheduler, resolution, conditioning inputs, implementation, and other generation settings constant—and reviewing actual outputs—no image/video quality claim follows.
- **No guaranteed exact replay.** OpenAI says outputs are nondeterministic and describes `seed` behavior as only mostly deterministic.[^advanced-usage] Codex CLI documentation cited here documents `--json`, model/configuration controls, and inherited configuration, but not a general CLI seed guarantee.[^codex-cli][^codex-config]
- **Unknown means unknown.** A requested alias is not proof of a resolved immutable snapshot. An absent `system_fingerprint`, hidden instruction, effective provider parameter, or platform-side change cannot be reconstructed later.
- **Trace boundary.** JSONL captures documented Codex state-change events, not proof that every hidden prompt fragment or provider-side event was captured.[^codex-cli]
- **Environment sensitivity.** Implicit skill selection depends on the description and available context; differences in installed skills, surrounding instructions, tools, working directory, or fixtures can change behavior.[^build-skills]
- **Judge limitations.** Human reviewers can disagree; model judges can exhibit position and verbosity bias. Neither should be presented as objective rendered quality.[^eval-best-practices]
- **Small-suite limits.** A targeted suite is appropriate for early regression detection, not a claim about all user requests. Add cases from observed failures and real usage.[^eval-skills]
- **Hosted Evals lifecycle.** Building this minimal protocol around the retiring OpenAI Evals platform would create avoidable migration work.[^eval-best-practices]

## Decisions left to the maintainer

This research intentionally does not decide:

1. Which exact cases and fixtures constitute the first maintained suite, and whether implicit activation is in scope on every supported host.
2. How many repeats and human reviewers are affordable for routine and release comparisons.
3. Which deterministic checks are must-pass, their aggregation, and every acceptance/regression threshold.
4. Whether qualitative comparison is human-only or uses a human-calibrated model judge, and who qualifies as a domain expert.
5. Which Codex surface, pinned model/snapshot, reasoning effort, verbosity, permissions, search mode, and effective configuration become the reference environment.
6. Whether token/cost/latency are product goals; if so, which measures and limits matter.
7. Whether a later, separate rendered-output study is warranted and which generator-specific provenance and review protocol it would require.
8. Retention/redaction policy for traces and artifacts that may contain user-supplied material.

## Source retrieval

All web sources below were retrieved on **2026-09-19**.

[^eval-skills]: OpenAI, [“Testing Agent Skills Systematically with Evals”](https://developers.openai.com/blog/eval-skills/).
[^build-skills]: OpenAI, [“Build skills”](https://developers.openai.com/codex/build-skills).
[^eval-best-practices]: OpenAI, [“Evaluation best practices”](https://developers.openai.com/api/docs/guides/evaluation-best-practices).
[^codex-cli]: OpenAI, [“Codex CLI reference”](https://developers.openai.com/codex/cli/reference) (`codex exec`).
[^advanced-usage]: OpenAI, [“Advanced usage”](https://developers.openai.com/api/docs/guides/advanced-usage#reproducible-outputs) (“Reproducible outputs”).
[^api-overview]: OpenAI, [“API Overview”](https://developers.openai.com/api/reference/overview.md) (“Backwards compatibility” and request IDs).
[^model-snapshot]: OpenAI, [“GPT-5.6 Sol”](https://developers.openai.com/api/docs/models/gpt-5.6-sol) (“Snapshots”), used only as an example of the documented snapshot concept; it is **not** a recommendation that this eval use that model.
[^datasets]: OpenAI, [“Getting started with datasets”](https://developers.openai.com/api/docs/guides/evaluation-getting-started).
[^codex-config]: OpenAI, [“Codex configuration reference”](https://developers.openai.com/codex/config-reference) (model, reasoning effort, verbosity, sandbox, approval, provider, and web-search fields).
