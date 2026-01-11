# 🎓 Plan de Présentation du Projet - Gestion d'Archives (SGAU)

Ce plan découpe le projet en **4 parties équilibrées**, permettant à chaque membre de briller sur des aspects techniques et fonctionnels spécifiques.

---

## 👤 Membre 1 : Architecture, Backend & Base de Données
**"Le Cœur Technique"**

### Fichiers Clés à présenter :
*   `backend/db.py` : Le cerveau de l'application (connexion Neo4j, requêtes Cypher).
*   `backend/init_db.py` : Script d'initialisation de la base de données.
*   `frontend/components/login_dialog.py` : IHM de connexion.

### Sujets à couvrir :
1.  **Architecture du Projet** : Explication du choix de **Python** avec **PyQt5** pour le Desktop et separation Frontend/Backend.
2.  **Innovation Database (Neo4j)** :
    *   Pourquoi une base de données **Graphe** (Neo4j) plutôt que SQL classique ?
    *   Avantage pour gérer les relations complexes entre *Utilisateurs*, *Dossiers* et *Mouvements*.
3.  **Sécurité & Authentification** :
    *   Comment fonctionne le système de Login (Vérification mot de passe/Matricule).
    *   Gestion des sessions (Admin vs Archiviste).

### Démo suggérée :
*   Lancer l'application (Login screen).
*   Montrer une requête Cypher ou le graphe dans Neo4j Browser pour prouver la complexité technique.

---

## 👤 Membre 2 : Interface Utilisateur (UI/UX) & Dashboard
**"L'Expérience Visuelle"**

### Fichiers Clés à présenter :
*   `frontend/main.py` : Point d'entrée de l'application.
*   `frontend/components/main_window.py` : Structure principale, dashboard.
*   `frontend/components/styles.py` : Gestion centralisée du design (CSS/QSS, Palettes de couleurs).

### Sujets à couvrir :
1.  **Design Moderne en Desktop** :
    *   Sortir du look "vieux logiciel Windows".
    *   Utilisation de feuilles de style **CSS** intégrées à PyQt.
    *   Implémentation des **Ombres Portées (Drop Shadows)** et des dégradés.
2.  **Ergonomie du Dashboard** :
    *   Les **Cartes d'Actions Rapides** (Justification du design "Tuiles" pour l'accessibilité).
    *   La **Barre de Recherche Dynamique** (Filtrage temps réel sans recharger).
3.  **Statistiques** : Affichage des indicateurs clés (Actifs/Retraités) en haut de page.

### Démo suggérée :
*   Présenter la `MainWindow`.
*   Faire une recherche en direct ("tapant juste quelques lettres").
*   Utiliser les filtres (ComboBox) pour montrer la réactivité de l'interface.

---

## 👤 Membre 3 : Gestion Core Business (Dossiers & Fichiers)
**"Le Fonctionnel Pur"**

### Fichiers Clés à présenter :
*   `frontend/components/add_dossier_dialog.py` : Formulaire complexe + Logique Drag & Drop.
*   `frontend/components/gestion_pieces_jointes.py` : Visualisation des fichiers attachés.
*   `archives/` (Dossier physique) : Montrer où sont réellement stockés les fichiers sur le disque.

### Sujets à couvrir :
1.  **CRUD Dossier** (Create, Read, Update, Delete) :
    *   Les formulaires de saisie et la validation des données.
    *   La gestion des statuts (*Actif, Retraité, Décédé*).
2.  **Gestion Documentaire (GED)** :
    *   Système de **Pièces Jointes**.
    *   Fonctionnalité technique : Le **Drag & Drop** (Glisser-Déposer) de fichiers dans l'application.
    *   Stockage physique des fichiers dans le dossier `/archives`.

### Démo suggérée :
*   Cliquer sur "Ajouter".
*   Remplir un dossier test.
*   **Glisser un fichier** depuis le bureau windows vers la zone de drop.
*   Valider et montrer qu'il apparaît dans la liste.

---

## Membre 4 : Traçabilité, Historique & Administration
**"Le Contrôle & Le Processus"**

### Fichiers Clés à présenter :
*   `frontend/components/historique_mouvements.py` : Visualisation temporelle des actions.
*   `frontend/components/gestion_utilisateurs.py` : Interface d'administration RH.
*   Backend : Fonctions `lister_historique` et `gestion_users` dans `db.py`.

### Sujets à couvrir :
1.  **Suivi des Mouvements (Traceability)** :
    *   L'importance de savoir *qui* a pris un dossier et *quand*.
    *   Modèle de données : Relations `[:A_CONSULTÉ]` ou `[:A_EMPRUNTÉ]` dans Neo4j.
2.  **Fonctionnalités Administrateur** :
    *   Gestion des comptes utilisateurs (Ajouter un nouvel archiviste).
    *   Attribution des rôles et permissions.
3.  **Conclusion & Perspectives** :
    *   Ce qui pourrait être amélioré (Version Web ? Cloud ?).

### Démo suggérée :
*   Sélectionner un dossier -> "Historique".
*   Montrer la timeline des actions.
*   Aller dans "Gérer les utilisateurs" (Zone Admin) et montrer la liste des employés.



