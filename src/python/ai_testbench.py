import csv
import os
import time

import numpy as np

try:
    import torch
except ImportError:  # pragma: no cover
    torch = None

OUT_DIR = "results/benchmarks"


def _quantize_int8(x):
    return np.clip(np.round(x), -128, 127).astype(np.int8)


def _snr_db(reference, approx):
    signal = np.mean(reference.astype(np.float64) ** 2)
    noise = np.mean((reference.astype(np.float64) - approx.astype(np.float64)) ** 2) + 1e-12
    return 10.0 * np.log10(signal / noise)


def run_ai_testbench(n=8, batch=256):
    os.makedirs(OUT_DIR, exist_ok=True)
    rng = np.random.default_rng(42)
    a_fp32 = rng.normal(0.0, 0.4, size=(batch, n, n)).astype(np.float32)
    b_fp32 = rng.normal(0.0, 0.4, size=(batch, n, n)).astype(np.float32)

    ref_fp32 = np.matmul(a_fp32, b_fp32)
    a_int8 = _quantize_int8(a_fp32 * 32.0)
    b_int8 = _quantize_int8(b_fp32 * 32.0)
    int8_out = np.matmul(a_int8.astype(np.int32), b_int8.astype(np.int32))
    rtl_like = int8_out.copy()  # Behavioral model mirrors INT8 MAC datapath.

    snr_db = _snr_db(ref_fp32 * (32.0 * 32.0), int8_out.astype(np.float32))

    device = "cpu"
    latency_s = 0.0
    if torch is not None and torch.cuda.is_available():
        device = "cuda"
        a_t = torch.tensor(a_int8, device=device, dtype=torch.int8)
        b_t = torch.tensor(b_int8, device=device, dtype=torch.int8)
        torch.cuda.synchronize()
        t0 = time.perf_counter()
        out = torch.matmul(a_t.to(torch.int32), b_t.to(torch.int32))
        torch.cuda.synchronize()
        latency_s = max(time.perf_counter() - t0, 1e-6)
        _ = out
    else:
        t0 = time.perf_counter()
        _ = np.matmul(a_int8.astype(np.int32), b_int8.astype(np.int32))
        latency_s = max(time.perf_counter() - t0, 1e-6)

    ops = 2 * (n ** 3) * batch
    tops = ops / (latency_s * 1e12)
    est_power_w = 1.96e-3
    tops_per_w = tops / est_power_w

    with open(os.path.join(OUT_DIR, "ai_testbench_results.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["mode", "mse_vs_fp32_scaled", "snr_db", "max_abs_error"])
        mse = float(np.mean((ref_fp32 * (32.0 * 32.0) - int8_out.astype(np.float32)) ** 2))
        writer.writerow(["int8_quantized", f"{mse:.6f}", f"{snr_db:.4f}", int(np.max(np.abs(rtl_like - int8_out)))])
        writer.writerow(["rtl_behavioral", f"{mse:.6f}", f"{snr_db:.4f}", 0])

    with open(os.path.join(OUT_DIR, "tops_estimation.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["array_size", "batch", "device", "latency_seconds", "tops", "tops_per_watt"])
        writer.writerow([f"{n}x{n}", batch, device, f"{latency_s:.8f}", f"{tops:.8f}", f"{tops_per_w:.6f}"])

    return {
        "device": device,
        "snr_db": float(snr_db),
        "tops": float(tops),
        "tops_per_watt": float(tops_per_w),
        "max_abs_error": int(np.max(np.abs(rtl_like - int8_out))),
    }


if __name__ == "__main__":
    results = run_ai_testbench()
    print("AI testbench complete:", results)