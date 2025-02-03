# SPZ - systém poslední záchrany
Systém poslední záchrany na Fyziklání

## Použití
### Stáhnutí dat
Aby systém znal jména a jiné údaje o týmech, je potřeba stáhnout data z
FKSDB pomocí `python3 spz.py download`. To vytvoří soubor `teams.json` ve
kterém jsou data o týmech uloženy.

> [!WARNING]
> Data musí být stažena předtím, než spadne FKSDB, jinak se k datům nepůjde
> dostat. Pro je vhodné stáhnout data dopředu a pokud to situace umožní, tak
> je na soutěží jen aktualizovat.

### Spuštění
Script najde všechny `.csv` soubory ve složce `in`. Pokud není v této složce
nebo má jiný typ, script jej nenajde. Poté stačí spustit pomocí `python3
spz.py` a script zkontroluje zadané kódy, zpracuje je a spočítá pořadí.

## Specifikace
### Formát CSV
CSV musí být ve formátu `kód;body`, tedy například `001234AA7;5`. Preferovaným
oddělovačem je středník, lze ale použít libovolně i čárky, mezery nebo
tabulátory. Uvozovky jsou ignorovány. Více oddělovačů za sebou je složených do
jednoho.

### Testování
Pro spuštění testů stačí spustit `pytest`. Pro vytvoření statistik o podchycení
lze využít `coverage run -m pytest` a následně `coverage report` pro vypsání
nebo `coverage html` pro vygenerování html.
