"""
Rendu des images (PNG/SVG/JPG) et des GIF animés avec matplotlib.

Deux animations :
  - courbe        : les anomalies mensuelles se tracent mois après mois ;
  - extrapolation : la fenêtre de 30 ans avance, la tendance et la date
                    d'atteinte de +1,5 °C se mettent à jour.

Exemples :
    python pipeline/render.py --animation both --sortie ./exports
    python pipeline/render.py --animation extrapolation --debut 2010-01 --pas 1 --fps 8
    python pipeline/render.py --statique --format svg --sortie ./exports
    python pipeline/render.py --donnees https://…/data/series.json --pas-de-gif
"""
from __future__ import annotations

import argparse
import io
import json
import re
import shutil
import sys
import zipfile
from datetime import datetime, timedelta
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config as C
from download import http_get

COLORS = C.RENDER_COLORS
LAYOUT = C.RENDER_LAYOUT


# --------------------------------------------------------------------------
# Données
# --------------------------------------------------------------------------
def load_series(source: str | None) -> dict:
    """Lit series.json depuis un chemin local ou une URL."""
    src = source or str(C.SERIES_JSON)
    if src.startswith(("https://", "http://")):
        return json.loads(http_get(src))
    return json.loads(Path(src).read_text(encoding="utf-8"))


def fmt_num(x: float, lang: str, signed: bool = False) -> str:
    """Nombre à 2 décimales, virgule décimale en français."""
    s = f"{x:+.2f}" if signed else f"{x:.2f}"
    return s.replace(".", ",") if lang == "fr" else s


def to_date(month: str) -> datetime:
    """'YYYY-MM' → datetime au 15 du mois (convention du notebook)."""
    y, m = map(int, month.split("-"))
    return datetime(y, m, 15)


def add_months(d: datetime, k: float) -> datetime:
    return d + timedelta(days=k * C.DAYS_PER_MONTH)


def labels(lang: str) -> dict:
    return dict(C.LABELS[lang], _lang=lang)


# --------------------------------------------------------------------------
# Figure : fond dessiné une fois, update() ne change que les courbes
# --------------------------------------------------------------------------
def style_axes(ax, cfg, L):
    """Axes en gras avec flèches, grille pointillée grise."""
    ax.set_xlim(datetime.fromisoformat(cfg["x_range"][0]),
                datetime.fromisoformat(cfg["x_range"][1]))
    ax.set_ylim(*cfg["y_range"])
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_linewidth(1.8)
    # Flèches au bout des axes
    ax.plot(1, ax.get_ylim()[0], ">k", transform=ax.get_yaxis_transform(),
            clip_on=False, markersize=7)
    ax.plot(ax.get_xlim()[0], 1, "^k", transform=ax.get_xaxis_transform(),
            clip_on=False, markersize=7)
    ax.yaxis.set_major_locator(plt.MultipleLocator(C.GRID_STEP))
    ax.grid(axis="y", linestyle=":", color=COLORS["grid"], linewidth=0.9)
    ax.xaxis.set_major_locator(mdates.YearLocator(10))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.tick_params(labelsize=LAYOUT["tick_size"], width=1.5)
    ax.set_ylabel(L["ylabel"], fontweight="bold")


def draw_background(ax, data, L):
    cfg, ipcc = data["config"], data["ipcc"]
    years = [datetime(int(y), 1, 1) for y in ipcc["year"]]
    ax.fill_between(years, ipcc["min_t"], ipcc["max_t"], color=COLORS["ipcc"],
                    lw=0, label=L["ipcc"], zorder=1)
    ax.axhline(cfg["target"], color=COLORS["target"], lw=0.8, ls="--", zorder=2)
    lr = [datetime.fromisoformat(d) for d in cfg["likely_range"]]
    ax.plot(lr, [cfg["target"]] * 2, color=COLORS["target"], lw=4,
            solid_capstyle="butt", label=L["likely"], zorder=3)


