### 🚀 La "Catchphrase" (Description courte)

> 🏎️ **Devenez le prochain génie du muret des stands grâce à ce simulateur Python qui optimise vos stratégies de course en temps réel (Météo, Pneus, Fuel) \!**
> 📊 **Une fusion parfaite entre Algorithmique et Data Viz pour prouver que la victoire se joue à la milliseconde près. 🏁**

# 🏎️ F1 Strategy Simulator : Le Cerveau Virtuel de la Course

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![DataScience](https://img.shields.io/badge/Data-Science-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Ready%20to%20Race-red?style=for-the-badge)

> **"La course ne se gagne pas seulement sur la piste, elle se gagne sur les écrans."**

Ce projet est un moteur de simulation et d'optimisation de stratégie de Formule 1. Il combine **modélisation physique** et **puissance algorithmique** pour résoudre le casse-tête ultime : quelle est la stratégie la plus rapide pour rallier l'arrivée ?

---

## ☕ L'histoire (presque) vraie de ce projet

Tout est parti d'un dimanche après-midi, devant un Grand Prix, à crier devant ma télé : *"Mais pourquoi ils ne s'arrêtent pas maintenant ?!"*.
Plutôt que de continuer à hurler dans le vide (et d'effrayer mon chat), j'ai décidé de coder un outil capable de **battre les stratèges de Ferrari** (ce qui, entre nous, n'est pas toujours très difficile 😉).

Le résultat ? Un simulateur capable de digérer des variables complexes (météo changeante, dégradation gomme, consommation d'essence) pour sortir **LA** stratégie gagnante.

---

## ⚙️ Sous le capot : Architecture Technique

Ce n'est pas juste une calculatrice, c'est un outil d'aide à la décision basé sur la donnée.

### 1. Le Moteur Physique 🧮
Le script simule chaque tour de roue en prenant en compte :
* **La physique des pneus :** Gestion de 5 types de gommes (Soft, Medium, Hard, Inter, Wet) avec leurs courbes de dégradation et fenêtres de performance.
* **La dynamique des fluides (simplifiée) :** Impact du poids du carburant sur le temps au tour (0.03s/L) et consommation variable selon la météo.
* **L'aléatoire maîtrisé :** Injection de "bruit" statistique pour simuler les imperfections humaines et mécaniques.

### 2. L'Algorithme de Stratégie 🧠
C'est le cœur du réacteur. Le programme n'essaie pas au hasard ; il **génère intelligemment** des arbres de décision :
* Utilisation de **méthodes récursives (Backtracking)** pour explorer les combinaisons de relais (stints) possibles.
* Filtrage dynamique selon la météo (impossible de mettre des *Slicks* sous la pluie).
* Comparaison de centaines de scénarios pour minimiser la fonction de coût (le temps total de course).

### 3. La Data Visualization 📈
Parce qu'un tableau de chiffres c'est bien, mais un graphique c'est mieux. Utilisation de **Matplotlib** et **Seaborn** pour générer un rapport de course complet post-simulation.

---

## 🎮 Comment ça marche ?

Le programme suit une logique en 4 temps, digne d'une écurie professionnelle :

1.  **Initialization** : On charge les paramètres du circuit (64 tours, temps de base 90s) et le scénario météo (Sec -> Pluie -> Sec).
2.  **Generation** : L'algorithme découpe la course en segments et propose des configurations de pneus valides.
3.  **Simulation** : Chaque stratégie est "jouée" virtuellement. On calcule l'usure tour par tour, on applique le *Lift & Coast* si le carburant manque.
4.  **Analytics** : Le script élit la stratégie championne et plot les graphiques de télémétrie.

---

## 🚀 Installation et Usage

Pré-requis : Avoir Python installé et un casque de pilote (optionnel).

```bash
# 1. Cloner le repo
git clone [https://github.com/votre-username/Simulateur-Strategie-F1.git](https://github.com/votre-username/Simulateur-Strategie-F1.git)

# 2. Installer les dépendances (la Sainte Trinité de la Data)
pip install numpy pandas matplotlib seaborn

# 3. Lancer la simulation
python app.py
````

### Exemple de Sortie Console

Le programme vous dira exactement quoi faire :

```text
=== MEILLEURE STRATÉGIE ===
Stints : [('hard', 35 tours), ('medium', 4 tours), ('intermediate', 20 tours)...]
Temps total : 5806.21 s
```

-----

## 📊 Visualisation

À la fin de l'exécution, vous obtenez un dashboard complet comprenant :

  * **Temps au tour :** Visualisez votre rythme s'effondrer quand vos pneus sont morts.
  * **Carburant :** La courbe de consommation (attention à la panne sèche \!).
  * **Usure des pneus :** Suivez la dégradation en pourcentage.
  * **Météo :** Corrélation directe entre la pluie et vos choix de pneus.

-----

## 🤝 Crédits & Remerciements

  * **Auteur :** Corentin Cartallier - *Développeur & Stratège du dimanche.*
  * **Expertise Technique :** Un immense merci à **Loris ALUNNO**. Son approche analytique et nos débats passionnés sur la précision des modèles mathématiques ont été le carburant de ce projet.

-----

*Ce projet est open-source. N'hésitez pas à forker pour ajouter la gestion des Safety Cars ou des drapeaux rouges \!* 🚩
