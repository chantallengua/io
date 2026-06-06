2026/06/06
# Regole SEO

----- Per racconti: -----
nell <head> :
riga 8:
<title>Nike | Racconto breve gratuito di Chantal Lengua</title>

<meta name="description" content="Racconto breve di Chantal Lengua. Narrativa originale tra coscienza, percezione e irreale.">
(per tutti i racconti)

  <meta property="og:title" content="Nike | Chantal Lengua">
  <meta property="og:description" content="Racconto breve di Chantal Lengua. Narrativa originale tra coscienza, percezione e irreale.">
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://chantallengua.github.io/io/racconti/nike.html">
  <meta property="og:image" content="https://chantallengua.github.io/io/img/logo2.png">
  <link rel="canonical" href="https://chantallengua.github.io/io/racconti/nike.html">

nel <body>:
<h1 class="visually-hidden">Nike</h1>

Chat consiglia di aggiungere anche un primo <p> tipo:
<p class="visually-hidden">Racconto breve di narrativa speculativa in cui la statua della Nike di Samotracia diventa centro di un evento globale che trasforma la percezione della realtà.</p>

----- Per newsletter: -----
nell <head> :
<title>La Tazza Vuota #7 | Una vita piena di vita | Chantal Lengua</title>	<meta name="description" content="La Tazza Vuota: newsletter settimanale gratuita dedicata a mindfulness, concentrazione e consapevolezza.">        
	<link rel="icon" href="../img/ico.png">
	<meta property="og:title" content="La Tazza Vuota #7 | Una vita piena di vita | Chantal Lengua">
	<meta property="og:description" content="La Tazza Vuota: newsletter settimanale gratuita dedicata a mindfulness, concentrazione e consapevolezza.">
	<meta property="og:url" content="https://chantallengua.github.io/io/newsletter7.html">
	<meta property="og:type" content="website">
	<meta property="og:image" content="https://chantallengua.github.io/io/img/logo2.png">
	<link rel="canonical" href="https://chantallengua.github.io/io/newsletter7.html">

nel <body> (prima di <!-- Container principale -->) :
<h1 class="visually-hidden"> La Tazza Vuota #7 – Una vita piena di vita </h1>

----------------

- Ho aggiunto robots.txt per indicizzazione
- Ho aggiunto sitemap.xml per indicizzazione
- con comando 'python sitemap.py' si crea nuova sitemap via via che si aggiungono i racconti e le newsl ("sitemap.xml") e la vecchia viene cambiata di nome con suo timestamp