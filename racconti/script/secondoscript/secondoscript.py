def load_html():
    html_files = glob.glob("*.html")

    if len(html_files) == 0:
        raise Exception("Nessun file HTML trovato.")

    if len(html_files) == 1:
        return html_files[0]

    print("HTML trovati:\n")
    for i, f in enumerate(html_files, 1):
        print(f"{i}) {f}")

    while True:
        scelta = input("\nScegli il file HTML da usare: ")

        if scelta.isdigit():
            idx = int(scelta) - 1
            if 0 <= idx < len(html_files):
                return html_files[idx]

        print("Scelta non valida, riprova.")