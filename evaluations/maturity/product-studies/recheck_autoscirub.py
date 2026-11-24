"""Offline numerical check of two selected AutoSciRub reports. See archive-checks.md."""

import argparse
import ast
import hashlib
import json
import math
import re
from pathlib import Path
from statistics import fmean


FILES = {
    "astro/DESI_EDE_Repro_Data.txt": "6a72c1d974b8d5c332f81c4c6f20b3976da6de762122a88c25ae59adc4fde620",
    "phys/MATBG Superfluid Stiffness Core Dataset.txt": "25b06e1ade20e5f15b0f4aa96eae63f2f297c2e8e73dca4f52ce3e2f65b88858",
    "astro/outputs/distance_chi2.json": "6897a17bb9e3b208b4579ffb913e56623a57f536b91fb97a5c18d9b97184bcc3",
}


def distances(z, params):
    """Return D_V/r_d, F_AP and luminosity distance under the report's proxy."""
    h0, omega, w0, wa = params

    def expansion(t):
        dark_energy = (1 + t) ** (3 * (1 + w0 + wa)) * math.exp(-3 * wa * t / (1 + t))
        return math.sqrt(omega * (1 + t) ** 3 + (1 - omega) * dark_energy)

    # Composite Simpson integration of 1/E(z), independent of the archived integrator.
    n = 512
    terms = ((4 if j % 2 else 2) / expansion(j * z / n) for j in range(1, n))
    d = z / (3 * n) * (1 + 1 / expansion(z) + sum(terms))
    rd = 147 * (0.1431 / (omega * (h0 / 100) ** 2)) ** 0.25
    dv = 299792.458 / h0 * (z * d**2 / expansion(z)) ** (1 / 3)
    return dv / rd, d * expansion(z), (1 + z) * 299792.458 / h0 * d


def astronomy(raw):
    # The input uses Python literals. Decode values without executing the input.
    arrays = {}
    for node in ast.parse(raw).body:
        if not (isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name)):
            raise ValueError("Expected a named literal in the astronomy data")
        arrays[node.targets[0].id] = ast.literal_eval(node.value)

    fiducial = (67.4, 0.315, -1.0, 0.0)
    results = {}
    for model in ("lcdm", "ede", "w0wa"):
        p = arrays[model + "_params"]
        params = (p["H0"][0], p["omega_m"][0], p.get("w0", (-1,))[0], p.get("wa", (0,))[0])
        parts = {}
        for i, (label, key) in enumerate((("dvrd", "desi_dvrd_points"), ("fap", "desi_fap_points"), ("sne_mu", "sne_mu_points"))):
            squared_errors = []
            for z, observed, sigma in arrays[key]:
                ratio = distances(z, params)[i] / distances(z, fiducial)[i]
                predicted = ratio - 1 if i < 2 else 5 * math.log10(ratio)
                squared_errors.append(((observed - predicted) / sigma) ** 2)
            parts[label] = sum(squared_errors)
        results[model] = {**parts, "total": sum(parts.values())}
    return results


def line_fit(x, y):
    """Ordinary least squares with an intercept, evaluated on the fitted points."""
    pairs = list(zip(x, y, strict=True))
    mx, my = fmean(x), fmean(y)
    slope = sum((t - mx) * (v - my) for t, v in pairs) / sum((t - mx) ** 2 for t in x)
    intercept = my - slope * mx
    sse = sum((v - intercept - slope * t) ** 2 for t, v in pairs)
    return {"intercept": intercept, "slope": slope, "rmse": math.sqrt(sse / len(y)),
            "r_squared": 1 - sse / sum((v - my) ** 2 for v in y)}


