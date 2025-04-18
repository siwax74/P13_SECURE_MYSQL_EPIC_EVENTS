# 🧠 Application de Gestion BDD SÉCURISÉ - Utilisateurs, Clients, Contrats & Événements

Une application console en Python pour gérer des utilisateurs, clients, contrats et événements avec authentification sécurisée, rôles, permissions, et une architecture modulaire. Idéal pour les équipes commerciales et support.

---

## 📚 Sommaire

- [Description](#description)
- [Fonctionnalités](#fonctionnalités)
- [Technologies utilisées](#technologies-utilisées)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Structure du projet](#structure-du-projet)
- [Contribution](#contribution)
- [License](#license)

---

<h2 id="description">📝 Description</h2>

Cette application de gestion permet de :
- Gérer les connexions utilisateur avec vérification par email/mot de passe
- Naviguer dans des menus dynamiques selon le rôle de l'utilisateur
- Gérer les entités : Utilisateurs, Clients, Contrats, Événements
- Sécuriser les actions par des permissions basées sur les rôles
- Suivre les activités et les modifications apportées aux données

---

<h2 id="fonctionnalités">✨ Fonctionnalités</h2>

### Sécurité
- Authentification sécurisée avec `bcrypt`
- Système de permissions granulaires basé sur les rôles
- Validation des données en entrée
- Protection contre les injections SQL via ORM

### Gestion
- Gestion complète des utilisateurs (CRUD)
- Gestion des clients et de leurs informations
- Suivi des contrats avec dates et états
- Planification et suivi des événements

### Technique
- Suivi des erreurs avec `Sentry`
- Décorateurs pour la robustesse (`safe_execution`, `with_banner`)
- Contrôleurs modulaires
- Interface console interactive avec menus colorés
- Architecture extensible MVC
- Journalisation des actions effectuées

---

<h2 id="technologies-utilisées">🧰 Technologies utilisées</h2>

- Python 3.7+
- SQLAlchemy (ORM)
- MySQL/PostgreSQL (ou autre base de données SQL)
- bcrypt (hashing sécurisé)
- Sentry SDK (monitoring d'erreurs)
- python-dotenv (gestion des variables d'environnement)
- Architecture MVC (Modèle - Vue - Contrôleur)

---

<h2 id="prérequis">⚙️ Prérequis</h2>

- Python 3.7 ou supérieur
- PostgreSQL, MySQL ou autre base SQL compatible
- `pip` installé et à jour
- Un DSN Sentry (optionnel pour suivi des erreurs)
- Git (pour cloner le projet)

---

<h2 id="installation">🚀 Installation</h2>

1. **Cloner le projet :**
   ```bash
   git clone https://github.com/siwax74/P13_SECURE_MYSQL_EPIC_EVENTS.git .
   ```

2. **Créer un environnement virtuel :**
   ```bash
   # Sur Linux/Mac
   python -m venv venv
   source venv/bin/activate
   
   # Sur Windows
   python -m venv venv
   venv\scripts\activate
   ```

3. **Installer les dépendances :**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer la base de données :**
   ```bash
   # Créer un fichier .env avec les informations de connexion
   
   # Sur Linux/Mac
   touch .env
   
   # Sur Windows
   echo.>.env
   ```

5. **Éditer le fichier .env avec les informations suivantes :**
   ```
   DB_USERNAME=votre_utilisateur
   DB_PASSWORD=votre_mot_de_passe
   DB_HOST=localhost
   DB_PORT=3306 # Defaut
   DB_NAME=nom_de_votre_base
   DSN_SENTRY=votre_dsn_sentry
   ```

---

<h2 id="utilisation">🖥️ Utilisation</h2>

1. **Lancement de l'application :**
   ```bash
   python main.py
   ```

2. **Connexion :**
   - Utilisez les identifiants par défaut pour la première connexion :
     - Email : admin@example.com
     - Mot de passe : admin123
   - N'oubliez pas de changer ce mot de passe après la première connexion !

3. **Navigation :**
   - Utilisez les numéros pour naviguer dans les menus
   - Suivez les instructions à l'écran
   - Appuyez sur 'q' ou '0' pour quitter un menu ou l'application

---

<h2 id="structure-du-projet">📂 Structure du projet</h2>

```
.
├── app/
│   ├── controllers/                # Logique de l'application
│   │   ├── client_controller.py    # Gestion des clients
│   │   ├── contract_controller.py  # Gestion des contrats
│   │   ├── event_controller.py     # Gestion des événements
│   │   ├── login_controller.py     # Authentification
│   │   ├── main_controller.py      # Contrôleur principal
│   │   └── user_controller.py      # Gestion des utilisateurs
│   ├── models/                     # Modèles de données
│   │   ├── base.py                 # Classe de base pour les modèles
│   │   ├── client.py               # Modèle Client
│   │   ├── contract.py             # Modèle Contrat
│   │   ├── event.py                # Modèle Événement
│   │   └── user.py                 # Modèle Utilisateur
│   ├── views/                      # Interface utilisateur
│   │   ├── BaseView.py             # Classe de base pour les vues
│   │   ├── client_view.py          # Vue des clients
│   │   ├── contract_view.py        # Vue des contrats
│   │   ├── event_view.py           # Vue des événements
│   │   ├── main_view.py            # Vue principale
│   │   └── user_view.py            # Vue des utilisateurs
│   ├── decorators.py               # Décorateurs utilitaires
│   ├── mixins.py                   # Classes de mixins
│   └── permissions.py              # Système de permissions
├── flake8.py                       # Configuration de linting
├── main.py                         # Point d'entrée de l'application
├── pyproject.toml                  # Configuration du projet
├── README.md                       # Documentation
├── requirements.txt                # Dépendances
└── settings.py                     # Configuration globale
```

---

<h2 id="contribution">🤝 Contribution</h2>

Les contributions sont les bienvenues ! Pour contribuer :

1. Fork le projet
2. Créez votre branche de fonctionnalité (`git checkout -b feature/ma-nouvelle-fonctionnalite`)
3. Commit vos changements (`git commit -m 'Ajout de ma fonctionnalité'`)
4. Push vers la branche (`git push origin feature/ma-nouvelle-fonctionnalite`)
5. Ouvrez une Pull Request

Veuillez respecter les standards de code et ajouter des tests pour les nouvelles fonctionnalités.

---

<h2 id="license">📄 License</h2>

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

---

© 2025 Siwax74 - Tous droits réservés