import re
from bs4 import BeautifulSoup, Comment
from docx import Document


def split_sentences(text):
    text = re.sub(r'\s+', ' ', text.strip())
    if not text:
        return []
    return re.split(r'(?<=[.!?])\s+', text)


def sentence_to_html(sentence):
    sentence = sentence.strip()
    if not sentence:
        return "<p></p>"
    return f"<p>{sentence}</p>"


def read_docx(path):
    doc = Document(path)
    blocks = []

    for para in doc.paragraphs:
        raw = para.text.strip()

        if raw == "":
            blocks.append("<p></p>")
            continue

        html = ""
        for run in para.runs:
            if run.text:
                if run.italic:
                    html += f"<i>{run.text}</i>"
                else:
                    html += run.text

        sentences = split_sentences(html)

        for s in sentences:
            if s.strip():
                blocks.append(sentence_to_html(s))

    return blocks


def distribute_blocks(blocks, articles):
    sizes = []

    for a in articles:
        base = a.get_text(" ", strip=True)
        sizes.append(max(len(base), 1))

    total = sum(sizes)
    n = len(blocks)

    out = []
    start = 0

    for i, s in enumerate(sizes):
        if i == len(sizes) - 1:
            out.append(blocks[start:])
        else:
            k = max(1, int(n * (s / total)))
            out.append(blocks[start:start + k])
            start += k

    return out


def inject(html_file, blocks_by_article, output_file):
    with open(html_file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "lxml")

    articles = soup.find_all("article")

    for article, blocks in zip(articles, blocks_by_article):
        marker = None

        for c in article.find_all(string=lambda t: isinstance(t, Comment)):
            if "INSERIRE QUI" in c:
                marker = c
                break

        if marker:
            fragment = BeautifulSoup("\n".join(blocks), "lxml")
            marker.insert_after(fragment)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(str(soup))


def build():
    blocks = read_docx("_testo.docx")

    with open("_modello.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "lxml")

    articles = soup.find_all("article")

    distributed = distribute_blocks(blocks, articles)

    inject("_modello.html", distributed, "_output.html")


if __name__ == "__main__":
    build()