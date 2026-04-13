# HEPHAESTUS: Energy-Efficient AI Hardware Accelerator

HEPHAESTUS is an end-to-end silicon design project featuring an 8-bit Integer Multiply-Accumulate (MAC) unit, optimized for Edge AI applications. The design was synthesized using the SkyWater 130nm CMOS process via the OpenLane flow.

## Key Features
* Systolic Core: High-throughput 8-bit MAC architecture designed for neural network inference.
* CYCLOPS-RTL Optimization: Integrated custom causal power-gating engine that intelligently manages switching activity.
* Ultra-Low Power: Achieved a total power consumption of 1.96 mW at 100 MHz (a 13% improvement over baseline designs).
* Silicon Ready: Passed all Sign-off checks, including DRC (Design Rule Check) and LVS (Layout Vs Schematic).

## Project Structure
* openlane/mac_int8/: OpenLane configuration and flow scripts.
* src/: SystemVerilog source code (optimized and baseline) and Python tools.
* results/gdsii/: Final silicon layout (mac_int8.gds).
* results/benchmarks/: Power and Area reports.
* paper/: Technical documentation and LaTeX reports.
* tb/cpp/: C++/Verilator testbench for RTL verification.

## Performance Metrics (Sign-off)
* Technology Node: SkyWater 130nm
* Clock Frequency: 100 MHz
* Internal Power: 0.927 mW
* Switching Power: 1.040 mW
* Total Dynamic Power: 1.96 mW
* Status: DRC/LVS Clean

## How to Run
1. Simulation: Use the provided Makefile to run the Verilator testbench:
   make run_sim

2. Synthesis: To reproduce the GDSII layout, run the automated synthesis script:
   ./run_synthesis.sh

## License
This project is part of an academic research initiative into low-power AI hardware architectures.