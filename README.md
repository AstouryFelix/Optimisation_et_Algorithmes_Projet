# Projet d'Optimisation et Algorithmes.  
Le détail des attentes est dans "gurobipy_ Evaluation.pdf".  
La problématique, ainsi que le détail du format d'entrée et de sortie, est dans "hashcode_2017_qualification_round.pdf".  
Afin de lancer le projet :
- Avec la dernière version, lancant respectivement un exemple léger et une instance lourde :
    - python .\videos.py .\datasets\example.in
    - python .\videos.py .\datasets\trending_4000_10k.in

- Avec la version non optimisé, suivant la modélisation :
    - python .\videos_classique_old.py .\datasets\example.in
    - python .\videos_classique_old.py .\datasets\trending_4000_10k.in

- Avec la version matricielle /!\ trending_4000_10k.ini prend plus de 30 minutes : 
    - python .\videos_matrix.py .\datasets\example.in
    - python .\videos_matrix.py .\datasets\trending_4000_10k.in
