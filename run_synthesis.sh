#!/bin/bash
# HEPHAESTUS Physical Design Flow Orchestrator

echo "=== HEPHAESTUS: Starting Physical Synthesis for mac_int8 ==="

mkdir -p results/gdsii
mkdir -p results/benchmarks
mkdir -p pdks

# Το 'volare enable' ενεργοποιεί το PDK ώστε να το βρει το OpenLane
sudo docker run --rm \
    -v $(pwd):/work \
    -e PDK_ROOT=/work/pdks \
    -u $(id -u):$(id -g) \
    efabless/openlane:latest \
    bash -c "volare enable bdc9412b3e468c102d01b7cf6337be06ec6e9c9a && flow.tcl -design /work/openlane/mac_int8 -config_file /work/openlane/mac_int8/config.json -tag hephaestus_v1 -overwrite"

echo "=== Synthesis Finished! ==="
