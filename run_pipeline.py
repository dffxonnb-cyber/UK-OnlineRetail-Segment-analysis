from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent
NOTEBOOKS_DIR = ROOT / "분석 과정"
DATASET_DIR = ROOT / "데이터셋"
ARTIFACTS_DIR = ROOT / "artifacts"
EXECUTED_DIR = ARTIFACTS_DIR / "executed_notebooks"
LOGS_DIR = ARTIFACTS_DIR / "logs"
JUPYTER_RUNTIME_DIR = ARTIFACTS_DIR / "jupyter_runtime"
JUPYTER_CONFIG_DIR = ARTIFACTS_DIR / "jupyter_config"
JUPYTER_DATA_DIR = ARTIFACTS_DIR / "jupyter_data"

DEFAULT_NOTEBOOKS = [
    "00_전처리_코드정리.ipynb",
    "01_분석_RFM_코드정리.ipynb",
    "02_통계검정_코드정리.ipynb",
    "03_시각화_코드정리.ipynb",
]
REQUIRED_INPUT = "Online_Retail.csv"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Execute the retail notebook pipeline without modifying the source notebooks."
    )
    parser.add_argument(
        "--clear-artifacts",
        action="store_true",
        help="Delete previous executed notebooks and logs before running.",
    )
    parser.add_argument(
        "--stop-on-error",
        action="store_true",
        help="Stop immediately when a notebook execution fails.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=-1,
        help="Per-notebook execution timeout in seconds. Default is -1 (no timeout).",
    )
    parser.add_argument(
        "--notebook",
        action="append",
        dest="selected_notebooks",
        default=[],
        help="Run only the specified notebook filename. Repeat to select multiple notebooks.",
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        help="Directory containing Online_Retail.csv.",
    )
    parser.add_argument(
        "--skip-data-sync",
        action="store_true",
        help="Do not copy the discovered input CSV into this repository's dataset directory.",
    )
    return parser.parse_args()


def ensure_nbconvert_available() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "nbconvert", "--version"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(
            "nbconvert is not available in the current Python environment. "
            "Install the notebook execution dependencies first."
        )


def resolve_notebooks(args: argparse.Namespace) -> list[Path]:
    notebook_names = args.selected_notebooks or DEFAULT_NOTEBOOKS
    notebooks: list[Path] = []
    for name in notebook_names:
        notebook_path = NOTEBOOKS_DIR / name
        if not notebook_path.exists():
            raise SystemExit(f"Notebook not found: {notebook_path}")
        notebooks.append(notebook_path)
    return notebooks


def prepare_directories(clear_artifacts: bool) -> None:
    if clear_artifacts and ARTIFACTS_DIR.exists():
        shutil.rmtree(ARTIFACTS_DIR)

    EXECUTED_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    DATASET_DIR.mkdir(parents=True, exist_ok=True)
    JUPYTER_RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    JUPYTER_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    JUPYTER_DATA_DIR.mkdir(parents=True, exist_ok=True)


def has_required_input(data_dir: Path) -> bool:
    return (data_dir / REQUIRED_INPUT).exists()


def discover_input_directory() -> Path | None:
    workspace_root = ROOT.parents[2]
    search_roots = [
        ROOT,
        ROOT.parent,
        workspace_root,
        workspace_root / "01_projects",
    ]
    for search_root in search_roots:
        if not search_root.exists():
            continue
        for match in search_root.rglob(REQUIRED_INPUT):
            return match.parent
    return None


def sync_input_data(args: argparse.Namespace) -> Path:
    source_dir = args.data_dir.resolve() if args.data_dir else None
    if source_dir and not source_dir.exists():
        raise SystemExit(f"Input data directory does not exist: {source_dir}")

    if not source_dir and has_required_input(DATASET_DIR):
        return DATASET_DIR

    if not source_dir:
        source_dir = discover_input_directory()

    if source_dir is None:
        raise SystemExit(
            f"Required input CSV was not found. Place {REQUIRED_INPUT} in {DATASET_DIR} or pass --data-dir."
        )

    if args.skip_data_sync:
        if has_required_input(source_dir):
            return source_dir
        raise SystemExit(f"Input data directory does not contain {REQUIRED_INPUT}: {source_dir}")

    src = source_dir / REQUIRED_INPUT
    dst = DATASET_DIR / REQUIRED_INPUT
    if not src.exists():
        raise SystemExit(f"Missing required input file: {src}")
    if not dst.exists() or src.resolve() != dst.resolve():
        shutil.copy2(src, dst)
        print(f"Copied input data into repository dataset directory: {REQUIRED_INPUT}")

    return DATASET_DIR


