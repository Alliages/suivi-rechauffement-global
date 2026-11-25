/* Page de suivi : lit data/series.json (données + config du pipeline) et
   data/content.json (textes des onglets), tous deux générés par pipeline/. */

/* ======================================================================
   Paramètres
   ====================================================================== */
const DATA_URL = "data/series.json";
const CONTENT_URL = "data/content.json";
const TAB_IDS = ["apropos", "faq", "glossaire", "source"];
const TAB_ALIAS = { code: "source" };
const I18N = {
  fr: {
    title: "Suivi du réchauffement mondial et du seuil de 1,5\u00A0°C",
    updated: "Données jusqu’à {m}", updatedDate: "mise à jour le {d}",
    loadError: "Les données n’ont pas pu être chargées. Vérifiez votre connexion, puis réessayez.",
    allMonths: "un pas par mois sur le curseur",
    skip: "Aller au contenu", loading: "Chargement…", retry: "Réessayer", empty: "Contenu momentanément indisponible.",
    sliderLabel: "Fin de la fenêtre de 30 ans",
    chartLabel: "Graphique\u00A0: réchauffement mondial mensuel depuis 1850-1900, tendance linéaire sur 30 ans et date d’atteinte de 1,5\u00A0°C. Les valeurs clés sont reprises dans le texte au-dessus.",
    tabsLabel: "Sections de la page", glossaryLabel: "Termes du glossaire",
    pngLabel: "Graphique en PNG", svgLabel: "Graphique en SVG", jsonLabel: "Données en JSON",
    metaDesc: "Suivi mensuel du réchauffement mondial (ERA5, Copernicus) et estimation de la date d’atteinte de +1,5\u00A0°C par extrapolation de la tendance sur 30 ans.",
    syntheseTitle: "En {m}…",
    tabAbout: "Application", tabFaq: "FAQ", tabGlossary: "Glossaire", tabSource: "Code source",
    introTitle: "À quel point sommes-nous proches d’un réchauffement mondial de 1,5\u00A0°C\u00A0?",
    introText: "Atteindre 1,5\u00A0°C de réchauffement mondial par rapport aux niveaux préindustriels — la limite fixée par l’accord de Paris — peut sembler une réalité très lointaine, mais elle est peut-être plus proche qu’on ne le croit. Les experts estiment qu’il est probable qu’elle soit atteinte entre la fin des années 2020 et le début des années 2050. Voyez où en est le réchauffement aujourd’hui et quand cette limite serait atteinte s’il se poursuivait au rythme actuel.",
    synthese1: "Le réchauffement du mois {m1} est de\u00A0:",
    synthese2: "Le réchauffement mondial a atteint une valeur estimée à\u00A0:",
    synthese3: "Si la tendance sur 30 ans se poursuivait, le réchauffement mondial atteindrait {target} en\u00A0:",
    crossingHover: "Si la tendance de {years} ans menant à <b>{from}</b> se poursuit, la limite de {target} serait atteinte d’ici <b>{to}</b>.",
    exportsTitle: "Exports", exportsChart: "Graphique (vue actuelle)", exportsData: "Données",
    csvMonthly: "Série mensuelle (CSV)", csvTrends: "Tendances 30 ans (CSV)", csvIpcc: "Enveloppe GIEC (CSV)",
    ipcc: "Projections GIEC (SR15)", likely: "Fourchette GIEC 1,5\u00A0°C (2030-2052)",
    series: "Anomalie mensuelle ERA5", window: "Anomalie observée (fenêtre de 30 ans)",
    trend: "Tendance linéaire 30 ans",
    prelim: "provisoire", never: "non atteint",
    hoverTitle: "Changement de température observé",
    hoverSub: "Depuis l’époque préindustrielle (1850-1900)",
    methodTitle: "Méthode",
    method: [
      "Température de l’air à 2 m, moyenne mondiale ERA5 publiée par Copernicus, agrégée en moyennes mensuelles (mois complets uniquement).",
      "Anomalie par rapport à 1991-2020, convertie en anomalie par rapport à 1850-1900 en ajoutant un écart mensuel fixe ({omin} à {omax}\u00A0°C) issu du bulletin climatique C3S.",
      "Tendance\u00A0: régression linéaire sur 30 ans. La date d’atteinte de 1,5\u00A0°C est l’extrapolation de cette droite\u00A0; ce n’est pas une prévision.",
      "Les derniers mois sont provisoires (ERA5T) et peuvent être légèrement révisés.",
      "Méthode reprise du «\u00A0Global Temperature Trend Monitor\u00A0» de Copernicus C3S, réimplémentée dans cet outil pour une mise à jour automatique mensuelle.",
    ],
    footer: "Données\u00A0: Copernicus Climate Change Service (C3S) / ECMWF, ERA5. Projections\u00A0: GIEC SR15. Outil non officiel, ni produit ni approuvé par Copernicus.",
    c3sMention: "Le Copernicus Climate Change Service (C3S) est mis en œuvre par le Centre européen pour les prévisions météorologiques à moyen terme (ECMWF) pour le compte de la Commission européenne et fait partie du programme spatial de l’Union européenne.",
    footerLinks: 'Version {v} · <a href="https://github.com/Alliages/suivi-rechauffement-global">Code source</a> · <a href="https://apps.climate.copernicus.eu/global-temperature-trend-monitor/">Application originale (C3S)</a> · <a href="https://guillaume-meunier.fr/">Guillaume Meunier</a>',
  },
  en: {
    title: "Tracking global warming and the 1.5\u00A0°C threshold",
    updated: "Data up to {m}", updatedDate: "updated {d}",
    loadError: "The data could not be loaded. Check your connection, then try again.",
    allMonths: "one slider step per month",
    skip: "Skip to content", loading: "Loading…", retry: "Try again", empty: "Content temporarily unavailable.",
    sliderLabel: "End of the 30-year window",
    chartLabel: "Chart: monthly global warming since 1850-1900, 30-year linear trend and date when 1.5\u00A0°C is reached. Key values are repeated in the text above.",
    tabsLabel: "Page sections", glossaryLabel: "Glossary terms",
    pngLabel: "Chart as PNG", svgLabel: "Chart as SVG", jsonLabel: "Data as JSON",
    metaDesc: "Monthly tracker of global warming (ERA5, Copernicus) and estimate of when +1.5\u00A0°C is reached by extrapolating the 30-year trend.",
    syntheseTitle: "In {m}…",
    tabAbout: "Application", tabFaq: "FAQs", tabGlossary: "Glossary", tabSource: "Source code",
    introTitle: "How close are we to reaching a global warming of 1.5\u00A0°C?",
    introText: "Reaching 1.5\u00A0°C of global warming above pre-industrial levels — a limit agreed under the Paris Agreement — may feel like a very distant reality, but it might be closer than you think. Experts suggest it is likely to happen between the late 2020s and the early 2050s. See where global warming stands today and when the limit would be reached if it continued at today’s pace.",
    synthese1: "The warming in the month {m1} is:",
    synthese2: "Global warming has reached an estimated value of:",
    synthese3: "If the 30-year trend continued, global warming would reach {target} in:",
    crossingHover: "If the {years}-year warming trend leading up to <b>{from}</b> continued, the {target} limit would be reached by <b>{to}</b>.",
    exportsTitle: "Exports", exportsChart: "Chart (current view)", exportsData: "Data",
    csvMonthly: "Monthly series (CSV)", csvTrends: "30-year trends (CSV)", csvIpcc: "IPCC envelope (CSV)",
    ipcc: "IPCC projections (SR15)", likely: "IPCC 1.5\u00A0°C likely range (2030-2052)",
    series: "ERA5 monthly anomaly", window: "Observed anomaly (30-year window)",
    trend: "30-year linear trend",
    prelim: "preliminary", never: "not reached",
    hoverTitle: "Observed temperature change",
    hoverSub: "Since pre-industrial times (1850-1900)",
    methodTitle: "Method",
    method: [
      "2 m air temperature, ERA5 global mean published by Copernicus, aggregated to monthly means (complete months only).",
      "Anomaly relative to 1991-2020, converted to 1850-1900 by adding a fixed monthly offset ({omin} to {omax}\u00A0°C) from the C3S Climate Bulletin.",
      "Trend: 30-year linear regression. The 1.5\u00A0°C date extrapolates this line; it is not a forecast.",
      "The most recent months are preliminary (ERA5T) and may be slightly revised.",
      "Method taken from the Copernicus C3S “Global Temperature Trend Monitor”, reimplemented here for automatic monthly updates.",
    ],
    footer: "Data: Copernicus Climate Change Service (C3S) / ECMWF, ERA5. Projections: IPCC SR15. Unofficial tool, not produced or endorsed by Copernicus.",
    c3sMention: "The Copernicus Climate Change Service (C3S) is implemented by the European Centre for Medium-Range Weather Forecasts (ECMWF) on behalf of the European Commission and is part of the European Union’s space programme.",
    footerLinks: 'Version {v} · <a href="https://github.com/Alliages/suivi-rechauffement-global">Source code</a> · <a href="https://apps.climate.copernicus.eu/global-temperature-trend-monitor/">Original application (C3S)</a> · <a href="https://guillaume-meunier.fr/">Guillaume Meunier</a>',
  },
};

