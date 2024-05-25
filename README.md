# Interaktivní mapa měst a krajů v České republice

Tento projekt je interaktivní aplikace postavená na frameworku Dash, která zobrazuje města a kraje České republiky na mapě. Aplikace umožňuje prozkoumat statistiky měst a zobrazit podrobné informace o vybraném regionu.

## Struktura projektu

- `app.py`: Hlavní soubor aplikace Dash, který obsahuje logiku pro vykreslování mapy a grafů.
- `geogenerator.py`: Skript pro generování souřadnic měst pomocí knihovny `geopy` a jejich uložení do JSON souboru.
- `utils.py`: Skript obsahující pomocné funkce pro získávání a zpracování dat z API.

### Spuštění aplikace

1. Ujistěte se, že máte připravené datové soubory `kraje.json`, `souradnice_mest.json` a `mesta.csv` ve složce `data`.

2. Spusťte aplikaci:

    ```sh
    python app.py
    ```

3. Otevřete webový prohlížeč a přejděte na `http://127.0.0.1:8050/`.

## Funkce

- **Mapa měst a krajů**: Zobrazení měst a hranic krajů na interaktivní mapě.
- **Grafy a statistiky**: Zobrazení grafů s průměrnou měsíční frekvencí záznamů, prvním záznamem a celkovým počtem záznamů pro jednotlivá města.
- **Modal okno**: Po kliknutí na město se zobrazí detailní informace o regionu včetně odkazu na PDF dokument.
- **Dynamická aktualizace dat**: Data se dynamicky aktualizují, což zajišťuje aktuálnost zobrazených informací.

## Přizpůsobení

- Pro přizpůsobení vzhledu grafů můžete upravit soubor `assets/fig_layout.py`.
- Data o městech a krajích můžete aktualizovat v souborech `mesta.csv`, `kraje.json` a `souradnice_mest.json`.

## Autoři

- Martin Kučera, Front end
- Jakub Jelínek, Data processing
- Jan Poloha, Back end
- Filip Éder, Back end