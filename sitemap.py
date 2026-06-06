import os
from datetime import datetime
from pathlib import Path
import shutil

BASE_URL = "https://chantallengua.github.io/io"

ROOT = Path(__file__).parent
OUTPUT_FILE = ROOT / "sitemap.xml"

STATIC_URLS = [
    "/",
    "/romanzi/romanzi.html",
    "/newsletter.html",
    "/about.html"
]

BACKUP_FILE = None


def get_lastmod(file_path: Path):
    if file_path.exists():
        ts = file_path.stat().st_mtime
        return datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d")
    return None


def archive_old_sitemap():
    global BACKUP_FILE

    if OUTPUT_FILE.exists():
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
        BACKUP_FILE = ROOT / f"sitemap-old-{timestamp}.xml"
        shutil.move(str(OUTPUT_FILE), str(BACKUP_FILE))
        print(f"📦 Vecchia sitemap archiviata: {BACKUP_FILE.name}")


def collect_urls():
    static = []
    racconti = []
    newsletter = []

    for u in STATIC_URLS:
        file_path = ROOT / u.lstrip("/")
        static.append((f"{BASE_URL}{u}", get_lastmod(file_path)))

    # RACCONTI
    r_dir = ROOT / "racconti"
    if r_dir.exists():
        for f in r_dir.glob("*.html"):
            if f.name.startswith("zzz_"):
                continue
            racconti.append((f"{BASE_URL}/racconti/{f.name}", get_lastmod(f)))

    # NEWSLETTER
    n_dir = ROOT / "newsl"
    if n_dir.exists():
        for f in n_dir.glob("*.html"):
            if f.name.startswith("zzz_"):
                continue
            newsletter.append((f"{BASE_URL}/newsl/{f.name}", get_lastmod(f)))

    return static, racconti, newsletter


def url_line(loc, lastmod):
    if lastmod:
        return f"<url><loc>{loc}</loc><lastmod>{lastmod}</lastmod></url>"
    return f"<url><loc>{loc}</loc></url>"


def build_xml(static, racconti, newsletter):
    xml = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]

    for loc, lm in static:
        xml.append(url_line(loc, lm))

    xml.append("<!-- RACCONTI -->")
    for loc, lm in racconti:
        xml.append(url_line(loc, lm))

    xml.append("<!-- NEWSLETTER -->")
    for loc, lm in newsletter:
        xml.append(url_line(loc, lm))

    xml.append("</urlset>")
    return "\n".join(xml)


def maybe_delete_backup():
    global BACKUP_FILE

    if not BACKUP_FILE:
        return

    answer = input(f"❓ Vuoi eliminare il backup timestamp '{BACKUP_FILE.name}'? (y/n): ").strip().lower()

    if answer == "y":
        try:
            BACKUP_FILE.unlink()
            print("✨ Backup eliminato")
        except Exception as e:
            print(f"⚠️ Errore eliminazione backup: {e}")
    else:
        print("Backup mantenuto")


def main():
    archive_old_sitemap()

    static, racconti, newsletter = collect_urls()
    xml = build_xml(static, racconti, newsletter)

    OUTPUT_FILE.write_text(xml, encoding="utf-8")
    print("✅ Nuova sitemap.xml generata")

    maybe_delete_backup()


if __name__ == "__main__":
    main()