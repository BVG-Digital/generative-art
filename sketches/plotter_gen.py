#!/usr/bin/env python3
import math, random, os

PEN_MM       = 0.5
SEED         = 42
WIDTH_MM     = 152.4
HEIGHT_MM    = 101.6
MARGIN_MM    = 6.0
FIELD_SCALE  = 0.022
LINE_STEPS   = 120
STEP_MM      = 0.8
NUM_SEEDS    = 600
MIN_LINE_GAP = PEN_MM * 1.8
STROKE_WIDTH = PEN_MM

def field_angle(x, y):
    sx, sy = x * FIELD_SCALE, y * FIELD_SCALE
    return (math.sin(sx + math.sin(sy * 0.8) * 2.1) +
            math.cos(sy * 1.2 + math.sin(sx * 0.6) * 1.7) * 0.7) * math.pi

def trace_line(sx, sy):
    pts = [(sx, sy)]
    x, y = sx, sy
    for _ in range(LINE_STEPS):
        angle = field_angle(x, y)
        x += math.cos(angle) * STEP_MM
        y += math.sin(angle) * STEP_MM
        if not (MARGIN_MM < x < WIDTH_MM - MARGIN_MM and MARGIN_MM < y < HEIGHT_MM - MARGIN_MM):
            break
        pts.append((x, y))
    return pts

def pt_seg_dist(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    if dx == dy == 0:
        return math.hypot(px - ax, py - ay)
    t = max(0, min(1, ((px-ax)*dx + (py-ay)*dy) / (dx*dx + dy*dy)))
    return math.hypot(px - (ax + t*dx), py - (ay + t*dy))

def too_close(new_pts, existing, gap):
    for line in existing:
        for i in range(0, len(line) - 1, 4):
            for px, py in new_pts[::4]:
                if pt_seg_dist(px, py, line[i][0], line[i][1], line[i+1][0], line[i+1][1]) < gap:
                    return True
    return False

def generate():
    random.seed(SEED)
    seeds = [
        (random.uniform(MARGIN_MM, WIDTH_MM - MARGIN_MM),
         random.uniform(MARGIN_MM, HEIGHT_MM - MARGIN_MM))
        for _ in range(NUM_SEEDS)
    ]
    lines = []
    for sx, sy in seeds:
        pts = trace_line(sx, sy)
        if len(pts) >= 4 and not too_close(pts, lines, MIN_LINE_GAP):
            lines.append(pts)
    print("Generated " + str(len(lines)) + " lines from " + str(NUM_SEEDS) + " seeds.")

    paths = []
    for pts in lines:
        d = "M " + str(round(pts[0][0], 3)) + "," + str(round(pts[0][1], 3))
        for x, y in pts[1:]:
            d += " L " + str(round(x, 3)) + "," + str(round(y, 3))
        paths.append('  <path d="' + d + '" stroke="black" stroke-width="' +
                     str(STROKE_WIDTH) + '" fill="none" stroke-linecap="round"/>')

    comment = "<!-- Pen:" + str(PEN_MM) + "mm Seed:" + str(SEED) + " Lines:" + str(len(lines)) + " -->"
    svg_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<svg xmlns="http://www.w3.org/2000/svg"',
        '     width="' + str(WIDTH_MM) + 'mm" height="' + str(HEIGHT_MM) + 'mm"',
        '     viewBox="0 0 ' + str(WIDTH_MM) + ' ' + str(HEIGHT_MM) + '">',
        '  ' + comment,
        '  <rect x="0" y="0" width="' + str(WIDTH_MM) + '" height="' + str(HEIGHT_MM) + '" fill="white"/>',
    ] + paths + ['</svg>']

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.svg")
    with open(out, "w") as f:
        f.write("\n".join(svg_lines))
    print("Saved: " + out)

if __name__ == "__main__":
    generate()
