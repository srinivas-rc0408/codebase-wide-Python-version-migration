"""Check paper.md against the artefacts it cites. Run after any benchmark rerun.

The paper's provenance rule (see its header comment) is that a `<!-- SOURCE: -->`
comment covers every line above it back to the previous SOURCE or the nearest
heading. This script enforces that rule mechanically for the Abstract and
§3-§4, §7-§9, re-diffs the §7.1 and §7.8 tables against their results.md, and
re-derives the §8 counts from failure-analysis.md and results.json. It exists
because the §7.1 grid has silently gone stale once.

The post-P5 sections (§3.6, §4.4, §7.7, §7.8, §8.1, §9 item 6) are checked
phrase by phrase against corpus/edge/results.json, the ablation-E results, and,
for the two figures no artefact kept, the messages of commits ab9e267 and bb1dd07.

RESULTS_SUMMARY.md gets the same treatment for a different reason: the paper's
SOURCE pointers cite it, but unlike results.md nothing regenerates it, so a
benchmark rerun moves the run records and leaves the summary behind in silence.
Every cell of its four tables is re-derived here from results.json, and any
figure in a cell the grammar does not recognise is reported rather than skipped.

    python docs/paper/verify_paper.py      # exit 0 = every check passes
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "docs/paper/paper.md"
RESULTS_MD = ROOT / "runs/benchmark/results.md"
RESULTS_JSON = ROOT / "runs/benchmark/results.json"
FAILURES_MD = ROOT / "runs/benchmark/failure-analysis.md"
SUMMARY_MD = ROOT / "runs/benchmark/RESULTS_SUMMARY.md"
EDGE_JSON = ROOT / "corpus/edge/results.json"
ABLATION_E_MD = ROOT / "runs/benchmark/ablation-e/results.md"
ABLATION_E_JSON = ROOT / "runs/benchmark/ablation-e/results.json"
EXPERIENCE_PY = ROOT / "src/mra/memory/experience.py"
# Commits whose messages are the only record of a figure (no artefact was kept).
EDGE_COMMIT, FIX_COMMIT = "ab9e267", "bb1dd07"

GRID_HEADER = (
    "| task / config | outcome | M1 recall | M1 prec | M1 F1 | M2 % "
    "| regr | corr | steps | tokens | cost $ | wall s |"
)
# `task05` is an identifier, not a figure; don't treat its digits as a claim.
# A leading "2. " is a list marker, not a figure.
IDENTIFIER_DIGITS = re.compile(
    r"^\s*\d+\.\s|task0\d|V4-|c-i{1,3}\b|§\d|FR-\d|NB-\d|NFR-\d|M[123]\b"
)
# Padding words cut from §1 by hand; a later pass must not reintroduce them.
INTENSIFIERS = r"\b(?:completely|absolutely|merely|significantly)\b"
# The Abstract spells its figures as words ("three of the five"), so a digit-only
# test would pass it with no pointer at all.
NUMBER_WORDS = re.compile(r"\b(?:one|two|three|four|five|six|seven|eight|nine|ten)\b", re.I)

LOOP_HEADER = "| task | loop on | loop off |"
ORDER_HEADER = "| task | dependency | file-name | dependents-first |"
E_HEADER = "| task | config | outcome | corrections | tokens | hints served | hint chars |"
BASELINE_HEADER = (
    "| task | \\|A\\| | ruff detected | ruff fixed | M1 after fix "
    "| suite after fix | pyupgrade detected |"
)
# The ORDER_HEADER tables in document order: ablation B with the loop off, then
# the same three orders with it on. Ablation B's "dependency" arm is a distinct
# config only when recovery is off; with it on, dependency order at batch 1 is
# the `batch-1` config.
ORDER_CONFIGS = (
    (
        "order-dependency-b1-norecovery",
        "order-alphabetical-b1-norecovery",
        "order-fr3-violating-b1-norecovery",
    ),
    ("batch-1", "order-alphabetical-b1", "order-fr3-violating-b1"),
)
# How a summary cell spells each metric: "3x gave_up, M1 33, M2 85.7, 1 regr".
CELL_FIGURES = (
    ("repeats", re.compile(r"(\d+)×")),
    ("m1", re.compile(r"M1 (\d+(?:\.\d+)?)")),
    ("m2", re.compile(r"M2 (\d+(?:\.\d+)?)")),
    ("regr", re.compile(r"(\d+) regr")),
    ("corr", re.compile(r"(\d+) corr")),
)

results: list[tuple[bool, str]] = []


def check(condition: bool, message: str) -> None:
    results.append((bool(condition), message))


def table_after(lines: list[str], header: str) -> list[str]:
    i = lines.index(header)
    out = []
    while i < len(lines) and lines[i].startswith("|"):
        out.append(lines[i])
        i += 1
    return out


def carries_a_figure(line: str) -> bool:
    """True if the line states a number, ignoring identifiers that contain digits."""
    return bool(re.search(r"\d", IDENTIFIER_DIGITS.sub("", line)))


def states_a_count(line: str) -> bool:
    return carries_a_figure(line) or bool(NUMBER_WORDS.search(line))


def uncovered_spans(
    lines: list[str], s: int, e: int, is_claim=carries_a_figure
) -> tuple[int, list[str]]:
    """Claim lines in lines[s+1:e] whose span reaches a heading or `e` without a SOURCE comment."""
    pending: int | None = None
    pointers = 0
    gaps: list[str] = []
    in_comment = False
    for k in range(s + 1, e):
        line = lines[k]
        if in_comment:
            in_comment = "-->" not in line
            continue
        if line.lstrip().startswith("<!--"):
            in_comment = "-->" not in line
            pointers += 1
            pending = None
            continue
        if line.startswith("#"):
            if pending is not None:
                gaps.append(f"line {pending + 1}: {lines[pending][:60]!r}")
            pending = None
            continue
        if not line.startswith(">") and is_claim(line) and pending is None:
            pending = k
    if pending is not None:
        gaps.append(f"line {pending + 1}: {lines[pending][:60]!r}")
    return pointers, gaps


def section(lines: list[str], start: str, end: str) -> tuple[int, int]:
    s = next(i for i, line in enumerate(lines) if line.startswith(start))
    e = next(i for i, line in enumerate(lines) if line.startswith(end))
    return s, e


def tables_after(lines: list[str], header: str) -> list[list[str]]:
    """Every table under `header`, in document order, header and rule dropped."""
    return [table_after(lines[i:], header)[2:] for i, line in enumerate(lines) if line == header]


def cells(row: str) -> list[str]:
    return [c.strip().strip("*").strip() for c in row.strip().strip("|").split("|")]


def figures(text: str) -> list[float]:
    return [float(n) for n in re.findall(r"\d+(?:\.\d+)?", text)]


def commit_message(sha: str) -> str:
    return subprocess.run(
        ["git", "-C", str(ROOT), "show", "-s", "--format=%B", sha],
        capture_output=True,
        text=True,
        check=True,
    ).stdout


def post_p5_claims(matrix: dict[str, Any]) -> dict[str, list[str]]:
    """The exact phrases the post-P5 sections must contain, built from their sources."""
    edge = json.loads(EDGE_JSON.read_text())
    cases = {c["case"]: c for c in edge["cases"]}
    by = lambda key, value: sum(1 for c in edge["cases"] if c[key] == value)  # noqa: E731
    hint_budget = re.search(r"HINT_BUDGET_CHARS = (\d+)", EXPERIENCE_PY.read_text()).group(1)

    abl = json.loads(ABLATION_E_JSON.read_text())
    agg = {(a["config"], a["task_id"][:6]): a for a in abl["aggregates"]}
    corr = lambda config, task: round(agg[(config, task)]["corrections_mean"])  # noqa: E731
    gave_up = [
        f"`{a['task_id'][:6]}`"
        for a in abl["aggregates"]
        if a["config"] == "memory-off" and list(a["outcomes"]) == ["gave_up"]
    ]
    warm = abl["experience_warmup"]
    (fix_class,) = warm["by_class"]

    before = re.search(r"before the \[fix\] commit: (\d+)/(\d+)", commit_message(EDGE_COMMIT))
    fix_msg = commit_message(FIX_COMMIT)
    bug_count = re.search(r"fix\(agent\): (\w+) verdict-accuracy bugs", fix_msg).group(1)
    rerun = re.search(r"identical\s+\((\d+)/(\d+)\)", fix_msg)

    suites = [
        int(t["suite_after_fix"].split("/")[1].split()[0])
        for b in matrix["baselines"]
        for t in b["tools"]
        if t["tool"] == "ruff (DTZ)"
    ]
    gaps = ("bare_reference", "star_import", "deprecated_call_in_test_file")
    return {
        "§3.6 experience store": [f"capped at {hint_budget} characters"],
        "§4.4 edge suite": [
            f"holds **{edge['total']}** small repositories",
            f"**common ({by('category', 'common')})**",
            f"**rare ({by('category', 'rare')})**",
            f"**twisted ({by('category', 'twisted')})**",
            f"**failure ({by('category', 'failure')})**",
            f"{by('expected', 'GREEN')} GREEN, {by('expected', 'YELLOW')} YELLOW "
            f"and {by('expected', 'RED')} RED",
        ],
        "§7.7 edge accuracy": [
            f"version {edge['agent_version']}",
            f"**{edge['passed']} of {edge['total']}** edge cases",
            f"(generated {edge['generated_at'][:19]}Z)",
            f"it passed **{before.group(1)} of {before.group(2)}**",
        ],
        "§7.8 ablation E": [
            f"over {len(warm['train_tasks'])} edge-corpus tasks",
            f"stored {warm['fixes']} fix, of class `{fix_class}`",
            f"(generated {abl['generated_at'][:19]}Z, {abl['repeats']} repeats",
            f"need a corrective edit: {', '.join(gave_up[:-1])} and {gave_up[-1]}",
            f"`task03` with {corr('memory-warm', 'task03')} corrective edit",
            f"`task04` with {corr('memory-warm', 'task04')}, each run",
            f"gives up after {corr('memory-warm', 'task02')} corrective edits",
            f"its {len(abl['skipped'])} (task, config) pairs",
        ],
        "§8.1 edge-suite defects": [
            f"The fix commit records {bug_count};",
            f"the {rerun.group(2)}-row matrix was re-run",
            f"{rerun.group(1)} of {rerun.group(2)} rows",
        ],
        "§9 limitations": [
            *(
                f"`{case}`"
                if cases[case]["expected"] == cases[case]["actual"] == "YELLOW"
                else f"<{case} is no longer a YELLOW gap: {cases[case]['actual']}>"
                for case in gaps
            ),
            f"suites of {min(suites)}–{max(suites)} tests",
        ],
    }


def main() -> int:
    paper = PAPER.read_text()
    lines = paper.split("\n")

    # 1. §7.1 is spliced from results.md §1, not transcribed. Prove it.
    src_grid = table_after(RESULTS_MD.read_text().split("\n"), GRID_HEADER)
    paper_grid = table_after(lines, GRID_HEADER)
    check(
        src_grid == paper_grid,
        f"§7.1 grid is byte-identical to results.md §1 ({len(src_grid) - 2} data rows)",
    )

    # 2. Provenance: no numeric span in a fact-assembled section may close
    #    without a SOURCE pointer.
    for name, start, end, is_claim in (
        ("Abstract", "# Abstract", "# 1. Introduction", states_a_count),
        ("§3", "# 3. System", "# 4. Corpus", carries_a_figure),
        ("§4", "# 4. Corpus", "# 5. Metrics", carries_a_figure),
        ("§7", "# 7. Results", "# 8. Failure", carries_a_figure),
        ("§8", "# 8. Failure", "# 9. Limitations", carries_a_figure),
        ("§9", "# 9. Limitations", "# 10. Conclusion", carries_a_figure),
    ):
        pointers, gaps = uncovered_spans(lines, *section(lines, start, end), is_claim)
        check(
            not gaps, f"{name}: every numeric span closed by a SOURCE pointer ({pointers} pointers)"
        )
        for gap in gaps:
            print(f"    uncovered -> {gap}")

    # 3. §8 counts are re-derived, never typed.
    failures = FAILURES_MD.read_text()
    pairs = failures.count("\n## `")
    behaviour = failures.count("**behaviour** break")
    disabled = failures.count("why it was not recovered:** recovery disabled")
    check(
        "42 of 165 runs failed" in failures and "42 did not reach green" in paper,
        "§8: 42 of 165 runs failed",
    )
    check(pairs == 14 and "14 distinct" in paper, f"§8: {pairs} distinct (config, task) pairs")
    check(
        behaviour == 26 and "all 26 surviving failures" in paper,
        f"§8: {behaviour}/{behaviour} surviving failures classify as behaviour",
    )
    check(disabled == pairs, f"§8: all {pairs} pairs cite a disabled loop, not an exhausted one")

    # 4. The retry-cap claim, straight from the run records.
    data = json.loads(RESULTS_JSON.read_text())
    rows = data["rows"]
    peak = lambda r: max((r.get("fix_attempts") or {"_": 0}).values())  # noqa: E731
    at_cap = sorted({(r["config"], r["task_id"], r["outcome"]) for r in rows if peak(r) == 3})
    exhausted = [r for r in rows if r["outcome"] == "gave_up" and peak(r) >= 3]
    check(
        max(peak(r) for r in rows) == 3 and not exhausted,
        "§8: no run gave up by exhausting MAX_FIX_ATTEMPTS = 3",
    )
    check(
        len(at_cap) == 2 and all(o == "success" for _, _, o in at_cap),
        f"§8: the cap is reached only by {', '.join(c for c, _, _ in at_cap)} — both green",
    )
    check(
        len(rows) == 165 and len(data["skipped"]) == 10,
        "§6/§7.6: 165 offline rows, 10 pairs skipped for want of a key",
    )

    # 5. The prose sections stay stubs, and §2 invents no citation.
    # The Abstract and §1 are written, so they are checked for what they must NOT contain.
    for heading in (
        "# 2. Related Work",
        "# 10. Conclusion",
        "# References",
    ):
        body = "\n".join(lines[lines.index(heading) : lines.index(heading) + 6])
        check("STUB" in body, f"stub preserved: {heading.lstrip('# ')}")
    for name, start, end in (
        ("Abstract", "# Abstract", "# 1. Introduction"),
        ("§1", "# 1. Introduction", "# 2. Related Work"),
    ):
        a, b = section(lines, start, end)
        body = "\n".join(lines[a:b])
        check("STUB" not in body, f"{name}: written — the stub outline is gone")
        padding = sorted(set(re.findall(INTENSIFIERS, body, re.IGNORECASE)))
        found = f" — found {', '.join(padding)}" if padding else ""
        check(not padding, f"{name}: no intensifier padding{found}")
    lit_start, lit_end = section(lines, "# 2. Related Work", "# 3. System")
    related = "\n".join(lines[lit_start:lit_end])
    check(
        related.count("[CITE:") == 9,
        f"§2: {related.count('[CITE:')} unresolved [CITE:] placeholders",
    )
    check(
        not re.search(r"\n\[\d+\]\s|\n- [A-Z][a-z]+,\s+[A-Z]\.", paper),
        "§2/References: no reference filled in yet, so none can be fabricated",
    )

    # 6. RESULTS_SUMMARY.md is hand-written, paper-cited and regenerated by
    #    nothing. Re-derive every table cell from results.json so a rerun that
    #    moves a number cannot leave the summary quietly behind.
    slines = SUMMARY_MD.read_text().split("\n")
    agg = {(a["config"], a["task_id"]): a for a in data["aggregates"]}
    base = {b["task_id"]: b for b in data["baselines"]}
    drift: list[str] = []
    claims = 0

    def derived(config: str, task: str) -> dict[str, Any]:
        a = agg[(config, task)]
        return {
            "repeats": a["n"],
            "outcomes": a["outcomes"],
            "m1": round(a["m1_recall_mean"]),
            "m2": round(a["m2_pass_rate_mean"], 1),
            "regr": round(a["m2_regressions_mean"]),
            "corr": round(a["corrections_mean"]),
        }

    def verify_cell(cell: str, exp: dict[str, Any], where: str) -> None:
        """Every figure in `cell` must match `exp`; none may go unread."""
        nonlocal claims
        rest = cell
        for name, pattern in CELL_FIGURES:
            m = pattern.search(cell)
            if m is None:
                continue
            rest = rest.replace(m.group(0), " ", 1)
            claims += 1
            if float(m.group(1)) != float(exp[name]):
                drift.append(f"{where}: {name} reads {m.group(1)}, results.json has {exp[name]}")
        for word in ("gave_up", "success"):
            if word in cell:
                rest = rest.replace(word, " ")
                claims += 1
                if list(exp["outcomes"]) != [word]:
                    drift.append(
                        f"{where}: outcome reads {word}, results.json has {exp['outcomes']}"
                    )
        if re.search(r"\d", re.sub(r"task\d\w*|M[12]", "", rest)):
            drift.append(f"{where}: figure not covered by the check -> {cell!r}")

    def task_of(label: str) -> str:
        return re.search(r"task\d\w*", label).group(0)

    # (a) baseline vs no-recovery, and (c) the two ablation-B tables.
    for row in tables_after(slines, LOOP_HEADER)[0]:
        col = cells(row)
        task = task_of(col[0])
        for cell, config in zip(col[1:], ("baseline", "no-recovery"), strict=True):
            verify_cell(cell, derived(config, task), f"(a) {task}/{config}")
    order_tables = tables_after(slines, ORDER_HEADER)
    for row in order_tables[0]:
        col = cells(row)
        task = task_of(col[0])
        for cell, config in zip(col[1:], ORDER_CONFIGS[0], strict=True):
            verify_cell(cell, derived(config, task), f"(c1) {task}/{config}")
    for row in order_tables[1]:
        col = cells(row)
        task = task_of(col[0])
        for cell, config in zip(col[1:], ORDER_CONFIGS[1], strict=True):
            # This table reports mean corrective edits and nothing else.
            claims += 1
            edits = derived(config, task)["corr"]
            if figures(cell) != [float(edits)]:
                drift.append(
                    f"(c2) {task}/{config}: reads {cell!r}, "
                    f"results.json has {edits} corrective edit(s)"
                )

    # (b) the deterministic baselines, straight from results.json["baselines"].
    for row in tables_after(slines, BASELINE_HEADER)[0]:
        col = cells(row)
        task = task_of(col[0])
        tools = {t["tool"]: t for t in base[task]["tools"]}
        ruff, pyup = tools["ruff (DTZ)"], tools["pyupgrade"]
        want: list[tuple[str, list[float] | str]] = [
            ("|A|", [float(base[task]["ground_truth_sites"])]),
            ("ruff fixed", [float(ruff["fixed_files"])]),
            ("M1 after fix", [round(ruff["m1_recall_after_fix"])]),
            ("suite after fix", ruff["suite_after_fix"]),
            ("pyupgrade detected", [float(pyup["detected"]), round(pyup["detect_recall"])]),
        ]
        detected = [float(ruff["detected"]), round(ruff["detect_recall"])]
        claims += 1
        if figures(col[2]) not in (detected, detected + [round(ruff["detect_precision"])]):
            drift.append(
                f"(b) {task}/ruff detected: reads {col[2]!r}, results.json has "
                f"detected {ruff['detected']}, recall {ruff['detect_recall']}, "
                f"precision {ruff['detect_precision']}"
            )
        plain = (col[1], col[3], col[4], col[5], col[6])
        for (name, expected), cell in zip(want, plain, strict=True):
            claims += 1
            got = cell if isinstance(expected, str) else figures(cell)
            if got != expected:
                drift.append(f"(b) {task}/{name}: reads {cell!r}, results.json has {expected}")

    # The header's provenance line and its arithmetic.
    head = "\n".join(slines[:12])
    stamp = re.search(r"generated (\S+?)Z", head)
    claims += 1
    if stamp is None or stamp.group(1)[:19] != data["generated_at"][:19]:
        drift.append(
            f"header: generated stamp is {stamp and stamp.group(1)}, "
            f"results.json was generated {data['generated_at'][:19]}"
        )
    matrix = re.search(
        r"(\d+) tasks × (\d+) offline\s+configurations × (\d+) "
        r"repeats = (\d+) runs",
        head,
    )
    claims += 1
    counted = (len(data["tasks"]), len({r["config"] for r in rows}), data["repeats"], len(rows))
    if matrix is None or tuple(int(g) for g in matrix.groups()) != counted:
        drift.append(
            f"header: matrix reads {matrix and matrix.groups()}, results.json has {counted}"
        )

    # The two prose figures no table restates.
    gave_up = sum(
        1 for t in data["tasks"] if list(agg[("no-recovery", t)]["outcomes"]) == ["gave_up"]
    )
    claims += 1
    if f"{gave_up} of the {len(data['tasks'])} Tier-A tasks end in" not in "\n".join(slines):
        drift.append(
            f"(a) prose: results.json has {gave_up} of {len(data['tasks'])} "
            f"tasks ending in gave_up without the loop"
        )
    dependents_first = [
        r
        for r in rows
        if r["config"] == "order-fr3-violating-b1" and r["task_id"] == "task04_multimodule"
    ]
    ceiling = max(peak(r) for r in dependents_first)
    claims += 1
    if f"retry ceiling of {ceiling} attempts" not in "\n".join(slines):
        drift.append(f"(c2) prose: the dependents-first task04 arm peaks at {ceiling} fix attempts")

    check(not drift, f"RESULTS_SUMMARY.md: {claims} figures re-derived from results.json")
    for item in drift:
        print(f"    drift -> {item}")

    # 7. Post-P5 additions (§3.6, §4.4, §7.7, §7.8, §8.1, §9.6), each figure
    #    re-derived from the file or commit its SOURCE pointer names.
    flat = " ".join(paper.split())
    e_paper = table_after(lines, E_HEADER)
    check(
        e_paper == table_after(ABLATION_E_MD.read_text().split("\n"), E_HEADER),
        f"§7.8 ablation E table byte-identical to its results.md ({len(e_paper) - 2} rows)",
    )
    for label, claims_ in post_p5_claims(data).items():
        missing = [c for c in claims_ if c not in flat]
        check(not missing, f"{label}: {len(claims_)} figures re-derived")
        for c in missing:
            print(f"    expected in paper -> {c!r}")

    width = max(len(m) for _, m in results)
    for passed, message in results:
        print(f"{'PASS' if passed else 'FAIL'}  {message.ljust(width)}")
    failed = sum(1 for passed, _ in results if not passed)
    print(f"\n{len(results) - failed}/{len(results)} checks passed.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
