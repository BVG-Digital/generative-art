#!/usr/bin/env python3
"""
Samila plotter — uses Samila exactly as documented, saves SVG via matplotlib.
Docs: https://github.com/sepandhaghighi/samila

Run:    python3 samila_plotter.py
Output: samila_output.svg
"""

import random, math
import matplotlib
matplotlib.use('Agg')  # non-interactive backend
import matplotlib.pyplot as plt
from samila import GenerativeImage, Projection, Marker

# ── SETTINGS ──────────────────────────────────────────────────────────────────

SEED       = 2847         # change for a different composition
STEP       = 0.01         # default from docs (smaller = more points/detail)

# Canvas: 6×4 inches
FIG_W      = 6
FIG_H      = 4

PEN_MM     = 0.5
SPOT_SIZE  = PEN_MM * 0.28   # scale spot size to physical pen diameter

# ── PROJECTION ────────────────────────────────────────────────────────────────
# Options: RECTILINEAR, POLAR, AITOFF, HAMMER, LAMBERT, MOLLWEIDE, RANDOM
PROJECTION = Projection.POLAR

# ── MATH FUNCTIONS ────────────────────────────────────────────────────────────
# From Samila docs — change these to explore styles

def f1(x, y):
    return random.uniform(-1, 1) * x**2 - math.sin(y**2) + abs(y - x)

def f2(x, y):
    return random.uniform(-1, 1) * y**3 - math.cos(x**2) + 2 * x

# ── OTHER STYLES (uncomment to try) ──────────────────────────────────────────

# -- Circular/spiral --
# def f1(x, y): return math.sin(x + math.sin(y)) * math.cos(y)
# def f2(x, y): return math.cos(x + math.sin(y)) * math.sin(x)

# -- Lissajous family --
# def f1(x, y): return math.sin(3*x + y)
# def f2(x, y): return math.sin(2*y - x)

# ─────────────────────────────────────────────────────────────────────────────

fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=300)

g = GenerativeImage(f1, f2)
g.generate(seed=SEED, step=STEP)

g.plot(
    projection=PROJECTION,
    spot_size=SPOT_SIZE,
    color="black",
    bgcolor="white",
    marker=Marker.VLINE,
)

print(f"Seed used: {g.seed}")
print(f"Points generated: {len(g.data1)}")

import os
out = os.path.expanduser("~/Documents/Plotter/generative-art/sketches/samila_output.svg")
plt.savefig(out, format="svg", bbox_inches="tight",
            facecolor="white", edgecolor="none")
plt.close()

print("Saved: " + out)
print(f"Canvas: {FIG_W}x{FIG_H} in | Pen: {PEN_MM}mm | Projection: {PROJECTION.value}")