class Scene:
    """Une figure pour une animation ; update() pour chaque image."""

    def __init__(self, fig, data, L, animation: str):
        self.data, self.L, self.animation = data, L, animation
        cfg, mon = data["config"], data["monthly"]
        self.target = cfg["target"]
        self.months = mon["month"]
        self.dates = [to_date(m) for m in self.months]
        self.vals = mon["anomaly_preindustrial"]
        self.index = {m: i for i, m in enumerate(self.months)}

        ax = fig.add_axes(LAYOUT["axes"])
        draw_background(ax, data, L)
        if animation == "courbe":
            (self.series,) = ax.plot([], [], color=COLORS["series"], lw=1.2,
                                     label=L["series"], zorder=4)
            (self.last,) = ax.plot([], [], "o", color=COLORS["series"], ms=6, zorder=5)
        else:
            ax.plot(self.dates, self.vals, color=COLORS["series_light"], lw=1,
                    label=L["series"], zorder=4)
            (self.window,) = ax.plot([], [], color=COLORS["window"], lw=1.3,
                                     label=L["window"], zorder=5)
            (self.trend,) = ax.plot([], [], color=COLORS["trend"], lw=2.2,
                                    label=L["trend"], zorder=6)
            (self.cross,) = ax.plot([], [], "o", ms=9, mfc="white", mec=COLORS["trend"],
                                    mew=2.2, label=L["crossing"], zorder=7)
        style_axes(ax, cfg, L)
        ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0), frameon=False,
                  fontsize=LAYOUT["legend_size"])
        self.info = fig.text(*LAYOUT["info_xy"], "", fontsize=LAYOUT["info_size"],
                             fontweight="bold", va="top", color=COLORS["text"],
                             linespacing=1.7)
        fig.text(*LAYOUT["title_xy"], L["title"], fontsize=LAYOUT["title_size"],
                 fontweight="bold")
        fig.text(*LAYOUT["source_xy"], L["source"], fontsize=LAYOUT["source_size"],
                 color=COLORS["source"])

    def update(self, upto: int | None = None, trend: dict | None = None) -> None:
        """upto : dernier mois affiché (courbe) ; trend : ligne de tendances.csv (extrapolation)."""
        L, lang = self.L, self.L["_lang"]
        if self.animation == "courbe":
            n = upto + 1
            self.series.set_data(self.dates[:n], self.vals[:n])
            self.last.set_data([self.dates[n - 1]], [self.vals[n - 1]])
            prelim = f" ({L['prelim']})" if self.data["monthly"]["status"][n - 1] == "preliminary" else ""
            info = [(L["month"], self.months[n - 1]),
                    (L["anomaly"], f"{fmt_num(self.vals[n - 1], lang, True)} °C{prelim}")]
        else:
            i0, i1 = self.index[trend["window_start"]], self.index[trend["window_end"]]
            self.window.set_data(self.dates[i0:i1 + 1], self.vals[i0:i1 + 1])
            # Droite de tendance prolongée jusqu'à 1,5 °C (ou bord du graphe)
            m, c = trend["slope_per_decade"] / 120, trend["intercept"]
            k_end = max((self.target - c) / m if m > 0 else 0, i1 - i0)
            start = self.dates[i0]
            self.trend.set_data([start, add_months(start, k_end)], [c, c + m * k_end])
            info = [(L["from"], trend["window_end"]),
                    (L["warming"], f"{fmt_num(trend['warming_at_end'], lang)} °C")]
            if trend["crossing_1_5"]:
                self.cross.set_data([to_date(trend["crossing_1_5"])], [self.target])
                info.append((L["reach"], trend["crossing_1_5"]))
            else:
                self.cross.set_data([], [])
        sep = " : " if lang == "fr" else ": "
        self.info.set_text("\n".join(f"{k}{sep}{v}" for k, v in info))


def new_figure(size):
    return plt.figure(figsize=(size[0] / C.DPI, size[1] / C.DPI), dpi=C.DPI)


# --------------------------------------------------------------------------
# Animations
# --------------------------------------------------------------------------
def select_frames(data, animation, debut, fin, pas):
    """Liste des (upto, trend) à dessiner pour une animation."""
    mon, tr = data["monthly"], data["trends"]
    if animation == "courbe":
        items = [(i, None) for i, m in enumerate(mon["month"])
                 if (debut is None or m >= debut) and (fin is None or m <= fin)]
    else:
        rows = [dict(zip(tr.keys(), vals)) for vals in zip(*tr.values())]
        items = [(None, r) for r in rows if (debut is None or r["window_end"] >= debut)
                 and (fin is None or r["window_end"] <= fin)]
    sel = items[::pas]
    if items and sel[-1] != items[-1]:
        sel.append(items[-1])            # toujours finir sur le dernier mois
    return sel


def render_animation(data, animation, out_dir: Path, *, lang="fr", debut=None,
                     fin=None, pas=1, fps=8, fmt="png", size=C.DEFAULT_SIZE_PX,
                     frames=True, gif=True, zip_frames=False) -> dict:
    """Génère les images et/ou le GIF d'une animation. Renvoie les chemins créés."""
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{animation}_{lang}"
    frame_dir = out_dir / f"images_{stem}"
    if frames:
        if frame_dir.exists():
            shutil.rmtree(frame_dir)
        frame_dir.mkdir()
    fig = new_figure(size)
    scene = Scene(fig, data, labels(lang), animation)
    gif_frames = []
    todo = select_frames(data, animation, debut, fin, pas)
    for k, (upto, trend) in enumerate(todo):
        scene.update(upto=upto, trend=trend)
        label = data["monthly"]["month"][upto] if trend is None else trend["window_end"]
        path = frame_dir / f"{animation}_{k:04d}_{label}.{fmt}"
        if gif or (frames and fmt == "png"):
            # Un seul rendu PNG, réutilisé pour le GIF et le fichier PNG
            buf = io.BytesIO()
            fig.savefig(buf, format="png", dpi=C.DPI)
            if gif:
                gif_frames.append(Image.open(buf).convert("RGB").quantize(colors=C.GIF_COLORS))
            if frames and fmt == "png":
                path.write_bytes(buf.getvalue())
        if frames and fmt != "png":
            fig.savefig(path, dpi=C.DPI)
    plt.close(fig)

    created = {}
    if frames:
        created["frames"] = str(frame_dir)
        if zip_frames:
            zpath = out_dir / f"images_{stem}.zip"
            with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
                for f in sorted(frame_dir.iterdir()):
                    z.write(f, f.name)
            created["zip"] = str(zpath)
    if gif and gif_frames:
        gpath = out_dir / f"{stem}.gif"
        durations = [int(1000 / fps)] * len(gif_frames)
        durations[-1] = C.LAST_FRAME_HOLD_MS
        gif_frames[0].save(gpath, save_all=True, append_images=gif_frames[1:],
                           duration=durations, loop=0, optimize=True)
        created["gif"] = str(gpath)
    print(f"{stem} : {len(todo)} images → {out_dir}")
    return created


