# Metodika — Seimo 110/120 rinkimų sistemos tyrimas v0.5

## Tyrimo klausimas
Tyrimas nėra politinis pasirinkimas už konkretų Seimo dydį. Jis lygina institucinių konstrukcijų efektus: Seimo dydį, regioninės proporcinės dalies geografiją, kandidato personalizavimą, nacionalinį 5 % filtrą ir parlamento darbinį pajėgumą.

## Tiriami modeliai
- 120 = 60 vienmandačių + 60 regioninių vietų.
- 110 = 55 vienmandatės + 55 regioninės vietos.
- 5 regioninės daugiamandatės apygardos.
- Vienas kandidatas = vienas kelias: arba vienmandatė, arba regioninė dalis; dvigubas kandidatavimas neleidžiamas.
- Regioninėje dalyje rinkėjas balsuoja už konkretų kandidatą; kandidato balsas kartu skaičiuojamas jo partijai regione.
- Partijos regioninius mandatus gauna jos daugiausia asmeninių balsų surinkę kandidatai.
- Partijų mandatams regione naudojamas D’Hondt metodas.
- Pagrindinis scenarijus netaiko nacionalinio 5 % filtro; atskirai rodomas jautrumo testas su vienodu 5 % nacionaliniu filtru.

## Regionų mandatų paskirstymas
Regionų vietos dalijamos pagal registruotų rinkėjų skaičių, naudojant Hare kvotą ir didžiausias liekanas. Rinkimų aktyvumas vietų regionams neskirsto.

## Istoriniai testiniai duomenys
- 2024: PASS.
- 2020: PASS.
- 2016: OPEN / PROVISIONAL dėl viešo apylinkių rinkinio `registered_voters` vardiklio neatitikimo oficialiai nacionalinei 2016 rinkėjų bazei. Robustumo testas pagrindinės kokybinės išvados nekeičia.

Istoriniai rezultatai naudojami kaip testiniai duomenų rinkiniai, o ne kaip argumentai už ar prieš konkrečią partiją.

## Ką galima ir ko negalima perskaičiuoti
Galima perskaičiuoti partijų balsų geografiją, regioninių mandatų pasiskirstymą, Gallagher indeksą, balsų už regione 0 mandatų gavusius sąrašus ir faktinius regioninius slenksčius.

Negalima tiksliai nustatyti, kurie konkretūs kandidatai būtų buvę išrinkti personalizuotoje regioninėje sistemoje, nes istoriniai rinkėjai balsavo pagal kitą kandidatų pasirinkimo mechanizmą. Taip pat negalima tiksliai nustatyti hipotetinių 55/60 naujų vienmandačių nugalėtojų, kol nenubrėžtos jų ribos.

## Rodiklis „0 mandatų balsai“
Tai balsai už sąrašą, kuris rinkėjo regioninėje daugiamandatėje negavo nė vieno mandato. Tai nėra normatyvinis „iššvaistyto balso“ vertinimas.

## Darbingumo streso testas
Komitetų ir komisijų blokas nėra rinkimų rezultato prognozė. Jis tikrina, ar mažesnio parlamento vidinė darbo architektūra turėtų būti peržiūrima kartu su narių skaičiumi.


## Komitetų architektūros scenarijus

Mažesnio Seimo darbingumo testas nelaiko dabartinės 17 komitetų struktūros nekintama. White paper scenarijuje tikrinama 11 funkcinių komitetų konsolidacija:

1. Biudžeto ir finansų.
2. Viešojo audito ir atskaitomybės.
3. Ekonomikos, energetikos, transporto ir inovacijų.
4. Aplinkos, žemės ūkio ir teritorinės plėtros.
5. Socialinės politikos, sveikatos ir demografijos.
6. Švietimo, mokslo, kultūros ir sporto.
7. Teisės ir žmogaus teisių.
8. Nacionalinio saugumo ir gynybos.
9. Užsienio ir Europos reikalų.
10. Valstybės valdymo ir savivaldos.
11. Ateities, skaitmenizavimo ir strateginės raidos.

Tai nėra normatyvinė rekomendacija ar galutinis Statuto projektas. Tai institucinės architektūros scenarijus, skirtas patikrinti, ar mažesnis 110 / 120 narių Seimas galėtų išlaikyti pakankamo dydžio pagrindinius komitetus, jei artimos funkcijos būtų konsoliduotos.

Palyginamieji atspirties taškai:
- Estijos 101 nario Riigikogu turi 11 nuolatinių komitetų; narys priklauso vienam nuolatiniam komitetui, be galimos narystės ES reikalų ar kituose specialiuose komitetuose.
- Latvijos 100 narių Saeima naudoja platesnius funkcinius komitetus ir pakomitečius; narys gali dirbti iki dviejų nuolatinių komitetų.
- Suomijos Parlamento Ateities komitetas veikia nuo 1993 m.; tai naudojama kaip argumentas konsoliduojant neprarasti ilgalaikės strateginės raidos funkcijos.

11 komitetų scenarijus automatiškai nereiškia komisijų panaikinimo. Nuolatinių, laikinųjų ir tyrimo komisijų poreikis bei narių apkrova yra atskiras projekto sluoksnis.
