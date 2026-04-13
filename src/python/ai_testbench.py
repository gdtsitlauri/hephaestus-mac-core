import numpy as np
import subprocess
import re
import sys

def run_software_inference():
    print("--- SOFTWARE (AI) INFERENCE ---")
    matrix_a = np.ones((4, 4), dtype=np.int8)
    matrix_b = np.ones((4, 4), dtype=np.int8)
    
    expected_output = np.dot(matrix_a, matrix_b)
    
    print("Matrix A (Activations):")
    print(matrix_a)
    print("Matrix B (Weights):")
    print(matrix_b)
    print("Expected Output (Row 1):", expected_output[0])
    return expected_output

def run_hardware_simulation():
    print("\n--- HARDWARE (SILICON) SIMULATION ---")
    process = subprocess.Popen(['./obj_dir/hephaestus_sim'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = process.communicate()
    
    if err:
        print("Error in simulation:", err)
        return None

    hw_result = []
    for line in out.split('\n'):
        print(line) 
        if "Cycle 10" in line:
            match = re.search(r'\[(.*?)\]', line)
            if match:
                numbers = match.group(1).strip().split()
                hw_result = [int(n) for n in numbers]
                
    return hw_result

def verify_results(sw_out, hw_out):
    print("\n=== VERIFICATION ===")
    sw_row = list(sw_out[0]) 
    
    print(f"AI Expected : {sw_row}")
    print(f"Silicon Out : {hw_out}")
    
    if sw_row == hw_out:
        print("✅ SUCCESS: Silicon matches AI software perfectly!")
        print("✅ Ready for CYCLOPS-RTL Optimization.")
    else:
        print("❌ FAILED: Hardware mismatch.")

if __name__ == "__main__":
    sw_result = run_software_inference()
    hw_result = run_hardware_simulation()
    
    if hw_result:
        verify_results(sw_result, hw_result)
    else:
        print("Simulation failed to produce results.")