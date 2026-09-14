from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

SEED = 20260910
N_SAMPLES = 128
N_PER_LEVEL = 3
LEVELS = ("low", "medium", "high")

OUT_DIR = Path("generated_dataset")
IMAGE_DATASET_DIR = OUT_DIR / "image_noise_demo"

# Experiment-compatible image structure:
# generated_dataset/image_noise_demo/low/
# generated_dataset/image_noise_demo/medium/
# generated_dataset/image_noise_demo/high/

# Fixed Y-axis ranges per domain
MACHINE_YLIM = (-1.7, 1.7)
PV_YLIM = (0.35, 1.02)

# Plot appearance
FIGSIZE = (12, 6)
DPI = 220
LINE_WIDTH = 1.8
LINE_COLOR = "#1f77b4"
GRID_COLOR = "#d3d3d3"
GRID_WIDTH = 0.8
AXIS_LABEL_SIZE = 18
TICK_LABEL_SIZE = 14


def ar1_noise(rng, n, sigma, rho=0.55):
    eps = rng.normal(0.0, sigma, n)
    x = np.zeros(n, dtype=float)
    for i in range(1, n):
        x[i] = rho * x[i - 1] + eps[i]
    return x


def gaussian_burst(t, center, width, amplitude):
    envelope = np.exp(-0.5 * ((t - center) / width) ** 2)
    carrier = np.sin(2 * np.pi * 13.0 * t)
    return amplitude * envelope * carrier


def generate_machine_signal(rng, level, n=N_SAMPLES):
    t = np.linspace(0.0, 2.0, n, endpoint=False)

    base = (
        0.85 * np.sin(2 * np.pi * 4.0 * t)
        + 0.22 * np.sin(2 * np.pi * 8.0 * t + 0.35)
    )

    params = {
        "low": {"noise_sigma": 0.035, "burst_count": 0, "burst_amp": 0.00},
        "medium": {"noise_sigma": 0.105, "burst_count": 2, "burst_amp": 0.18},
        "high": {"noise_sigma": 0.220, "burst_count": 4, "burst_amp": 0.38},
    }[level]

    signal = base + ar1_noise(rng, n, sigma=params["noise_sigma"], rho=0.45)

    if params["burst_count"] > 0:
        centers = rng.uniform(0.20, 1.80, params["burst_count"])
        widths = rng.uniform(0.025, 0.060, params["burst_count"])
        for center, width in zip(centers, widths):
            amp = params["burst_amp"] * rng.uniform(0.75, 1.15)
            signal += gaussian_burst(t, center, width, amp)

    return signal


def smooth_cloud_dip(x, center, width, depth):
    return depth * np.exp(-0.5 * ((x - center) / width) ** 2)


def generate_pv_signal(rng, level, n=N_SAMPLES):
    x = np.linspace(0.0, 1.0, n)

    clear_sky = 0.68 + 0.30 * np.sin(np.pi * (0.18 + 0.64 * x))

    params = {
        "low": {
            "n_clouds": 1,
            "depth": (0.025, 0.060),
            "width": (0.050, 0.085),
            "measurement_sigma": 0.004,
        },
        "medium": {
            "n_clouds": 3,
            "depth": (0.080, 0.170),
            "width": (0.035, 0.075),
            "measurement_sigma": 0.006,
        },
        "high": {
            "n_clouds": 6,
            "depth": (0.160, 0.340),
            "width": (0.020, 0.060),
            "measurement_sigma": 0.009,
        },
    }[level]

    attenuation = np.zeros(n, dtype=float)
    centers = rng.uniform(0.08, 0.92, params["n_clouds"])

    for center in centers:
        width = rng.uniform(*params["width"])
        depth = rng.uniform(*params["depth"])
        attenuation += smooth_cloud_dip(x, center, width, depth)

    transmittance = np.clip(1.0 - attenuation, 0.42, 1.0)
    measurement_noise = ar1_noise(rng, n, sigma=params["measurement_sigma"], rho=0.65)

    power = clear_sky * transmittance + measurement_noise
    return np.clip(power, 0.0, None)


