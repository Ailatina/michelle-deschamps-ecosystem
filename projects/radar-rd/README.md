# Momentum by AiLatina · Radar RD

[Leer el periódico en español](https://radar-rd.ailatina.chatgpt.site/#ahora) · [Read the Dominican desk in English](https://radar-rd.ailatina.chatgpt.site/en/#ahora)

Michelle R. Deschamps adapts Dominican news into short live-class exercises. The site reads published Spanish or English stories from AiLatina’s editorial database. Each story is written once per language. Historical editions retain their original dates.

## Source and reproduction

This directory documents the public reader deployed from revision `d4cc3509accd5c7681933fc8ee08d4b590eae62f`. The `.in` files are HTML source templates. The production site above is the reader shared with visitors.

1. Copy `es.html.in` to `index.html` and `en.html.in` to `en/index.html` under a static server root. Copy both stylesheets and `noticias.js` to that root.
2. Before `noticias.js` loads, set `window.RADAR_PUBLISHABLE_KEY` to the Supabase publishable browser key for the AiLatina public articles project. Anonymous row-level access permits reading published articles. No administrative credential belongs in frontend code. To use another backend, configure its public endpoint and its own publishable key.
3. Preserve the archived PDFs at `/ediciones/radar-rd-2026-w37.pdf` and `/ediciones/radar-rd-2026-w38.pdf` from the [public reader](https://radar-rd.ailatina.chatgpt.site/#ediciones). With JavaScript disabled, the reader includes dated links to the November articles. With a connection, it also shows subsequent published stories.
4. Run `python radar_cover.py --help` for the original 4:5 newsroom card. `python render_radar_clip.py SOURCE_CARD.jpg OUTPUT.mp4` recreates the 18-second vertical explainer about the November 5 proposal. The media tools use Pillow, DejaVu fonts and FFmpeg.

The article archive, underlying database, private correspondence and social credentials are maintained by their respective owners. Project documentation and code here are safe to show as part of Michelle’s developer portfolio.
