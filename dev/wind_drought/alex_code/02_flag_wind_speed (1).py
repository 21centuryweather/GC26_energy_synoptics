"""
Script 2 — Categorise Daily Wind Speed & Write Per-Category NetCDFs
=====================================================================
Reads the wind speed files produced by Script 1 and writes one NetCDF
per wind speed category per year. Each file contains the actual wind
speed where that category is active, and NaN everywhere else.

This means Script 3 (cc3d) can:
  - Track any category by loading its masked file
  - Compute mean/max wind speed of each event directly from the values

Categories:
  Category | Label    | Speed range (m/s)
  ---------|----------|-------------------
     0     | none     |  0.0 – 3.5
     1     | low      |  3.5 – 6.5
     2     | medium   |  6.5 – 12.0
     3     | rated    | 12.0 – 23.0
     4     | cut_out  | > 23.0

Output per year, per category:
  barra_wind_cat0_none_{year}.nc
  barra_wind_cat1_low_{year}.nc
  barra_wind_cat2_medium_{year}.nc
  barra_wind_cat3_rated_{year}.nc
  barra_wind_cat4_cut_out_{year}.nc

Variable in each file: wind_speed_masked (m/s, NaN outside category)
"""

import os
import numpy as np
import xarray as xr

# ------------------------------------------------------------------ #
#  USER SETTINGS
# ------------------------------------------------------------------ #

WIND_SPEED_DIR   = "/g/data/w42/ad1803/Wind_blobs/Data/WindSpeed/"
WIND_SPEED_FNAME = "barra_wind_speed_{year}.nc"

OUTPUT_DIR   = "/g/data/w42/ad1803/Wind_blobs/Data/Daily_flags/"
OUTPUT_FNAME = "barra_wind_cat{cat_id}_{label}_{year}.nc"

YEAR_START = 1979
YEAR_END   = 2024

SKIP_EXISTING = True   # set False to overwrite existing files

# Category definitions — (lower_edge_inclusive, upper_edge_exclusive)
CATEGORIES = [
    (0,  "none",    0.0,   3.5),
    (1,  "low",     3.5,   6.5),
    (2,  "medium",  6.5,  12.0),
    (3,  "rated",  12.0,  23.0),
    (4,  "cut_out", 23.0, np.inf),
]


# ------------------------------------------------------------------ #
#  HELPERS
# ------------------------------------------------------------------ #

def make_category_mask(ws, lo, hi):
    """
    Return a boolean mask where ws falls in [lo, hi).
    cut_out is open-ended (hi = inf).
    """
    if np.isinf(hi):
        return ws >= lo
    return (ws >= lo) & (ws < hi)


def print_category_summary(ws, year):
    total = ws.size
    print(f"\n  Category distribution for {year}:")
    for cat_id, label, lo, hi in CATEGORIES:
        mask  = make_category_mask(ws, lo, hi)
        count = int(mask.sum())
        pct   = 100.0 * count / total
        hi_str = f"{hi:.1f}" if not np.isinf(hi) else "  ∞"
        print(f"    {cat_id} ({label:8s}) [{lo:5.1f} – {hi_str}  m/s] : "
              f"{count:>12,d}  ({pct:5.1f}%)")


# ------------------------------------------------------------------ #
#  MAIN LOOP
# ------------------------------------------------------------------ #

os.makedirs(OUTPUT_DIR, exist_ok=True)

for year in range(YEAR_START, YEAR_END + 1):

    in_path = os.path.join(WIND_SPEED_DIR, WIND_SPEED_FNAME.format(year=year))

    if not os.path.exists(in_path):
        print(f"{year}: WARNING — wind speed file not found: {in_path}")
        continue

    # Check if all category outputs already exist
    all_exist = all(
        os.path.exists(os.path.join(
            OUTPUT_DIR,
            OUTPUT_FNAME.format(cat_id=cat_id, label=label, year=year)
        ))
        for cat_id, label, *_ in CATEGORIES
    )
    if SKIP_EXISTING and all_exist:
        print(f"{year}: skipping — all category outputs already exist.")
        continue

    print(f"\n{'='*55}\n  {year}\n{'='*55}")

    ds = xr.open_dataset(in_path)
    ws = ds["wind_speed"].values   # (time, lat, lon), float32/64

    print_category_summary(ws, year)

    for cat_id, label, lo, hi in CATEGORIES:

        out_path = os.path.join(
            OUTPUT_DIR,
            OUTPUT_FNAME.format(cat_id=cat_id, label=label, year=year)
        )

        if SKIP_EXISTING and os.path.exists(out_path):
            print(f"  cat{cat_id} ({label}): skipping — already exists.")
            continue

        # Mask: wind speed where in category, NaN elsewhere
        cat_mask = make_category_mask(ws, lo, hi)
        ws_masked = np.where(cat_mask, ws, np.nan).astype(np.float32)

        hi_str = f"{hi:.1f}" if not np.isinf(hi) else "∞"

        masked_da = xr.DataArray(
            ws_masked,
            coords=ds["wind_speed"].coords,
            dims=ds["wind_speed"].dims,
            name="wind_speed_masked",
            attrs={
                "long_name":       f"Wind speed — category {cat_id} ({label})",
                "units":           "m s-1",
                "category_id":     cat_id,
                "category_label":  label,
                "speed_range_ms":  f"{lo}–{hi_str}",
                "description":     (
                    f"Wind speed values where speed falls in [{lo}, {hi_str}) m/s. "
                    f"NaN outside this category. Use np.isfinite() to binarise for cc3d."
                ),
            },
        )

        ds_out = masked_da.to_dataset()
        ds_out.attrs = ds.attrs.copy()
        ds_out.attrs["wind_category"]   = f"{cat_id} — {label}"
        ds_out.attrs["speed_range_ms"]  = f"{lo}–{hi_str}"
        ds_out.attrs["history"] = (
            ds.attrs.get("history", "") +
            f"; masked to category {cat_id} ({label}: {lo}–{hi_str} m/s)"
        )

        ds_out.to_netcdf(
            out_path,
            encoding={"wind_speed_masked": {
                "dtype": "float32", "zlib": True, "complevel": 4,
                "_FillValue": np.float32(np.nan),
            }},
        )
        print(f"  cat{cat_id} ({label:8s}) → {os.path.basename(out_path)}")

    ds.close()

print("\nAll years complete.")
