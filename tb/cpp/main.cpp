#include <iostream>
#include <memory>
#include <verilated.h>
#include "Vsystolic_array.h"

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    
    // Δημιουργία του hardware module στη μνήμη
    auto top = std::make_unique<Vsystolic_array>();

    // 1. Reset Sequence (Καθαρίζουμε το chip)
    top->clk = 0;
    top->rst_n = 0;
    top->en = 0;
    top->eval();

    for (int i = 0; i < 5; i++) {
        top->clk = 1; top->eval();
        top->clk = 0; top->eval();
    }

    // 2. Ενεργοποίηση
    top->rst_n = 1;
    top->en = 1;
    std::cout << "=== HEPHAESTUS AI CORE INITIALIZED ===" << std::endl;
    std::cout << "Running Systolic Array Simulation..." << std::endl;

    // 3. Στέλνουμε δεδομένα για 10 κύκλους ρολογιού
    for (int cycle = 1; cycle <= 10; cycle++) {
        // Βάζουμε "άσσους" στα weights και στα activations για να δούμε τα νούμερα να αθροίζονται
        for (int r = 0; r < 4; r++) {
            top->acts_in[r] = 1;
            for (int c = 0; c < 4; c++) {
                top->weights[r][c] = 1;
            }
        }

        // Posedge (Θετική ακμή ρολογιού)
        top->clk = 1;
        top->eval();

        // Διαβάζουμε το αποτέλεσμα από το κάτω μέρος του array
        std::cout << "Cycle " << cycle << " | Output: [ ";
        for (int c = 0; c < 4; c++) {
            std::cout << top->results_out[c] << " ";
        }
        std::cout << "]" << std::endl;

        // Negedge (Αρνητική ακμή ρολογιού)
        top->clk = 0;
        top->eval();
    }

    std::cout << "=== SIMULATION COMPLETE ===" << std::endl;
    return 0;
}