#!/usr/bin/env python3
"""
photon_units_tool.py

A single-file Python utility to convert between common photon-related units and
produce an overlaid multi-axis plot. Includes:

  • CLI (argparse): convert values, make plots, or launch a tiny GUI.
  • GUI (tkinter): enter a value+unit, see conversions, optionally plot.
  • Plot (matplotlib): overlaid axes for wavelength (nm), frequency (THz),
    photon energy (eV), and wavenumber (cm⁻1). A marker shows the input point.

Supported units (case-insensitive, spaces optional):
  Frequency: Hz, kHz, MHz, GHz, THz, PHz
  Wavelength: m, cm, mm, μm, um, nm, pm
  Energy: eV, meV, keV
  Wavenumber: cm^-1, cm⁻1, 1/cm
  Period: s, ms, μs, us, ns, ps, fs, as

You can pass numbers in standard or scientific notation (e.g. 3e14, 532e-9),
with units like "200 THz", "532 nm", "1.55 um", "2.33 eV", "1000 cm^-1".

Examples:
  $ python photon_units_tool.py convert 800 nm
  $ python photon_units_tool.py convert 193 THz
  $ python photon_units_tool.py plot 2.33 eV --span 0.4 --outfile axes.png
  $ python photon_units_tool.py gui

Author: ChatGPT (for Sam)
License: MIT
"""
from __future__ import annotations

import argparse
import math
import re
import sys
from dataclasses import dataclass
from typing import Callable, Dict, Tuple

# --- Physical constants (CODATA 2018/2019)
# Using widely accepted conventional values is fine for spectroscopy-level work.
C = 299_792_458.0                 # speed of light [m/s]
H = 6.626_070_15e-34              # Planck constant [J·s] (exact by SI)
E_CHARGE = 1.602_176_634e-19      # elementary charge [C] (exact by SI)
TWO_PI = 2.0 * math.pi

# --- Unit prefixes
SI_PREFIX = {
    'y': 1e-24, 'z': 1e-21, 'a': 1e-18, 'f': 1e-15, 'p': 1e-12, 'n': 1e-9,
    'u': 1e-6,  'µ': 1e-6,   'm': 1e-3,  'c': 1e-2,  'd': 1e-1,
    '': 1.0,
    'da': 1e1,  'h': 1e2,    'k': 1e3,  'M': 1e6,   'G': 1e9,
    'T': 1e12,  'P': 1e15,   'E': 1e18, 'Z': 1e21,  'Y': 1e24,
}

# --- Parsing helpers
_U_RE = re.compile(r"^\s*([+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)\s*([A-Za-zµμ^/\-°⁻]+)?\s*$")

@dataclass
class Canonical:
    """Canonical representation; core variable is frequency in Hz."""
    freq_hz: float  # frequency [Hz]

    @property
    def wavelength_m(self) -> float:
        return C / self.freq_hz

    @property
    def energy_j(self) -> float:
        return H * self.freq_hz

    @property
    def energy_ev(self) -> float:
        return self.energy_j / E_CHARGE

    @property
    def wavenumber_cm1(self) -> float:
        # 1/λ in cm^-1
        return 1.0 / (self.wavelength_m * 100.0)

    @property
    def omega_rad_s(self) -> float:
        return TWO_PI * self.freq_hz

    @property
    def period_s(self) -> float:
        return 1.0 / self.freq_hz

# --- Unit normalization

def _norm_unit(u: str) -> str:
    u = u.strip()
    u = u.replace('μ', 'u').replace('µ', 'u')
    u = u.replace('⁻', '-')
    u = u.replace('–', '-')
    u = u.replace('−', '-')
    return u

# --- Input dispatch