def physics(raw):
    arrays = {name: [float(x) for x in values.split()] for name, values in
              re.findall(r"^\*\*([^\n]+):\*\*\s*\[([^\]]+)\]", raw.decode(), re.M)}
    density = {}
    for branch in ("Hole-doped (D_s_exp_hole)", "Electron-doped (D_s_exp_electron)"):
        y = arrays["Experimental Superfluid Stiffness " + branch]
        density[branch] = {}
        for ref in ("Conventional Superfluid Stiffness (D_s_conv)", "Quantum Geometric Superfluid Stiffness (D_s_geom)"):
            x = arrays[ref]
            pairs = list(zip(x, y, strict=True))
            ratios = [v / t for t, v in pairs]
            scale = sum(t * v for t, v in pairs) / sum(t * t for t in x)
            density[branch][ref] = {"min": min(ratios), "mean": fmean(ratios), "max": max(ratios),
                                    "scaled_rmse": math.sqrt(fmean((v - scale * t) ** 2 for t, v in pairs))}

    observations = arrays["Experimental Data with Noise (D_s_experimental)"]
    axis = arrays["Temperature Array (T in K)"]
    # The 110 observations have no matching 110-point temperature column. This
    # is the report's assumed equally spaced grid, not measured coordinates.
    temp = [min(axis) + (max(axis) - min(axis)) * i / (len(observations) - 1) for i in range(len(observations))]
    low = [t for t in temp if t < 0.6]
    y = observations[:len(low)]

    def profile(exponent):
        return line_fit([t**exponent for t in low], y)

    # Eliminate D0 and the amplitude by linear least squares at each exponent.
    lo, hi = 0.2, 3.0
    for _ in range(75):
        left, right = (2 * lo + hi) / 3, (lo + 2 * hi) / 3
        if profile(left)["rmse"] < profile(right)["rmse"]:
            hi = right
        else:
            lo = left
    exponent = (lo + hi) / 2
    current = arrays["Microwave Current Amplitude (I_mw_amplitude in nA)"]
    response = arrays["Experimental Microwave Data (D_s_mw_exp)"]
    return {"density": density, "temperature_fit": {"points": len(low), "exponent": exponent, **profile(exponent)},
            "bcs_equals_n2": arrays["BCS Model Data (D_s_bcs)"] == arrays["Power Law n=2.0 Data (D_s_power_n2)"],
            "microwave_I_squared": line_fit([i * i for i in current], response), "microwave_I": line_fit(current, response)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", required=True, type=Path, help="Local root with the three files listed in archive-checks.md")
    root = parser.parse_args().data_root
    data = {}
    for name, digest in FILES.items():
        data[name] = (root / name).read_bytes()
        if hashlib.sha256(data[name]).hexdigest() != digest:
            raise ValueError(f"SHA-256 mismatch: {name}")
    astro = astronomy(data["astro/DESI_EDE_Repro_Data.txt"])
    phys = physics(data["phys/MATBG Superfluid Stiffness Core Dataset.txt"])
    print(json.dumps({"astronomy_chi2": astro, "physics": phys}, indent=2))

    # Only now compare with the archived reference values. The tolerance for
    # the published JSON allows for the different numerical integration rule.
    archived = json.loads(data["astro/outputs/distance_chi2.json"])
    for model, components in astro.items():
        for name, value in components.items():
            if abs(value - archived[name][model]) > 1e-6:
                raise ValueError(f"Mismatch in {model} {name}: {value} vs {archived[name][model]}")
    conventional = "Conventional Superfluid Stiffness (D_s_conv)"
    for branch, expected in (("Hole-doped (D_s_exp_hole)", 55.3), ("Electron-doped (D_s_exp_electron)", 52.5)):
        if round(phys["density"][branch][conventional]["mean"], 1) != expected:
            raise ValueError(f"Mean density enhancement differs from the report for {branch}")
    if round(phys["temperature_fit"]["exponent"], 3) != 0.795 or round(phys["microwave_I_squared"]["r_squared"], 3) != 0.994:
        raise ValueError("Temperature exponent or microwave R² differs from the report at its stated precision")


if __name__ == "__main__":
    main()
