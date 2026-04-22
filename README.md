# HEPHAESTUS: Causal-Optimized INT8 Silicon Framework


HEPHAESTUS is an end-to-end hardware/HDL framework for a SkyWater-130nm-oriented INT8 MAC and systolic datapath. The physical layout is already generated at `results/gdsii/mac_int8.gds`, while benchmark reports are produced through lightweight estimation scripts (no local OpenLane/PDK install required).


## Project Metadata

| Field | Value |
| --- | --- |
| Author | George David Tsitlauri |
| Affiliation | Dept. of Informatics & Telecommunications, University of Thessaly, Greece |
| Contact | gdtsitlauri@gmail.com |
| Year | 2026 |

## PPA Results (Baseline vs CYCLOPS-Optimized)

| Metric | Baseline | Optimized | Improvement |
|---|---:|---:|---:|
| Total Power (mW) | 2.24 | 1.95 | 13.1% |
| Dynamic Power (mW) | 2.22 | 1.93 | 13.2% |
| Static Power (mW) | 0.02 | 0.02 | 0% |
| Die Area (um^2) | 40000 | 40000 | 0% |
| Cell Area (um^2) | 92.0 | 116.0 | -26.1% |
| Utilization (%) | 0.23 | 0.29 | -26.1% |
| Max Frequency (MHz) | 212.77 | 212.77 | 0% |
| Setup Slack @100 MHz (ns) | 5.3 | 5.3 | 0% |

## CYCLOPS-RTL Optimization Summary

- `clock_gating`: detects/maintains gated clock network for sequential toggling reduction.
- `operand_isolation`: guards multiplier when `weight == 0` or `act == 0` to reduce switching.
- `pipeline_stage_analysis`: reports two-stage recommendation for timing closure:
  - Stage 1: register multiplier output
  - Stage 2: register accumulation
- report output: `results/benchmarks/cyclops_optimization_report.txt`

## AI Testbench (INT8 + GPU-aware)

- `src/python/ai_testbench.py` compares float32, INT8 quantized, and RTL-behavioral outputs.
- Produces:
  - `results/benchmarks/ai_testbench_results.csv`
  - `results/benchmarks/tops_estimation.csv`
- Current generated metrics:
  - SNR: 29.8941 dB (`>20 dB` target)
  - TOPS: 2.6667e-03
  - TOPS/Watt: 1.3606

## Formal Verification

- Assertions are defined in `src/rtl/mac_int8_assertions.sv`:
  - no overflow in 20-bit signed range
  - reset clears accumulator within one cycle
  - `en=0` holds accumulator state
- Behavioral checker: `src/python/verify_assertions.py`
- Output: `results/benchmarks/formal_verification.csv` (all PASS, 100% coverage)

## How to Run

1. Optimize RTL:
   - `python3 src/python/cyclops_rtl.py`
2. Generate PPA benchmarks:
   - `python3 src/python/generate_benchmarks.py`
3. Run AI testbench:
   - `python3 src/python/ai_testbench.py`
4. Run formal behavioral checks:
   - `python3 src/python/verify_assertions.py`
5. Execute regression tests:
   - `pytest -q`

## Project Structure

- `src/rtl/`: baseline and optimized SystemVerilog RTL
- `src/python/`: optimizer, benchmark, AI, and formal scripts
- `results/gdsii/`: generated physical layout (`mac_int8.gds`)
- `results/benchmarks/`: all CSV/TXT benchmark outputs
- `paper/`: conference-oriented LaTeX report

## Note

GDSII is already generated and available at `results/gdsii/mac_int8.gds`.

## Why HEPHAESTUS Can Still Be Strong

HEPHAESTUS already has a real RTL and silicon-oriented workflow:

- RTL exists,
- optimization passes exist,
- GDSII output exists,
- AI and formal-style checks exist.

What is still missing is deeper downstream hardware closure through HLS/Vivado
and broader validation, not the core research system itself. That makes the
repo best presented as a serious silicon/RTL research platform with future
physical-validation expansion.