/* ======================================================================
   État
   ====================================================================== */
let DATA = null, CONTENT = null, APP_VERSION = null, COLORS = null;
let lang = "fr", steps = [], currentStep = 0;
const $ = (id) => document.getElementById(id);
const t = (k) => I18N[lang][k];
const NARROW = matchMedia("(max-width: 700px)"), COARSE = matchMedia("(pointer: coarse)");
const DTF = {};                                         // cache des Intl.DateTimeFormat (langue + style)
const dtf = (month) => (DTF[lang + month] ??= new Intl.DateTimeFormat(lang, { month, year: "numeric", timeZone: "UTC" }));
const fmt1 = (v) => v.toLocaleString(lang, { minimumFractionDigits: 1, maximumFractionDigits: 1 });
// Marques et sigles à ne pas faire traduire automatiquement par le navigateur
const nt = (html) => html.replace(/\b(ERA5T?|C3S|ECMWF|Copernicus|SR15|Guillaume Meunier)\b/g, '<span translate="no">$1</span>');

/* ---------- Formatage ---------- */
const toDate = (m) => m + "-15";                       // AAAA-MM → 15 du mois
const monthDate = (m) => { const [y, mo] = m.split("-").map(Number); return Date.UTC(y, mo - 1, 15); };
const fmtMonth = (m) => dtf("short").format(monthDate(m));
const monthFull = (m) => dtf("long").format(monthDate(m));
const fmtNum = (x, signed = false) =>
  (signed && x >= 0 ? "+" : "") + x.toLocaleString(lang, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
const targetLabel = () => `${DATA.config.target.toLocaleString(lang)}\u00A0°C`;
function addMonths(m, k) {                              // 'AAAA-MM' + k mois (réel) → date ISO
  const [y, mo] = m.split("-").map(Number);
  const d = new Date(Date.UTC(y, mo - 1, 15));
  d.setUTCDate(d.getUTCDate() + Math.round(k * DATA.config.days_per_month));
  return d.toISOString().slice(0, 10);
}

/* ======================================================================
   Graphique
   ====================================================================== */
function buildColors() {
  const pc = DATA.config.colors;
  COLORS = {
    ipcc: pc.peach_transparent, ipccLine: pc.peach, likely: pc.likely,
    series: pc.orange_transparent, marker: pc.orange, window: pc.orange,
    trend: pc.accent, target: pc.accent, grid: pc.grid, zeroline: pc.zeroline,
  };
}

function exportSize() {
  const [width, height] = DATA.config.export_size;
  return { width, height };
}

function trendRow(i) {
  const tr = DATA.trends;
  return Object.fromEntries(Object.keys(tr).map((k) => [k, tr[k][i]]));
}

function trendTraces(row) {
  const mon = DATA.monthly, cfg = DATA.config;
  const i0 = mon.month.indexOf(row.window_start), i1 = mon.month.indexOf(row.window_end);
  const m = row.slope_per_decade / 120, c = row.intercept;
  const kEnd = Math.max(m > 0 ? (cfg.target - c) / m : 0, i1 - i0);
  const reaches = row.crossing_1_5 && i1 - i0 < kEnd;
  return {
    window: { x: mon.month.slice(i0, i1 + 1).map(toDate), y: mon.anomaly_preindustrial.slice(i0, i1 + 1) },
    trend: {
      x: [toDate(row.window_start), reaches ? toDate(row.crossing_1_5) : addMonths(row.window_start, kEnd)],
      y: [c, reaches ? cfg.target : c + m * kEnd],
    },
    cross: row.crossing_1_5 ? { x: [toDate(row.crossing_1_5)], y: [cfg.target] } : { x: [], y: [] },
    current_y: row.warming_at_end,
  };
}

function yTicks([y0, y1]) {
  const step = DATA.config.grid_step;
  const vals = [];
  for (let v = Math.ceil(y0 / step) * step; v <= y1 + 1e-9; v += step) vals.push(+v.toFixed(1));
  return {
    tickmode: "array", tickvals: vals,
    ticktext: vals.map((v, i) => i === vals.length - 1 ? `${fmt1(v)}\u00A0°C` : fmt1(v)),
  };
}

function stepLabel(i) {
  const row = trendRow(steps[i]);
  return /^\d{4}$/.test(row.step_label) ? row.step_label : fmtMonth(row.window_end);
}

function stepAnnotations(row, tt) {
  const cfg = DATA.config;
  const cal = (m) => `<b>${fmtMonth(m)}</b>`;
  return [
    {
      text: ` <b>${targetLabel()}</b> `, xref: "paper", x: 1, xshift: 8,
      y: cfg.target, xanchor: "left", yanchor: "middle",
      showarrow: true, arrowhead: 2, arrowsize: 1, arrowwidth: 1.5, arrowcolor: COLORS.trend,
      ax: 0, axref: "pixel", ay: -34, ayref: "pixel",
      font: { color: COLORS.trend, size: 15 },
    },
    {
      text: ` <b>${fmtNum(tt.current_y)}\u00A0°C</b> `, xref: "paper", x: 1, xshift: 6,
      y: tt.current_y, xanchor: "left", yanchor: "middle",
      showarrow: false, font: { color: COLORS.marker, size: 15 },
    },
    {
      text: cal(row.window_start), x: toDate(row.window_start), y: -0.02,
      xanchor: "center", yanchor: "top", showarrow: false,
      font: { color: COLORS.marker, size: 14 }, bgcolor: "white",
      bordercolor: COLORS.marker, borderwidth: 2, borderpad: 2,
    },
    row.crossing_1_5 ? {
      text: cal(row.crossing_1_5), x: toDate(row.crossing_1_5), y: -0.02,
      xanchor: "center", yanchor: "top", showarrow: false,
      font: { color: COLORS.trend, size: 14 }, bgcolor: "white",
      bordercolor: COLORS.trend, borderwidth: 2, borderpad: 2,
    } : { text: "", showarrow: false },
  ];
}

function layout() {
  const cfg = DATA.config;
  const narrow = NARROW.matches;
  // Mode « un pas par mois » : étiquettes du curseur espacées pour rester lisibles
  const every = $("all-months").checked ? Math.ceil(steps.length / 12) : 1;
  const showLabel = (i) => (steps.length - 1 - i) % every === 0;
  const axis = { ticks: "outside", tickwidth: 1.5, tickfont: { size: 12 }, showgrid: false,
                 showline: false, zeroline: false };
  return {
    margin: narrow ? { l: 52, r: 66, t: 120, b: 130 } : { l: 70, r: 70, t: 130, b: 80 },
    separators: lang === "fr" ? ",\u00A0" : ".,",
    font: { family: "system-ui, -apple-system, Segoe UI, Roboto, sans-serif", color: "#1d1d1f", size: 14 },
    xaxis: { ...axis, type: "date", range: cfg.x_view, dtick: "M120", tickformat: "%Y" },
    yaxis: { ...axis, range: cfg.y_range, showgrid: true, griddash: "dot", gridcolor: COLORS.grid,
             gridwidth: 1, zeroline: true, zerolinecolor: COLORS.zeroline, zerolinewidth: 1.5,
             fixedrange: true, ...yTicks(cfg.y_range) },
    legend: { x: 0.5, y: narrow ? -0.2 : -0.10, xanchor: "center", yanchor: "top", orientation: "h", font: { size: 12 } },
    hovermode: "closest",
    dragmode: COARSE.matches ? false : "zoom",      // tactile : ne pas capter le défilement de la page
    sliders: [{
      active: currentStep,
      x: 0, xanchor: "left", y: 1.24, len: 1,
      pad: { l: 0, r: 0, t: 0, b: 4 },
      font: { size: 12 },
      steps: steps.map((rowIdx, i) => ({ label: showLabel(i) ? stepLabel(i) : "", value: rowIdx, method: "skip", execute: false })),
    }],
    plot_bgcolor: "#fff", paper_bgcolor: "#fff",
  };
}

function staticTraces() {
  const mon = DATA.monthly, ipcc = DATA.ipcc, cfg = DATA.config;
  const yrs = ipcc.year.map((y) => `${y}-01-01`);
  return [
    { x: yrs, y: ipcc.min_t, mode: "lines", line: { width: 0 }, hoverinfo: "skip", showlegend: false },
    { x: yrs, y: ipcc.max_t, mode: "lines", line: { width: 0 }, fill: "tonexty",
      fillcolor: COLORS.ipcc, name: t("ipcc"), hoverinfo: "skip" },
    { x: cfg.likely_range, y: [cfg.target, cfg.target], mode: "lines+markers", name: t("likely"),
      line: { color: COLORS.likely, width: 3 },
      marker: { symbol: "diamond", size: 7, color: "white",
                line: { width: 3, color: COLORS.likely } },
      hoverinfo: "skip", showlegend: true },
    { x: mon.month.map(toDate), y: mon.anomaly_preindustrial, mode: "lines", name: t("series"),
      line: { color: COLORS.series, width: 1 },
      customdata: mon.month.map((m, i) => [fmtMonth(m), mon.status[i] === "preliminary" ? ` (${t("prelim")})` : ""]),
      hovertemplate: `<b>${t("hoverTitle")}</b><br>${t("hoverSub")}<br>%{customdata[0]} - %{y:+.2f}\u00A0°C%{customdata[1]}<extra></extra>`,
      hoverlabel: { bgcolor: COLORS.marker, font: { color: "#1d1d1f" } } },
  ];
}

function dynamicTraces(row, tt) {
  const cfg = DATA.config, xRight = cfg.x_range[1], yEnd = tt.current_y;
  const hoverCross = t("crossingHover")
    .replaceAll("{years}", DATA.meta.trend_years)
    .replaceAll("{from}", fmtMonth(row.window_end))
    .replaceAll("{target}", targetLabel())
    .replaceAll("{to}", row.crossing_1_5 ? fmtMonth(row.crossing_1_5) : t("never"));
  const line = (x, y, color, extra = {}) => ({ x, y, mode: "lines", line: { color, width: 1 },
    hoverinfo: "skip", showlegend: false, ...extra });
  const cross = row.crossing_1_5 && toDate(row.crossing_1_5);
  return [
    { ...tt.window, mode: "lines+markers", name: t("window"), showlegend: false,
      line: { color: COLORS.window, width: 1.2 },
      marker: { size: 6, color: "white", line: { width: 1, color: COLORS.window } }, hoverinfo: "skip" },
    line([toDate(row.window_start), toDate(row.window_start)], [tt.trend.y[0], 0], COLORS.marker),
    line([toDate(row.window_end), xRight], [yEnd, yEnd], COLORS.marker, { line: { color: COLORS.marker, width: 2, dash: "dot" } }),
    cross ? line([cross, cross], [cfg.target, 0], COLORS.trend) : line([], [], COLORS.trend),
    cross
      ? line([cross, xRight], [cfg.target, cfg.target], COLORS.trend,
             { line: { color: COLORS.trend, width: 2, dash: "dot" } })
      : line([], [], COLORS.trend),
    // Liseré blanc sous la tendance
    { x: tt.trend.x, y: tt.trend.y, mode: "lines", line: { color: "white", width: 5 },
      hoverinfo: "skip", showlegend: false },
    { x: tt.trend.x, y: tt.trend.y, mode: "lines", name: t("trend"),
      line: { color: COLORS.trend, width: 2.5 }, hoverinfo: "skip" },
    { ...tt.cross, mode: "markers", showlegend: false, text: [hoverCross],
      hovertemplate: "%{text}<extra></extra>",
      hoverlabel: { bgcolor: COLORS.trend, font: { color: "#fff" } },
      marker: { size: 15, color: "rgba(255, 255, 255, 0.5)", line: { color: COLORS.trend, width: 1.5 } } },
  ];
}

function draw() {
  currentStep = Math.min(currentStep, steps.length - 1);
  const row = trendRow(steps[currentStep]);
  const tt = trendTraces(row);
  Plotly.react("chart", [...staticTraces(), ...dynamicTraces(row, tt)],
    { ...layout(), annotations: stepAnnotations(row, tt) },
    { responsive: true, displaylogo: false,
      modeBarButtonsToRemove: ["select2d", "lasso2d"],
      toImageButtonOptions: { ...exportSize(), filename: fileStem() } })
    .then(() => {
      updateCards(row);
      attachSliderEvents();
      syncStepper();
    });
}

function applyStep(i) {
  const chart = $("chart");
  const row = trendRow(steps[i]);
  const tt = trendTraces(row);
  const dyn = dynamicTraces(row, tt);
  const first = chart.data.length - dyn.length;          // les traces dynamiques sont en fin de liste
  Plotly.restyle(chart, {
    x: dyn.map((tr) => tr.x),
    y: dyn.map((tr) => tr.y),
    text: dyn.map((tr) => tr.text || null),
  }, dyn.map((_, k) => first + k));
  Plotly.relayout(chart, { annotations: stepAnnotations(row, tt) });
  updateCards(row);
  currentStep = i;
  syncStepper();
  syncUrl();
}

function syncStepper() {                               // curseur natif : alternative clavier au curseur Plotly
  const range = $("step-range"), n = steps.length;
  $("stepper").hidden = n < 2;
  range.max = n - 1;
  range.value = currentStep;
  const label = stepLabel(currentStep);
  range.setAttribute("aria-valuetext", label);
  $("step-out").textContent = label;
}

let urlTimer;
function syncUrl() {                                   // langue, pas du curseur et option dans l'URL (anti-rafale)
  clearTimeout(urlTimer);
  urlTimer = setTimeout(() => {
    const p = new URLSearchParams({ lang });
    if ($("all-months").checked) p.set("all", "1");
    if (currentStep < steps.length - 1) p.set("m", trendRow(steps[currentStep]).window_end);
    try { history.replaceState(null, "", `${location.pathname}?${p}${location.hash}`); } catch (_) {}
  }, 250);
}

function attachSliderEvents() {
  const chart = $("chart");
  if (chart._sliderHooked) return;
  chart._sliderHooked = true;
  chart.on("plotly_sliderchange", (ev) => {
    const s = ev.slider && typeof ev.slider.active === "number" ? ev.slider
      : chart._fullLayout && chart._fullLayout.sliders && chart._fullLayout.sliders[0];
    const idx = s && typeof s.active === "number" ? s.active : currentStep;
    if (idx !== currentStep && idx >= 0 && idx < steps.length) applyStep(idx);
  });
}

/* ======================================================================
   Textes, synthèse, onglets
   ====================================================================== */
function updateCards(row) {
  const mon = DATA.monthly, n = mon.month.length - 1;
  $("quand").innerHTML = t("syntheseTitle").replace("{m}", monthFull(row.window_end));
  $("s-month").innerHTML = `${fmtNum(mon.anomaly_preindustrial[n], true)}\u00A0°C` +
    (mon.status[n] === "preliminary" ? ` <span class="prelim">(${t("prelim")})</span>` : "");
  $("s-warming").textContent = `${fmtNum(row.warming_at_end, true)}\u00A0°C`;
  $("s-crossing").textContent = row.crossing_1_5 ? fmtMonth(row.crossing_1_5) : t("never");
}

function buildSteps() {
  const tr = DATA.trends, all = $("all-months").checked;
  steps = tr.window_end.map((_, i) => i).filter((i) => all || tr.is_slider_step[i]);
  currentStep = steps.length - 1;
}

function renderGlossary() {
  const list = $("glossary-list"), defBox = $("glossary-def");
  list.innerHTML = "";
  defBox.innerHTML = "";
  const terms = (CONTENT && CONTENT[lang] && CONTENT[lang].glossary) || [];
  terms.forEach((item, i) => {
    const li = document.createElement("li");
    const btn = document.createElement("button");
    btn.textContent = item.term;
    btn.setAttribute("aria-current", i === 0 ? "true" : "false");
    btn.addEventListener("click", () => {
      list.querySelectorAll("button").forEach((b) => b.setAttribute("aria-current", b === btn ? "true" : "false"));
      defBox.innerHTML = item.def;
    });
    li.appendChild(btn);
    list.appendChild(li);
  });
  defBox.innerHTML = terms.length ? terms[0].def : `<p class="empty">${t("empty")}</p>`;
}

function renderFaq() {
  const list = $("faq-list");
  const wasOpen = [...list.querySelectorAll("details")].map((d) => d.open);   // conserve l'état au changement de langue
  list.innerHTML = "";
  const items = (CONTENT && CONTENT[lang] && CONTENT[lang].faq) || [];
  if (!items.length) { list.innerHTML = `<li class="empty">${t("empty")}</li>`; return; }
  items.forEach((item, i) => {
    const li = document.createElement("li");
    const det = document.createElement("details");          // natif : clavier, état ouvert/fermé annoncé
    det.open = wasOpen.length === items.length ? wasOpen[i] : i === 0;
    const sum = document.createElement("summary");
    const h3 = document.createElement("h3");
    h3.textContent = item.q;
    sum.appendChild(h3);
    const body = document.createElement("div");
    body.className = "body";
    body.innerHTML = item.a;
    det.append(sum, body);
    li.appendChild(det);
    list.appendChild(li);
  });
}

function initTabs() {
  const btns = [...document.querySelectorAll("#tabs button")];
  const fromHash = () => {
    const h = location.hash.slice(1), name = TAB_ALIAS[h] || h;
    return TAB_IDS.includes(name) ? name : "apropos";
  };
  const current = () => btns.find((b) => b.getAttribute("aria-selected") === "true").dataset.tab;
  const activate = (name) => {
    btns.forEach((b) => {
      const on = b.dataset.tab === name;
      b.setAttribute("aria-selected", on);
      b.tabIndex = on ? 0 : -1;                          // tabindex itinérant : une seule tabulation pour la liste
    });
    TAB_IDS.forEach((id) => { $("panel-" + id).hidden = id !== name; });
  };
  const go = (name) => {                                 // clic / clavier : entrée d'historique + URL
    if (name === current()) return;
    activate(name);
    history.pushState(null, "", location.pathname + location.search + (name === "apropos" ? "" : "#" + name));
  };
  btns.forEach((btn, i) => {
    btn.addEventListener("click", () => go(btn.dataset.tab));
    btn.addEventListener("keydown", (e) => {            // flèches, Début, Fin
      const k = { ArrowRight: i + 1, ArrowLeft: i - 1, Home: 0, End: btns.length - 1 }[e.key];
      if (k === undefined) return;
      e.preventDefault();
      const next = btns[(k + btns.length) % btns.length];
      next.focus();
      go(next.dataset.tab);
    });
  });
  window.addEventListener("popstate", () => activate(fromHash()));
  window.addEventListener("hashchange", () => activate(fromHash()));
  activate(fromHash());
}

function applyStatic() {                                 // libellés indépendants des données
  document.documentElement.lang = lang;
  document.querySelectorAll("[data-i18n]").forEach((el) => { el.textContent = t(el.dataset.i18n); });
  document.querySelectorAll("[data-i18n-label]").forEach((el) => el.setAttribute("aria-label", t(el.dataset.i18nLabel)));
  document.querySelectorAll(".lang button").forEach((b) => b.setAttribute("aria-pressed", b.dataset.lang === lang));
  document.querySelector('meta[name="description"]').content = t("metaDesc");
  document.title = t("title");
}

function renderContent() {                               // onglets et pied de page (content.json)
  renderGlossary();
  renderFaq();
  $("source-content").innerHTML = (CONTENT && CONTENT[lang] && CONTENT[lang].source) || `<p class="empty">${t("empty")}</p>`;
  $("footer").innerHTML = `<div class="footer-inner"><p class="credit">${nt(t("footer"))}</p>`
    + `<p class="credit mention">${nt(t("c3sMention"))}</p>`
    + `<p class="credit">${nt(t("footerLinks").replace("{v}", APP_VERSION ?? "—"))}</p></div>`;
}

function applyLang() {
  applyStatic();
  renderContent();
  const mon = DATA.monthly, n = mon.month.length - 1, meta = DATA.meta;
  $("synthese").innerHTML = `
    <p class="p1">${t("synthese1").replace("{m1}", monthFull(mon.month[n]))} <strong class="v v-orange" id="s-month"></strong></p>
    <div class="encart" id="encart">
      <h2 class="quand" id="quand"></h2>
      <p>${t("synthese2")} <strong class="v v-red" id="s-warming"></strong></p>
      <p>${t("synthese3").replace("{target}", targetLabel())} <strong class="v v-red" id="s-crossing"></strong></p>
    </div>`;
  const off = meta.monthly_offsets;
  $("method").innerHTML = t("method").map((li) => `<li>${nt(li
    .replace("{omin}", fmtNum(Math.min(...off))).replace("{omax}", fmtNum(Math.max(...off))))}</li>`).join("");
  $("updated").innerHTML = t("updated").replace("{m}", fmtMonth(meta.last_month))
    + "<br>" + t("updatedDate").replace("{d}", new Date(meta.generated_at).toLocaleDateString(lang));
  draw();
}

/* ======================================================================
   Exports
   ====================================================================== */
function fileStem() {
  const row = trendRow(steps[currentStep]);
  return `rechauffement_1-5C_extrapolation-${row.window_end}_${lang}`;
}

/* ======================================================================
   Démarrage
   ====================================================================== */
async function fetchOptional(url, as = "json") {
  try {
    const res = await fetch(url, { cache: "no-cache" });
    return res.ok ? await res[as]() : null;
  } catch (_) { return null; }
}

$("exports").addEventListener("click", (e) => {
  const fmt = e.target.dataset && e.target.dataset.export;
  if (fmt) Plotly.downloadImage("chart", { format: fmt, ...exportSize(), filename: fileStem() });
});
$("all-months").addEventListener("change", () => { if (!DATA) return; buildSteps(); draw(); syncUrl(); });
$("step-range").addEventListener("input", (e) => {       // alternative clavier au curseur Plotly
  if (!DATA) return;
  const i = +e.target.value;
  applyStep(i);
  Plotly.relayout("chart", { "sliders[0].active": i });
});
document.querySelectorAll(".lang button").forEach((b) =>
  b.addEventListener("click", () => setLang(b.dataset.lang)));
NARROW.addEventListener("change", () => { if (DATA) draw(); });

function detectLang() {                                  // ?lang= > choix mémorisé > langues du navigateur
  let saved = null;
  try { saved = localStorage.getItem("lang"); } catch (_) {}
  const prefs = [new URLSearchParams(location.search).get("lang"), saved, ...(navigator.languages || [navigator.language])];
  return prefs.map((l) => (l || "").slice(0, 2)).find((l) => l === "fr" || l === "en") || "en";
}

function setLang(l) {
  lang = l;
  try { localStorage.setItem("lang", l); } catch (_) {}
  if (DATA) { applyLang(); syncUrl(); }
  else { applyStatic(); renderContent(); showError(); }
}

function showError() {
  $("synthese").innerHTML = `<div role="alert"><p class="load-error">${t("loadError")}</p>`
    + `<button type="button" id="retry">${t("retry")}</button></div>`;
  $("retry").addEventListener("click", init);
}

async function init() {
  lang = detectLang();
  applyStatic();
  $("synthese").innerHTML = `<p class="loading">${t("loading")}</p>`;
  [DATA, CONTENT, APP_VERSION] = await Promise.all([
    fetchOptional(DATA_URL), fetchOptional(CONTENT_URL), fetchOptional("VERSION", "text"),
  ]);
  APP_VERSION = APP_VERSION && APP_VERSION.trim();
  document.querySelector(".method").hidden = !DATA;
  if (!DATA) { renderContent(); showError(); return; }   // onglets FAQ/glossaire restent utilisables
  buildColors();
  const q = new URLSearchParams(location.search);
  $("all-months").checked = q.get("all") === "1";
  buildSteps();
  const k = steps.findIndex((r) => DATA.trends.window_end[r] === q.get("m"));
  if (k >= 0) currentStep = k;
  applyLang();
  syncUrl();
}

initTabs();
init();