def parse_quantity(s: str) -> Canonical:
    """Parse a value+unit string and return canonical (frequency in Hz).

    Supports: frequency, wavelength, energy, wavenumber, and period.
    """
    m = _U_RE.match(s)
    if not m:
        raise ValueError(f"Could not parse input '{s}'. Expected like '532 nm' or '200 THz'.")
    val = float(m.group(1))
    unit = _norm_unit(m.group(2) or '')
    unit_lower = unit.lower()

    if not unit:
        raise ValueError("Unit missing. Provide e.g. '800 nm', '200 THz', '2.33 eV'.")

    # Frequency
    if unit_lower in ('hz', '1/s', 's^-1', 's-1'):
        return Canonical(freq_hz=val)
    for pfx, scale in (('khz',1e3),('mhz',1e6),('ghz',1e9),('thz',1e12),('phz',1e15)):
        if unit_lower == pfx:
            return Canonical(freq_hz=val*scale)

    # Wavelength
    WL = {
        'm': 1.0,
        'cm': 1e-2,
        'mm': 1e-3,
        'um': 1e-6,
        'nm': 1e-9,
        'pm': 1e-12,
    }
    if unit_lower in WL:
        wl_m = val * WL[unit_lower]
        if wl_m <= 0:
            raise ValueError('Wavelength must be > 0.')
        return Canonical(freq_hz=C / wl_m)

    # Energy
    if unit_lower == 'ev':
        if val <= 0:
            raise ValueError('Energy must be > 0.')
        return Canonical(freq_hz=(val * E_CHARGE) / H)
    if unit_lower == 'mev':
        return Canonical(freq_hz=((val*1e-3) * E_CHARGE) / H)
    if unit_lower == 'kev':
        return Canonical(freq_hz=((val*1e3) * E_CHARGE) / H)

    # Wavenumber
    if unit_lower in ('cm^-1','1/cm'):
        if val <= 0:
            raise ValueError('Wavenumber must be > 0.')
        wl_m = 1.0/(val*100.0)
        return Canonical(freq_hz=C / wl_m)

    # Period
    T = {
        's': 1.0,
        'ms': 1e-3,
        'us': 1e-6,
        'ns': 1e-9,
        'ps': 1e-12,
        'fs': 1e-15,
        'as': 1e-18,
    }
    if unit_lower in T:
        period = val*T[unit_lower]
        if period <= 0:
            raise ValueError('Period must be > 0.')
        return Canonical(freq_hz=1.0/period)

    raise ValueError(f"Unrecognized unit '{unit}'.")

# --- Formatting helpers

def fmt_eng(x: float, unit: str, *, sci_threshold: Tuple[float,float]=(1e-3,1e3)) -> str:
    """Engineering-ish formatting with fallback to scientific notation."""
    ax = abs(x)
    if ax > 0 and (ax < sci_threshold[0] or ax >= sci_threshold[1]):
        return f"{x:.6g} {unit}"
    return f"{x:.6f} {unit}"

# --- Conversions table

def to_all(c: Canonical) -> Dict[str, float]:
    return {
        'frequency_hz': c.freq_hz,
        'frequency_thz': c.freq_hz/1e12,
        'omega_rad_s': c.omega_rad_s,
        'period_s': c.period_s,
        'wavelength_m': c.wavelength_m,
        'wavelength_nm': c.wavelength_m*1e9,
        'wavelength_um': c.wavelength_m*1e6,
        'energy_j': c.energy_j,
        'energy_ev': c.energy_ev,
        'wavenumber_cm^-1': c.wavenumber_cm1,
    }

# --- Pretty print

def print_conversions(c: Canonical) -> None:
    d = to_all(c)
    lines = [
        "Conversions (vacuum):",
        f"  Frequency:   {fmt_eng(d['frequency_hz'],'Hz')}  | {fmt_eng(d['frequency_thz'],'THz')}",
        f"  Angular ω:   {fmt_eng(d['omega_rad_s'],'rad/s')}",
        f"  Period:      {fmt_eng(d['period_s'],'s')}",
        f"  Wavelength:  {fmt_eng(d['wavelength_m'],'m')}  | {fmt_eng(d['wavelength_um'],'μm')}  | {fmt_eng(d['wavelength_nm'],'nm')}",
        f"  Energy:      {fmt_eng(d['energy_j'],'J')}  | {fmt_eng(d['energy_ev'],'eV')}",
        f"  Wavenumber:  {fmt_eng(d['wavenumber_cm^-1'],'cm⁻¹')}",
    ]
    print("\n".join(lines))

# --- Plotting with overlaid axes

def _forward_inverse(fwd: Callable[[float], float], inv: Callable[[float], float]):
    return fwd, inv


