# Importing some useful library
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scienceplots
from scipy.interpolate import CubicSpline
plt.style.use(['science', 'notebook', 'grid'])

# Data Extraction from the xlsx file
df = pd.read_excel("PROFILE Group 2.xlsx", sheet_name=2)
x = np.array(df["Off Axis [mm]"])
y = np.array(df["Crossline dose"])
center_idx_raw = np.argmin(np.abs(x))
y = y / y[center_idx_raw] * 100

# Sort data by x to satisfy spline requirements.
sort_idx = np.argsort(x)
x = x[sort_idx]
y = y[sort_idx]

# Build a cubic spline interpolation of the beam profile.
spline = CubicSpline(x, y)

# Dense sampling for smooth curve display and derivative analysis.
x_dense = np.linspace(x.min(), x.max(), 3000)
y_dense = spline(x_dense)
d2y_dense = spline(x_dense, 2)

# Find inflection candidates where second derivative changes sign.
sign_change_idx = np.where(np.diff(np.sign(d2y_dense)) != 0)[0]
inflection_x = []
for idx in sign_change_idx:
    x1, x2 = x_dense[idx], x_dense[idx + 1]
    y1, y2 = d2y_dense[idx], d2y_dense[idx + 1]
    if y2 != y1:
        x_root = x1 - y1 * (x2 - x1) / (y2 - y1)
        inflection_x.append(x_root)

if len(inflection_x) == 0:
    raise RuntimeError("No inflection point found in the interpolated cubic curve.")

inflection_x = np.array(inflection_x)
inflection_slope = spline(inflection_x, 1)

left_mask = inflection_x < 0
right_mask = inflection_x > 0
if not np.any(left_mask) or not np.any(right_mask):
    raise RuntimeError("Could not find inflection points on both sides of central axis.")

# Left side: steepest descent outward corresponds to largest positive dy/dx.
left_idx_local = np.argmax(inflection_slope[left_mask])
# Right side: steepest descent outward corresponds to most negative dy/dx.
right_idx_local = np.argmin(inflection_slope[right_mask])

x_inflect_left = inflection_x[left_mask][left_idx_local]
y_inflect_left = spline(x_inflect_left)
m_left = inflection_slope[left_mask][left_idx_local]

x_inflect_right = inflection_x[right_mask][right_idx_local]
y_inflect_right = spline(x_inflect_right)
m_right = inflection_slope[right_mask][right_idx_local]

# RDV for each side is dose value at inflection point.
rdv_left = y_inflect_left
rdv_right = y_inflect_right
rdv_avg = 0.5 * (rdv_left + rdv_right)

def tangent_x_at_y(x0, y0, m, y_level):
    if np.isclose(m, 0.0):
        raise RuntimeError("Tangent slope is too small for robust penumbra estimation.")
    return x0 + (y_level - y0) / m

def side_penumbra_from_rdv(x0, y0, m, rdv):
    y_upper = 1.6 * rdv
    y_lower = 0.4 * rdv
    x_upper = tangent_x_at_y(x0, y0, m, y_upper)
    x_lower = tangent_x_at_y(x0, y0, m, y_lower)
    return x_upper, x_lower, abs(x_upper - x_lower), y_upper, y_lower

xu_l, xl_l, penumbra_left, yu_l, yl_l = side_penumbra_from_rdv(x_inflect_left, y_inflect_left, m_left, rdv_avg)
xu_r, xl_r, penumbra_right, yu_r, yl_r = side_penumbra_from_rdv(x_inflect_right, y_inflect_right, m_right, rdv_avg)

def crossing_from_center(level, side):
    center_idx = np.argmin(np.abs(x_dense))
    if side == "left":
        xs = x_dense[:center_idx + 1][::-1]
        ys = y_dense[:center_idx + 1][::-1]
    else:
        xs = x_dense[center_idx:]
        ys = y_dense[center_idx:]

    for i in range(len(ys) - 1):
        y1, y2 = ys[i], ys[i + 1]
        if (y1 >= level and y2 <= level) or (y1 <= level and y2 >= level):
            if np.isclose(y2, y1):
                return xs[i]
            return xs[i] + (level - y1) * (xs[i + 1] - xs[i]) / (y2 - y1)
    raise RuntimeError(f"No crossing found for {level}% on {side} side.")

levels = [90, 75, 60]
aerb_left = {lev: crossing_from_center(lev, "left") for lev in levels}
aerb_right = {lev: crossing_from_center(lev, "right") for lev in levels}

# Field size for FFF: lateral separation between inflection points.
field_size_inflection = x_inflect_right - x_inflect_left

# Symmetry evaluated similarly to flat-beam area comparison method
# over region bounded by left/right inflection points.
left_region = (x_dense >= x_inflect_left) & (x_dense <= 0)
right_region = (x_dense >= 0) & (x_dense <= x_inflect_right)
area_left = np.trapezoid(y_dense[left_region], x_dense[left_region])
area_right = np.trapezoid(y_dense[right_region], x_dense[right_region])
symmetry = abs(area_left - area_right) / (area_left + area_right) * 100

