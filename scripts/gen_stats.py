#!/usr/bin/env python3
"""Генерирует карточки языков и активности в чёрно-белой манга-стилистике.

Языки различаются не цветом, а скринтоном — точками разной плотности,
диагональной штриховкой и заливкой, как в печатной манге. Пишет по два файла
на карточку, светлый и тёмный, README выбирает нужный тегом <picture>.

Данные берутся из GitHub API, картинки коммитятся в репозиторий, поэтому
профиль не зависит от сторонних сервисов, которые имеют обыкновение падать.
"""
import json, os, sys, urllib.request, urllib.error
from collections import Counter

USER = os.environ.get("GH_USER", "juijitsu")
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN", "")
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")

FONT = "'Segoe UI',system-ui,-apple-system,sans-serif"
NL = "\n"

# Семь скринтонов. Порядок задаёт очередь языков: от сплошной заливки к воздуху.
TONES = [
    ("solid", None),
    ("dots-dense", 2.3),
    ("diag", None),
    ("dots-mid", 1.7),
    ("cross", None),
    ("dots-thin", 1.1),
    ("dots-faint", 0.7),
]


def palette(dark):
    """Чернила и бумага. На тёмной теме роли меняются местами."""
    if dark:
        return dict(ink="#F0F0F0", paper="#0D1117", dim="#9AA0A6", rule="#3A3F46")
    return dict(ink="#16181D", paper="#FFFFFF", dim="#5B6169", rule="#D5D9DE")


def defs(dark):
    """Определения скринтонов. Точки рисуются чернилами по прозрачному фону."""
    c = palette(dark)
    p = ["<defs>"]
    for name, r in TONES:
        if name == "solid":
            continue
        p.append('<pattern id="%s" width="7" height="7" patternUnits="userSpaceOnUse">' % name)
        if r is not None:
            p.append('<circle cx="3.5" cy="3.5" r="%.1f" fill="%s"/>' % (r, c["ink"]))
        elif name == "diag":
            p.append('<path d="M-1 5 L5 -1 M1 8 L8 1" stroke="%s" stroke-width="2.1"/>' % c["ink"])
        elif name == "cross":
            p.append('<path d="M-1 5 L5 -1 M1 8 L8 1 M-1 2 L2 -1 M5 8 L8 5" stroke="%s" stroke-width="1.2"/>' % c["ink"])
            p.append('<path d="M-1 2 L8 11 M-1 -1 L8 8" stroke="%s" stroke-width="1.2"/>' % c["ink"])
        p.append("</pattern>")
    p.append("</defs>")
    return NL.join(p)


def fill_for(i, dark):
    name = TONES[i % len(TONES)][0]
    return palette(dark)["ink"] if name == "solid" else "url(#%s)" % name


def style(dark):
    c = palette(dark)
    return ("<style>" + NL
            + "  .t { fill:%s; font-family:%s; }" % (c["ink"], FONT) + NL
            + "  .lg { fill:%s; font-family:%s; }" % (c["dim"], FONT) + NL
            + "  .rule { stroke:%s; fill:none; }" % c["rule"] + NL
            + "  .sw { stroke:%s; stroke-width:1; }" % c["rule"] + NL
            + "</style>")


def api(url):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "juijitsu-profile"}
    if TOKEN:
        headers["Authorization"] = "Bearer " + TOKEN
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as r:
        return json.load(r)


