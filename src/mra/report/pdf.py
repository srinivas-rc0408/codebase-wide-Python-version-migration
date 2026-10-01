"""Report model -> PDF, inside a hard 14-page budget.

White page, black text, one grey for rules. Colour appears only where it
means something: the status (green / amber / red) and diff +/- markers.
One sans family (Helvetica, built into every PDF reader), one type scale.

The budget is enforced by building, counting pages, and rebuilding with the
next truncation level until the document fits: diff excerpts go first, then
timeline detail, then file-table rows (then plan rows, as a last resort).
Every cut says "+N more — see report.json"; report.json is never cut.
"""

from __future__ import annotations

import io
from typing import Any
from xml.sax.saxutils import escape

import networkx as nx
from reportlab.graphics.charts.barcharts import HorizontalBarChart
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.shapes import Circle, Drawing, Line, String
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

MAX_PAGES = 14
GRAPH_NODE_CAP = 30

FONT, BOLD = "Helvetica", "Helvetica-Bold"
INK = colors.black
STATUS_HEX = {"GREEN": "#1E7B34", "YELLOW": "#B7791F", "RED": "#B42318"}
STATUS = {name: colors.HexColor(value) for name, value in STATUS_HEX.items()}
ADD_HEX, DEL_HEX, GREY_HEX = STATUS_HEX["GREEN"], STATUS_HEX["RED"], "#9A9A9A"
GREY = colors.HexColor(GREY_HEX)

MARGIN = 20 * mm
WIDTH = A4[0] - 2 * MARGIN

#: Truncation levels, tried in order until the document fits.
LADDER: list[dict[str, int]] = [
    {},
    {"diff_files": 8}, {"diff_files": 3}, {"diff_files": 0},
    {"diff_files": 0, "timeline": 60}, {"diff_files": 0, "timeline": 25},
    {"diff_files": 0, "timeline": 10},
    {"diff_files": 0, "timeline": 10, "file_rows": 80},
    {"diff_files": 0, "timeline": 10, "file_rows": 40},
    {"diff_files": 0, "timeline": 10, "file_rows": 15},
    {"diff_files": 0, "timeline": 10, "file_rows": 15, "plan_rows": 15},
    {"diff_files": 0, "timeline": 5, "file_rows": 10, "plan_rows": 5},
]


def _style(name: str, size: float, font: str = FONT, color: Any = INK,
           space_after: float = 0, **extra: Any) -> ParagraphStyle:
    extra.setdefault("leading", size * 1.3)
    return ParagraphStyle(name, fontName=font, fontSize=size, textColor=color,
                          spaceAfter=space_after, **extra)


TITLE = _style("title", 18, BOLD, space_after=4)
H1 = _style("h1", 13, BOLD, space_after=6, spaceBefore=10)
BODY = _style("body", 9, space_after=4)
CELL = _style("cell", 8)
CELL_B = _style("cellb", 8, BOLD)
SMALL = _style("small", 7.5, color=GREY)
CODE = _style("code", 7.5, leading=9.5)


def _p(text: Any, style: ParagraphStyle = BODY) -> Paragraph:
    return Paragraph(escape(str(text)), style)


def _more(hidden: int) -> list[Any]:
    return [_p(f"+{hidden} more — see report.json", SMALL)] if hidden > 0 else []


def _table(header: list[str], rows: list[list[Any]], widths: list[float]) -> Table:
    data = [[_p(h, CELL_B) for h in header]] + [
        [cell if isinstance(cell, Paragraph) else _p(cell, CELL) for cell in row]
        for row in rows]
    table = Table(data, colWidths=widths, repeatRows=1)
    table.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, GREY),
        ("LINEBELOW", (0, 1), (-1, -1), 0.3, GREY),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
    ]))
    return table


def _mark(passed: bool | None) -> Paragraph:
    if passed is None:
        return _p("n/a", CELL)
    color = ADD_HEX if passed else DEL_HEX
    return Paragraph(f'<font color="{color}"><b>{"PASS" if passed else "FAIL"}</b></font>',
                     CELL)


def banner(model: dict[str, Any]) -> Table:
    status = model["verdict"]["status"]
    table = Table([[Paragraph(status, _style("status", 26, BOLD, colors.white))],
                   [_p(model["headline"], _style("why", 10.5, color=colors.white))]],
                  colWidths=[WIDTH])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), STATUS[status]),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, 0), 14),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 12),
    ]))
    return table


# -- sections ---------------------------------------------------------------


