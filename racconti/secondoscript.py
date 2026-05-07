# secondoscript.py

import glob
import os
from bs4 import BeautifulSoup


def extract_paragraphs_from_txt(txt_path):
    with open(txt_path, "r", encoding="utf-8") as f:
        content = f.read()

    soup = BeautifulSoup(content, "html.parser")
    paragraphs = [p.get_text() for p in soup.find_all("p")]

    print(f"{txt_path} -> paragrafi trovati:", len(paragraphs))
    return paragraphs


def get_file_pairs():
    html_files = glob.glob("*.html")
    txt_files = glob.glob("*.txt")

    html_map = {os.path.splitext(f)[0]: f for f in html_files}
    txt_map = {os.path.splitext(f)[0]: f for f in txt_files}

    common_keys = sorted(set(html_map.keys()) & set(txt_map.keys()))

    pairs = [(key, txt_map[key], html_map[key]) for key in common_keys]

    print("Coppie trovate:")
    for k, t, h in pairs:
        print(f"- {k}: {t} + {h}")

    return pairs


def main():
    pairs = get_file_pairs()

    if not pairs:
        print("Nessuna coppia .txt + .html trovata.")
        return

    for name, txt_file, html_file in pairs:
        txt_paragraphs = extract_paragraphs_from_txt(txt_file)

        base = os.path.splitext(html_file)[0]
        renamed_html = f"{base}EX.html"

        # rinomina HTML originale con overwrite sicuro
        if os.path.exists(renamed_html):
            os.remove(renamed_html)

        os.replace(html_file, renamed_html)

        with open(renamed_html, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        html_paragraphs = soup.find_all("p")

        print(f"{renamed_html} -> paragrafi HTML:", len(html_paragraphs))

        if len(html_paragraphs) == 0:
            print(f"Saltato {name}: nessun <p> trovato")
            continue

        min_len = min(len(txt_paragraphs), len(html_paragraphs))

        for i in range(min_len):
            html_paragraphs[i].string = txt_paragraphs[i]

        output_file = f"{base}.html"

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(str(soup))

        print("Creato:", output_file)


if __name__ == "__main__":
    main()