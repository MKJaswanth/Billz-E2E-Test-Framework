"""
Generate a single, self-contained HTML report from pytest's JUnit XML output.

Usage:
  pytest                               # runs tests, writes results.xml automatically
  python report.py                     # reads results.xml, writes reports/report.html
  python report.py --results results.xml --out reports/report.html
"""

import argparse
import html
import os
import xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import datetime

STATUS_COLORS = {
    "passed":  "#1a7f37",
    "failed":  "#cf222e",
    "error":   "#bc4c00",
    "skipped": "#9a6700",
}


def load_results(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # handle both <testsuites> and bare <testsuite> roots
    suites = root.findall("testsuite") if root.tag == "testsuites" else [root]

    tests = []
    for suite in suites:
        suite_name = suite.get("name", "ungrouped")
        for tc in suite.findall("testcase"):
            name = tc.get("name", "unnamed")
            duration_s = float(tc.get("time", 0))

            if tc.find("failure") is not None:
                status = "failed"
                msg = (tc.find("failure").get("message") or "").strip().splitlines()[0][:200]
            elif tc.find("error") is not None:
                status = "error"
                msg = (tc.find("error").get("message") or "").strip().splitlines()[0][:200]
            elif tc.find("skipped") is not None:
                status = "skipped"
                msg = (tc.find("skipped").get("message") or "").strip()
            else:
                status = "passed"
                msg = ""

            tests.append({
                "name": name,
                "suite": suite_name,
                "status": status,
                "duration_s": duration_s,
                "message": msg,
            })
    return tests


def fmt_duration(s):
    if s < 60:
        return f"{s:.1f}s"
    m, s = divmod(s, 60)
    return f"{int(m)}m {s:.0f}s"


def build_html(tests, xml_path):
    total = len(tests)
    counts = defaultdict(int)
    for t in tests:
        counts[t["status"]] += 1
    passed = counts["passed"]
    total_s = sum(t["duration_s"] for t in tests)
    pass_rate = (passed / total * 100) if total else 0
    generated = datetime.now().strftime("%d %b %Y, %I:%M %p")

    by_suite = defaultdict(list)
    for t in tests:
        by_suite[t["suite"]].append(t)
    order = ["failed", "error", "skipped", "passed"]
    for v in by_suite.values():
        v.sort(key=lambda t: order.index(t["status"]) if t["status"] in order else 99)

    def card(label, value, color):
        return f'<div class="card"><div class="card-value" style="color:{color}">{value}</div><div class="card-label">{label}</div></div>'

    cards = (
        card("Total", total, "#24292f")
        + card("Passed", passed, STATUS_COLORS["passed"])
        + card("Failed", counts["failed"], STATUS_COLORS["failed"])
        + card("Skipped", counts["skipped"], STATUS_COLORS["skipped"])
        + card("Pass rate", f"{pass_rate:.0f}%",
               STATUS_COLORS["passed"] if pass_rate >= 90 else STATUS_COLORS["error"])
        + card("Duration", fmt_duration(total_s), "#24292f")
    )

    rows = ""
    for suite in sorted(by_suite):
        suite_tests = by_suite[suite]
        s_pass = sum(1 for t in suite_tests if t["status"] == "passed")
        rows += f'<tr class="suite-row"><td colspan="3">📁 {html.escape(suite)}<span class="suite-meta">{s_pass}/{len(suite_tests)} passed</span></td></tr>'
        for t in suite_tests:
            color = STATUS_COLORS.get(t["status"], "#57606a")
            msg = f'<div class="err">{html.escape(t["message"])}</div>' if t["message"] else ""
            rows += f'<tr><td><span class="pill" style="background:{color}">{t["status"]}</span></td><td class="tname">{html.escape(t["name"])}{msg}</td><td class="dur">{fmt_duration(t["duration_s"])}</td></tr>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Test Report — {generated}</title>
<style>
  *{{box-sizing:border-box}}body{{font-family:-apple-system,Segoe UI,Roboto,sans-serif;margin:0;background:#f6f8fa;color:#24292f}}
  .wrap{{max-width:960px;margin:0 auto;padding:32px 20px}}h1{{font-size:22px;margin:0 0 4px}}
  .sub{{color:#57606a;font-size:13px;margin-bottom:24px}}
  .cards{{display:grid;grid-template-columns:repeat(6,1fr);gap:12px;margin-bottom:28px}}
  .card{{background:#fff;border:1px solid #d0d7de;border-radius:10px;padding:16px 12px;text-align:center}}
  .card-value{{font-size:24px;font-weight:700}}.card-label{{font-size:11px;color:#57606a;text-transform:uppercase;letter-spacing:.04em;margin-top:4px}}
  table{{width:100%;border-collapse:collapse;background:#fff;border:1px solid #d0d7de;border-radius:10px;overflow:hidden}}
  td{{padding:10px 14px;border-top:1px solid #eaeef2;font-size:14px;vertical-align:top}}
  .suite-row td{{background:#f6f8fa;font-weight:600;font-size:13px}}
  .suite-meta{{color:#57606a;font-weight:400;margin-left:8px;font-size:12px}}
  .pill{{color:#fff;padding:2px 10px;border-radius:20px;font-size:11px;font-weight:600;text-transform:uppercase}}
  .tname{{font-family:ui-monospace,Consolas,monospace;font-size:13px}}.dur{{text-align:right;color:#57606a;white-space:nowrap}}
  .err{{color:#cf222e;font-size:12px;margin-top:6px;font-family:ui-monospace,Consolas,monospace}}
  .foot{{color:#8b949e;font-size:12px;text-align:center;margin-top:24px}}
</style>
</head>
<body>
  <div class="wrap">
    <h1>Playwright Test Report</h1>
    <div class="sub">Generated {generated} · source: {html.escape(xml_path)}</div>
    <div class="cards">{cards}</div>
    <table>{rows}</table>
    <div class="foot">Self-contained report · open anywhere, no server needed</div>
  </div>
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(description="Build a shareable HTML test report.")
    parser.add_argument("--results", default="results.xml", help="JUnit XML file (default: results.xml)")
    parser.add_argument("--out", default="reports/report.html", help="output HTML file")
    args = parser.parse_args()

    tests = load_results(args.results)
    if not tests:
        print(f"No test cases found in '{args.results}'.")
        return

    out_dir = os.path.dirname(args.out)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    with open(args.out, "w", encoding="utf-8") as f:
        f.write(build_html(tests, args.results))

    passed = sum(1 for t in tests if t["status"] == "passed")
    print(f"Wrote {args.out} — {passed}/{len(tests)} passed. Share this file with your team.")


if __name__ == "__main__":
    main()
