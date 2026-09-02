#!/usr/bin/env python3
"""Обновляет секции README между маркерами: цитата дня и «Now Building».

Секции размечены парами <!--START_SECTION:x--> / <!--END_SECTION:x-->, поэтому
скрипт правит только их и никогда не трогает остальной текст.
"""
import datetime, json, os, re, sys, urllib.request, urllib.error

USER = os.environ.get("GH_USER", "juijitsu")
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN", "")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(ROOT, "README.md")


def api(url):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "juijitsu-profile"}
    if TOKEN:
        headers["Authorization"] = "Bearer " + TOKEN
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as r:
        return json.load(r)


def replace_section(text, name, body):
    start, end = "<!--START_SECTION:%s-->" % name, "<!--END_SECTION:%s-->" % name
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    if not pattern.search(text):
        print("маркер %s не найден — секция пропущена" % name, file=sys.stderr)
        return text
    return pattern.sub(start + "\n" + body + "\n" + end, text)


# ── цитата дня ────────────────────────────────────────────────────────────────
def anime_quote():
    try:
        req = urllib.request.Request("https://api.animechan.io/v1/quotes/random",
                                     headers={"User-Agent": "juijitsu-profile"})
        with urllib.request.urlopen(req, timeout=25) as r:
            d = json.load(r)["data"]
    except Exception as e:  # сеть или сервис недоступны — оставляем прошлую цитату
        print("цитата недоступна: %s" % e, file=sys.stderr)
        return None
    quote = " ".join(d["content"].split())
    return ('<table><tr><td>\n\n'
            '> *%s*\n>\n'
            '> **%s** &mdash; %s\n\n'
            '</td></tr></table>' % (quote, d["character"]["name"], d["anime"]["name"]))


# ── что сейчас в работе ───────────────────────────────────────────────────────
def now_building(limit=3):
    repos = [r for r in api("https://api.github.com/users/%s/repos?type=owner&sort=pushed&per_page=100" % USER)
             if not r.get("fork") and not r.get("archived") and r["name"] != USER]
    lines = []
    for r in repos[:limit]:
        pushed = r["pushed_at"][:10]
        desc = (r.get("description") or "").split(".")[0].strip()
        if len(desc) > 90:
            desc = desc[:87].rstrip() + "..."
        lines.append("- **[%s](%s)** &mdash; %s `%s`" % (r["name"], r["html_url"], desc or "in progress", pushed))
    today = os.environ.get("RUN_DATE") or datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    lines.append("")
    lines.append("<sub>Refreshed automatically on %s (UTC).</sub>" % today)
    return "\n".join(lines)


def main():
    if not os.path.exists(README):
        print("README.md не найден", file=sys.stderr)
        return 1
    with open(README, encoding="utf-8") as f:
        original = f.read()
    text = original

    q = anime_quote()
    if q:
        text = replace_section(text, "quote", q)
    text = replace_section(text, "now-building", now_building())

    if text == original:
        print("изменений нет")
        return 0
    with open(README, "w", encoding="utf-8") as f:
        f.write(text)
    print("README обновлён")
    return 0


if __name__ == "__main__":
    sys.exit(main())