def make_axes_plot(c: Canonical, span: float=0.4, points: int=500, outfile: str|None=None, show: bool=True) -> None:
    """Make an overlaid multi-axis plot around the input value.

    Args:
        c: Canonical (defines central frequency).
        span: Fractional half-span around the central value (0.4 → ±40%).
        points: Number of sample points for the ruler.
        outfile: If given, save to this path.
        show: If True, show() the figure.
    """
    import matplotlib.pyplot as plt
    from mpl_toolkits.axes_grid1 import host_subplot
    import mpl_toolkits.axisartist as AA

    # x-domain in wavelength (nm), centered at the given value
    x0_nm = c.wavelength_m * 1e9
    x_min = x0_nm * (1.0 - span)
    x_max = x0_nm * (1.0 + span)
    if x_min <= 0:
        x_min = x0_nm * 1e-2
    xs_nm = [x_min + (x_max-x_min)*i/(points-1) for i in range(points)]

    # Conversion functions defined in terms of wavelength [nm]
    def nm_to_freq_thz(nm: float) -> float:
        return (C / (nm*1e-9)) / 1e12
    def freq_thz_to_nm(thz: float) -> float:
        return (C / (thz*1e12)) * 1e9

    def nm_to_ev(nm: float) -> float:
        # E[eV] = h*c / (λ) / e
        return (H*C)/(nm*1e-9)/E_CHARGE
    def ev_to_nm(ev: float) -> float:
        return (H*C)/(ev*E_CHARGE) * 1e9

    def nm_to_cm1(nm: float) -> float:
        return 1.0 / ((nm*1e-9)*100.0)
    def cm1_to_nm(cm1: float) -> float:
        return (1.0/(cm1*100.0)) * 1e9

    # Base (host) axis: wavelength [nm]
    host = host_subplot(111, axes_class=AA.Axes)
    plt.subplots_adjust(right=0.78, top=0.82)

    host.set_xlabel('Wavelength (nm)')
    host.set_xlim(x_min, x_max)

    # Parasite axes for overlaid scales
    par_top1 = host.twiny()
    par_top2 = host.twiny()
    par_top3 = host.twiny()

    # Stack the extra top axes with pixel offsets
    par_top1.axis['top'] = par_top1.new_fixed_axis(loc='top', axes=par_top1, offset=(0, 0))
    par_top2.axis['top'] = par_top2.new_fixed_axis(loc='top', axes=par_top2, offset=(0, 24))
    par_top3.axis['top'] = par_top3.new_fixed_axis(loc='top', axes=par_top3, offset=(0, 48))

    # Link scales via function transforms (secondary axes style)
    # We approximate ticks by transforming major ticks from host domain.
    for ax, label, fwd, inv in [
        (par_top1, 'Frequency (THz)', nm_to_freq_thz, freq_thz_to_nm),
        (par_top2, 'Energy (eV)',     nm_to_ev,       ev_to_nm),
        (par_top3, 'Wavenumber (cm$^{-1}$)', nm_to_cm1, cm1_to_nm),
    ]:
        ax.set_xlim(host.get_xlim())
        ax.set_xlabel(label)
        # Create roughly 6 ticks by sampling and formatting
        host_ticks = host.get_xticks()
        vals = [fwd(t) for t in host_ticks]
        # Clean labels
        fmt = lambda v: f"{v:.3g}"
        ax.set_xticks(host_ticks)
        ax.set_xticklabels([fmt(v) for v in vals])

    # Draw a vertical line at the input value
    host.axvline(x=x0_nm, linestyle='--', linewidth=1.5)

    # Add a small info box with numeric conversions
    txt = (
        f"λ = {c.wavelength_m*1e9:.4g} nm\n"
        f"ν = {c.freq_hz/1e12:.4g} THz\n"
        f"E = {c.energy_ev:.4g} eV\n"
        f"\u0303ν = {c.wavenumber_cm1:.4g} cm$^{{-1}}$"
    )
    host.text(0.02, 0.95, txt, transform=host.transAxes,
              va='top', ha='left', bbox=dict(boxstyle='round', fc='w', alpha=0.7))

    if outfile:
        plt.savefig(outfile, dpi=200, bbox_inches='tight')
    if show:
        plt.show()
    plt.close()

# --- Minimal tkinter GUI