def _summary(model: dict[str, Any], generated: str) -> list[Any]:
    meta, m, llm = model["meta"], model["metrics"], model["llm"]
    providers = ", ".join(f"{p['provider']} ({p['model']}): {p['calls']} call(s)"
                          for p in llm["providers"]) or "none — deterministic path, no LLM calls"
    facts = [
        ("Project", meta.get("repo_name")),
        ("Migration", f"{meta.get('source_api')} -> {meta.get('target_api')}"),
        ("Agent version", meta.get("agent_version")),
        ("Run id", meta.get("run_id")),
        ("Run date", meta.get("started_at")),
        ("Outcome", m.get("outcome", "no metrics (run did not finish)")),
        ("Providers used", providers),
        ("Data egress", llm["egress_line"]),
    ]
    metric_rows = [
        ["M1 recall / precision", f"{m['m1_recall']:.1f}% / {m['m1_precision']:.1f}%"
         if m else "—"],
        ["M2 pass rate / regressions", f"{m['m2_pass_rate']:.1f}% / {m['m2_regressions']}"
         if m else "—"],
        ["M3 tokens / steps / cost", f"{m['m3_tokens']:,} / {m['m3_steps']} / "
                                     f"${m['m3_cost_usd']:.4f}" if m else "—"],
    ]
    return [
        _p("Migration report", TITLE), Spacer(1, 4), banner(model), Spacer(1, 14),
        _table(["", ""], [[_p(k, CELL_B), v] for k, v in facts], [40 * mm, WIDTH - 40 * mm]),
        Spacer(1, 12), _p("Metrics", H1),
        _table(["Metric", "Value"], metric_rows, [60 * mm, WIDTH - 60 * mm]),
        Spacer(1, 10), _p(f"Generated {generated}", SMALL),
    ]


def _graph_figure(graph: dict[str, Any]) -> list[Any]:
    nodes, changed = graph["nodes"], set(graph["changed"])
    if not nodes:
        return [_p("No in-repo imports to draw.")]
    g = nx.DiGraph()
    g.add_nodes_from(nodes)
    g.add_edges_from(graph["edges"])
    # Changed files first, then the most connected: the ones a reviewer needs.
    keep = sorted(nodes, key=lambda n: (n not in changed, -g.degree(n), n))[:GRAPH_NODE_CAP]
    sub = g.subgraph(keep)
    # Layered, not force-directed: dependencies on the left, importers to the
    # right, an import cycle sharing one column. Deterministic and numpy-free.
    condensed = nx.condensation(sub.reverse())
    layers = [sorted(n for scc in layer for n in condensed.nodes[scc]["members"])
              for layer in nx.topological_generations(condensed)]
    height = 95 * mm
    drawing = Drawing(WIDTH, height)
    pos = {node: (20 + (WIDTH - 110) * col / max(len(layers) - 1, 1),
                  height - 10 - (height - 20) * (row + 0.5) / len(layer))
           for col, layer in enumerate(layers) for row, node in enumerate(layer)}

    def xy(node: str) -> tuple[float, float]:
        return pos[node]

    for a, b in sorted(sub.edges()):
        (x1, y1), (x2, y2) = xy(a), xy(b)
        drawing.add(Line(x1, y1, x2, y2, strokeColor=GREY, strokeWidth=0.5))
    for node in sorted(sub.nodes()):
        x, y = xy(node)
        drawing.add(Circle(x, y, 3.2, fillColor=INK if node in changed else colors.white,
                           strokeColor=INK, strokeWidth=0.6))
        drawing.add(String(x + 5, y - 2.5, node.rsplit("/", 1)[-1], fontName=FONT,
                           fontSize=6, fillColor=INK))
    note = (f"Filled: changed by the migration. Showing {len(keep)} of {len(nodes)} files"
            + (f"; +{len(nodes) - len(keep)} more — see report.json." if len(nodes) > len(keep)
               else "."))
    return [drawing, _p(note, SMALL)]


def _repo_map(model: dict[str, Any], limits: dict[str, int]) -> list[Any]:
    files = model["files"]
    shown = files[:limits.get("file_rows", len(files))]
    return [
        _p("Repository map", H1),
        _table(["File", "LOC", "Call sites", "Final status"],
               [[f["file"], f["loc"], f["sites"], f["status"]] for f in shown],
               [WIDTH - 75 * mm, 18 * mm, 22 * mm, 35 * mm]),
        *_more(len(files) - len(shown)), Spacer(1, 8),
        _p("Dependency graph (importer -> imported)", CELL_B), *_graph_figure(model["graph"]),
    ]


def _plan(model: dict[str, Any], limits: dict[str, int]) -> list[Any]:
    plan = model["plan"]
    batches = plan["batches"]
    shown = batches[:limits.get("plan_rows", len(batches))]
    cycles = {frozenset(c) for c in plan["cycles"]}
    rows = [[str(i), ", ".join(b), "cycle (atomic)" if frozenset(b) in cycles else ""]
            for i, b in enumerate(shown)]
    return [
        _p("Plan", H1), _p(plan["rationale"]),
        _table(["Batch", "Files", "Note"], rows, [14 * mm, WIDTH - 44 * mm, 30 * mm]),
        *_more(len(batches) - len(shown)),
        _p("Collapsed cycles: " + ("; ".join(" <-> ".join(c) for c in plan["cycles"]) or
                                    "none") + f". FR-3 violations: {plan['fr3_violations']}.",
           SMALL),
    ]


