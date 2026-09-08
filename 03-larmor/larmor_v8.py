"""
Larmor Precession NMR — v8
Changes from v7c:
  - Duration cut to 25 s (FID decays by t~8s; nothing new after ~20s)
  - Title: version removed
  - Disclaimer line: split into 2 readable lines, larger font (10 → 11)
  - 3D watermark text (dM/dt, rotating frame): font 10/9 → 13/11, bold
  - Phase timings recompressed to fit 25 s
  - All 5 physics fixes from v7 preserved
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.animation import FFMpegWriter
from mpl_toolkits.mplot3d import Axes3D
from scipy.io import wavfile
import subprocess, os

# ══════════════════════════════════════════════════
#  CONSTANTS
# ══════════════════════════════════════════════════
FPS           = 30
DURATION      = 25                    # ← shortened to 25 s
N_FRAMES      = FPS * DURATION        # 750

GAMMA_H       = 267.522e6
B0            = 9.4
T1            = 1.5
T2            = 0.8

PULSE_FRAME   = 180
PULSE_RAMP    = 30
t_pulse       = PULSE_RAMP / FPS
B1_AMP        = (np.pi/2) / (GAMMA_H * t_pulse)
T1_PULSE      = 1e8
T2_PULSE      = 1e8

DELTA_F       = 4.2
OMEGA_VIS     = 0.040
TRAIL_LEN     = 450
THETA_CONCEPT = np.radians(22)
N_SMOOTH      = 10

# ══════════════════════════════════════════════════
#  COLOURS
# ══════════════════════════════════════════════════
BG       = '#0a0f1e'
C_M      = '#FFD700'
C_B0     = '#00FFB3'
C_B1     = '#FF4FD8'
C_TAU    = '#C87FFF'
C_FID    = '#FF6B35'
C_SPEC   = '#00E5FF'
C_LOREN  = '#FF2D6F'
C_TRAIL  = '#9966FF'
C_TEXT   = '#f0f0f8'
C_DIM    = '#8899b8'
C_PULSE  = '#FFE566'
C_MXY    = '#7BFFB0'
C_AX     = '#0d1428'

# ══════════════════════════════════════════════════
#  PHASES  — recompressed for 25 s
# ══════════════════════════════════════════════════
PHASES = [
    (0,   "[1] Nuclear Spin & Equilibrium",
           "¹H spin-½ → magnetic moment μ",
           "In B₀: Boltzmann excess → net Mz = M₀",
           "3D here: conceptual lab-frame view"),
    (90,  "[2] Rotating-Frame Bloch Eq.  [FIX-2]",
           "Solved in rotating frame — ω₀ removed",
           "dM/dt = γ(M×B_eff) − relaxation",
           "Pre-pulse: B_eff=0 → M static at +Z"),
    (180, "[3] 90° RF Pulse via Bloch ODE  [FIX-3]",
           "B_eff = (0,−B₁,0)  in rotating frame",
           "γB₁t_p = π/2  →  exact 90° flip: Z→X",
           "t_pulse=1s animation only — real ¹H pulse ≈ 10 µs"),
    (250, "[4] FID — Single Bloch Trajectory  [FIX-1]",
           "FID = Mx from rotating-frame Bloch",
           "3D trail: smooth sub-frame (N×10)",
           "R_z(ω_vis·t)·M_rot — same source as FID"),
    (400, "[5] Rotating-Frame Freq. Offset  [FIX-4]",
           f"Δf = {DELTA_F} Hz  (rot.-frame offset, NOT ppm)",
           "Real ¹H NMR: 1 ppm at 400 MHz = 400 Hz",
           f"{DELTA_F} Hz for FPS-limited demo (~0.01 ppm)"),
    (500, "[6] Chemical Shift Concept",
           "Shielding σ: ω_eff = γ(1−σ)B₀",
           "Different environments → different peaks",
           "δ(ppm) = (ω−ω_ref)/ω₀ × 10⁶"),
    (600, "[7] FFT + Lorentzian Overlay  [FIX-5]",
           "Cyan = |FFT(FID)|  (Hann-windowed)",
           "Rose = analytical L(f) = 1/[1+(2π·Δf·T₂)²]",
           "FWHM = 1/(π T₂)  |  compare shapes directly"),
    (700, "[8] NMR Spectrum & Molecular ID",
           "Many spins → many peaks at their Δf",
           "Peak position δ (ppm) = chemical environment",
           "Full spectrum = molecular fingerprint"),
]

# ══════════════════════════════════════════════════
#  BLOCH ODE
# ══════════════════════════════════════════════════
def bloch_rhs(M, B_eff, T1, T2, M0=1.0):
    Mx,My,Mz = M; Bx,By,Bz = B_eff
    return np.array([
        GAMMA_H*(My*Bz-Mz*By) - Mx/T2,
        GAMMA_H*(Mz*Bx-Mx*Bz) - My/T2,
        GAMMA_H*(Mx*By-My*Bx) - (Mz-M0)/T1
    ])

def rk4_step(M, dt, B_eff, T1, T2):
    k1=bloch_rhs(M,B_eff,T1,T2); k2=bloch_rhs(M+.5*dt*k1,B_eff,T1,T2)
    k3=bloch_rhs(M+.5*dt*k2,B_eff,T1,T2); k4=bloch_rhs(M+dt*k3,B_eff,T1,T2)
    return M+(dt/6)*(k1+2*k2+2*k3+k4)

# ══════════════════════════════════════════════════
#  SIMULATION
# ══════════════════════════════════════════════════
dt = 1./FPS
Mtrack = np.zeros((N_FRAMES,3)); Mtrack[0]=[0,0,1]
for fi in range(1,PULSE_FRAME):
    Mtrack[fi]=rk4_step(Mtrack[fi-1],dt,[0,0,0],T1,T2)
for fi in range(PULSE_FRAME,PULSE_FRAME+PULSE_RAMP):
    Mtrack[fi]=rk4_step(Mtrack[fi-1],dt,[0,-B1_AMP,0],T1_PULSE,T2_PULSE)
delta_omega=2*np.pi*DELTA_F; B_rot_z=delta_omega/GAMMA_H
for fi in range(PULSE_FRAME+PULSE_RAMP,N_FRAMES):
    Mtrack[fi]=rk4_step(Mtrack[fi-1],dt,[0,0,B_rot_z],T1,T2)

POST_PULSE = PULSE_FRAME+PULSE_RAMP  # 210

fid_all = Mtrack[:,0].copy(); fid_all[:POST_PULSE]=0
FID_TOTAL_S = (N_FRAMES-PULSE_FRAME)/FPS

# ══════════════════════════════════════════════════
#  3D VIS — frame-level
# ══════════════════════════════════════════════════
phi_arr = OMEGA_VIS*np.arange(N_FRAMES)
Mx_vis=np.zeros(N_FRAMES); My_vis=np.zeros(N_FRAMES); Mz_vis=np.zeros(N_FRAMES)
for fi in range(N_FRAMES):
    phi=phi_arr[fi]; cp,sp=np.cos(phi),np.sin(phi)
    if fi<PULSE_FRAME:
        Mx_vis[fi]=np.sin(THETA_CONCEPT)*cp
        My_vis[fi]=np.sin(THETA_CONCEPT)*sp
        Mz_vis[fi]=np.cos(THETA_CONCEPT)
    else:
        mx,my,mz=Mtrack[fi]
        Mx_vis[fi]=mx*cp-my*sp; My_vis[fi]=mx*sp+my*cp; Mz_vis[fi]=mz

Tx= My_vis*0.50; Ty=-Mx_vis*0.50; Tz=np.zeros(N_FRAMES)

# ══════════════════════════════════════════════════
#  SMOOTH TRAIL
# ══════════════════════════════════════════════════
print("Pre-computing smooth trail ...")
n_smooth=N_FRAMES*N_SMOOTH
fi_sub=np.arange(n_smooth)/N_SMOOTH
phi_sub=OMEGA_VIS*fi_sub
Mx_smooth=np.zeros(n_smooth); My_smooth=np.zeros(n_smooth); Mz_smooth=np.zeros(n_smooth)
Mx0_pp=Mtrack[POST_PULSE-1,0]; My0_pp=Mtrack[POST_PULSE-1,1]

for i in range(n_smooth):
    fi_f=fi_sub[i]; cp,sp=np.cos(phi_sub[i]),np.sin(phi_sub[i])
    if fi_f<PULSE_FRAME:
        Mx_smooth[i]=np.sin(THETA_CONCEPT)*cp
        My_smooth[i]=np.sin(THETA_CONCEPT)*sp
        Mz_smooth[i]=np.cos(THETA_CONCEPT)
    elif fi_f<POST_PULSE:
        fi_lo=int(fi_f); fi_hi=min(fi_lo+1,N_FRAMES-1)
        frac=fi_f-fi_lo; M_int=(1-frac)*Mtrack[fi_lo]+frac*Mtrack[fi_hi]
        mx,my,mz=M_int
        Mx_smooth[i]=mx*cp-my*sp; My_smooth[i]=mx*sp+my*cp; Mz_smooth[i]=mz
    else:
        t_pp=(fi_f-POST_PULSE)/FPS; env=np.exp(-t_pp/T2)
        ph2=delta_omega*t_pp; c2,s2=np.cos(ph2),np.sin(ph2)
        mx_r=env*(Mx0_pp*c2-My0_pp*s2); my_r=env*(Mx0_pp*s2+My0_pp*c2)
        mz_r=1.-np.exp(-t_pp/T1)
        Mx_smooth[i]=mx_r*cp-my_r*sp; My_smooth[i]=mx_r*sp+my_r*cp; Mz_smooth[i]=mz_r
print("Done.")

f_lor=np.linspace(0,10,2000)
L_analytic=1./(1.+(2*np.pi*(f_lor-DELTA_F)*T2)**2)

# ══════════════════════════════════════════════════
#  FIGURE
# ══════════════════════════════════════════════════
plt.rcParams.update({'font.family':'monospace','font.size':13,
                     'axes.titlesize':14,'axes.labelsize':12,
                     'xtick.labelsize':10,'ytick.labelsize':10})

fig=plt.figure(figsize=(18,10),dpi=110,facecolor=BG)
fig.patch.set_facecolor(BG)

gs=gridspec.GridSpec(4,2,left=0.02,right=0.98,top=0.87,bottom=0.04,
                     wspace=0.30,hspace=0.70,
                     width_ratios=[1.5,1],height_ratios=[1,1,0.06,0.80])

ax3d  =fig.add_subplot(gs[:,0],projection='3d')
ax_fid=fig.add_subplot(gs[0,1])
ax_sp =fig.add_subplot(gs[1,1])
ax_txt=fig.add_subplot(gs[3,1])

ax3d.set_facecolor(BG)
for ax in [ax_fid,ax_sp]: ax.set_facecolor(C_AX)
ax_txt.set_facecolor(BG); ax_txt.axis('off')

for ax in [ax_fid,ax_sp]:
    ax.tick_params(colors=C_DIM,labelsize=10)
    for sp in ax.spines.values():
        sp.set_color('#2a3a5c'); sp.set_linewidth(1.2)

# ── HEADER ── (no version)
fig.text(0.50,0.963,
         'Larmor Precession in NMR — Single Rotating-Frame Bloch Simulation',
         ha='center',color=C_TEXT,fontsize=19,fontweight='bold',fontfamily='monospace')

sub_items=[
    (0.03,f'B₀ = {B0} T',C_B0),
    (0.18,f'ω₀/2π ≈ {GAMMA_H*B0/(2*np.pi)/1e6:.0f} MHz (¹H)',C_M),
    (0.42,f'T₁={T1} s   T₂={T2} s',C_TEXT),
    (0.60,f'Δf={DELTA_F} Hz  rot.-frame (~0.01 ppm)',C_DIM),
]
for x,txt,col in sub_items:
    fig.text(x,0.922,txt,color=col,fontsize=10,fontfamily='monospace')

# ── DISCLAIMER — split into 2 lines, font 11, readable  ──
fig.text(0.03, 0.902,
         '⚠  Pre-pulse 3D: conceptual θ=22° (labeled)  |  Post-pulse: R_z(ω_vis·t)·M_rot  [single Bloch traj.]',
         color=C_PULSE, fontsize=10.5, fontfamily='monospace')
fig.text(0.03, 0.885,
         '   Trail: smooth sub-frame interpolation (N×10)  |  ω_vis = ω₀ / 1×10⁸  (3D speed)',
         color=C_PULSE, fontsize=10.5, fontfamily='monospace')

leg=[('─ μ',C_M,0.68),('─ τ',C_TAU,0.76),('─ B₀',C_B0,0.84),
     ('─ B₁',C_B1,0.89),('─ FID',C_FID,0.94)]
for lbl,col,x in leg:
    fig.text(x,0.902,lbl,color=col,fontsize=9,fontfamily='monospace')
leg2=[('─ FFT',C_SPEC,0.68),('─ Lor.',C_LOREN,0.77)]
for lbl,col,x in leg2:
    fig.text(x,0.885,lbl,color=col,fontsize=9,fontfamily='monospace')

# ══════════════════════════════════════════════════
#  STATIC 3D SCENE
# ══════════════════════════════════════════════════
def build_3d():
    ax3d.set_xlim(-1.35,1.35); ax3d.set_ylim(-1.35,1.35); ax3d.set_zlim(-0.15,1.75)
    ax3d.set_box_aspect([1,1,1.1])
    ax3d.set_xlabel('X',color=C_DIM,fontsize=12,labelpad=3)
    ax3d.set_ylabel('Y',color=C_DIM,fontsize=12,labelpad=3)
    ax3d.set_zlabel('Z',color=C_DIM,fontsize=12,labelpad=3)
    ax3d.tick_params(colors=C_DIM,labelsize=8)
    for pane in [ax3d.xaxis.pane,ax3d.yaxis.pane,ax3d.zaxis.pane]:
        try:    pane.fill=False
        except: pass
        try:    pane.set_edgecolor('#ffffff0c')
        except: pass
    ax3d.grid(False)
    for xe,ye,ze in [(1.2,0,0),(0,1.2,0)]:
        ax3d.plot([0,xe],[0,ye],[0,ze],color='#445577',lw=0.8,alpha=0.5)
    ax3d.quiver(0,0,0,0,0,1.50,color=C_B0,lw=4.0,arrow_length_ratio=0.07,alpha=1.0)
    ax3d.text(0.08,0.08,1.58,'B₀',color=C_B0,fontsize=16,fontweight='bold')
    ph=np.linspace(0,2*np.pi,120)
    ax3d.plot(np.sin(THETA_CONCEPT)*np.cos(ph),
              np.sin(THETA_CONCEPT)*np.sin(ph),
              np.cos(THETA_CONCEPT)*np.ones(120),
              color='#6688aa',alpha=0.18,lw=1.3,linestyle='--')
    ax3d.text(0.38,0.10,np.cos(THETA_CONCEPT)+0.04,
              '← conceptual\n   (pre-pulse)',color='#a0b8cc',fontsize=8.5,alpha=0.85)
    ax3d.plot(np.cos(ph),np.sin(ph),np.zeros(120),
              color=C_MXY,alpha=0.13,lw=1.2,linestyle=':')

    # ── 3D watermark — LARGER & BOLD ──
    ax3d.text(-1.30,-1.30,1.67,
              'dM/dt = γ(M×B_eff) − relax',
              color=C_M, fontsize=13, fontweight='bold',
              fontfamily='monospace', alpha=0.92)
    ax3d.text(-1.30,-1.30,1.48,
              '[rotating frame only  —  FIX-2]',
              color=C_TAU, fontsize=11,
              fontfamily='monospace', alpha=0.88)

    ax3d.view_init(elev=22,azim=35)

build_3d()

# FID subplot
ax_fid.set_title('FID — Re[Mxy]  from rotating-frame Bloch  [FIX-1]',
                  color=C_TEXT,fontsize=12,pad=7,fontweight='bold')
ax_fid.set_xlabel('time from pulse  (s)',color=C_DIM,fontsize=11)
ax_fid.set_ylabel('Mx(t)',color=C_DIM,fontsize=11)
ax_fid.set_xlim(0,FID_TOTAL_S); ax_fid.set_ylim(-1.12,1.12)
ax_fid.axhline(0,color='#2a3a5c',lw=1.0)
ax_fid.text(0.28,0.89,
            f'cos(2π·{DELTA_F}Hz·t)·exp(−t/T₂)   [rot. frame Mx]',
            transform=ax_fid.transAxes,color=C_DIM,fontsize=8.5)

# Spectrum subplot
ax_sp.set_title('FFT(FID) [cyan] + Analytical Lorentzian [rose−−]  [FIX-5]',
                 color=C_TEXT,fontsize=12,pad=7,fontweight='bold')
ax_sp.set_xlabel('frequency  (Hz)',color=C_DIM,fontsize=11)
ax_sp.set_ylabel('intensity',color=C_DIM,fontsize=11)
ax_sp.set_xlim(0,10); ax_sp.set_ylim(0,1.22)
lw_hz=1./(np.pi*T2)
ax_sp.text(0.27,0.89,
           f'L(f)=1/[1+(2π·Δf·T₂)²]   FWHM=1/(πT₂)={lw_hz:.2f} Hz',
           transform=ax_sp.transAxes,color=C_DIM,fontsize=8.5)

lor_ln_static,=ax_sp.plot(f_lor,L_analytic,color=C_LOREN,lw=2.2,
                            linestyle='--',alpha=0.0)

# ══════════════════════════════════════════════════
#  ANIMATED OBJECTS
# ══════════════════════════════════════════════════
trail_ln,=ax3d.plot([],[],[],color=C_TRAIL,alpha=0.55,lw=2.0)
vec_ln,  =ax3d.plot([],[],[],color=C_M,   lw=4.5)
tau_ln,  =ax3d.plot([],[],[],color=C_TAU, lw=2.8)
mxy_ln,  =ax3d.plot([],[],[],color=C_MXY, lw=2.0,linestyle='--',alpha=0.80)
b1_ln,   =ax3d.plot([],[],[],color=C_B1,  lw=4.0,alpha=0.0)
vec_dot, =ax3d.plot([],[],[],'o',color=C_M,  ms=10,zorder=6)
tau_dot, =ax3d.plot([],[],[],'o',color=C_TAU,ms=7, zorder=6)

fid_ln,  =ax_fid.plot([],[],color=C_FID, lw=2.5)
spec_ln, =ax_sp.plot([],[],  color=C_SPEC,lw=2.5)
peak_ln, =ax_sp.plot([],[],  color=C_SPEC,lw=1.4,alpha=0.60,linestyle='--')
peak_txt  =ax_sp.text(0,0,'',color=C_SPEC,fontsize=10,va='bottom',fontweight='bold')

pulse_vline=ax_fid.axvline(x=0,color=C_PULSE,lw=2.0,linestyle=':',alpha=0.0)
pulse_txt  =ax_fid.text(0.50,0.72,'',color=C_PULSE,fontsize=9,
                         transform=ax_fid.transAxes,ha='center')

_box=dict(boxstyle='round,pad=0.7',facecolor='#080c1a',
          edgecolor='#3344aa',alpha=0.97,linewidth=2.0)
ph_title=ax_txt.text(0.02,0.98,'',transform=ax_txt.transAxes,
                      color=C_TEXT,fontsize=12,fontweight='bold',va='top',bbox=_box)
ph_l1=ax_txt.text(0.02,0.60,'',transform=ax_txt.transAxes,color=C_B0, fontsize=10,va='top')
ph_l2=ax_txt.text(0.02,0.35,'',transform=ax_txt.transAxes,color=C_MXY,fontsize=10,va='top')
ph_l3=ax_txt.text(0.02,0.10,'',transform=ax_txt.transAxes,color=C_DIM,fontsize=10,va='top')

time_lbl=fig.text(0.98,0.005,'',color=C_DIM,fontsize=9,ha='right',fontfamily='monospace')

# ══════════════════════════════════════════════════
#  UPDATE
# ══════════════════════════════════════════════════
_cur_phase=[-1]; _spec_frq=[None]; _spec_F=[None]
_tau_label=[ax3d.text(0,0,0,'',color=C_TAU,fontsize=11,fontweight='bold')]

def update(fi):
    x,y,z  =Mx_vis[fi],My_vis[fi],Mz_vis[fi]
    tx,ty   =Tx[fi],Ty[fi]
    in_pulse=PULSE_FRAME<=fi<POST_PULSE

    # Smooth trail
    fi_s=fi*N_SMOOTH; t0_s=max(0,fi_s-TRAIL_LEN*N_SMOOTH)
    trail_ln.set_data(Mx_smooth[t0_s:fi_s+1],My_smooth[t0_s:fi_s+1])
    trail_ln.set_3d_properties(Mz_smooth[t0_s:fi_s+1])

    # μ vector
    vec_ln.set_data([0,x],[0,y]); vec_ln.set_3d_properties([0,z])
    vec_dot.set_data([x],[y]);    vec_dot.set_3d_properties([z])

    # Mxy projection
    mxy_ln.set_data([x,x],[y,y]); mxy_ln.set_3d_properties([z,0])

    # B₁ (only during pulse)
    if in_pulse:
        b1_ln.set_data([0,0.8],[0,0]); b1_ln.set_3d_properties([0,0]); b1_ln.set_alpha(0.90)
    else:
        b1_ln.set_alpha(0.0)

    # τ
    tau_ln.set_data([x,x+tx],[y,y+ty]); tau_ln.set_3d_properties([z,z])
    tau_dot.set_data([x+tx],[y+ty]);     tau_dot.set_3d_properties([z])
    _tau_label[0].remove()
    _tau_label[0]=ax3d.text(x+tx+0.06,y+ty+0.06,z,
                             'τ' if fi>60 else '',
                             color=C_TAU,fontsize=11,fontweight='bold')

    # FID
    if fi>=PULSE_FRAME:
        n_pts=fi-PULSE_FRAME+1
        t_fid=np.linspace(0,FID_TOTAL_S,N_FRAMES-PULSE_FRAME)
        sig=fid_all[PULSE_FRAME:]
        fid_ln.set_data(t_fid[:n_pts],sig[:n_pts])
        pulse_vline.set_xdata([0,0]); pulse_vline.set_alpha(0.85)
        if in_pulse or fi==POST_PULSE:
            pulse_txt.set_text('90° RF pulse  B₁(t)  [Bloch ODE, FIX-3]')
        elif fi>POST_PULSE+90:
            pulse_txt.set_text('')

        age=fi-PULSE_FRAME
        if age>90 and fi%6==0:
            raw=fid_all[PULSE_FRAME:fi+1]; N=len(raw)
            Nfft=max(N,4096); padded=np.zeros(Nfft); padded[:N]=raw*np.hanning(N)
            F=np.abs(np.fft.rfft(padded)); frq=np.fft.rfftfreq(Nfft,d=1./FPS)
            F/=F.max()+1e-9; msk=(frq>=0)&(frq<=10.)
            _spec_frq[0]=frq[msk]; _spec_F[0]=F[msk]

        if _spec_frq[0] is not None:
            spec_ln.set_data(_spec_frq[0],_spec_F[0])
            pk_idx=np.argmax(_spec_F[0]); pk_f=_spec_frq[0][pk_idx]
            peak_ln.set_data([pk_f,pk_f],[0,1.0])
            peak_txt.set_position((pk_f+0.15,0.82)); peak_txt.set_text(f'{pk_f:.1f} Hz')
            lor_ln_static.set_alpha(min(0.90,(age-90)/350.))
    else:
        fid_ln.set_data([],[])
        pulse_vline.set_alpha(0.0)
        lor_ln_static.set_alpha(0.0)

    best=0
    for idx,(pf,*_) in enumerate(PHASES):
        if fi>=pf: best=idx
    if best!=_cur_phase[0]:
        _cur_phase[0]=best
        _,ttl,l1,l2,l3=PHASES[best]
        ph_title.set_text(ttl)
        ph_l1.set_text('▸ '+l1); ph_l2.set_text('▸ '+l2); ph_l3.set_text('▸ '+l3)

    Mrot_mag=np.linalg.norm(Mtrack[fi])
    stage="pulse" if in_pulse else ("pre" if fi<PULSE_FRAME else "FID")
    time_lbl.set_text(f't = {fi/FPS:.1f} s   |M_rot| = {Mrot_mag:.3f}  [{stage}]')

    return (trail_ln,vec_ln,tau_ln,mxy_ln,b1_ln,vec_dot,tau_dot,
            fid_ln,spec_ln,peak_ln,lor_ln_static,pulse_vline)

# ══════════════════════════════════════════════════
#  RENDER
# ══════════════════════════════════════════════════
print(f"Rendering {N_FRAMES} frames ({DURATION}s) ...")
writer=FFMpegWriter(fps=FPS,codec='libx264',
    extra_args=['-pix_fmt','yuv420p','-crf','16','-preset','fast'])
out_silent='larmor_silent_v8.mp4'
with writer.saving(fig,out_silent,dpi=110):
    for fi in range(N_FRAMES):
        update(fi); writer.grab_frame()
        if fi%100==0:
            print(f'  {fi:4d}/{N_FRAMES}  {100*fi//N_FRAMES:3d}%  t={fi/FPS:.1f}s')
print(f'Saved: {out_silent}')

print("Building audio ...")
SR=44100; t_a=np.linspace(0,DURATION,SR*DURATION)
t_p=PULSE_FRAME/FPS
env=np.where(t_a<t_p,0.,np.exp(-(t_a-t_p)/T2))
tone=(env*np.sin(2*np.pi*432.*t_a)*28000).astype(np.int16)
wav='larmor_v8.wav'; wavfile.write(wav,SR,tone)

out_sound='larmor_with_tone_v8.mp4'
r=subprocess.run(['ffmpeg','-y','-i',out_silent,'-i',wav,
                   '-c:v','copy','-c:a','aac','-b:a','192k','-shortest',out_sound],
                  capture_output=True,text=True)
os.remove(wav)
if r.returncode==0: print(f'Saved: {out_sound}')
else: print('ffmpeg error:',r.stderr[-300:])
for f in [out_silent,out_sound]:
    if os.path.exists(f):
        print(f'  {f}  →  {os.path.getsize(f)/1024**2:.1f} MB')