plt.figure(figsize=(12, 7))
plt.plot(x, y, "o", alpha=0.7)
plt.plot(x_dense, y_dense, "b-", linewidth=2)

# CAX line for distance measurements.
plt.axvline(0, color="gray", linestyle="--", linewidth=1)

# Inflection points used to define the averaged RDV.
plt.plot([x_inflect_left, x_inflect_right], [y_inflect_left, y_inflect_right], "ro", markersize=7)

# Averaged RDV reference.
x_rdv_mid = 0.5 * (x_inflect_left + x_inflect_right)
plt.plot([x_inflect_left, x_inflect_right], [rdv_avg, rdv_avg], color="black", linestyle="--", linewidth=1.4)
plt.plot(x_rdv_mid, rdv_avg, "ks", markersize=7)

# Tangent lines at inflection points, clipped to RDV construction range.
plt.plot([xl_l, xu_l], [yl_l, yu_l], "r-", linewidth=2)
plt.plot([xl_r, xu_r], [yl_r, yu_r], "r-", linewidth=2)

# 1.6*RDV and 0.4*RDV points on tangents.
plt.plot([xu_l, xl_l], [yu_l, yl_l], "ms", markersize=6)
plt.plot([xu_r, xl_r], [yu_r, yl_r], "ms", markersize=6)

# AERB points (90/75/60%) on both sides.
for lev, marker in zip(levels, ["^", "v", "d"]):
    plt.plot(aerb_left[lev], lev, marker=marker, color="green", markersize=7)
    plt.plot(aerb_right[lev], lev, marker=marker, color="green", markersize=7)

# Direct annotations instead of legend.
plt.annotate("1.6RDV", xy=(xu_l, yu_l), xytext=(-45, 10), textcoords="offset points", fontsize=9, color="magenta")
plt.annotate("0.4RDV", xy=(xl_l, yl_l), xytext=(-45, -18), textcoords="offset points", fontsize=9, color="magenta")
plt.annotate("1.6RDV", xy=(xu_r, yu_r), xytext=(8, 10), textcoords="offset points", fontsize=9, color="magenta")
plt.annotate("0.4RDV", xy=(xl_r, yl_r), xytext=(8, -18), textcoords="offset points", fontsize=9, color="magenta")

# Field size indication between inflection points.
y_field = 8
plt.annotate("", xy=(x_inflect_left, y_field), xytext=(x_inflect_right, y_field), arrowprops=dict(arrowstyle="<->", color="black", lw=1.6))
plt.annotate(f"Field size = {field_size_inflection:.2f} mm", xy=(x_rdv_mid, y_field), xytext=(-55, -18), textcoords="offset points", fontsize=9)

# Penumbra region markers (left/right) shown only as RDV level points.
plt.annotate("", xy=(xu_l, yu_l), xytext=(xl_l, yl_l), arrowprops=dict(arrowstyle="<->", color="magenta", lw=1.5))
plt.annotate("", xy=(xu_r, yu_r), xytext=(xl_r, yl_r), arrowprops=dict(arrowstyle="<->", color="magenta", lw=1.5))

# AERB level region labels.
plt.annotate("90%", xy=(aerb_right[90], 90), xytext=(8, 0), textcoords="offset points", fontsize=8, color="green")
plt.annotate("75%", xy=(aerb_right[75], 75), xytext=(8, 0), textcoords="offset points", fontsize=8, color="green")
plt.annotate("60%", xy=(aerb_right[60], 60), xytext=(8, 0), textcoords="offset points", fontsize=8, color="green")

# Horizontal guides for AERB dose levels.
for lev in levels:
    plt.axhline(lev, color="green", linestyle=":", linewidth=0.8, alpha=0.4)

info_text = (
    f"Field size (IP-IP): {field_size_inflection:.2f} mm\n"
    f"Symmetry: {symmetry:.2f} %\n"
    f"90% L/R: {abs(aerb_left[90]):.2f} / {abs(aerb_right[90]):.2f} mm\n"
    f"75% L/R: {abs(aerb_left[75]):.2f} / {abs(aerb_right[75]):.2f} mm\n"
    f"60% L/R: {abs(aerb_left[60]):.2f} / {abs(aerb_right[60]):.2f} mm"
)

plt.text(
    0.015,
    0.985,
    info_text,
    transform=plt.gca().transAxes,
    va="top",
    ha="left",
    fontsize=10,
    family="DejaVu Sans",
    bbox=dict(boxstyle="round,pad=0.45", facecolor="white", alpha=0.92, edgecolor="black", linewidth=0.8),
)

plt.title("Beam Profile for 6MV FFF (20x20 cm² field)", fontsize=14)
plt.xlabel("Off Axis [mm]")
plt.ylabel("Crossline dose")
plt.savefig("Figures/Profile/6MV FFF(20 by 20)/Beam_Profile_FFF_Crossline.pdf", dpi=300, bbox_inches="tight")
plt.show()