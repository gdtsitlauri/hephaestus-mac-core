# HEPHAESTUS Build System

RTL_DIR = src/rtl
TB_DIR = tb/cpp
OBJ_DIR = obj_dir
TARGET = hephaestus_sim

# Βρίσκει όλα τα SystemVerilog αρχεία
VSRCS = $(wildcard $(RTL_DIR)/*.sv)
CSRCS = $(TB_DIR)/main.cpp

# Παράμετροι Verilator (Προσθέσαμε το --top-module!)
VFLAGS = -Wall -Wno-DECLFILENAME -Wno-fatal --top-module systolic_array --cc --exe --build -j 4

all: run

sim:
	verilator $(VFLAGS) $(VSRCS) $(CSRCS) -o $(TARGET)

run: sim
	./$(OBJ_DIR)/$(TARGET)

clean:
	rm -rf $(OBJ_DIR)