#!/usr/bin/env python3
"""Neofetch-карточка профиля: слева портрет, справа моноширинная сводка.

Форма позаимствована у терминальных info-карточек, но поля выбраны так, чтобы
не показывать нули: вместо звёзд и подписчиков — возраст аккаунта, раскладка
языков и три проекта с проверяемыми цифрами.
"""
import base64, datetime, io, json, os, sys, urllib.request
from collections import Counter

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets")
USER = os.environ.get("GH_USER", "juijitsu")
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN", "")

W, H = 880, 384
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
NL = "\n"

WORK = [
    ("docqa", "cites its source, or says unsupported", "8x"),
    ("leadqual", "idempotent webhook scoring", "0"),
    ("agentic-course", "nine layers, twenty days", "20"),
]


def palette(dark):
    if dark:
        return dict(ink="#F0F0F0", paper="#0D1117", dim="#9AA0A6", rule="#3A3F46", key="#D5D9DE")
    return dict(ink="#16181D", paper="#FFFFFF", dim="#5B6169", rule="#D5D9DE", key="#16181D")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def api(path):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "juijitsu-profile"}
    if TOKEN:
        headers["Authorization"] = "Bearer " + TOKEN
    req = urllib.request.Request("https://api.github.com/" + path, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def gather():
    u = api("users/" + USER)
    created = datetime.datetime.fromisoformat(u["created_at"].replace("Z", "+00:00")).date()
    today = datetime.datetime.now(datetime.timezone.utc).date()
    days = (today - created).days
    y, rem = divmod(days, 365)
    m, d = divmod(rem, 30)
    parts = []
    if y:
        parts.append("%d year%s" % (y, "" if y == 1 else "s"))
    if m:
        parts.append("%d month%s" % (m, "" if m == 1 else "s"))
    parts.append("%d days" % d)

    totals = Counter()
    for r in api("users/%s/repos?type=owner&per_page=100" % USER):
        if r.get("fork") or r.get("archived"):
            continue
        try:
            for lang, n in api("repos/%s/%s/languages" % (USER, r["name"])).items():
                totals[lang] += n
        except Exception:
            pass
    grand = sum(totals.values()) or 1
    langs = ", ".join("%s %.0f%%" % (k, 100.0 * v / grand) for k, v in totals.most_common(3))
    return ", ".join(parts), langs, today.isoformat()


def avatar_data_uri(px=260):
    """Портрет кодируется в base64: SVG как картинка внешние файлы не тянет."""
    src = os.path.join(OUT, "avatar.png")
    if not os.path.exists(src):
        return None
    try:
        from PIL import Image
        im = Image.open(src).convert("L").resize((px, px), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, format="PNG", optimize=True)
        raw = buf.getvalue()
    except Exception:
        raw = open(src, "rb").read()
    return "data:image/png;base64," + base64.b64encode(raw).decode()


def render(dark, uptime, langs, today, avatar):
    c = palette(dark)
    BOX = 236                     # сторона портрета
    LX, LY = 26, 26               # левая панель
    RX = LX + BOX + 34            # начало правой колонки
    KEY_W = 86

    p = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" role="img" aria-label="%s">'
         % (W, H, W, H, USER)]
    p.append('<defs><pattern id="tone" width="6" height="6" patternUnits="userSpaceOnUse">'
             '<circle cx="3" cy="3" r="1.4" fill="%s"/></pattern>'
             '<clipPath id="av"><rect x="%d" y="%d" width="%d" height="%d"/></clipPath></defs>'
             % (c["ink"], LX, LY, BOX, BOX))
    p.append('<style>text{font-family:%s}.k{fill:%s;font-weight:700}.v{fill:%s}'
             '.d{fill:%s}.h{fill:%s;font-weight:700}</style>'
             % (MONO, c["key"], c["dim"], c["dim"], c["ink"]))
    p.append('<rect width="%d" height="%d" fill="%s"/>' % (W, H, c["paper"]))

    # портрет
    if avatar:
        p.append('<image href="%s" x="%d" y="%d" width="%d" height="%d" clip-path="url(#av)" preserveAspectRatio="xMidYMid slice"/>'
                 % (avatar, LX, LY, BOX, BOX))
    p.append('<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="%s" stroke-width="2"/>'
             % (LX, LY, BOX, BOX, c["ink"]))
    # скринтон под портретом, поверх него плашка с подписью — иначе текст тонет в растре
    ty = LY + BOX + 14
    p.append('<rect x="%d" y="%d" width="%d" height="44" fill="url(#tone)" opacity="0.5"/>' % (LX, ty, BOX))
    p.append('<rect x="%d" y="%d" width="%d" height="28" fill="%s" stroke="%s" stroke-width="1.5"/>'
             % (LX + 10, ty + 8, BOX - 20, c["paper"], c["ink"]))
    p.append('<text class="h" x="%d" y="%d" font-size="13" text-anchor="middle">%s@github</text>'
             % (LX + BOX // 2, ty + 27, USER))

    y = LY + 22
    p.append('<text class="h" x="%d" y="%d" font-size="17">&lt; %s &gt;</text>' % (RX, y, USER))
    y += 12
    p.append('<text class="d" x="%d" y="%d" font-size="12">%s</text>' % (RX, y, "-" * 58))

    rows = [("OS", "Linux, Docker, systemd"),
            ("Host", "Almaty, Kazakhstan (UTC+5), remote"),
            ("Uptime", uptime),
            ("Lang", langs),
            ("Focus", "AI agents, automation, integrations"),
            ("Shell", "Python, FastAPI, n8n, PostgreSQL")]
    y += 26
    for k, v in rows:
        p.append('<text class="k" x="%d" y="%d" font-size="13">%s:</text>' % (RX, y, k))
        p.append('<text class="v" x="%d" y="%d" font-size="13">%s</text>' % (RX + KEY_W, y, esc(v)))
        y += 22

    y += 8
    p.append('<text class="d" x="%d" y="%d" font-size="12">%s selected work %s</text>'
             % (RX, y, "-" * 18, "-" * 18))
    y += 24
    for name, what, stat in WORK:
        p.append('<text class="h" x="%d" y="%d" font-size="13">%s</text>' % (RX, y, esc(name)))
        p.append('<text class="v" x="%d" y="%d" font-size="12">%s</text>' % (RX + 148, y, esc(what)))
        p.append('<text class="h" x="%d" y="%d" font-size="14" text-anchor="end">%s</text>' % (W - 26, y, esc(stat)))
        y += 22

    # нижняя строка приглашения
    by = H - 40
    p.append('<rect x="%d" y="%d" width="150" height="26" fill="%s"/>' % (LX, by, c["ink"]))
    p.append('<text x="%d" y="%d" font-size="12" font-weight="700" fill="%s">gh ~/ %s</text>'
             % (LX + 12, by + 18, c["paper"], USER))
    p.append('<text class="d" x="%d" y="%d" font-size="12">_</text>' % (LX + 160, by + 18))
    p.append('<rect x="%d" y="%d" width="120" height="26" rx="13" fill="none" stroke="%s" stroke-width="1.5"/>'
             % (W - 146, by, c["rule"]))
    p.append('<text class="v" x="%d" y="%d" font-size="12" text-anchor="middle">%s</text>' % (W - 86, by + 18, today))

    p.append('<rect x="1.25" y="1.25" width="%.1f" height="%.1f" fill="none" stroke="%s" stroke-width="2.5"/>'
             % (W - 2.5, H - 2.5, c["ink"]))
    p.append("</svg>")
    return NL.join(p)


def main():
    os.makedirs(OUT, exist_ok=True)
    uptime, langs, today = gather()
    avatar = avatar_data_uri()
    for dark, suf in ((False, ""), (True, "-dark")):
        with open(os.path.join(OUT, "neofetch%s.svg" % suf), "w", encoding="utf-8") as f:
            f.write(render(dark, uptime, langs, today, avatar))
    print("neofetch: uptime %s | %s | портрет %s" % (uptime, langs, "вшит" if avatar else "НЕ НАЙДЕН"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
