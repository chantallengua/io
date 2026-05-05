document.addEventListener('DOMContentLoaded', () => {
    const { jsPDF } = window.jspdf;

    const downloadLink = document.getElementById('download-pdf');
    if (!downloadLink) return;

    downloadLink.addEventListener('click', async (e) => {
        e.preventDefault();

        const doc = new jsPDF('p', 'pt', 'a4');

        const margin = 60;
        const lineHeight = 16;
        const pageWidth = doc.internal.pageSize.width;
        const pageHeight = doc.internal.pageSize.height;

        const indent = 17; // 0.6 cm

        let x = margin;
        let y = margin;

        // ====== PRENDE TUTTO IL TESTO (tutte le pagine) ======
        const paragraphs = Array.from(document.querySelectorAll('.open-book article p'));

        // ====== FONT (Times New Roman simulato) ======
        doc.setFont('times', 'normal');

        const addParagraph = (p) => {
            if (!p) return;

            const text = p.innerText.trim();
            if (!text) return;

            const words = text.split(/(\s+)/);

            let firstLine = true;
            x = margin;

            words.forEach(word => {
                const textWidth = doc.getTextWidth(word);

                // rientro SOLO prima riga
                if (firstLine) {
                    x += indent;
                    firstLine = false;
                }

                if (x + textWidth > pageWidth - margin) {
                    y += lineHeight;
                    x = margin; // NIENTE indent qui
                    if (y + lineHeight > pageHeight - margin) {
                        doc.addPage();
                        y = margin;
                    }
                }

                doc.text(word, x, y);
                x += textWidth;
            });

            y += lineHeight;
        };

        // ====== BANNER ======
        const bannerUrl = 'https://raw.githubusercontent.com/chantallengua/repository/master/banner-pdf1.jpg';
        const bannerImg = await fetch(bannerUrl)
            .then(res => res.blob())
            .then(blob => new Promise((resolve) => {
                const reader = new FileReader();
                reader.onloadend = () => resolve(reader.result);
                reader.readAsDataURL(blob);
            }));

        doc.addImage(bannerImg, 'JPEG', 0, 0, pageWidth, 50);
        y = 90;

        // ====== AUTORE ======
        const authorName = 'Chantal Lengua';
        doc.setFontSize(10);
        doc.setTextColor(136,136,136);
        doc.setFont('times', 'normal');

        const authorWidth = doc.getTextWidth(authorName);
        doc.text(authorName, (pageWidth - authorWidth) / 2, y);
        y += lineHeight;

        // ====== SITO (CORRETTO) ======
        const siteUrl = 'https://chantallengua.github.io/io';
        const siteWidth = doc.getTextWidth(siteUrl);
        const siteX = (pageWidth - siteWidth) / 2;

        doc.textWithLink(siteUrl, siteX, y, { url: siteUrl });
        doc.line(siteX, y + 2, siteX + siteWidth, y + 2);

        y += lineHeight;

        // ====== LINEA ======
        doc.setDrawColor(200, 200, 200);
        doc.line(margin + 40, y + 4, pageWidth - margin - 40, y + 4);

        // ====== 2 A CAPO ======
        y += lineHeight * 2;

        // ====== TITOLO (no uppercase) ======
        const titleEl = document.querySelector('h2');
        let articleTitle = 'Latte';

        if (titleEl) {
            articleTitle = titleEl.innerText.trim();
        }

        doc.setFont('times', 'bold');
        doc.setFontSize(20);
        doc.setTextColor(33, 37, 41); // #212529

        doc.text(articleTitle, margin, y);

        // ====== 4 A CAPO ======
        y += lineHeight * 4;

        // ====== TESTO ======
        doc.setFont('times', 'normal');
        doc.setFontSize(11);
        doc.setTextColor(0,0,0);

        paragraphs.forEach(p => addParagraph(p));

        // ====== NOME FILE CamelCase ======
        const fileName = `Lengua_${articleTitle.charAt(0).toUpperCase() + articleTitle.slice(1)}.pdf`;

        doc.save(fileName);
    });
});