# VintedPyInterface
    Interface python pour vinted

## Installation
    Pour installer le module, il suffit de lancer la commande suivante dans le terminal :
    ```bash
    pip install vintedpyinterface
    ```

## Utilisation
### Recherche
    Pour le moment, la recherche est limitée à la recherche par nom, taille et marque.
    ```python
    from VintedPyInterface import VintedPyInterface, SearchSetting

    search = SearchSetting("chaussures", "42", "nike")
    vinted = VintedPyInterface()
    print(vinted.Search(search))
    ```