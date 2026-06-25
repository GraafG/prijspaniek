"""Scrape real Action.com product data (name, price, image, link) into products.js / products.json.

Action runs on Next.js; product data lives in the RSC payload of category pages.
We parse that payload and emit a compact dataset the game consumes.
Run: python scrape.py
"""
import re, json, urllib.request, time, os

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36'
HERE = os.path.dirname(os.path.abspath(__file__))

CATS = {
  "Gereedschap":   "https://www.action.com/nl-nl/c/doe-het-zelf/gereedschap/",
  "Verlichting":   "https://www.action.com/nl-nl/c/doe-het-zelf/verlichting/",
  "Chocolade":     "https://www.action.com/nl-nl/c/eten--drinken/chocolade/",
  "Snoep":         "https://www.action.com/nl-nl/c/eten--drinken/drop--snoep/",
  "Chips":         "https://www.action.com/nl-nl/c/eten--drinken/chips/",
  "Koek":          "https://www.action.com/nl-nl/c/eten--drinken/koek--bakproducten/",
  "Drinken":       "https://www.action.com/nl-nl/c/eten--drinken/drinken/",
  "Schoonmaak":    "https://www.action.com/nl-nl/c/huishouden/schoonmaakmiddelen/",
  "Opbergen":      "https://www.action.com/nl-nl/c/huishouden/opbergen/",
  "Verzorging":    "https://www.action.com/nl-nl/c/persoonlijke-verzorging/",
  "Speelgoed":     "https://www.action.com/nl-nl/c/speelgoed/",
  "Wonen":         "https://www.action.com/nl-nl/c/wonen/woonaccessoires/",
  "Tuin":          "https://www.action.com/nl-nl/c/tuin/",
  "Huisdier":      "https://www.action.com/nl-nl/c/huisdieren/",
  "Keuken":        "https://www.action.com/nl-nl/c/keuken/",
  "Kantoor":       "https://www.action.com/nl-nl/c/kantoor--school/",
  "Multimedia":    "https://www.action.com/nl-nl/c/multimedia/",
  "Sport":         "https://www.action.com/nl-nl/c/sportartikelen/",
}


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept-Language': 'nl-NL'})
    return urllib.request.urlopen(req, timeout=30).read().decode('utf-8', 'replace')


def payload(html):
    parts = re.findall(r'self\.__next_f\.push\(\[1,(".*?")\]\)', html, re.S)
    buf = ""
    for s in parts:
        try:
            buf += json.loads(s)
        except Exception:
            pass
    return buf


def brace_match(buf, start):
    depth = 0
    i = start
    while i < len(buf):
        ch = buf[i]
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                return buf[start:i + 1]
        i += 1
    return None


def parse_products(buf, cat):
    out = []
    for m in re.finditer(r'"product":\{', buf):
        start = buf.index('{', m.start() + len('"product":') - 1)
        frag = brace_match(buf, start)
        if not frag:
            continue
        try:
            o = json.loads(frag)
        except Exception:
            continue
        if not o.get("title") or not isinstance(o.get("price"), dict):
            continue
        cur = o["price"].get("current", {}).get("amount")
        if cur is None:
            continue
        out.append({
            "code": o.get("code"),
            "name": o.get("title"),
            "desc": o.get("description") or "",
            "brand": o.get("brand") or "",
            "cat": cat,
            "price": round(float(cur), 2),
            "original": (o["price"].get("original") or {}).get("amount"),
            "isDeal": bool(o.get("isDeal")),
            "image": o.get("image"),
            "href": o.get("href"),
        })
    return out


def square_img(u, w=500):
    return u.replace("/image/upload/", f"/image/upload/t_digital_square,w_{w},f_auto/") + ".webp"


def main():
    allp = {}
    for cat, url in CATS.items():
        try:
            ps = parse_products(payload(fetch(url)), cat)
            for p in ps:
                if p["image"] and p["href"]:
                    allp[p["code"]] = p
            print(f"{cat:14} {len(ps):3} products")
        except Exception as e:
            print(f"{cat:14} ERR {e}")
        time.sleep(0.6)

    data = list(allp.values())
    print("TOTAL unique:", len(data))

    json.dump(data, open(os.path.join(HERE, "products.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=0)

    game = []
    for x in data:
        game.append({
            "n": x["name"], "b": x.get("brand", ""), "d": x.get("desc", ""),
            "c": x["cat"], "p": x["price"], "o": x.get("original"),
            "deal": bool(x.get("isDeal")), "img": square_img(x["image"]), "u": x["href"],
        })
    js = "window.PRODUCTS=" + json.dumps(game, ensure_ascii=False) + ";"
    open(os.path.join(HERE, "products.js"), "w", encoding="utf-8").write(js)
    print("wrote", len(game), "products -> products.js / products.json")


if __name__ == "__main__":
    main()
