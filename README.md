# Seimo 110/120 – rinkimų sistemos tyrimas

Viešas, neutralus Lietuvos Seimo dydžio ir rinkimų sistemos architektūros tyrimas.

Tyrimo klausimas nėra „kuri sistema geriausia?“. Tikriname, kaip keistųsi atstovavimas, proporcingumas ir Seimo darbinis pajėgumas, jei kartu būtų keičiami Seimo narių skaičius ir proporcinės dalies geografija.

## Tiriami modeliai

- **120 = 60 vienmandačių + 60 regioninių vietų**
- **110 = 55 vienmandatės + 55 regioninės vietos**
- 5 regioninės daugiamandatės apygardos
- regioninėje dalyje balsuojama už konkretų kandidatą
- kandidato balsas kartu skaičiuojamas jo partijai regione
- partijos regionines vietas gauna daugiausia asmeninių balsų surinkę jos kandidatai
- **vienas kandidatas = vienas kelias**: arba vienmandatė, arba regioninis sąrašas; dvigubas kandidatavimas neleidžiamas
- partijų mandatams regione naudojamas D’Hondt metodas
- pagrindinis scenarijus – be nacionalinio 5 % filtro; 5 % rodomas kaip jautrumo testas

## Istoriniai testai

- **2024 – PASS**
- **2020 – PASS**
- **2016 – OPEN / PROVISIONAL** dėl viešo apylinkių rinkinio registruotų rinkėjų vardiklio neatitikimo oficialiai nacionalinei bazei; robustumo testas pagrindinės kokybinės išvados nekeičia.

Istoriniai rinkimų rezultatai naudojami kaip testiniai duomenų rinkiniai, o ne kaip argumentai už ar prieš konkrečią partiją.

## Struktūra

- `index.html` – interaktyvus tyrimo puslapis
- `METHODOLOGY.md` – metodika, ribos ir statusai
- `data/` – reprodukuojami duomenų priedai
- `scripts/` – skaičiavimo atkūrimo skriptai

## Statusas

**v0.5 release-candidate**. Turinys ir modelio taisyklės stabilizuotos; kitas etapas – viešas GitHub Pages preview ir mobili QA.
