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

# --------------------------------------------------------------------------
# Paramètres graphiques (palette et libellés : config.py)
# --------------------------------------------------------------------------
COLORS = C.RENDER_COLORS
DEFAULT_SIZE_PX = C.DEFAULT_SIZE_PX
DPI = C.DPI
GRID_STEP = C.GRID_STEP
LAST_FRAME_HOLD_MS = C.LAST_FRAME_HOLD_MS
LABELS = C.LABELS


# --------------------------------------------------------------------------
# Données
# --------------------------------------------------------------------------
def load_series(source: str | None) -> dict:
    """Lit series.json depuis un chemin local ou une URL."""
    src = source or str(C.SERIES_JSON)
    if src.startswith("http"):
        return json.loads(http_get(src))
    return json.loads(Path(src).read_text())


def fmt_num(x: float, lang: str, signed: bool = False) -> str:
    """Nombre à 2 décimales, virgule décimale en français."""
    s = f"{x:+.2f}" if signed else f"{x:.2f}"
    return s.replace(".", ",") if lang == "fr" else s


def to_date(month: str) -> datetime:
    """'YYYY-MM' → datetime au 15 du mois (convention du notebook)."""
    y, m = map(int, month.split("-"))
    return datetime(y, m, 15)


# --------------------------------------------------------------------------
# Dessin d'une image
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
    ax.yaxis.set_major_locator(plt.MultipleLocator(GRID_STEP))
    ax.grid(axis="y", linestyle=":", color=COLORS["grid"], linewidth=0.9)
    ax.xaxis.set_major_locator(mdates.YearLocator(10))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.tick_params(labelsize=10, width=1.5)
    ax.set_ylabel(L["ylabel"], fontweight="bold")


def draw_background(ax, data, L):
    cfg = data["config"]
    ipcc = data["ipcc"]
    years = [datetime(int(y), 1, 1) for y in ipcc["year"]]
    ax.fill_between(years, ipcc["min_t"], ipcc["max_t"], color=COLORS["ipcc"],
                    lw=0, label=L["ipcc"], zorder=1)
    ax.axhline(cfg["target"], color=COLORS["target"], lw=0.8, ls="--", zorder=2)
    lr = [datetime.fromisoformat(d) for d in cfg["likely_range"]]
    ax.plot(lr, [cfg["target"]] * 2, color=COLORS["target"], lw=4,
            solid_capstyle="butt", label=L["likely"], zorder=3)


def draw_frame(fig, data, L, upto: int | None = None, trend: dict | None = None):
    """Dessine une image.

    upto  : index du dernier mois affiché (animation « courbe »)
    trend : ligne de tendance à afficher (animation « extrapolation »)
    """
    fig.clf()
    ax = fig.add_axes([0.07, 0.12, 0.66, 0.76])
    cfg, mon = data["config"], data["monthly"]
    draw_background(ax, data, L)

    n = len(mon["month"]) if upto is None else upto + 1
    dates = [to_date(m) for m in mon["month"][:n]]
    vals = mon["anomaly_preindustrial"][:n]

    if trend is None:
        ax.plot(dates, vals, color=COLORS["series"], lw=1.2, label=L["series"], zorder=4)
        ax.plot(dates[-1], vals[-1], "o", color=COLORS["series"], ms=6, zorder=5)
        status = mon["status"][n - 1]
        info = [(L["month"], mon["month"][n - 1]),
                (L["anomaly"], f"{fmt_num(vals[-1], L['_lang'], True)} °C"
                 + (f" ({L['prelim']})" if status == "preliminary" else ""))]
    else:
        all_dates = [to_date(m) for m in mon["month"]]
        ax.plot(all_dates, mon["anomaly_preindustrial"], color=COLORS["series_light"],
                lw=1, label=L["series"], zorder=4)
        i0 = mon["month"].index(trend["window_start"])
        i1 = mon["month"].index(trend["window_end"])
        ax.plot(all_dates[i0:i1 + 1], mon["anomaly_preindustrial"][i0:i1 + 1],
                color=COLORS["window"], lw=1.3, label=L["window"], zorder=5)
        # Droite de tendance prolongée jusqu'à 1,5 °C (ou bord du graphe)
        m = trend["slope_per_decade"] / 120
        c = trend["intercept"]
        k_end = (cfg["target"] - c) / m if m > 0 else (i1 - i0)
        k_end = max(k_end, i1 - i0)
        start = all_dates[i0]
        xs = [start, _add_months(start, k_end)]
        ax.plot(xs, [c, c + m * k_end], color=COLORS["trend"], lw=2.2,
                label=L["trend"], zorder=6)
        info = [(L["from"], trend["window_end"]),
                (L["warming"], f"{fmt_num(trend['warming_at_end'], L['_lang'])} °C")]
        if trend["crossing_1_5"]:
            cx = to_date(trend["crossing_1_5"])
            ax.plot(cx, cfg["target"], "o", ms=9, mfc="white", mec=COLORS["trend"],
                    mew=2.2, label=L["crossing"], zorder=7)
            info.append((L["reach"], trend["crossing_1_5"]))

    style_axes(ax, cfg, L)
    ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0), frameon=False, fontsize=10)

    # Encadré d'information à droite, sous la légende
    sep = " : " if L["_lang"] == "fr" else ": "
    text = "\n".join(f"{k}{sep}{v}" for k, v in info)
    fig.text(0.755, 0.40, text, fontsize=12, fontweight="bold", va="top",
             color=COLORS["text"], linespacing=1.7)
    fig.text(0.07, 0.94, L["title"], fontsize=16, fontweight="bold")
    fig.text(0.07, 0.03, L["source"], fontsize=8, color="#555555")