def render_static(data, out_dir: Path, *, lang="fr", fmt="png", size=C.DEFAULT_SIZE_PX):
    """Graphique actuel (dernière tendance), pour export."""
    out_dir.mkdir(parents=True, exist_ok=True)
    latest = {k: v[-1] for k, v in data["trends"].items()}
    fig = new_figure(size)
    Scene(fig, data, labels(lang), "extrapolation").update(trend=latest)
    path = out_dir / f"graphique_{latest['window_end']}_{lang}.{fmt}"
    fig.savefig(path, dpi=C.DPI)
    plt.close(fig)
    return str(path)


def render_defaults(out_dir: Path, data: dict | None = None) -> None:
    """Exports précalculés chaque mois par GitHub Actions (mode « téléchargement »).

    Le manifeste garde aussi les anciennes clés sans langue (= fr) pour les
    copies de export.ps1 antérieures à la 1.3.0.
    """
    data = data or load_series(None)
    files = {}
    for lang in C.LANGS:
        for fmt in ("png", "svg"):
            files[f"static_{lang}_{fmt}"] = Path(render_static(data, out_dir, lang=lang, fmt=fmt)).name
        for anim, kw in C.DEFAULT_ANIMATIONS.items():
            res = render_animation(data, anim, out_dir, lang=lang, zip_frames=True, **kw)
            shutil.rmtree(res["frames"])          # on ne publie que le zip
            for kind in ("gif", "zip"):
                files[f"{anim}_{lang}_{kind}"] = Path(res[kind]).name
                if lang == "fr":
                    files[f"{anim}_{kind}"] = Path(res[kind]).name
    (out_dir / "manifest.json").write_text(json.dumps(files, indent=2), encoding="utf-8")


# --------------------------------------------------------------------------
# Ligne de commande
# --------------------------------------------------------------------------
def month_arg(s: str) -> str:
    if not re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", s):
        raise argparse.ArgumentTypeError(f"mois attendu au format AAAA-MM : {s!r}")
    return s


def bounded(lo, hi, cast=int):
    def check(s):
        v = cast(s)
        if not lo <= v <= hi:
            raise argparse.ArgumentTypeError(f"valeur entre {lo} et {hi} attendue : {s}")
        return v
    return check


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    px = bounded(*C.SIZE_BOUNDS_PX)
    p.add_argument("--donnees", help="series.json (chemin ou URL) ; défaut : data/series.json")
    p.add_argument("--animation", choices=["courbe", "extrapolation", "both"], default="both")
    p.add_argument("--statique", action="store_true", help="uniquement le graphique actuel")
    p.add_argument("--debut", type=month_arg, help="premier mois AAAA-MM")
    p.add_argument("--fin", type=month_arg, help="dernier mois AAAA-MM")
    p.add_argument("--pas", type=bounded(1, 120), default=1, help="un mois sur N")
    p.add_argument("--fps", type=bounded(0.5, 50, float), default=8,
                   help="images par seconde du GIF")
    p.add_argument("--format", default="png", choices=["png", "svg", "jpg", "pdf"])
    p.add_argument("--largeur", type=px, default=C.DEFAULT_SIZE_PX[0], help="pixels")
    p.add_argument("--hauteur", type=px, default=C.DEFAULT_SIZE_PX[1], help="pixels")
    p.add_argument("--langue", default="fr", choices=list(C.LANGS))
    p.add_argument("--sortie", default="exports", help="dossier de sortie")
    p.add_argument("--pas-de-gif", action="store_true")
    p.add_argument("--pas-d-images", action="store_true")
    a = p.parse_args(argv)

    data = load_series(a.donnees)
    out = Path(a.sortie)
    size = (a.largeur, a.hauteur)
    if a.statique:
        print(render_static(data, out, lang=a.langue, fmt=a.format, size=size))
        return 0
    anims = ["courbe", "extrapolation"] if a.animation == "both" else [a.animation]
    for anim in anims:
        render_animation(data, anim, out, lang=a.langue, debut=a.debut, fin=a.fin,
                         pas=a.pas, fps=a.fps, fmt=a.format, size=size,
                         frames=not a.pas_d_images, gif=not a.pas_de_gif)
    return 0


if __name__ == "__main__":
    sys.exit(main())
