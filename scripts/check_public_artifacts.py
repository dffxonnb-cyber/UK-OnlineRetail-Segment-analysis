from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    ROOT / "README.md",
    ROOT / "docs" / "README.md",
    ROOT / "docs" / "한페이지_요약.md",
    ROOT / "docs" / "PPT_Retail.md",
    ROOT / "리테일_시각화_png" / "도넛차트.png",
    ROOT / "리테일_시각화_png" / "월별고객별매출추이&성장률분석.png",
    ROOT / "리테일_시각화_png" / "ARPU.png",
    ROOT / "run_pipeline.py",
    ROOT / "AUTOMATION_GUIDE.md",
]


def main() -> int:
    missing = [path for path in REQUIRED_PATHS if not path.exists()]
    if missing:
        print("Missing required public review artifacts:")
        for path in missing:
            print(f"- {path.relative_to(ROOT)}")
        return 1

    print("Public review artifacts verified:")
    for path in REQUIRED_PATHS:
        print(f"- {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