def _add_months(d: datetime, k: float) -> datetime:
    """Ajoute k mois (réel) à une date, en approximation 30,4375 j/mois."""
    return d + timedelta(days=k * 30.4375)


# --------------------------------------------------------------------------
# Animations
# --------------------------------------------------------------------------
def select_frames(data, animation, debut, fin, pas):
    """Liste des (upto, trend) à dessiner pour une animation."""
    mon, tr = data["monthly"], data["trends"]
    if animation == "courbe":
        months = mon["month"]
        idx = [i for i, m in enumerate(months)
               if (debut is None or m >= debut) and (fin is None or m <= fin)]
        sel = idx[::pas]
        if idx and sel[-1] != idx[-1]:
            sel.append(idx[-1])          # toujours finir sur le dernier mois
        return [(i, None) for i in sel]
    rows = [dict(zip(tr.keys(), vals)) for vals in zip(*tr.values())]
    rows = [r for r in rows if (debut is None or r["window_end"] >= debut)
            and (fin is None or r["window_end"] <= fin)]
    sel = rows[::pas]
    if rows and sel[-1] != rows[-1]:
        sel.append(rows[-1])
    return [(None, r) for r in sel]


def render_animation(data, animation, out_dir: Path, *, lang="fr", debut=None,
                     fin=None, pas=1, fps=8, fmt="png", size=DEFAULT_SIZE_PX,
                     frames=True, gif=True, zip_frames=False) -> dict:
    """Génère les images et/ou le GIF d'une animation. Renvoie les chemins créés."""
    L = dict(LABELS[lang], _lang=lang)
    out_dir.mkdir(parents=True, exist_ok=True)
    frame_dir = out_dir / f"images_{animation}"
    if frames:
        if frame_dir.exists():
            shutil.rmtree(frame_dir)
        frame_dir.mkdir()
    fig = plt.figure(figsize=(size[0] / DPI, size[1] / DPI), dpi=DPI)
    gif_frames = []
    todo = select_frames(data, animation, debut, fin, pas)
    for k, (upto, trend) in enumerate(todo):
        draw_frame(fig, data, L, upto=upto, trend=trend)
        label = data["monthly"]["month"][upto] if trend is None else trend["window_end"]
        # Un seul rendu PNG par image, réutilisé pour le GIF et (si PNG) pour
        # les fichiers ; les autres formats redessinent, matplotlib ne
        # sérialise pas directement le SVG/JPG depuis le tampon.
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=DPI)
        if gif:
            # Palette adaptative : GIF nettement plus léger
            gif_frames.append(Image.open(buf).convert("RGB").quantize(colors=64))
        if frames:
            path = frame_dir / f"{animation}_{k:04d}_{label}.{fmt}"
            if fmt == "png":
                path.write_bytes(buf.getvalue())
            else:
                fig.savefig(path, dpi=DPI)
    plt.close(fig)

    created = {}
    if frames:
        created["frames"] = str(frame_dir)
        if zip_frames:
            zpath = out_dir / f"images_{animation}.zip"
            with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
                for f in sorted(frame_dir.iterdir()):
                    z.write(f, f.name)
            created["zip"] = str(zpath)
    if gif and gif_frames:
        gpath = out_dir / f"{animation}.gif"
        durations = [int(1000 / fps)] * len(gif_frames)
        durations[-1] = LAST_FRAME_HOLD_MS
        gif_frames[0].save(gpath, save_all=True, append_images=gif_frames[1:],
                           duration=durations, loop=0, optimize=True)
        created["gif"] = str(gpath)
    print(f"{animation} : {len(todo)} images → {out_dir}")
    return created


