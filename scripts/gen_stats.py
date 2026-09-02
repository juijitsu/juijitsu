#!/usr/bin/env python3
"""Генерирует карточки языков и активности в палитре Sakura.

Пишет по два файла на карточку — светлый и тёмный, — а README выбирает нужный
тегом <picture>. Данные берутся из GitHub API, картинки коммитятся в репозиторий,
поэтому профиль не зависит от сторонних сервисов, которые имеют обыкновение падать.
"""
import json, os, sys, urllib.request, urllib.error
from collections import Counter

USER = os.environ.get("GH_USER", "amirk-dev")
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN", "")
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")

# ── палитра Sakura ────────────────────────────────────────────────────────────
PINK, LAV, MINT = "#FF8FB1", "#C8A2E0", "#7FD1B9"
PEACH, ROSE, IRIS, SKY = "#FFC49B", "#FFC0D9", "#B98BD9", "#9AD5E8"
WHEEL = [PINK, LAV, MINT, PEACH, IRIS, SKY, ROSE]
# шкала интенсивности календаря: от бледной сакуры к насыщенной
HEAT = ["#F6E6F0", "#FFD6E6", "#FFACC9", "#FF8FB1", "#E8629A"]
HEAT_DARK = ["#2A2130", "#4D2F45", "#8A4A6E", "#D9739F", "#FF8FB1"]

FONT = "'Segoe UI',system-ui,-apple-system,sans-serif"
NL = "\n"


# Нейтральная схема: читается и на светлом, и на тёмном фоне. Нужна потому,
# что GitHub оборачивает <img> внутри <picture> в ссылку, а <source> действует
# только на прямого потомка — переключение темы может не сработать.
HEAT_NEUTRAL = ["#B98BD933", "#FFACC966", "#FF8FB199", "#FF8FB1", "#E8629A"]


def style(dark, heat=False):
    """Цвета под тему. dark=False даёт нейтральный вариант для обеих тем."""
    if dark:
        title, label, track, scale = "#E7D3F2", "#C9AEDD", "#2A2130", HEAT_DARK
    else:
        title, label, track, scale = "#A97BC4", "#9B7BB8", "#B98BD92E", HEAT_NEUTRAL
    rules = NL.join("  .h%d { fill:%s; }" % (i, scale[i]) for i in range(5)) if heat else ""
    return (
        "<style>" + NL
        + "  .t { fill:%s; font-family:%s; }" % (title, FONT) + NL
        + "  .lg { fill:%s; font-family:%s; }" % (label, FONT) + NL
        + "  .track { fill:%s; }" % track + NL
        + (rules + NL if rules else "")
        + "</style>"
    )


def api(url):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "amirk-dev-profile"}
    if TOKEN:
        headers["Authorization"] = "Bearer " + TOKEN
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as r:
        return json.load(r)


def graphql(query):
    body = json.dumps({"query": query}).encode()
    req = urllib.request.Request("https://api.github.com/graphql", data=body, headers={
        "Authorization": "Bearer " + TOKEN,
        "User-Agent": "amirk-dev-profile",
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
    W, BAR_Y, BAR_H, PAD = 480, 34, 14, 16
    items = totals.most_common(top)
    other = sum(totals.values()) - sum(n for _, n in items)
    if other > 0:
        items.append(("Other", other))
    grand = sum(n for _, n in items) or 1

    rows = (len(items) + 1) // 2
    H = BAR_Y + BAR_H + 18 + rows * 20 + 8
    span = W - 2 * PAD

    p = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" role="img" aria-label="Languages">' % (W, H, W, H)]
    p.append(style(dark))
    p.append('<text class="t" x="%d" y="22" font-size="14" font-weight="600">Languages</text>' % PAD)

    # дорожка со скруглением: сегменты рисуются внутри clipPath
    p.append('<clipPath id="r"><rect x="%d" y="%d" width="%d" height="%d" rx="%d"/></clipPath>' % (PAD, BAR_Y, span, BAR_H, BAR_H // 2))
    p.append('<rect class="track" x="%d" y="%d" width="%d" height="%d" rx="%d"/>' % (PAD, BAR_Y, span, BAR_H, BAR_H // 2))
    p.append('<g clip-path="url(#r)">')
    x = float(PAD)
    for i, (_, n) in enumerate(items):
        w = span * n / grand
        p.append('<rect x="%.2f" y="%d" width="%.2f" height="%d" fill="%s"/>' % (x, BAR_Y, w, BAR_H, WHEEL[i % len(WHEEL)]))
        x += w
    p.append("</g>")

    ly = BAR_Y + BAR_H + 26
    for i, (lang, n) in enumerate(items):
        lx = PAD + (i % 2) * (span // 2)
        yy = ly + (i // 2) * 20
        p.append('<circle cx="%d" cy="%d" r="5" fill="%s"/>' % (lx + 5, yy - 4, WHEEL[i % len(WHEEL)]))
        p.append('<text class="lg" x="%d" y="%d" font-size="12">%s <tspan opacity="0.65">%.1f%%</tspan></text>'
                 % (lx + 17, yy, esc(lang), 100.0 * n / grand))
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
    CELL, GAP, PAD, TOP, W = 12, 4, 16, 34, 480
    grid_w = len(weeks) * (CELL + GAP) - GAP
    x0 = (W - grid_w) // 2
    H = TOP + 7 * (CELL + GAP) - GAP + 26
    peak = max((d["contributionCount"] for w in weeks for d in w["contributionDays"]), default=0)

    def level(c):
        if c <= 0:
            return 0
        if peak <= 1:
            return 3
        r = c / peak
        return 1 if r <= .25 else 2 if r <= .5 else 3 if r <= .75 else 4

    p = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" role="img" aria-label="Activity">' % (W, H, W, H)]
    p.append(style(dark, heat=True))
    p.append('<text class="t" x="%d" y="22" font-size="14" font-weight="600">Activity</text>' % PAD)
    p.append('<text class="lg" x="%d" y="22" font-size="12" text-anchor="end" opacity="0.8">%d contributions this year</text>' % (W - PAD, total))

    for wi, w in enumerate(weeks):
        for d in w["contributionDays"]:
            p.append('<rect class="h%d" x="%d" y="%d" width="%d" height="%d" rx="3"><title>%s: %d</title></rect>'
                     % (level(d["contributionCount"]), x0 + wi * (CELL + GAP), TOP + d["weekday"] * (CELL + GAP),
                        CELL, CELL, d["date"], d["contributionCount"]))

    ly = TOP + 7 * (CELL + GAP) + 8
    p.append('<text class="lg" x="%d" y="%d" font-size="11" opacity="0.75">Less</text>' % (x0, ly + 9))
    for i in range(5):
        p.append('<rect class="h%d" x="%d" y="%d" width="12" height="12" rx="3"/>' % (i, x0 + 34 + i * 15, ly))
    p.append('<text class="lg" x="%d" y="%d" font-size="11" opacity="0.75">More</text>' % (x0 + 34 + 5 * 15 + 4, ly + 9))
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
