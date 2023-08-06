## Objectif

`simple-pygraph` est un module de manipulation de graphe permettant à la fois de manipuler la stucture et de la visualiser dans un notebook. Il est notamment utile pour des enseignant•e•s souhaitant créer des ressources de cours autours des graphes, arbres etc. Le module s'appuie sur deux modules connus :

- un _modèle_ qui est un graphe au sens de networkx
- une _vue_ qui est un graphe au sens de graphviz

## Installation et utilisation

Le module s'installe simplement :

```
pip3 install simple-pygraph
```

Puis s'utilise (plutôt dans un notebook) :

```python
import PyGraph.pygraph as pg

mon_graphe = pg.Graph(5)
```

## Documentations

- Le dépot gitlab fourni un listing des fonctionnalités
- Ce tutoriel détaille un peu les choses : https://sebhoa.gitlab.io/iremi/01_Graphes/pygraph/