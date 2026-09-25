"""Source and executable fingerprints for explicit-backend campaigns."""
from __future__ import annotations

import hashlib
from pathlib import Path
import shutil
import subprocess


def file_digest(path):
    result = hashlib.sha256()
    with Path(path).open('rb') as handle:
        for block in iter(lambda: handle.read(1024*1024), b''):
            result.update(block)
    return result.hexdigest()


def source_tree(root):
    root = Path(root).resolve()
    entries = [(str(path.relative_to(root)), file_digest(path))
               for path in sorted(root.rglob('*.mo')) if path.is_file()]
    encoded = ''.join(f'{name}\0{digest}\n' for name, digest in entries).encode()
    return dict(path=str(root), modelica_files=len(entries),
                modelica_tree_sha256=hashlib.sha256(encoded).hexdigest())


def capture(args):
    executable = shutil.which('omc' if args.backend == 'openmodelica' else args.rumoca)
    if executable is None:
        candidate = Path(args.rumoca) if args.backend != 'openmodelica' else None
        executable = str(candidate.resolve()) if candidate and candidate.is_file() else None
    version = None
    if executable:
        executable = str(Path(executable).resolve())
        try:
            result = subprocess.run([executable,'--version'], capture_output=True,
                                    text=True, timeout=5)
            version = (result.stdout+result.stderr).strip()
        except (OSError, subprocess.TimeoutExpired):
            version = 'unavailable'
    roots = set(map(Path, args.source_root))
    roots.update(Path(p).resolve().parent for p in args.library)
    return dict(backend=args.backend, executable=executable, version=version,
        executable_sha256=file_digest(executable) if executable else None,
        stop_time=args.stop_time, intervals=args.intervals, timeout_seconds=args.timeout,
        native_solver=('rk-like' if args.backend == 'rumoca-source' else
                       'auto' if args.backend == 'rumoca' else None),
        execution_profile={'rumoca':'editable-equation-artifact',
                           'rumoca-source':'native-source',
                           'openmodelica':'external-simulation'}[args.backend],
        parameter_policy=('frozen' if getattr(args, 'freeze_parameters', False) else 'declared'),
        library_files=[dict(path=str(Path(p).resolve()), sha256=file_digest(p)) for p in args.library],
        source_trees=[source_tree(root) for root in sorted(roots)],
        scope='Tree fingerprints cover .mo sources, not external binaries or C resources.')
