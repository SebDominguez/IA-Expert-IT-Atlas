# M5 -Brief 1 -Déployer un projet IA en architecture modulaire avec CI/CD

Dans ce projet, vous allez poser les bases d’une architecture moderne en séparant le frontend et le backend, en dockerisant les composants, en définissant une logique de calcul simple, et en préparant le projet pour une intégration continue. Ce template servira de socle aux futurs projets déployés.

### Référentiels
Compétences transversales

### Ressources
- opco-atlas-docker-compose.docx
- opco-atlas-github-actions-ci.pdf

### Contexte du projet
FastIA souhaite mettre en place une architecture de base pour ses projets IA.

L’objectif est d’avoir un frontend utilisateur simple, une API FastAPI bien structurée, un environnement conteneurisé avec Docker et une automatisation des tests via GitHub Actions.

**Cette architecture servira de modèle reproductible pour tous les futurs projets de déploiement.**

L'équipe MLOps vous confie donc la mission de créer un template minimaliste, facilement extensible, conforme aux bonnes pratiques d’ingénierie logicielle.

Vos tâches seront de :

- structurer le dépôt de code et versionner le code.
- préparer un script de déploiement de l’API (FastAPI).
- connecter les différentes étapes de test, déploiement, mise à jour et suivi à travers une chaîne CI/CDD via GitHub Actions

Ce geste professionnel s’inscrit dans une logique d’amélioration continue, où les données évolutives, les retours métier et les performances du modèle sont pris en compte pour piloter les mises à jour futures.

### Modalités pédagogiques
Projet individuel. Les livrables doivent être versionnés dans un dépôt Git propre, organisé, avec un fichier README clair.

Les outils à utiliser sont :

- Streamlit pour le frontend
- FastAPI + Pydantic pour l’API
- Docker & Docker Compose pour l’environnement
- Loguru pour les logs
- pytest pour les tests backend
- GitHub + GitHub Actions pour l’intégration continue

**Contraintes techniques spécifiques :**

- Le champ du frontend envoie un entier vers une API REST.
- L’API retourne le carré de l’entier après validation du type.
- Le calcul se fait dans un fichier dédié modules/calcul.py.
- Le backend contient un dossier tests/ avec un test de cette fonction.
- Le Docker Compose ne doit lancer que le frontend et le backend.
- Aucune base de données n’est requise à ce stade.

Structure à respecter :
```txt
📁 frontend/
└── app.py (Streamlit + Loguru)
└── Dockerfile
📁 backend/
└── main.py (FastAPI avec 3 routes)
└── modules/calcul.py
└── tests/test\_calcul.py
└── Dockerfile
📄 docker-compose.yml
```


### Modalités d'évaluation
L’API répond bien aux 3 routes définies (/, /health, /calcul)
Le frontend affiche une UI simple et fonctionnelle
Le calcul est correct et validé via Pydantic
La structure du projet est propre et conforme
Le Docker Compose démarre sans erreur les deux services
Les logs sont lisibles et correctement intégrés via Loguru
Les tests pytest fonctionnent et couvrent la fonction calcul()
Un fichier .github/workflows/test.yml valide l’exécution des tests automatisés


### Livrables

Dépôt Git avec :
- frontend/app.py + Dockerfile
- backend/main.py, modules/calcul.py, tests/test_calcul.py, Dockerfile
- docker-compose.yml
- .github/workflows/test.yml

README.md décrivant l’architecture, les routes, les instructions de lancement


### Critères de performance
Le projet respecte les standards de développement MLOps (modularité, logs, tests, CI/CD)
L’environnement Docker est isolé, reproductible et bien configuré
La logique métier est découplée, testable, réutilisable
L’intégration continue fonctionne dès le push sur GitHub
Le code est clair, documenté, et facilement maintenable


dépot git https://github.com/SebDominguez/M5B1