def _timeline(model: dict[str, Any], limits: dict[str, int]) -> list[Any]:
    rows = model["timeline"]
    shown = rows[:limits.get("timeline", len(rows))]
    return [
        _p("Execution timeline", H1),
        _table(["Step", "Node", "What happened"],
               [[r["step"], r["node"], r["text"]] for r in shown],
               [14 * mm, 20 * mm, WIDTH - 34 * mm]),
        *_more(len(rows) - len(shown)),
    ]


def _diff_line(line: str) -> Paragraph:
    text = escape(line).replace(" ", "&nbsp;") or "&nbsp;"
    if line.startswith("+"):
        text = f'<font color="{ADD_HEX}">{text}</font>'
    elif line.startswith("-"):
        text = f'<font color="{DEL_HEX}">{text}</font>'
    elif line.startswith("@@"):
        text = f'<font color="{GREY_HEX}">{text}</font>'
    return Paragraph(text, CODE)


def _changes(model: dict[str, Any], limits: dict[str, int]) -> list[Any]:
    changes = model["changes"]
    salvaged = (" Salvaged from the run's git history: the run crashed before writing it."
                if model["verification"]["patch_salvaged"] else "")
    flow: list[Any] = [
        _p("Changes", H1),
        _p(f"Full patch: migration.patch ({len(changes)} file(s), "
           f"+{sum(c['added'] for c in changes)} / -{sum(c['removed'] for c in changes)})."
           + salvaged),
    ]
    if not changes:
        return [*flow, _p("No changes.")]
    flow += [
        _table(["File", "+", "-", "Sites"],
               [[c["file"], Paragraph(f'<font color="{ADD_HEX}">+{c["added"]}</font>', CELL),
                 Paragraph(f'<font color="{DEL_HEX}">-{c["removed"]}</font>', CELL), c["sites"]]
                for c in changes],
               [WIDTH - 54 * mm, 16 * mm, 16 * mm, 22 * mm]),
    ]
    excerpted = changes[:limits.get("diff_files", len(changes))]
    for change in excerpted:
        flow.append(KeepTogether([Spacer(1, 5), _p(change["file"], CELL_B),
                                  *[_diff_line(line) for line in change["excerpt"]]]))
    if len(changes) > len(excerpted):
        flow += _p(f"Diff excerpts: +{len(changes) - len(excerpted)} more — see report.json",
                   SMALL),
    return flow


def _verification(model: dict[str, Any]) -> list[Any]:
    v = model["verification"]
    pre, post = v["pre"], v["post"]

    def totals(r: dict[str, Any]) -> str:
        return (f"{r['passed']}/{r['total']} passed, {r['failed']} failed, {r['errors']} errors"
                if r.get("total") is not None else "not run")

    cov = v["coverage"]
    cov_rows = [[f, f"{len(c['executed'])}/{len(c['changed'])}",
                 _mark(bool(c["executed"]) or not c["changed"])]
                for f, c in sorted(cov.items())][:15]
    semantic = [[c["file"], c["detail"], _mark(c["passed"])] for c in v["semantic"]][:15]
    flow: list[Any] = [
        _p("Verification", H1),
        _p(f"Tests before: {totals(pre)}. Tests after: {totals(post)}. "
           f"Ruff: {v['lint']['summary']}."),
        _table(["Check", "Result", "Evidence"],
               [[c["check"], _mark(c["passed"]), c["evidence"]] for c in v["checks"]],
               [62 * mm, 16 * mm, WIDTH - 78 * mm]),
    ]
    if semantic:
        flow += [Spacer(1, 6), _table(["Semantic check: file", "Detail", "Result"], semantic,
                                      [70 * mm, WIDTH - 86 * mm, 16 * mm]),
                 *_more(len(v["semantic"]) - len(semantic))]
    if cov_rows:
        flow += [Spacer(1, 6), _table(["Coverage: edited file", "Changed lines run", "Result"],
                                      cov_rows, [WIDTH - 56 * mm, 40 * mm, 16 * mm]),
                 *_more(len(cov) - len(cov_rows))]
    return flow