def render_static(data, out_dir: Path, *, lang="fr", fmt="png", size=DEFAULT_SIZE_PX):
    """Graphique actuel (dernière tendance), pour export."""
    L = dict(LABELS[lang], _lang=lang)
    out_dir.mkdir(parents=True, exist_ok=True)
    tr = data["trends"]
    latest = {k: v[-1] for k, v in tr.items()}
    fig = plt.figure(figsize=(size[0] / DPI, size[1] / DPI), dpi=DPI)
    draw_frame(fig, data, L, trend=latest)
    path = out_dir / f"graphique_{latest['window_end']}_{lang}.{fmt}"
    fig.savefig(path, dpi=DPI)
    plt.close(fig)
    return str(path)


def render_defaults(out_dir: Path) -> None:
    """Exports précalculés chaque mois par GitHub Actions (mode « téléchargement »)."""
    data = load_series(None)
    files = {}
    for lang in ("fr", "en"):
        for fmt in ("png", "svg"):
            files[f"static_{lang}_{fmt}"] = Path(render_static(data, out_dir, lang=lang, fmt=fmt)).name
    for anim, kw in {"courbe": dict(debut="1971-01", pas=3, fps=12),
                     "extrapolation": dict(debut=f"{C.FIRST_TREND_YEAR}-12", pas=1, fps=10)}.items():
        res = render_animation(data, anim, out_dir, zip_frames=True, **kw)
        shutil.rmtree(res["frames"])          # on ne publie que le zip
        files[f"{anim}_gif"] = Path(res["gif"]).name
        files[f"{anim}_zip"] = Path(res["zip"]).name
    (out_dir / "manifest.json").write_text(json.dumps(files, indent=2))


# --------------------------------------------------------------------------
def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--donnees", help="series.json (chemin ou URL) ; défaut : data/series.json")
    p.add_argument("--animation", choices=["courbe", "extrapolation", "both"], default="both")
    p.add_argument("--statique", action="store_true", help="uniquement le graphique actuel")
    p.add_argument("--debut", help="premier mois AAAA-MM")
    p.add_argument("--fin", help="dernier mois AAAA-MM")
    p.add_argument("--pas", type=int, default=1, help="un mois sur N")
    p.add_argument("--fps", type=float, default=8, help="images par seconde du GIF")
    p.add_argument("--format", default="png", choices=["png", "svg", "jpg", "pdf"])
    p.add_argument("--largeur", type=int, default=DEFAULT_SIZE_PX[0], help="pixels")
    p.add_argument("--hauteur", type=int, default=DEFAULT_SIZE_PX[1], help="pixels")
    p.add_argument("--langue", default="fr", choices=["fr", "en"])
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
                         pas=max(1, a.pas), fps=a.fps, fmt=a.format, size=size,
                         frames=not a.pas_d_images, gif=not a.pas_de_gif)
    return 0


if __name__ == "__main__":
    sys.exit(main())