def print_preflight_summary(data_dir: Path, notebooks: list[Path], log_path: Path) -> None:
    print(f"Notebook source directory: {NOTEBOOKS_DIR}")
    print(f"Input data directory: {data_dir}")
    print(f"Executed notebook output: {EXECUTED_DIR}")
    print(f"Log file: {log_path}")
    print("Notebook order:")
    for notebook in notebooks:
        print(f"- {notebook.name}")


def create_runtime_notebook_copy(notebook: Path) -> Path:
    runtime_path = NOTEBOOKS_DIR / f".runtime__{notebook.name}"
    notebook_json = json.loads(notebook.read_text(encoding="utf-8"))

    for cell in notebook_json.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        cell["execution_count"] = None
        cell["outputs"] = []

    runtime_path.write_text(
        json.dumps(notebook_json, ensure_ascii=False, indent=1),
        encoding="utf-8",
    )
    return runtime_path


def build_nbconvert_command(runtime_notebook: Path, output_name: str, timeout: int) -> list[str]:
    return [
        sys.executable,
        "-m",
        "nbconvert",
        "--to",
        "notebook",
        "--execute",
        runtime_notebook.name,
        "--output",
        output_name,
        "--output-dir",
        str(EXECUTED_DIR),
        f"--ExecutePreprocessor.timeout={timeout}",
    ]


def run_notebook(notebook: Path, timeout: int, log_handle) -> int:
    runtime_notebook = create_runtime_notebook_copy(notebook)
    command = build_nbconvert_command(runtime_notebook, notebook.name, timeout)
    started_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[RUN] {notebook.name} ({started_at})")
    log_handle.write(f"\n=== {notebook.name} | START {started_at} ===\n")
    log_handle.write("COMMAND: " + " ".join(command) + "\n")
    log_handle.flush()

    env = dict(os.environ)
    env["JUPYTER_RUNTIME_DIR"] = str(JUPYTER_RUNTIME_DIR)
    env["JUPYTER_CONFIG_DIR"] = str(JUPYTER_CONFIG_DIR)
    env["JUPYTER_DATA_DIR"] = str(JUPYTER_DATA_DIR)

    try:
        result = subprocess.run(
            command,
            cwd=NOTEBOOKS_DIR,
            env=env,
            stdout=log_handle,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
    finally:
        runtime_notebook.unlink(missing_ok=True)

    finished_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "OK" if result.returncode == 0 else f"FAILED ({result.returncode})"
    print(f"[{status}] {notebook.name} ({finished_at})")
    log_handle.write(f"=== {notebook.name} | END {finished_at} | {status} ===\n")
    log_handle.flush()
    return result.returncode


def main() -> int:
    args = parse_args()
    ensure_nbconvert_available()
    notebooks = resolve_notebooks(args)
    prepare_directories(clear_artifacts=args.clear_artifacts)
    data_dir = sync_input_data(args)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = LOGS_DIR / f"run_pipeline_{timestamp}.log"
    failures: list[tuple[str, int]] = []

    print_preflight_summary(data_dir=data_dir, notebooks=notebooks, log_path=log_path)

    with log_path.open("w", encoding="utf-8") as log_handle:
        for notebook in notebooks:
            return_code = run_notebook(notebook, timeout=args.timeout, log_handle=log_handle)
            if return_code != 0:
                failures.append((notebook.name, return_code))
                if args.stop_on_error:
                    break

    if failures:
        print("\nPipeline finished with errors:")
        for notebook_name, return_code in failures:
            print(f"- {notebook_name}: exit code {return_code}")
        print(f"See log: {log_path}")
        return 1

    print("\nPipeline completed successfully.")
    print(f"Executed notebooks saved to: {EXECUTED_DIR}")
    print(f"Log saved to: {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
