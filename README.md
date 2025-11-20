# Système de Gestion d'Archives Universel (SGAU)

## 📋 Description

Système de Gestion d'Archives Universel (SGAU) est une application modulaire et extensible pour la gestion complète des archives dans n'importe quelle organisation. Le système supporte la gestion des dossiers, des mouvements, des utilisateurs, et offre des fonctionnalités avancées de recherche et de reporting.

## 🎯 Fonctionnalités principales

### ✅ Gestion des Dossiers
- Création, modification, suppression de dossiers
- Classification par catégories et états
- Localisation physique et virtuelle
- Métadonnées personnalisables
- Historique complet des modifications

### ✅ Gestion des Mouvements
- Suivi des prêts, retours, transferts
- Types de mouvements configurables
- Historique détaillé avec timestamps
- Notifications automatiques
- Workflow d'approbation

### ✅ Gestion des Utilisateurs
- Système d'authentification sécurisé (une seule fenêtre de connexion à l'ouverture de l'application, via PyQt5)
- Gestion des rôles et permissions
- Profils utilisateurs personnalisables
- Audit trail des actions

### ✅ Recherche et Filtrage
- Recherche textuelle avancée
- Filtres par critères multiples
- Export des résultats
- Sauvegarde des recherches fréquentes

### ✅ Rapports et Analytics
- Tableaux de bord personnalisables
- Statistiques d'utilisation
- Rapports périodiques automatiques
- Export en différents formats

## 🏗️ Architecture

```
SGAU/
├── backend/                 # Backend Python
│   ├── api/                # API REST (FastAPI)
│   ├── models/             # Modèles de données
│   ├── services/           # Logique métier
│   ├── config/             # Configuration
│   └── utils/              # Utilitaires
├── frontend/               # Interface utilisateur
│   ├── components/         # Composants réutilisables
│   ├── pages/             # Pages principales
│   ├── services/          # Services API
│   └── assets/            # Ressources statiques
├── mobile/                # Application mobile (future)
├── docs/                  # Documentation
├── tests/                 # Tests automatisés
└── docker/                # Configuration Docker
```

## 🚀 Installation

### Prérequis
- Python 3.8+
- SQLite (développement) / PostgreSQL (production)
- Node.js 16+ (pour le frontend web)

### Installation rapide
```bash
# Cloner le projet
git clone <repository-url>
cd SGAU

# Installation backend
cd backend
pip install -r requirements.txt
python init_db.py

# Installation frontend (optionnel)
cd ../frontend
npm install
npm run dev
```

## 📖 Utilisation

### Démarrage rapide
```bash
# Lancer le backend
cd backend
python main.py

# Lancer l'interface desktop
cd frontend
python main.py
```

#### Authentification (Desktop)
- Lors du lancement de l'application desktop (`python main.py` dans le dossier `frontend`), une seule fenêtre de connexion s'affiche (PyQt5).
- Saisissez votre nom d'utilisateur et votre numéro de matricule pour vous connecter.
- Après authentification, l'interface principale s'ouvre avec vos droits et informations utilisateur.
- **Mode démo :** Si les identifiants ne correspondent à aucun compte, un accès testeur est accordé (permissions limitées).
- **Comptes de test disponibles :**
  - admin / EMP001
  - jean.dupont / EMP002
  - marie.martin / EMP003
  - ahmed.hassan / EMP004
  - fatima / EMP005

#### Note sur l'architecture Desktop
- L'application desktop n'utilise pas l'API REST du backend : elle accède directement à la base de données SQLite via le module `backend/db.py`.
- Le serveur backend n'a pas besoin d'être lancé pour utiliser l'application desktop.

### Configuration
1. Copier `config/config.example.py` vers `config/config.py`
2. Modifier les paramètres selon votre environnement
3. Configurer la base de données
4. Créer les premiers utilisateurs

## 🔧 Configuration

### Variables d'environnement
```bash
# Base de données
DATABASE_URL=sqlite:///archives.db
SECRET_KEY=your-secret-key

# Application
DEBUG=True
LOG_LEVEL=INFO
```

### Configuration multi-organisations
Le système supporte plusieurs organisations avec des configurations séparées :
- Base de données par organisation
- Thèmes et logos personnalisables
- Workflows spécifiques
- Permissions granulaires

## 📊 Cas d'usage

### 1. Archives d'entreprise
- Gestion des documents RH
- Archives techniques
- Documents financiers
- Contrats et accords

### 2. Archives publiques
- Documents administratifs
- Archives historiques
- Gestion des demandes d'accès
- Numérisation et préservation

### 3. Bibliothèques
- Gestion des prêts
- Catalogage
- Gestion des utilisateurs
- Statistiques d'utilisation

## 🛠️ Développement

### Structure du code
- **Backend** : Architecture en couches (API, Services, Modèles)
- **Frontend** : Composants modulaires et réutilisables
- **Base de données** : Migrations et versioning
- **Tests** : Couverture complète avec pytest

### Standards de code
- PEP 8 pour Python
- ESLint pour JavaScript
- Documentation automatique
- Tests unitaires et d'intégration

## 📈 Roadmap

### Version 1.0 (Actuelle)
- ✅ Gestion des dossiers
- ✅ Gestion des mouvements
- ✅ Interface desktop
- ✅ Système d'utilisateurs

### Version 2.0 (En cours)
- 🔄 Interface web moderne
- 🔄 API REST complète
- 🔄 Système de permissions avancé
- 🔄 Recherche avancée

### Version 3.0 (Future)
- 📋 Application mobile
- 📋 IA pour classification automatique
- 📋 Intégration OCR
- 📋 Workflow automatisé

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👥 Auteurs

- **Votre nom** - *Développement initial* - [Votre GitHub]

## 🙏 Remerciements

- OCP Khouribga pour le cas d'usage initial
- La communauté open source
- Les contributeurs du projet

---

**SGAU** - Système de Gestion d'Archives Universel
*Une solution moderne et flexible pour la gestion d'archives* 