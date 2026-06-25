# 🛒 Prijspaniek

Een mobile-first webgame in de stijl van *The Price Is Right*, maar dan met echte producten van **[Action](https://www.action.com/nl-nl/)**.

Je krijgt **10 seconden** om de prijs van een product te raden. Hoe dichterbij, hoe meer punten. Speel een ronde, bouw een combo op, en deel je score.

👉 **Speel:** https://graafg.github.io/prijspaniek/

## Modi

| Mode | Beschrijving |
|------|--------------|
| 📅 **Daily Deal Dash** | 10 vaste items per dag — iedereen speelt dezelfde set (Wordle-style). Deel je score! |
| ⚡ **Quick Play** | 5 willekeurige items voor tussendoor. |
| 💀 **Sudden Death** | Blijf raden tot je er meer dan €2 naast zit. |

## Features

- 📸 **Echte Action-data** — productnamen, foto's, prijzen en links rechtstreeks van action.com
- ⏱️ **10-seconden timer** die pas start zodra de foto geladen is
- 🔥 **Combo-multiplier** voor opeenvolgende goede gokken
- 🎯 Scoring met exact-bonus en speed
- 📊 Resultatenscherm met emoji-grid + deelbare scorekaart
- 💾 Lokale opslag van beste score, streak en aantal potjes
- 🔗 "Bekijk bij Action"-link naar de echte productpagina na elke gok

## Data

De productdataset (`products.js` / `products.json`) wordt gegenereerd door `scrape.py`,
dat de Next.js RSC-payload van Action-categoriepagina's parset.

```bash
python scrape.py
```

Een [GitHub Actions workflow](.github/workflows/refresh-data.yml) draait dit dagelijks
en commit een verse dataset.

> ⚠️ **Disclaimer:** Dit is een hobby-/fanproject. Prijzen en foto's zijn afkomstig van
> action.com en kunnen verlopen of wijzigen. Niet geaffilieerd met of goedgekeurd door Action.

## Lokaal draaien

```bash
python -m http.server 8731
# open http://localhost:8731/
```

## Stack

Pure HTML/CSS/vanilla JS — geen build, geen dependencies. Hosting via GitHub Pages.
