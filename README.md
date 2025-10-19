# 🏎️ Simulateur-Strategie-F1
  
**RaceStrategySimulator** est un projet Python de simulation et d’optimisation de stratégie de course inspiré de la Formule 1.  
Il combine **modélisation physique** (pneus, météo, carburant, dégradation) et **logique algorithmique** pour trouver la stratégie la plus rapide sur une course complète.

---

## Objectif

Simuler le comportement d’une voiture sur une course complète afin de **tester et comparer différentes stratégies** :
- Choix des **pneus** selon la météo (sec, pluie, intermédiaire)
- Gestion du **carburant** et de la consommation
- Effet du **Lift & Coast** sur le rythme et la consommation
- Impact des **arrêts aux stands** et du **nombre de relais**

Le programme détermine automatiquement la combinaison optimale pour obtenir le **meilleur temps total de course**.

---

## Logique de fonctionnement

1. **Paramétrage global**  
   L’utilisateur définit les conditions de course (nombre de tours, météo, types de pneus, consommation, etc.).

2. **Génération des stratégies**  
   Le simulateur crée automatiquement un ensemble de stratégies réalistes :
   - respect des contraintes pneus/météo,  
   - limites de tours par relais,  
   - nombre d’arrêts aux stands maximal.

3. **Simulation de chaque stratégie**  
   Pour chaque combinaison :
   - calcul du temps au tour (dégradation, carburant, hasard),
   - mise à jour du carburant et des pneus,
   - prise en compte des arrêts et du lift & coast.

4. **Évaluation et sélection**  
   Le programme trie toutes les stratégies et affiche celle qui minimise le **temps total de course**.

5. **Visualisation interactive**  
   Des graphiques illustrent :
   - le **temps au tour** (avec code couleur des pneus),
   - l’**évolution du carburant**,
   - la **dégradation des pneus** (reset à chaque relais),
   - et les **conditions météo** tour par tour.

---

## Exemple de sortie

```text
=== MEILLEURE STRATÉGIE ===
Stints : [('hard', 35, 0), ('medium', 4, 0), ('intermediate', 20, 0), ('intermediate', 5, 0)]
Temps total : 5806.21 s
```  
  
## Remerciements  
Un grand merci à ***Loris ALUNNO***, dont les réflexions, la curiosité et les échanges techniques autour de la stratégie de course et de la simulation m’ont inspiré dans le développement de ce projet.  
Son approche analytique et sa passion pour la précision des modèles ont largement contribué à faire évoluer cette version du simulateur.  
