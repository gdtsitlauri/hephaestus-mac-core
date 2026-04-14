import csv
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _run(pyfile):
    subprocess.run([sys.executable, str(ROOT / pyfile)], check=True, cwd=ROOT, timeout=120)


def _csv_rows(path):
    with open(path, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_rtl_baseline_exists():
    rtl = ROOT / "src/rtl/mac_int8.sv"
    assert rtl.exists()
    content = rtl.read_text(encoding="utf-8")
    assert "module mac_int8" in content and "always_ff" in content


def test_rtl_optimized_has_clock_gating():
    rtl = ROOT / "src/rtl/optimized/mac_int8.sv"
    assert rtl.exists()
    assert "clk_gated" in rtl.read_text(encoding="utf-8")


def test_cyclops_optimizer_runs():
    _run("src/python/cyclops_rtl.py")
    report = ROOT / "results/benchmarks/cyclops_optimization_report.txt"
    assert report.exists()


def test_benchmarks_generated():
    _run("src/python/generate_benchmarks.py")
    expected = [
        "power_analysis.csv",
        "area_analysis.csv",
        "timing_analysis.csv",
        "ppa_summary.csv",
    ]
    for name in expected:
        assert (ROOT / "results/benchmarks" / name).exists()


def test_power_improvement():
    rows = _csv_rows(ROOT / "results/benchmarks/power_analysis.csv")
    baseline = float(rows[0]["total_power_mW"])
    optimized = float(rows[1]["total_power_mW"])
    assert optimized < baseline


def test_ai_testbench_gpu():
    _run("src/python/ai_testbench.py")
    rows = _csv_rows(ROOT / "results/benchmarks/tops_estimation.csv")
    assert len(rows) == 1
    assert rows[0]["device"] in {"cuda", "cpu"}
    assert float(rows[0]["tops"]) > 0.0


def test_int8_accuracy():
    rows = _csv_rows(ROOT / "results/benchmarks/ai_testbench_results.csv")
    assert float(rows[0]["snr_db"]) > 20.0


def test_formal_assertions():
    _run("src/python/verify_assertions.py")
    rows = _csv_rows(ROOT / "results/benchmarks/formal_verification.csv")
    assert len(rows) == 3
    assert all(r["status"] == "PASS" for r in rows)