def _metrics(model: dict[str, Any]) -> list[Any]:
    series = model["series"]["tests_per_step"]
    flow: list[Any] = [_p("Metrics", H1)]
    if series:
        drawing = Drawing(WIDTH, 60 * mm)
        plot = LinePlot()
        plot.x, plot.y, plot.width, plot.height = 30, 22, WIDTH - 50, 60 * mm - 40
        plot.data = [[(i, passed) for i, (_, passed, _) in enumerate(series)]]
        plot.lines[0].strokeColor = INK
        plot.lines[0].symbol = makeMarker("FilledCircle", size=3, fillColor=INK)
        top = max([total for _, _, total in series] + [1])
        plot.yValueAxis.valueMin, plot.yValueAxis.valueMax = 0, top
        plot.xValueAxis.valueMin, plot.xValueAxis.valueMax = 0, max(len(series) - 1, 1)
        plot.xValueAxis.valueSteps = list(range(len(series)))
        plot.xValueAxis.labelTextFormat = lambda i: series[int(i)][0] \
            if int(i) < len(series) else ""
        for axis in (plot.xValueAxis, plot.yValueAxis):
            axis.strokeColor = GREY
            axis.labels.fontName, axis.labels.fontSize = FONT, 7
        drawing.add(plot)
        drawing.add(String(30, 60 * mm - 10, "Tests passing per step (x: step, 'pre' = baseline)",
                           fontName=FONT, fontSize=8))
        flow.append(drawing)
    by_role = model["series"]["tokens_by_role"]
    if by_role:
        height = 30 + 14 * len(by_role)
        drawing = Drawing(WIDTH, height)
        chart = HorizontalBarChart()
        chart.x, chart.y, chart.width, chart.height = 110, 12, WIDTH - 140, height - 26
        chart.data = [[tokens for _, tokens in by_role]]
        chart.categoryAxis.categoryNames = [label for label, _ in by_role]
        chart.bars[0].fillColor, chart.bars[0].strokeColor = INK, None
        chart.valueAxis.valueMin = 0
        for axis in (chart.categoryAxis, chart.valueAxis):
            axis.strokeColor = GREY
            axis.labels.fontName, axis.labels.fontSize = FONT, 7
        drawing.add(chart)
        drawing.add(String(0, height - 10, "Tokens by role / provider", fontName=FONT,
                           fontSize=8))
        flow.append(drawing)
    else:
        flow.append(_p("Tokens by role / provider: no LLM calls — deterministic run, 0 tokens."))
    return flow


def _issues(model: dict[str, Any]) -> list[Any]:
    issues = model["issues"]
    if not issues:
        return [_p("Issues & residuals", H1), _p("None. Every check passed.")]
    rows = [[Paragraph(f'<font color="{STATUS_HEX[r["level"]]}"><b>{r["level"]}'
                       f"</b></font>", CELL), f"{r['text']} Evidence: {r['evidence']}",
             r["action"]] for r in issues]
    return [_p("Issues & residuals", H1),
            _table(["Level", "Issue and evidence", "Recommended action"], rows,
                   [18 * mm, (WIDTH - 18 * mm) * 0.58, (WIDTH - 18 * mm) * 0.42])]


# -- assembly ---------------------------------------------------------------


def _story(model: dict[str, Any], limits: dict[str, int], generated: str) -> list[Any]:
    return [
        *_summary(model, generated), PageBreak(),
        *_repo_map(model, limits), *_plan(model, limits), *_timeline(model, limits),
        *_changes(model, limits), *_verification(model), *_metrics(model), *_issues(model),
        Spacer(1, 14), KeepTogether([_p("Final status", H1), banner(model)]),
    ]


def _build(model: dict[str, Any], limits: dict[str, int], generated: str) -> tuple[bytes, int]:
    buffer = io.BytesIO()
    run_id = model["meta"].get("run_id") or "?"

    def footer(canvas: Any, doc: Any) -> None:
        canvas.saveState()
        canvas.setStrokeColor(GREY)
        canvas.setLineWidth(0.4)
        canvas.line(MARGIN, 14 * mm, A4[0] - MARGIN, 14 * mm)
        canvas.setFont(FONT, 7.5)
        canvas.drawString(MARGIN, 10 * mm, f"MRA run {run_id}")
        canvas.drawRightString(A4[0] - MARGIN, 10 * mm, f"Page {doc.page}")
        canvas.restoreState()

    doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
                            topMargin=MARGIN, bottomMargin=MARGIN,
                            title=f"Migration report {run_id}", author="MRA")
    doc.build(_story(model, limits, generated), onFirstPage=footer, onLaterPages=footer)
    return buffer.getvalue(), doc.page


def render(model: dict[str, Any], generated: str) -> tuple[bytes, int, dict[str, int]]:
    """``(pdf bytes, pages, truncation applied)`` — the first ladder level that fits."""
    for limits in LADDER:
        data, pages = _build(model, limits, generated)
        if pages <= MAX_PAGES:
            return data, pages, limits
    raise RuntimeError(f"report exceeds {MAX_PAGES} pages even at the last truncation level")
