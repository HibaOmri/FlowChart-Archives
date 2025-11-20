# Étape 2 : Historique et mouvements - Guide d'utilisation
## Système de Gestion des Archives OCP Khouribga - Maroc

## Fonctionnalités ajoutées

### 1. Affichage de l'historique des mouvements
- **Bouton "Historique des mouvements"** : Sélectionnez un dossier et cliquez sur ce bouton
- **Double-clic sur un dossier** : Double-cliquez directement sur un dossier dans le tableau

### 2. Ajout de mouvements
- **Types de mouvements disponibles** :
  - **Prise** : Quand un dossier est emprunté/consulté
  - **Retour** : Quand un dossier est remis en place
  - **Transfert** : Quand un dossier est déplacé vers un autre service
  - **Consultation** : Consultation sur place des archives
  - **Restauration** : Envoi en restauration
  - **Numérisation** : Envoi pour numérisation

### 3. Gestion des mouvements
- **Suppression de mouvements** : Bouton "Supprimer" dans l'historique
- **Affichage détaillé** : Date, utilisateur, type, remarques

## Installation et configuration

### 1. Initialiser la base de données
```bash
cd backend
python init_db.py
```

### 2. Ajouter des utilisateurs de test
```bash
cd backend
python ajouter_utilisateurs_test.py
```

### 3. Ajouter des données de test (optionnel)
```bash
cd backend
python ajouter_donnees_test.py
```

### 4. Lancer l'application
```bash
cd frontend
python main.py
```

## Utilisation

### Consulter l'historique d'un dossier
1. Sélectionnez un dossier dans le tableau principal
2. Cliquez sur "Historique des mouvements" ou double-cliquez sur le dossier
3. Une nouvelle fenêtre s'ouvre avec tous les mouvements du dossier

### Ajouter un nouveau mouvement
1. Ouvrez l'historique d'un dossier
2. Cliquez sur "Ajouter un mouvement"
3. Remplissez les informations :
   - **Type** : Prise, Retour ou Transfert
   - **Utilisateur** : Sélectionnez l'utilisateur responsable
   - **Date et heure** : Date/heure du mouvement
   - **Remarques** : Commentaires optionnels
4. Cliquez sur "Ajouter"

### Supprimer un mouvement
1. Dans l'historique d'un dossier
2. Cliquez sur "Supprimer" à côté du mouvement à supprimer
3. Confirmez la suppression

## Structure de la base de données

### Table `mouvements`
- `id` : Identifiant unique
- `id_dossier` : Référence vers le dossier
- `id_utilisateur` : Référence vers l'utilisateur
- `type_mouvement` : Prise, Retour, Transfert
- `date_mouvement` : Date et heure du mouvement
- `remarques` : Commentaires optionnels

### Table `utilisateurs`
- `id` : Identifiant unique
- `nom` : Nom de l'utilisateur
- `fonction` : Fonction/statut de l'utilisateur
- `contact` : Informations de contact

## Fonctionnalités techniques

### Interface utilisateur
- **HistoriqueMouvementsDialog** : Fenêtre d'affichage de l'historique
- **AjouterMouvementDialog** : Fenêtre d'ajout de mouvement
- **Double-clic** : Ouverture rapide de l'historique
- **Tableau interactif** : Affichage des mouvements avec actions

### Backend
- **db.historique_mouvements()** : Récupère l'historique d'un dossier
- **db.ajouter_mouvement()** : Ajoute un nouveau mouvement
- **db.supprimer_mouvement()** : Supprime un mouvement
- **db.lister_utilisateurs()** : Liste tous les utilisateurs

## Notes importantes

1. **Utilisateurs requis** : Il faut au moins un utilisateur dans la base pour pouvoir ajouter des mouvements
2. **Validation** : Les champs obligatoires sont vérifiés avant l'ajout
3. **Format de date** : Les dates sont affichées au format français (dd/mm/yyyy hh:mm)
4. **Sécurité** : Confirmation requise pour la suppression de mouvements

## Contexte OCP Khouribga

Ce système est spécifiquement conçu pour l'Office Chérifien des Phosphates (OCP) - Site de Khouribga au Maroc, site historique d'extraction de phosphates. Les archives gérées incluent :

- **Archives historiques** : Documents des rois du Maroc liés à OCP Khouribga
- **Archives de direction** : Documents des dirigeants du site Khouribga
- **Archives techniques** : Documents techniques spécifiques au site de Khouribga
- **Archives administratives** : Documents RH, sécurité, formation du site Khouribga
- **Archives environnementales** : Documents liés à l'environnement et la sécurité

### Sites OCP Khouribga
- **Khouribga Centre** : Mine principale historique
- **Khouribga Nord/Sud/Est/Ouest** : Zones d'extraction
- **Khouribga Administration** : Bâtiments administratifs et services
- **Khouribga Technique** : Services techniques et maintenance

## Prochaines étapes

Cette étape 2 complète la gestion des mouvements. Les prochaines étapes pourraient inclure :
- Gestion des utilisateurs (ajout/modification/suppression)
- Rapports et statistiques sur les mouvements
- Export des données
- Authentification des utilisateurs
- Gestion des zones d'extraction Khouribga (Centre, Nord, Sud, Est, Ouest)
- Intégration avec les systèmes OCP Khouribga existants
- Gestion des équipements miniers spécifiques à Khouribga 