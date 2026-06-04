import os
import sys
import glob
import re
import webbrowser
from bs4 import BeautifulSoup

def select_file(extension_pattern, file_type_label):
    """Mostra una selezione interattiva dei file nella cartella corrente."""
    files = glob.glob(extension_pattern)
    if not files:
        print(f"\n[!] Nessun file {file_type_label} trovato nella cartella corrente.")
        return None
    
    print(f"\nSeleziona un file {file_type_label}:")
    for i, file in enumerate(files, 1):
        print(f"[{i}] {file}")
        
    while True:
        try:
            scelta = int(input(f"Inserisci il numero del file {file_type_label}: "))
            if 1 <= scelta <= len(files):
                return files[scelta - 1]
            else:
                print("Numero non valido, riprova.")
        except ValueError:
            print("Per favore, inserisci un numero valido.")

def clean_text(text):
    """Pulisce il testo per un confronto fuzzy robusto, ignorando formattazione e spazi."""
    text = re.sub(r'<[^>]+>', '', text)  # Rimuove eventuali tag HTML residui
    text = re.sub(r'[^\w]', '', text)     # Rimuove punteggiatura e spazi
    return text.lower()

def main():
    print("==================================================")
    print("   SINCRONIZZATORE AVANZATO STORYBOOK (FUZZY)     ")
    print("==================================================")
    
    # 1. Selezione interattiva dei file
    html_file = select_file("*.html", "HTML")
    if not html_file:
        sys.exit()
        
    txt_file = select_file("*.txt", "TXT")
    if not txt_file:
        sys.exit()
        
    # 2. Lettura dei file
    with open(html_file, 'r', encoding='utf-8') as f:
        html_data = f.read()
        
    with open(txt_file, 'r', encoding='utf-8') as f:
        txt_data = f.read()
        
    soup = BeautifulSoup(html_data, 'html.parser')
    txt_soup = BeautifulSoup(txt_data, 'html.parser')
    
    # Estrazione dei nuovi paragrafi dal TXT
    new_paragraphs = txt_soup.find_all('p')
    if not new_paragraphs:
        # Se il TXT non ha tag <p>, separa per linee vuote e creali
        raw_lines = [line.strip() for line in txt_data.split('\n') if line.strip()]
        new_paragraphs = []
        for line in raw_lines:
            p_tag = soup.new_tag('p')
            p_tag.string = line
            new_paragraphs.append(p_tag)

    # 3. Analisi della struttura HTML originale (i blocchi <article> / pagine)
    articles = soup.find_all('article')
    if not articles:
        print("[!] Errore: Nessun tag <article> trovato nel file HTML.")
        sys.exit()
        
    # Estraiamo tutti i vecchi paragrafi testuali validi e mappiamo a quale pagina appartengono
    old_paragraphs_mapped = []
    for art_idx, art in enumerate(articles):
        for p in art.find_all('p'):
            if p.get_text(strip=True) and p.get_text(strip=True) != ' ': # Salta spazi vuoti/padding
                old_paragraphs_mapped.append({
                    'text_clean': clean_text(p.get_text()),
                    'art_idx': art_idx
                })

    if not old_paragraphs_mapped:
        print("[!] Errore: L'HTML originale non contiene paragrafi di testo validi su cui tararsi.")
        sys.exit()

    # 4. Assegnazione Fuzzy dei nuovi paragrafi alle rispettive pagine (<article>)
    # Invece di contare 1:1, calcoliamo la posizione relativa del testo nel flusso narrativo
    new_art_lists = {i: [] for i in range(len(articles))}
    
    total_old = len(old_paragraphs_mapped)
    total_new = len(new_paragraphs)
    
    print(f"\n[*] Paragrafi nell'HTML originale: {total_old}")
    print(f"[*] Paragrafi nel nuovo TXT: {total_new}")
    print("[*] Sincronizzazione dinamica basata sul flusso narrativo...")

    for new_idx, p_new in enumerate(new_paragraphs):
        # Calcoliamo l'indice proporzionale stimato nel vecchio testo
        estimated_old_idx = int((new_idx / total_new) * total_old)
        # Troviamo la pagina associata a quel punto del racconto originale
        estimated_old_idx = min(estimated_old_idx, total_old - 1)
        target_article_idx = old_paragraphs_mapped[estimated_old_idx]['art_idx']
        
        new_art_lists[target_article_idx].append(p_new)

    # 5. Ricostruzione dell'HTML salvando elementi strutturali (titoli, pulsanti, ecc.)
    for idx, art in enumerate(articles):
        # Salviamo i tag di intestazione (es. titoli dei capitoli <h2>, bottoni PDF)
        headers = []
        for child in list(art.children):
            if child.name and child.name != 'p':
                headers.append(child.extract())
            elif child.name == 'p':
                child.extract() # Svuota i vecchi paragrafi
                
        # Reinseriamo i titoli/bottoni salvati all'inizio della pagina
        for h in headers:
            art.append(h)
            
        # Inseriamo i nuovi paragrafi assegnati a questa pagina
        for p_new in new_art_lists[idx]:
            art.append(p_new)
            art.append("\n\t\t\t\t") # Mantiene la formattazione pulita del codice sorgente
            
        # Se è l'ultimo blocco, aggiungiamo i tag di padding spaziatore originari (&nbsp;)
        if idx == len(articles) - 1:
            for _ in range(4):
                padding_p = soup.new_tag('p')
                padding_p.append(BeautifulSoup('&nbsp;', 'html.parser'))
                art.append(padding_p)

    # 6. Salvataggio del nuovo file con suffisso "2"
    base_name, ext = os.path.splitext(html_file)
    output_filename = f"{base_name}2{ext}"
    
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(str(soup))
        
    print(f"\n[V] Sincronizzazione completata con successo!")
    print(f"[->] File salvato: {output_filename}")
    
    # 7. Apertura automatica su Google Chrome / Browser predefinito
    try:
        abs_path = os.path.abspath(output_filename)
        print("[*] Apertura automatica del file su Chrome...")
        webbrowser.open(f"file://{abs_path}")
    except Exception as e:
        print(f"[!] Impossibile aprire il browser automaticamente: {e}")

if __name__ == '__main__':
    main()