def graphql(query):
    body = json.dumps({"query": query}).encode()
    req = urllib.request.Request("https://api.github.com/graphql", data=body, headers={
        "Authorization": "Bearer " + TOKEN,
        "User-Agent": "juijitsu-profile",
        "Content-Type": "application/json",
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ── языки ─────────────────────────────────────────────────────────────────────
def collect_languages():
    totals, page = Counter(), 1
    while True:
        repos = api("https://api.github.com/users/%s/repos?type=owner&per_page=100&page=%d" % (USER, page))
        if not repos:
            break
        for r in repos:
            if r.get("fork") or r.get("archived"):
                continue
            try:
                for lang, n in api(r["languages_url"]).items():
                    totals[lang] += n
            except urllib.error.HTTPError:
                pass
        if len(repos) < 100:
            break
        page += 1
    return totals


def render_languages(totals, dark, top=6):
    W, BAR_Y, BAR_H, PAD = 480, 36, 16, 16
    c = palette(dark)
    items = totals.most_common(top)
    other = sum(totals.values()) - sum(n for _, n in items)
    if other > 0:
        items.append(("Other", other))
    grand = sum(n for _, n in items) or 1

    rows = (len(items) + 1) // 2
    H = BAR_Y + BAR_H + 20 + rows * 21 + 8
    span = W - 2 * PAD

    p = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" role="img" aria-label="Languages">' % (W, H, W, H)]
    p.append(defs(dark))
    p.append(style(dark))
    p.append('<text class="t" x="%d" y="24" font-size="14" font-weight="700" letter-spacing="0.5">LANGUAGES</text>' % PAD)

    # полоса: сегменты рисуются скринтоном внутри общей рамки
    p.append('<clipPath id="clip"><rect x="%d" y="%d" width="%d" height="%d"/></clipPath>' % (PAD, BAR_Y, span, BAR_H))
    p.append('<g clip-path="url(#clip)">')
    x = float(PAD)
    for i, (_, n) in enumerate(items):
        w = span * n / grand
        p.append('<rect x="%.2f" y="%d" width="%.2f" height="%d" fill="%s"/>' % (x, BAR_Y, w, BAR_H, fill_for(i, dark)))
        x += w
    p.append("</g>")
    # разделители сегментов и внешняя рамка — чернилами
    x = float(PAD)
    for i, (_, n) in enumerate(items[:-1]):
        x += span * n / grand
        p.append('<line class="rule" x1="%.2f" y1="%d" x2="%.2f" y2="%d" stroke-width="1.5"/>' % (x, BAR_Y, x, BAR_Y + BAR_H))
    p.append('<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="%s" stroke-width="1.5"/>' % (PAD, BAR_Y, span, BAR_H, c["ink"]))

    ly = BAR_Y + BAR_H + 28
    for i, (lang, n) in enumerate(items):
        lx = PAD + (i % 2) * (span // 2)
        yy = ly + (i // 2) * 21
        p.append('<rect class="sw" x="%d" y="%d" width="11" height="11" fill="%s"/>' % (lx, yy - 9, fill_for(i, dark)))
        p.append('<text class="lg" x="%d" y="%d" font-size="12">%s <tspan opacity="0.7">%.1f%%</tspan></text>'
                 % (lx + 18, yy, esc(lang), 100.0 * n / grand))
    p.append("</svg>")
    return NL.join(p)


# ── календарь активности ──────────────────────────────────────────────────────
def collect_calendar():
    q = ('{ user(login: "%s") { contributionsCollection { contributionCalendar { '
         'totalContributions weeks { contributionDays { date contributionCount weekday } } } } } }') % USER
    cal = graphql(q)["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    return cal["weeks"], cal["totalContributions"]


def render_activity(weeks, total, dark, n_weeks=20):
    weeks = weeks[-n_weeks:]
    CELL, GAP, PAD, TOP, W = 12, 4, 16, 36, 480
    c = palette(dark)
    grid_w = len(weeks) * (CELL + GAP) - GAP
    x0 = (W - grid_w) // 2
    H = TOP + 7 * (CELL + GAP) - GAP + 28
    peak = max((d["contributionCount"] for w in weeks for d in w["contributionDays"]), default=0)

    # уровень -> индекс скринтона: пусто, редкие точки, средние, плотные, заливка
    LEVEL_TONE = ["dots-faint", "dots-thin", "dots-mid", "dots-dense", "solid"]

    def level(n):
        if n <= 0:
            return 0
        if peak <= 1:
            return 3
        r = n / peak
        return 1 if r <= .25 else 2 if r <= .5 else 3 if r <= .75 else 4

    def cell_fill(lv):
        t = LEVEL_TONE[lv]
        return c["ink"] if t == "solid" else "url(#%s)" % t

    p = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" role="img" aria-label="Activity">' % (W, H, W, H)]
    p.append(defs(dark))
    p.append(style(dark))
    p.append('<text class="t" x="%d" y="24" font-size="14" font-weight="700" letter-spacing="0.5">ACTIVITY</text>' % PAD)
    p.append('<text class="lg" x="%d" y="24" font-size="12" text-anchor="end">%d contributions this year</text>' % (W - PAD, total))

    for wi, w in enumerate(weeks):
        for d in w["contributionDays"]:
            lv = level(d["contributionCount"])
            p.append('<rect class="sw" x="%d" y="%d" width="%d" height="%d" fill="%s"><title>%s: %d</title></rect>'
                     % (x0 + wi * (CELL + GAP), TOP + d["weekday"] * (CELL + GAP), CELL, CELL,
                        cell_fill(lv), d["date"], d["contributionCount"]))

    ly = TOP + 7 * (CELL + GAP) + 8
    p.append('<text class="lg" x="%d" y="%d" font-size="11">Less</text>' % (x0, ly + 10))
    for i in range(5):
        p.append('<rect class="sw" x="%d" y="%d" width="12" height="12" fill="%s"/>' % (x0 + 34 + i * 16, ly, cell_fill(i)))
    p.append('<text class="lg" x="%d" y="%d" font-size="11">More</text>' % (x0 + 34 + 5 * 16 + 4, ly + 10))
    p.append("</svg>")
    return NL.join(p)


def main():
    os.makedirs(OUT, exist_ok=True)
    totals = collect_languages()
    if not totals:
        print("нет данных по языкам", file=sys.stderr)
        return 1
    for dark, suf in ((False, ""), (True, "-dark")):
        with open(os.path.join(OUT, "languages%s.svg" % suf), "w", encoding="utf-8") as f:
            f.write(render_languages(totals, dark))
    print("languages:", ", ".join("%s %d" % kv for kv in totals.most_common(6)))

    if not TOKEN:
        print("нет токена — календарь пропущен", file=sys.stderr)
        return 0
    weeks, total = collect_calendar()
    for dark, suf in ((False, ""), (True, "-dark")):
        with open(os.path.join(OUT, "activity%s.svg" % suf), "w", encoding="utf-8") as f:
            f.write(render_activity(weeks, total, dark))
    print("activity: %d вкладов за год" % total)
    return 0


if __name__ == "__main__":
    sys.exit(main())
