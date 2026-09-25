#!/usr/bin/env python3
"""Render the manually reviewed notes against the complete archived census.

No keyword classifier or detector results are inferred from issue labels.
Running this only rewrites evaluation artifacts in this directory.
"""
import csv
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
CATEGORIES = {
    'DOCUMENTATION': ('Outside numerical scope', 'None for the requested editorial/graphical change.', 'Documentation, diagram, link and source-style validation.'),
    'ENHANCEMENT': ('Feature/design request', 'No detection claim: requested behavior/API must first be specified.', 'API design, compatibility and targeted regression tests.'),
    'REFERENCE': ('Test/reference validation needed', 'DifferentialSan can compare traces, but a disagreement is not proof and current alignment is inadequate.', 'F5: reference metadata, meaningful signals, event alignment and mixed tolerances.'),
    'FRONTEND': ('Source/compiler analysis needed', 'Flattened numerical sanitizers do not implement these language/binding/effect checks.', 'F2/F3: source-aware binding, definite assignment, effects, local balance and compiler support.'),
    'SHAPE': ('Shape analysis needed', 'DimensionSan checks SI units, not array dimensions. No interprocedural extent/bounds detector.', 'F2: shape contracts, reduced/full representations and runtime bounds provenance.'),
    'EXTERNAL': ('External/platform scope', 'Modelica numerical sanitizers do not validate platform, file, C ABI or FMI protocols.', 'F9: platform CI, C/ABI/resource instrumentation, file and FMI contract tests.'),
    'UNIT': ('Partial dimensional capability', 'DimensionSan can flag known incompatible additive/relational units; this row has no demonstrated hit.', 'F7: unit propagation through bindings, calls, powers and quantity/conversion metadata.'),
    'CONTRACT': ('Semantic oracle needed', 'Finite plausible wrong results generally pass numeric/domain checks; generic physical checks do not encode this contract.', 'F4/F8: API metamorphic, analytic, thermodynamic or component-specific physical contracts.'),
    'NUMERIC': ('Possible symptom coverage only', 'Domain/Numeric/Solver/AssertSan may observe a reached failure; no executed issue-specific hit is established here.', 'F6: scaled residual/rank/conditioning, progress budgets and high-precision error oracles.'),
    'INIT': ('Possible initialization symptom only', 'InitSan/InitStaticSan/StructureSan and SolverSan can expose candidates or failures, not prove the reported root cause.', 'F6: branch/homotopy-aware initialization with numerical rank, binding and residual evidence.'),
    'EVENT': ('Temporal oracle needed', 'EventSan/ZenoSan measure event activity; they do not specify phase, sample delay, polarity or transition priority.', 'F3/F4: supported event/clock execution plus state-machine and sample-history contracts.'),
    'UNRESOLVED': ('Not established', 'No defensible defect/detectability verdict from the current evidence; do not count as clean or missed.', 'Resolve the stated contract/version/reproducer uncertainty; then choose an oracle.'),
    'EXCLUDED': ('Own report excluded', 'Not eligible for independent detection evaluation.', 'Retain provenance only; do not add to independent discovery totals.'),
}
PROBED = {3624, 4451, 4459, 4749, 4750, 4771}


def main():
    issues = json.loads((HERE/'issues.json').read_text())['issues']
    comments = {i['issue_number']: i['comments'] for i in
                json.loads((HERE/'comments.json').read_text())['comments']}
    with (HERE/'assessment-notes.tsv').open() as handle:
        notes = list(csv.DictReader(handle, delimiter='\t'))
    by_id = {int(x['issue']): x for x in notes}
    assert len(by_id) == len(notes), 'duplicate review note'
    ids = {i['issue_number'] for i in issues}
    assert len(ids) == len(issues) == 353
    assert ids == by_id.keys() == comments.keys(), 'missing or extra assessment/comment record'
    assert sum(len(c) for c in comments.values()) == 1637
    rows = []
    for issue in sorted(issues, key=lambda i: i['issue_number']):
        n = issue['issue_number']
        assert issue['state'] == 'open'
        assert issue['comments'] == len(comments[n]), f'comment count mismatch: {n}'
        note = by_id[n]
        status, current, needed = CATEGORIES[note['category']]
        own = issue['user']['login'].lower() == 'arslan8'
        assert own == (n == 4814) == (note['category'] == 'EXCLUDED')
        evidence = 'Issue/discussion capability assessment; no execution verdict'
        if n in PROBED:
            evidence = 'Issue-derived OMC witness; ModelSan path blocked; no detection credit'
            current = 'Executed probe blocked before relevant ModelSan observation; unrelated static warnings are not hits.'
        if own:
            evidence = 'Census only; excluded'
        rows.append(dict(issue=n, title=issue['title'], url=issue['url'],
                         author=issue['user']['login'], created_at=issue['created_at'],
                         updated_at=issue['updated_at'], labels=[l['name'] for l in (issue['labels'] or [])],
                         comment_count=len(comments[n]), independent=not own,
                         category=note['category'], status=status, evidence=evidence,
                         current_capability=current, rationale=note['rationale'],
                         needed=needed, demonstrated_modelsan_detection=False))
    result = dict(repository='modelica/ModelicaStandardLibrary', snapshot_date='2026-09-24',
                  scope='353 open issues including one excluded own report; not a recall benchmark',
                  category_counts=dict(sorted(Counter(r['category'] for r in rows).items())), issues=rows)
    (HERE/'assessment.json').write_text(json.dumps(result, indent=2)+'\n')
    with (HERE/'assessment.csv').open('w', newline='') as handle:
        fields = ['issue','title','url','independent','category','status','evidence','comment_count',
                  'current_capability','rationale','needed','demonstrated_modelsan_detection']
        writer = csv.DictWriter(handle, fields, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)
    def cell(value):
        return str(value).replace('|', '\\|').replace('\n', ' ').replace('<','&lt;')
    lines = ['# Complete open-issue index', '',
             'Snapshot: 2026-09-24. All 353 issues have an assessment; #4814 is excluded from the 352 independent entries. All 1,637 comments are archived. This is capability screening, not 352 executed bug reproducers. See [method and limits](README.md), [feature gaps](feature-gaps.md), and [focused results](focused-results.md).', '',
             'A missing demonstrated detection is **not** a measured sanitizer miss. Most entries were not run; unresolved questions and feature requests are not confirmed defects. Categories are analyst assessments, not GitHub label truth. Linked/umbrella issues remain separate rows but must not be counted as independent bugs.', '',
             '| Issue | Category | Evidence | Current capability | Assessment / why | Needed |',
             '|---|---|---|---|---|---|']
    for r in rows:
        link = f"[#{r['issue']}]({r['url']}) {cell(r['title'])}"
        evidence = '[OMC witness; blocked](focused-results.md)' if r['issue'] in PROBED else 'Not executed'
        if not r['independent']:
            evidence = 'Excluded'
        lines.append('| '+' | '.join([link, r['category'], evidence,
                     cell(r['current_capability']), cell(r['rationale']), cell(r['needed'])])+' |')
    (HERE/'index.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps({'issues':len(rows),'comments':1637,'independent':352,
                      'categories':result['category_counts']}, indent=2))


if __name__ == '__main__':
    main()
