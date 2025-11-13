#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generer_duckduckgo.py
Script sans dépendances externes.
Lit Jsp.csv (col "Artist Name(s)") et produit artists_enriched.json
Utilise l'API publique DuckDuckGo Instant Answer pour récupérer une image si possible.
"""

import csv, json, urllib.parse, urllib.request, time, random, os, re, sys

CSV_PATH = "Jsp.csv"
OUT_PATH = "artists_enriched.json"
PLACEHOLDER = "https://via.placeholder.com/400x400.png?text=Artist"  # fallback simple

RATINGS = ["★★★★★", "★★★★½", "★★★★", "★★★½"]

REGION_HINTS = {
    "fr": ["nekfeu","damso","laylow","freeze corleone","vald","pnl","ninho","gazo","alpha wann","booba","jul","sch"],
    "uk": ["central cee","dave","stormzy","aj tracey","skepta","headie one","arrdee","unknown t","digga d"],
    "us": ["kendrick lamar","travis scott","kanye west","drake","j. cole","21 savage","future","lil baby","playboi carti","young thug"]
}

def guess_region(name):
    n = name.lower()
    for reg, words in REGION_HINTS.items():
        if any(w in n for w in words):
            return reg
    if re.search(r"[éèàùçîïôêâ]", n):
        return "fr"
    return "other"

def clean_name(name):
    # remove parentheses like (feat ...) and [Remix], and trim
    name = re.sub(r"\(feat[^\)]*\)","", name, flags=re.I)
    name = re.sub(r"\[.*?\]","", name)
    return name.strip()

def split_artists(raw):
    # splits common separators and removes empty items
    if not raw: return []
    parts = re.split(r"[;,/]| feat\.| ft\. |&| and ", raw, flags=re.I)
    out = []
    for p in parts:
        p = clean_name(p).strip()
        if not p: continue
        # sometimes CSV has "Artist1;Artist2" already separated — keep unique
        out.append(p)
    return out

def ddg_search_image(artist):
    """
    Query DuckDuckGo Instant Answer API.
    Try top-level 'Image', then RelatedTopics[*].Icon.URL, then Result/FirstURL.
    Returns direct http(s) URL or empty string.
    """
    query = urllib.parse.quote(f"{artist} musician")
    url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1&skip_disambig=1"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = resp.read().decode("utf-8", errors="ignore")
            j = json.loads(data)
    except Exception as e:
        # network issue or parsing error
        return ""

    # 1) top-level Image
    img = j.get("Image") or j.get("image")
    if img and isinstance(img, str) and img.strip():
        return normalize_image_url(img)

    # 2) RelatedTopics (list) -> try Icon.URL or Icon.URL
    rt = j.get("RelatedTopics") or []
    if isinstance(rt, list):
        for item in rt:
            # item might be dict with 'Icon' or nested topics
            if isinstance(item, dict):
                icon = item.get("Icon") or {}
                # Icon might be {"URL":"..."}
                url_icon = icon.get("URL") or icon.get("url")
                if url_icon and url_icon.strip():
                    return normalize_image_url(url_icon)
                # sometimes item has 'FirstURL' or 'Result' containing images (rare)
            # if item has 'Topics' nested
            topics = item.get("Topics") if isinstance(item, dict) else None
            if topics and isinstance(topics, list):
                for sub in topics:
                    if isinstance(sub, dict):
                        icon = sub.get("Icon") or {}
                        url_icon = icon.get("URL") or icon.get("url")
                        if url_icon and url_icon.strip():
                            return normalize_image_url(url_icon)

    # 3) AbstractImage?
    abs_img = j.get("AbstractImage")
    if abs_img:
        return normalize_image_url(abs_img)

    # fallback empty
    return ""

def normalize_image_url(u):
    if not u: return ""
    u = u.split("?")[0]  # cut querystring
    # DuckDuckGo sometimes returns relative URLs like "/i/something" or "//upload..."
    if u.startswith("//"):
        u = "https:" + u
    if u.startswith("/"):
        u = "https://duckduckgo.com" + u
    # very basic check
    if u.startswith("http://") or u.startswith("https://"):
        if any(u.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]):
            return u
        # sometimes icons are .ashx or other endpoints — still return them
        return u
    return ""

def read_csv(path):
    if not os.path.exists(path):
        print("Fichier CSV introuvable:", path)
        sys.exit(1)
    artists = []
    seen = set()
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw = row.get("Artist Name(s)") or row.get("artist") or row.get("Artist") or ""
            parts = split_artists(raw)
            for p in parts:
                key = p.lower()
                if key not in seen:
                    seen.add(key)
                    artists.append(p)
    return artists

def main():
    artists = read_csv(CSV_PATH)
    print(f"Artistes uniques détectés: {len(artists)}")
    out = []
    total = len(artists)
    for i, artist in enumerate(artists, start=1):
        region = guess_region(artist)
        rating = random.choice(RATINGS)
        # Try DuckDuckGo
        img = ddg_search_image(artist)
        if not img:
            # fallback to Bing quick attempt (optional)
            img = ""  # keep empty; we'll use placeholder later
        if not img:
            img = PLACEHOLDER
            note_img = "placeholder"
        else:
            note_img = "ok"
        entry = {
            "name": artist,
            "url": f"https://open.spotify.com/search/artist%3A{urllib.parse.quote(artist)}",
            "region": region,
            "image": img,
            "rating": rating
        }
        out.append(entry)
        print(f"[{i}/{total}] {artist} | {region} | {rating} | img={note_img}")
        time.sleep(0.6)  # be polite
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"Fini — {len(out)} artistes sauvegardés dans {OUT_PATH}")

if __name__ == "__main__":
    main()
