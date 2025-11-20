# Guide de Migration - Vers le Système de Gestion d'Archives Universel (SGAU)

## 📋 Vue d'ensemble

Ce guide vous accompagne dans la migration de l'ancien système OCP spécifique vers le nouveau **Système de Gestion d'Archives Universel (SGAU)**.

## 🎯 Avantages de la migration

### ✅ Avantages techniques
- **Architecture modulaire** : Code plus maintenable et extensible
- **Multi-organisations** : Support de plusieurs organisations
- **Base de données moderne** : SQLAlchemy avec migrations
- **API REST** : Interface programmatique
- **Sécurité renforcée** : Authentification et autorisation avancées
- **Tests automatisés** : Couverture complète

### ✅ Avantages fonctionnels
- **Configuration flexible** : Adaptable à différents contextes
- **Interface moderne** : Design responsive et intuitif
- **Recherche avancée** : Moteur de recherche intelligent
- **Rapports détaillés** : Analytics et métriques
- **Notifications** : Système d'alertes automatiques

## 🚀 Étapes de migration

### Étape 1 : Sauvegarde des données existantes

```bash
# 1. Sauvegarder l'ancienne base de données
cp backend/archives.db backend/archives_backup.db

# 2. Exporter les données existantes (optionnel)
python export_old_data.py
```

### Étape 2 : Installation du nouveau système

```bash
# 1. Installer les nouvelles dépendances
pip install -r backend/requirements.txt

# 2. Initialiser le nouveau système
cd backend
python init_sgau.py

# 3. Tester l'installation
cd ..
python test_sgau.py
```

### Étape 3 : Migration des données

```bash
# 1. Exécuter le script de migration
python migrate_data.py

# 2. Vérifier l'intégrité des données
python verify_migration.py
```

### Étape 4 : Configuration de l'organisation

```bash
# 1. Configurer OCP Khouribga
python configure_organization.py --org OCP_KHOURIBGA

# 2. Personnaliser les paramètres
python customize_settings.py
```

## 📊 Comparaison des architectures

### Ancien système (OCP spécifique)
```
pfe/
├── backend/
│   ├── db.py              # Logique métier simple
│   ├── init_db.py         # Initialisation basique
│   └── archives.db        # SQLite simple
├── frontend/
│   └── main.py            # Interface PyQt5
└── README_etape2.md       # Documentation limitée
```

### Nouveau système (SGAU universel)
```
SGAU/
├── backend/
│   ├── api/               # API REST FastAPI
│   ├── models/            # Modèles SQLAlchemy
│   ├── services/          # Logique métier
│   ├── config/            # Configuration modulaire
│   └── utils/             # Utilitaires
├── frontend/
│   ├── components/        # Composants réutilisables
│   ├── pages/            # Pages principales
│   └── services/         # Services API
├── docs/                 # Documentation complète
├── tests/                # Tests automatisés
└── docker/               # Configuration Docker
```

## 🔄 Migration des données

### Structure des données

#### Ancien système
```sql
-- Tables simples
dossiers (id, nom_personne, etat_personne, localisation, date_creation, commentaire)
utilisateurs (id, nom, fonction, contact)
mouvements (id, id_dossier, id_utilisateur, type_mouvement, date_mouvement, remarques)
```

#### Nouveau système
```sql
-- Tables normalisées
organizations (id, code, name, description, theme, settings)
users (id, username, email, full_name, role, organization_id, ...)
categories (id, name, description, organization_id, ...)
dossiers (id, reference, title, description, category_id, organization_id, ...)
documents (id, title, filename, dossier_id, ...)
mouvements (id, type_mouvement, dossier_id, user_id, ...)
audit_logs (id, user_id, action, table_name, ...)
notifications (id, user_id, title, message, ...)
```

### Script de migration automatique

```python
# migrate_data.py
def migrate_old_to_new():
    """Migre les données de l'ancien système vers le nouveau"""
    
    # 1. Créer l'organisation OCP Khouribga
    ocp_org = create_organization("OCP_KHOURIBGA", "OCP Khouribga")
    
    # 2. Migrer les utilisateurs
    migrate_users(ocp_org.id)
    
    # 3. Créer les catégories
    create_categories(ocp_org.id)
    
    # 4. Migrer les dossiers
    migrate_dossiers(ocp_org.id)
    
    # 5. Migrer les mouvements
    migrate_mouvements()
    
    print("✅ Migration terminée avec succès")
```

## 🎨 Personnalisation

### Configuration de l'organisation