def make_rows(generator, prefix, rng):
    rows = []
    sample_columns = [f"s{i:03d}" for i in range(N_SAMPLES)]

    for level in LEVELS:
        for repetition in range(1, N_PER_LEVEL + 1):
            values = generator(rng, level)
            row = {"id": f"{prefix}_{level}_{repetition:02d}"}
            row.update({col: float(val) for col, val in zip(sample_columns, values)})
            row["class"] = level
            rows.append(row)

    return pd.DataFrame(rows)


def save_csvs(machine_df, pv_df):
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    machine_path = OUT_DIR / "machine_vibration.csv"
    pv_path = OUT_DIR / "pv_power.csv"
    combined_path = OUT_DIR / "time_series_noise_demo.csv"

    machine_df.to_csv(machine_path, index=False, encoding="utf-8")
    pv_df.to_csv(pv_path, index=False, encoding="utf-8")
    pd.concat([machine_df, pv_df], ignore_index=True).to_csv(
        combined_path, index=False, encoding="utf-8"
    )
    return machine_path, pv_path, combined_path


def render_domain_plots(df, domain_name, ylabel, y_limits):
    """
    Render plots directly into the ImageDataset-compatible class folders:

        generated_dataset/image_noise_demo/
            low/
            medium/
            high/

    Machine and PV images belonging to the same class are stored together,
    exactly as required by the experiment's ImageDataset structure.
    """
    sample_columns = [c for c in df.columns if c.startswith("s")]
    records = []

    for _, row in df.iterrows():
        stimulus_id = row["id"]
        label = str(row["class"]).lower()

        if label not in LEVELS:
            raise ValueError(
                f"Unexpected class {label!r} for stimulus {stimulus_id}"
            )

        class_dir = IMAGE_DATASET_DIR / label
        class_dir.mkdir(parents=True, exist_ok=True)

        x = np.arange(len(sample_columns))
        y = row[sample_columns].astype(float).to_numpy()

        fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)
        ax.plot(x, y, linewidth=LINE_WIDTH, color=LINE_COLOR)

        # No title: clean experimental stimulus.
        ax.set_xlabel("Sample index", fontsize=AXIS_LABEL_SIZE)
        ax.set_ylabel(ylabel, fontsize=AXIS_LABEL_SIZE)
        ax.tick_params(axis="both", labelsize=TICK_LABEL_SIZE)
        ax.grid(True, color=GRID_COLOR, linewidth=GRID_WIDTH)

        ax.set_xlim(0, len(sample_columns) - 1)
        ax.set_ylim(y_limits[0], y_limits[1])

        out_path = class_dir / f"{stimulus_id}.png"
        fig.tight_layout()
        fig.savefig(out_path, facecolor="white")
        plt.close(fig)

        records.append({
            "stimulus_id": stimulus_id,
            "domain": domain_name,
            "class": label,
            "image_path": str(out_path),
            "y_min": y_limits[0],
            "y_max": y_limits[1],
        })

    return pd.DataFrame(records)



def generate_plots(machine_df, pv_df):
    machine_index = render_domain_plots(
        machine_df,
        domain_name="machine",
        ylabel="Vibration amplitude",
        y_limits=MACHINE_YLIM,
    )

    pv_index = render_domain_plots(
        pv_df,
        domain_name="pv",
        ylabel="Power output",
        y_limits=PV_YLIM,
    )

    index_df = pd.concat([machine_index, pv_index], ignore_index=True)
    index_path = OUT_DIR / "plots_index.csv"
    index_df.to_csv(index_path, index=False, encoding="utf-8")
    return index_path


def main():
    rng = np.random.default_rng(SEED)

    machine_df = make_rows(generate_machine_signal, "machine", rng)
    pv_df = make_rows(generate_pv_signal, "pv", rng)

    save_csvs(machine_df, pv_df)
    index_path = generate_plots(machine_df, pv_df)

    print("Generated files in:", OUT_DIR.resolve())
    print("Plots index:", index_path)
    print("Machine Y limits:", MACHINE_YLIM)
    print("PV Y limits:", PV_YLIM)
    print("ImageDataset-compatible images saved in:", IMAGE_DATASET_DIR.resolve())


if __name__ == "__main__":
    main()