def launch_gui():
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog

    root = tk.Tk()
    root.title('Photon Unit Converter')

    frm = ttk.Frame(root, padding=10)
    frm.grid(row=0, column=0, sticky='nsew')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    ttk.Label(frm, text='Value').grid(row=0, column=0, sticky='w')
    val_var = tk.StringVar(value='800')
    val_entry = ttk.Entry(frm, textvariable=val_var, width=12)
    val_entry.grid(row=0, column=1, sticky='w')

    ttk.Label(frm, text='Unit').grid(row=0, column=2, sticky='w', padx=(10,0))
    unit_var = tk.StringVar(value='nm')
    unit_cb = ttk.Combobox(frm, textvariable=unit_var, width=10, values=[
        'Hz','kHz','MHz','GHz','THz','PHz',
        'm','cm','mm','um','nm','pm',
        'eV','meV','keV',
        'cm^-1','1/cm',
        's','ms','us','ns','ps','fs','as',
    ])
    unit_cb.grid(row=0, column=3, sticky='w')

    out_txt = tk.Text(frm, width=60, height=12)
    out_txt.grid(row=1, column=0, columnspan=4, pady=(10,0), sticky='nsew')
    frm.rowconfigure(1, weight=1)

    def do_convert(*_):
        try:
            s = f"{val_var.get()} {unit_var.get()}"
            c = parse_quantity(s)
            # Render conversions
            d = to_all(c)
            out_txt.delete('1.0', tk.END)
            out_txt.insert(tk.END,
                           "Conversions (vacuum)\n"+
                           f"Frequency: {d['frequency_hz']:.6g} Hz | {d['frequency_thz']:.6g} THz\n"+
                           f"Angular ω: {d['omega_rad_s']:.6g} rad/s\n"+
                           f"Period:    {d['period_s']:.6g} s\n"+
                           f"Wavelength:{d['wavelength_m']:.6g} m | {d['wavelength_um']:.6g} μm | {d['wavelength_nm']:.6g} nm\n"+
                           f"Energy:    {d['energy_j']:.6g} J | {d['energy_ev']:.6g} eV\n"+
                           f"Wavenumber:{d['wavenumber_cm^-1']:.6g} cm^-1\n")
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def do_plot():
        try:
            s = f"{val_var.get()} {unit_var.get()}"
            c = parse_quantity(s)
            path = filedialog.asksaveasfilename(defaultextension='.png',
                                                filetypes=[('PNG','*.png'),('PDF','*.pdf'),('SVG','*.svg')],
                                                title='Save plot as...')
            if not path:
                return
            make_axes_plot(c, span=0.4, points=600, outfile=path, show=False)
            messagebox.showinfo('Saved', f'Plot saved to:\n{path}')
        except Exception as e:
            messagebox.showerror('Error', str(e))

    btns = ttk.Frame(frm)
    btns.grid(row=2, column=0, columnspan=4, pady=(8,0), sticky='e')
    ttk.Button(btns, text='Convert', command=do_convert).grid(row=0, column=0, padx=4)
    ttk.Button(btns, text='Plot…', command=do_plot).grid(row=0, column=1, padx=4)

    # Enter triggers convert
    val_entry.bind('<Return>', do_convert)
    unit_cb.bind('<<ComboboxSelected>>', do_convert)

    do_convert()
    root.mainloop()

# --- CLI

def build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description='Photon unit converter + plotter')
    sub = p.add_subparsers(dest='cmd', required=True)

    p_conv = sub.add_parser('convert', help='Convert an input value to all units')
    p_conv.add_argument('value', type=str, help="Numeric value (e.g. '800', '2.33', '1e3')")
    p_conv.add_argument('unit', type=str, help="Unit (e.g. 'nm','THz','eV','cm^-1','ps')")

    p_plot = sub.add_parser('plot', help='Plot overlaid axes around the input value')
    p_plot.add_argument('value', type=str)
    p_plot.add_argument('unit', type=str)
    p_plot.add_argument('--span', type=float, default=0.4, help='Half-range fraction around the center (default 0.4 = ±40%)')
    p_plot.add_argument('--points', type=int, default=600, help='Points across the span (default 600)')
    p_plot.add_argument('--outfile', type=str, default=None, help='Path to save (png/pdf/svg). If omitted, just show()')
    p_plot.add_argument('--no-show', action='store_true', help='Do not display the window; typically used with --outfile')

    sub.add_parser('gui', help='Launch a tiny GUI')

    return p


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    ap = build_argparser()
    args = ap.parse_args(argv)

    if args.cmd == 'convert':
        c = parse_quantity(f"{args.value} {args.unit}")
        print_conversions(c)
        return 0

    if args.cmd == 'plot':
        c = parse_quantity(f"{args.value} {args.unit}")
        make_axes_plot(c, span=args.span, points=args.points, outfile=args.outfile, show=not args.no_show)
        return 0

    if args.cmd == 'gui':
        launch_gui()
        return 0

    return 1


if __name__ == '__main__':
    sys.exit(main())
