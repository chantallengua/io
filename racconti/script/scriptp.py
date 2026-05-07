import os
import re
from docx import Document

MARKER = "<!-- DUE PAGINE CREATE -->\n\n"

def wrap_italics_txt(text):
    return re.sub(r'_(.*?)_', r'<i>\1</i>', text)

def read_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.readlines()

def read_docx(path):
    doc = Document(path)
    out = []

    for p in doc.paragraphs:
        if not p.text.strip():
            out.append("")
            continue

        parts = []
        for run in p.runs:
            if run.italic:
                parts.append(f"<i>{run.text}</i>")
            else:
                parts.append(run.text)

        out.append("".join(parts))

    return out

def to_paragraphs(lines):
    output = []
    char_count = 0
    first_real_line_skipped = False

    for line in lines:
        line = line.strip("\r\n")

        if not line.strip():
            continue

        # ignora SEMPRE la prima riga utile
        if not first_real_line_skipped:
            first_real_line_skipped = True
            continue

        line = wrap_italics_txt(line)

        block = f"<p>{line}</p>"
        output.append(block)

        char_count += len(line)

        if char_count >= 4500:
            output.append(MARKER)
            char_count = 0

    # cancella il primo <p> creato
    if output:
        for i, item in enumerate(output):
            if item.startswith("<p>"):
                del output[i]
                break

    return output

def find_file():
    if os.path.exists("testo.docx"):
        return "testo.docx"
    if os.path.exists("testo.txt"):
        return "testo.txt"
    return None

def run():
    file = find_file()

    if not file:
        print("Errore: nessun file trovato.")
        return

    lines = read_docx(file) if file.endswith(".docx") else read_txt(file)

    result = to_paragraphs(lines)

    with open("p.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(result))

    print("Completato -> p.txt")

if __name__ == "__main__":
    run()