```python
# Configuration OCP Khouribga
ocp_config = {
    "name": "OCP Khouribga",
    "theme": {
        "primary_color": "#1976d2",
        "secondary_color": "#dc004e"
    },
    "document_types": [
        "Document administratif",
        "Document technique",
        "Document financier",
        "Document RH",
        "Document juridique",
        "Document historique",
        "Document de formation",
        "Document de sécurité",
        "Document environnemental"
    ],
    "locations": [
        "Archives Centrales - Khouribga Centre",
        "Archives Historiques - Khouribga Administration",
        "Archives Techniques - Khouribga Technique",
        # ... autres localisations
    ]
}
```

### Thème personnalisé

```css
/* Thème OCP Khouribga */
:root {
    --primary-color: #1976d2;
    --secondary-color: #dc004e;
    --background-color: #f5f5f5;
    --text-color: #333333;
}

.ocp-header {
    background-color: var(--primary-color);
    color: white;
}

.ocp-logo {
    /* Logo OCP personnalisé */
}
```

## 🔧 Configuration avancée

### Variables d'environnement

```bash
# .env
ENVIRONMENT=production
DATABASE_TYPE=postgresql
DATABASE_URL=postgresql://user:pass@localhost/sgau
SECRET_KEY=your-secret-key-change-in-production
DEBUG=False
LOG_LEVEL=INFO
```

### Configuration multi-organisations

```python
# config/multi_org.py
ORGANIZATIONS = {
    "OCP_KHOURIBGA": {
        "database": "ocp_khouribga.db",
        "theme": "ocp_theme",
        "settings": "ocp_settings.json"
    },
    "BIBLIO_UNIV": {
        "database": "biblio_univ.db",
        "theme": "biblio_theme",
        "settings": "biblio_settings.json"
    }
}
```

## 📈 Fonctionnalités avancées

### 1. API REST
```python
# Exemple d'utilisation de l'API
import requests

# Récupérer tous les dossiers
response = requests.get("http://localhost:8000/api/dossiers")
dossiers = response.json()

# Créer un nouveau dossier
new_dossier = {
    "title": "Nouveau dossier",
    "description": "Description du dossier",
    "category_id": 1,
    "location": "Archives Centrales"
}
response = requests.post("http://localhost:8000/api/dossiers", json=new_dossier)
```

### 2. Recherche avancée
```python
# Recherche avec filtres multiples
search_params = {
    "query": "Mohammed V",
    "category": "Documents Historiques",
    "date_from": "2023-01-01",
    "date_to": "2023-12-31",
    "location": "Archives Historiques"
}
```

### 3. Rapports automatisés
```python
# Génération de rapports
reports = {
    "daily": "Rapport quotidien des mouvements",
    "weekly": "Statistiques hebdomadaires",
    "monthly": "Rapport mensuel complet",
    "custom": "Rapport personnalisé"
}
```

## 🧪 Tests et validation

### Tests automatisés
```bash
# Exécuter tous les tests
python -m pytest tests/

# Tests avec couverture
python -m pytest --cov=backend tests/

# Tests spécifiques
python -m pytest tests/test_migration.py
```

### Validation des données
```python
# Vérifier l'intégrité des données migrées
def validate_migration():
    """Valide la migration des données"""
    
    # Vérifier le nombre de dossiers
    old_count = count_old_dossiers()
    new_count = count_new_dossiers()
    assert old_count == new_count
    
    # Vérifier les relations
    validate_relationships()
    
    print("✅ Validation réussie")
```

## 🚨 Résolution des problèmes

### Problèmes courants

1. **Erreur de dépendances**
   ```bash
   pip install --upgrade -r backend/requirements.txt
   ```

2. **Erreur de base de données**
   ```bash
   # Recréer la base de données
   rm backend/archives.db
   python backend/init_sgau.py
   ```

3. **Erreur de migration**
   ```bash
   # Restaurer la sauvegarde
   cp backend/archives_backup.db backend/archives.db
   # Relancer la migration
   python migrate_data.py
   ```

### Support et assistance

- **Documentation** : Consultez le README.md principal
- **Issues** : Signalez les problèmes sur GitHub
- **Tests** : Exécutez `python test_sgau.py` pour diagnostiquer

## 🎉 Conclusion

La migration vers le SGAU vous offre :

- ✅ **Flexibilité** : Adaptable à différents contextes
- ✅ **Évolutivité** : Architecture modulaire et extensible
- ✅ **Performance** : Optimisations et cache
- ✅ **Sécurité** : Authentification et autorisation avancées
- ✅ **Maintenabilité** : Code propre et documenté

**Le nouveau système est prêt pour votre PFE et votre carrière professionnelle !** 🚀

---

*Guide de migration SGAU - Version 1.0*
*Développé pour OCP Khouribga et au-delà* 