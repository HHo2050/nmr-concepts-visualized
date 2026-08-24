"""
Nyquist car wheel GIF v4
- Wheel rotates COUNTER-CLOCKWISE (negative angle) = physically correct for forward motion
- Phase badge: green "NYQUIST: TRUE" vs red "NYQUIST: ALIASED" bottom-left corner
- Phase A alias angle: -20 deg/frame (CCW = forward)
- Phase B alias angle: +8 to +14 deg/frame (CW = backward illusion)
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import Circle, Polygon, FancyBboxPatch
from PIL import Image

W, H = 1200, 675
dpi = 100

SKY_TOP    = np.array([55, 100, 175])
SKY_BOTTOM = np.array([255, 195, 130])
ROAD_COLOR = "#3A3F4A"
ROAD_LINE  = "#F4E9D8"
CAR_BODY      = "#FF6B6B"
CAR_BODY_DARK = "#D44040"
WINDOW_COLOR  = "#CCEEFF"
TIRE_COLOR    = "#1A1C22"
RIM_COLOR     = "#E8E2D0"
SPOKE_COLOR   = "#8A8370"

def make_sky(w, h):
    grad = np.linspace(0, 1, h)[:, None]
    sky = (SKY_TOP[None,None,:] * (1-grad[:,:,None]) +
           SKY_BOTTOM[None,None,:] * grad[:,:,None])
    return np.repeat(sky, w, axis=1).astype(np.uint8)

plt.rcParams["font.family"] = "DejaVu Sans"
fig, ax = plt.subplots(figsize=(W/dpi, H/dpi), dpi=dpi)
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
ax.imshow(make_sky(W, H), extent=[0,W,0,H], zorder=0, aspect="auto")

# sun
ax.add_patch(Circle((960,510), 52, facecolor="#FFE070", edgecolor="none", alpha=0.95, zorder=1))
ax.add_patch(Circle((960,510), 76, facecolor="#FFE8A0", edgecolor="none", alpha=0.30, zorder=1))

# hills
hx = np.linspace(0, W, 300)
hy = 200 + 22*np.sin(hx/130) + 12*np.sin(hx/60+1.2)
ax.fill_between(hx, hy, 0, color="#6E8F6B", alpha=0.55, zorder=1)

road_top = 200
ax.add_patch(plt.Rectangle((0,0), W, road_top, facecolor=ROAD_COLOR, zorder=2))

# trees
def draw_tree(ax, tx, ty, scale=1.0):
    tw, th = 14*scale, 55*scale
    ax.add_patch(plt.Rectangle((tx-tw/2, ty), tw, th,
                                facecolor="#6B4226", edgecolor="#4A2E17", linewidth=1.5, zorder=3))
    for oy, r, col in [(th*0.55,52*scale,"#2E7D32"),
                        (th*0.80,42*scale,"#388E3C"),
                        (th*1.00,35*scale,"#43A047")]:
        ax.add_patch(Circle((tx, ty+oy), r, facecolor=col,
                             edgecolor="#1B5E20", linewidth=1.2, zorder=4))

draw_tree(ax, 870, road_top, 1.05)
draw_tree(ax, 1060, road_top, 0.78)
draw_tree(ax, 130, road_top+3, 0.65)

# car
CX = 540
CY = road_top + 62
body_pts = np.array([
    [CX-195,CY-5],[CX-195,CY+28],[CX-155,CY+60],[CX-55,CY+78],
    [CX+82,CY+78],[CX+152,CY+54],[CX+198,CY+28],[CX+198,CY-5],
])
ax.add_patch(Polygon(body_pts, closed=True, facecolor=CAR_BODY,
                      edgecolor=CAR_BODY_DARK, linewidth=2.8, zorder=5, joinstyle="round"))
win_pts = np.array([
    [CX-115,CY+63],[CX-72,CY+90],[CX+58,CY+90],[CX+98,CY+63],
])
ax.add_patch(Polygon(win_pts, closed=True, facecolor=WINDOW_COLOR,
                      edgecolor=CAR_BODY_DARK, linewidth=1.8, zorder=6, joinstyle="round"))
ax.plot([CX-9,CX-5],[CY+63,CY+90], color=CAR_BODY_DARK, lw=2, zorder=6)
ax.add_patch(Circle((CX+190,CY+12), 9, facecolor="#FFF3D0",
                     edgecolor=CAR_BODY_DARK, linewidth=1.2, zorder=6))

# ── captions — TOP of frame ───────────────────────────────────────────────────
# y=H is the very top pixel; subtract to go down from top
cap_main_y = H - 55    # 55px from top
cap_sub_y  = H - 105   # 105px from top (50px gap)

caption_txt = ax.text(W/2, cap_main_y, "", color="white",
                       fontsize=26, fontweight="bold", ha="center", va="center", zorder=21,
                       path_effects=[pe.Stroke(linewidth=8, foreground="#1a1a2e"), pe.Normal()])
sub_txt = ax.text(W/2, cap_sub_y, "", color="#FFE08A",
                   fontsize=16, ha="center", va="center", zorder=21,
                   path_effects=[pe.Stroke(linewidth=5, foreground="#1a1a2e"), pe.Normal()])

# ── phase badge — bottom left ─────────────────────────────────────────────────
# We'll draw this dynamically each frame (it's part of dynamic elements)
# Store placeholder texts so we can remove/redraw
badge_bg   = ax.add_patch(FancyBboxPatch((14, 12), 370, 70,
                            boxstyle="round,pad=6", linewidth=2.5,
                            facecolor="#00000000", edgecolor="#00000000", zorder=25))
badge_dot  = ax.add_patch(Circle((42, 50), 11, facecolor="#00000000",
                                  edgecolor="none", zorder=26))
badge_txt  = ax.text(62, 56, "", color="white", fontsize=16, fontweight="bold",
                      va="center", ha="left", zorder=27,
                      path_effects=[pe.Stroke(linewidth=4, foreground="#000000AA"), pe.Normal()])
badge_sub  = ax.text(62, 32, "", color="#CCCCCC", fontsize=11,
                      va="center", ha="left", zorder=27,
                      path_effects=[pe.Stroke(linewidth=3, foreground="#000000AA"), pe.Normal()])

static_patch_count = len(ax.patches)
static_line_count  = len(ax.lines)

# ── wheel ─────────────────────────────────────────────────────────────────────
wheel_y       = road_top
rear_wheel_x  = CX - 122
front_wheel_x = CX + 128
R_TIRE = 47; R_RIM = 34; N_SPK = 6

def draw_wheel(ax, cx, cy, angle_deg, big=True):
    rt = R_TIRE * (1.0 if big else 0.87)
    rr = R_RIM  * (1.0 if big else 0.87)
    ax.add_patch(Circle((cx,cy), rt, facecolor=TIRE_COLOR, edgecolor="#0A0B0D", linewidth=2.2, zorder=7))
    ax.add_patch(Circle((cx,cy), rr, facecolor=RIM_COLOR,  edgecolor="#B7AF98", linewidth=1.5, zorder=8))
    th0 = np.deg2rad(angle_deg)
    for k in range(N_SPK):
        a = th0 + k*2*np.pi/N_SPK
        ax.plot([cx, cx+rr*0.88*np.cos(a)], [cy, cy+rr*0.88*np.sin(a)],
                 color=SPOKE_COLOR, lw=3.5, alpha=0.92, solid_capstyle="round", zorder=9)
    ax.add_patch(Circle((cx,cy), rr*0.22, facecolor="#3A3630", edgecolor="none", zorder=9))
    hx = cx + rr*0.96*np.cos(th0)
    hy = cy + rr*0.96*np.sin(th0)
    ax.add_patch(Circle((hx,hy), rr*0.10, facecolor="#FF5555", edgecolor="none", zorder=10))

n_dashes = 20; dash_w = 55

# ══════════════════════════════════════════════════════════════════════════════
# PHASE PHYSICS
# ══════════════════════════════════════════════════════════════════════════════
# A wheel rolling forward (left→right) rotates CLOCKWISE when viewed from
# the right side — i.e. the top moves to the right.
# In matplotlib (y-up), clockwise = DECREASING angle (negative delta).
#
# Phase A (TRUE):
#   displayed_delta = -20 deg/frame  → clockwise = forward ✓
#
# Phase B (ALIASED):
#   true rotation = -52 deg/frame (clockwise, fast forward)
#   spoke period  = 60 deg  →  alias = -52 - (-60) = +8 deg/frame
#   displayed_delta = +8 to +14 deg/frame  → CCW = appears to go BACKWARD ✓
# ══════════════════════════════════════════════════════════════════════════════

FPS = 10
frames_A     = int(7.0 * FPS)
frames_pause = int(3.0 * FPS)
frames_B     = int(9.0 * FPS)
frames_end   = int(3.0 * FPS)

deg_A = -20.0   # clockwise (forward)

t_B = np.linspace(0, 1, frames_B)
deg_B_true  = -52.0 + 6.0*t_B         # -52 → -46 (still fast CW)
spoke_period = -(360.0 / N_SPK)        # -60
# alias = true - round(true/period)*period
deg_B_alias = deg_B_true - np.round(deg_B_true / spoke_period) * spoke_period
# At -52: alias = -52 - (-60) = +8  (CCW = backward)  ✓
# At -46: alias = -46 - (-60) = +14 (CCW = more backward) ✓

# Section: (wheel_angle, road_pos, cap, sub, phase)
#   phase: 'A' | 'pause' | 'B' | 'end'
Section = []
road_pos    = 0.0
wheel_angle = 90.0   # start at top (spoke pointing up looks natural)

# Phase A
for i in range(frames_A):
    wheel_angle += deg_A
    road_pos    += abs(deg_A)
    frac = i / frames_A
    if frac < 0.50:
        cap, sub = "The wheel spins forward", ""
    else:
        cap, sub = "Watch what happens at higher speed...", ""
    Section.append((wheel_angle, road_pos, cap, sub, 'A'))

# Pause
for i in range(frames_pause):
    wheel_angle += deg_A
    road_pos    += abs(deg_A)
    frac = i / frames_pause
    if frac < 0.22:
        cap, sub = "", ""
    else:
        cap, sub = "Same wheel. Same road. Much faster.", ""
    Section.append((wheel_angle, road_pos, cap, sub, 'pause'))

# Phase B
for i in range(frames_B):
    wheel_angle += deg_B_alias[i]       # displayed: goes backward (CCW)
    road_pos    += abs(deg_B_true[i])   # road: still moves forward
    frac = i / frames_B
    if frac < 0.45:
        cap, sub = "It appears to go BACKWARD", ""
    else:
        cap, sub = "This is aliasing.", ""
    Section.append((wheel_angle, road_pos, cap, sub, 'B'))

# End
for i in range(frames_end):
    wheel_angle += deg_B_alias[-1]
    road_pos    += abs(deg_B_true[-1])
    frac = i / frames_end
    if frac < 0.55:
        cap, sub = "Same math as last week's NMR aliasing post", ""
    else:
        cap, sub = "Same math as last week's NMR aliasing post", ""
    Section.append((wheel_angle, road_pos, cap, sub, 'end'))

# ── render ────────────────────────────────────────────────────────────────────
frames_out = []

for (angle, rp, cap, sub, phase) in Section:
    while len(ax.patches) > static_patch_count:
        ax.patches[-1].remove()
    while len(ax.lines) > static_line_count:
        ax.lines[-1].remove()

    # road dashes
    dash_offset = rp * 0.55 % dash_w
    for d in range(n_dashes + 2):
        x0 = d*dash_w - dash_offset - dash_w
        ax.plot([x0, x0+dash_w*0.55], [road_top*0.42, road_top*0.42],
                 color=ROAD_LINE, lw=4, alpha=0.85, zorder=3, solid_capstyle="butt")

    draw_wheel(ax, rear_wheel_x,  wheel_y, angle, big=True)
    draw_wheel(ax, front_wheel_x, wheel_y, angle, big=False)

    # ── phase badge — update static objects only, never add_patch ───────────
    if phase == 'A':
        bg_color  = "#1B4332"
        bd_color  = "#52B788"
        dot_color = "#52B788"
        b_label   = "NYQUIST: TRUE"
        b_sub     = "Camera samples correctly"
    elif phase in ('B', 'end'):
        bg_color  = "#6B1010"
        bd_color  = "#FF6B6B"
        dot_color = "#FF6B6B"
        b_label   = "NYQUIST: ALIASED"
        b_sub     = "Frame rate too slow"
    else:
        bg_color  = "#1a1a2e"
        bd_color  = "#666688"
        dot_color = "#888888"
        b_label   = "Changing speed..."
        b_sub     = ""

    badge_bg.set_facecolor(bg_color)
    badge_bg.set_edgecolor(bd_color)
    badge_bg.set_alpha(0.88)
    badge_dot.set_facecolor(dot_color)
    badge_txt.set_text(b_label)
    badge_sub.set_text(b_sub)

    caption_txt.set_text(cap)
    sub_txt.set_text(sub)

    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())
    frames_out.append(Image.fromarray(buf, "RGBA").convert("RGB"))

out_path = r"C:\Users\Sara Tel\desktop\nyquist_2_wheel_post_2\nyquist_wheel.gif"
frames_out[0].save(out_path, save_all=True, append_images=frames_out[1:],
                   duration=55, loop=0, optimize=False)
print(f"Done — {len(frames_out)} frames, ~{len(frames_out)*55/1000:.0f}s")
