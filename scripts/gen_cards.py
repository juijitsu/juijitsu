#!/usr/bin/env python3
"""Рисует карточки проектов как панели манги: рамка, скоростные линии, скринтон.

Вместо дженерик-осьминога и пустоты — имя репозитория, что он делает и одна
крупная проверяемая цифра. Пишет по два файла на карточку, светлый и тёмный.
"""
import math, os, sys

try:  # консоль Windows по умолчанию не в UTF-8
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
FONT = "'Segoe UI',system-ui,-apple-system,sans-serif"
NL = "\n"
W, H = 640, 190
OWNER = "juijitsu"

CARDS = [
    dict(slug="docqa", name="docqa",
         tagline="Grounded document Q&A. The model must return the IDs of the passages "
                 "it used; anything invented is stripped and the answer flagged unsupported.",
         stat="8×", label="FASTER RE-INDEX ON A 4,669-CHUNK CORPUS"),
    dict(slug="leadqual", name="leadqual",
         tagline="Webhook lead qualification. Five criteria with fixed ceilings, evidence "
                 "quoted per criterion, the total computed in code — never by the model.",
         stat="0", label="DOUBLE-BILLED MODEL CALLS ON RETRY"),
    dict(slug="agentic-course", name="agentic-course",
         tagline="A course on agentic systems. The agent loop is one layer out of nine; "
                 "the other eight decide whether the thing holds up in production.",
         stat="20", label="DAYS · NINE ARCHITECTURAL LAYERS"),
]


def palette(dark):
    if dark:
        return dict(ink="#F0F0F0", paper="#0D1117", dim="#9AA0A6", rule="#3A3F46")
    return dict(ink="#16181D", paper="#FFFFFF", dim="#5B6169", rule="#D5D9DE")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def wrap(text, width_px, px_per_char):
    """Грубый перенос: SVG сам строки не ломает."""
    limit = max(8, int(width_px / px_per_char))
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if len(trial) <= limit:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def speed_lines(cx, cy, dark, n=26, r_in=120, r_out=900):
    """Клинья, расходящиеся от фокуса — классический приём динамики в манге."""
    c = palette(dark)
    # маска гасит линии к левому краю, чтобы они не резали текст описания
    out = ['<g clip-path="url(#frame)" mask="url(#fade)" opacity="0.55">']
    for i in range(n):
        a = math.pi * (0.62 + 0.76 * i / (n - 1))      # веер влево от фокуса
        half = 0.0055 + 0.0075 * ((i * 7919) % 100) / 100.0
        x1, y1 = cx + r_in * math.cos(a - half), cy + r_in * math.sin(a - half)
        x2, y2 = cx + r_out * math.cos(a), cy + r_out * math.sin(a)
        x3, y3 = cx + r_in * math.cos(a + half), cy + r_in * math.sin(a + half)
        out.append('<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f Z" fill="%s"/>'
                   % (x1, y1, x2, y2, x3, y3, c["ink"]))
    out.append("</g>")
    return NL.join(out)


def render(card, dark):
    c = palette(dark)
    p = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" role="img" aria-label="%s">'
         % (W, H, W, H, esc(card["name"]))]
    p.append('<defs>')
    p.append('<clipPath id="frame"><rect x="0" y="0" width="%d" height="%d"/></clipPath>' % (W, H))
    p.append('<pattern id="tone" width="6" height="6" patternUnits="userSpaceOnUse">'
             '<circle cx="3" cy="3" r="1.5" fill="%s"/></pattern>' % c["ink"])
    p.append('<linearGradient id="fadeGrad" x1="0" y1="0" x2="1" y2="0">'
             '<stop offset="0.30" stop-color="#000"/>'
             '<stop offset="0.74" stop-color="#fff"/></linearGradient>')
    p.append('<mask id="fade"><rect width="%d" height="%d" fill="url(#fadeGrad)"/></mask>' % (W, H))
    p.append('</defs>')
    p.append('<style>.n{font-family:%s;font-weight:800;fill:%s}'
             '.o{font-family:%s;font-weight:600;fill:%s}'
             '.d{font-family:%s;fill:%s}'
             '.s{font-family:%s;font-weight:800;fill:%s}'
             '.l{font-family:%s;font-weight:600;fill:%s;letter-spacing:0.6}</style>'
             % (FONT, c["ink"], FONT, c["dim"], FONT, c["dim"], FONT, c["ink"], FONT, c["dim"]))

    p.append('<rect width="%d" height="%d" fill="%s"/>' % (W, H, c["paper"]))
    # фокус скоростных линий — за блоком с цифрой
    p.append(speed_lines(W - 96, H // 2, dark))
    # скринтоновый клин в нижнем левом углу
    p.append('<path d="M0 %d L150 %d L0 %d Z" fill="url(#tone)" opacity="0.55" clip-path="url(#frame)"/>'
             % (H, H, H - 74))
    # правый блок: подложка бумагой, чтобы цифра читалась поверх линий
    p.append('<rect x="%d" y="8" width="%d" height="%d" fill="%s" opacity="0.92"/>' % (W - 186, 178, H - 16, c["paper"]))
    p.append('<line x1="%d" y1="18" x2="%d" y2="%d" stroke="%s" stroke-width="2"/>' % (W - 186, W - 186, H - 18, c["ink"]))

    # левая колонка
    p.append('<text class="o" x="26" y="44" font-size="13">%s/</text>' % OWNER)
    p.append('<text class="n" x="26" y="76" font-size="31">%s</text>' % esc(card["name"]))
    for i, line in enumerate(wrap(card["tagline"], 400, 6.35)[:4]):
        p.append('<text class="d" x="26" y="%d" font-size="12.5">%s</text>' % (108 + i * 18, esc(line)))

    # правая колонка
    p.append('<text class="s" x="%d" y="%d" font-size="52" text-anchor="middle">%s</text>'
             % (W - 96, H // 2 - 2, esc(card["stat"])))
    for i, line in enumerate(wrap(card["label"], 150, 5.2)[:3]):
        p.append('<text class="l" x="%d" y="%d" font-size="9" text-anchor="middle">%s</text>'
                 % (W - 96, H // 2 + 26 + i * 12, esc(line)))

    # рамка панели
    p.append('<rect x="1.25" y="1.25" width="%.1f" height="%.1f" fill="none" stroke="%s" stroke-width="2.5"/>'
             % (W - 2.5, H - 2.5, c["ink"]))
    p.append("</svg>")
    return NL.join(p)


def main():
    os.makedirs(OUT, exist_ok=True)
    for card in CARDS:
        for dark, suf in ((False, ""), (True, "-dark")):
            path = os.path.join(OUT, "card-%s%s.svg" % (card["slug"], suf))
            with open(path, "w", encoding="utf-8") as f:
                f.write(render(card, dark))
        print("card-%s: %s %s" % (card["slug"], card["stat"], card["label"][:40]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
