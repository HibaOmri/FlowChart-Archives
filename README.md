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
│   ├── db.py               # Connecteur Neo4j (Graph Database)
│   ├── init_db.py          # Script d'initialisation
│   └── ...
├── frontend/               # Interface Desktop (PyQt5)
│   ├── components/         # Composants graphiques
│   ├── pages/             # Pages principales
│   └── main.py            # Point d'entrée application
├── docs/                  # Documentation
└── tests/                 # Tests unitaires
```

## 🚀 Installation

### Prérequis
- **Python 3.10+**
- **Neo4j Desktop** (Base de données orientée Graphe)
- Git

### Installation étape par étape

1. **Cloner le projet**
```bash
git clone https://github.com/HibaOmri/FlowChart-Archives.git
cd FlowChart-Archives
```

2. **Configurer la Base de Données (Neo4j)**
   - Téléchargez et installez [Neo4j Desktop](https://neo4j.com/download/).
   - Créez un nouveau projet et une base de données locale.
   - Définissez le mot de passe de la base de données (par défaut : `password`).
   - **Démarrez** la base de données.

3. **Installation des dépendances Python**
```bash
pip install -r backend/requirements.txt
```

4. **Initialisation des données**
```bash
# Assurez-vous que Neo4j est lancé (Status: Active)
python backend/init_db.py
```
*Cela va créer les contraintes, les index et ajouter les utilisateurs par défaut.*

## 📖 Utilisation

### Lancer l'application
```bash
python frontend/main.py
```

### Authentification
Une fenêtre de connexion s'ouvrira. Utilisez les comptes par défaut :

| Rôle | Utilisateur | Matricule |
|------|-------------|-----------|
comme un testeur : 'n'importe quel nom et n'importe quel mdp'
| **RH (Admin)** | `admin` | `EMP001` |
| **Archiviste** | `ahmed.hassan` | `EMP002` |

### Note sur l'architecture Technique
- **Frontend** : Application Desktop native construite avec **PyQt5** pour une réactivité maximale.
- **Backend** : Logique métier en Python connectée directement à **Neo4j**.
- **Base de Données** : Utilise la puissance des graphes (**Neo4j**) pour gérer efficacement les relations complexes entre dossiers, utilisateurs et mouvements (emprunts).

## 🔧 Configuration

### Variables d'environnement
Le fichier `backend/db.py` contient la configuration par défaut. Vous pouvez surcharger ces valeurs via des variables d'environnement système :

```bash
NEO4J_URI=bolt://127.0.0.1:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=votre_mot_de_passe
```

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

- Hiba Omri - *Développement initial* - [HibaOmri]

## 🙏 Remerciements

- OCP Khouribga pour le cas d'usage initial
- La communauté open source
- Les contributeurs du projet

---

**SGAU** - Système de Gestion d'Archives Universel
*Une solution moderne et flexible pour la gestion d'archives* 
