import sqlite3

def create_tables():
    conn = sqlite3.connect('archives.db')  # Le fichier sera créé dans le dossier courant
    cursor = conn.cursor()

    # Table dossiers
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dossiers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom_personne TEXT NOT NULL,
        etat_personne TEXT NOT NULL,
        localisation TEXT NOT NULL,
        date_creation DATE NOT NULL,
        commentaire TEXT,
        responsable_id INTEGER,
        niveau_confidentialite TEXT DEFAULT 'Interne',
        FOREIGN KEY (responsable_id) REFERENCES utilisateurs(id)
    )
    """)

    # Table utilisateurs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS utilisateurs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        fonction TEXT NOT NULL,
        contact TEXT,
        role TEXT NOT NULL DEFAULT 'Archiviste',
        permissions TEXT,
        is_active BOOLEAN DEFAULT 1
    )
    """)

    # Table mouvements
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mouvements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_dossier INTEGER NOT NULL,
        id_utilisateur INTEGER NOT NULL,
        type_mouvement TEXT NOT NULL,
        date_mouvement DATETIME NOT NULL,
        date_retour_prevue DATE,
        destinataire_nom TEXT,
        destinataire_fonction TEXT,
        motif TEXT NOT NULL,
        remarques TEXT,
        signature_utilisateur TEXT,
        date_retour_effective DATETIME,
        FOREIGN KEY (id_dossier) REFERENCES dossiers(id),
        FOREIGN KEY (id_utilisateur) REFERENCES utilisateurs(id)
    )
    """)

    # Table comptes 
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS comptes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        matricule TEXT UNIQUE NOT NULL,
        id_utilisateur INTEGER NOT NULL,
        FOREIGN KEY (id_utilisateur) REFERENCES utilisateurs(id)
    )
    """)

    # Table pièces jointes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pieces_jointes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_dossier INTEGER NOT NULL,
        nom_fichier TEXT NOT NULL,
        chemin_fichier TEXT NOT NULL,
        type_fichier TEXT,
        taille_fichier INTEGER,
        date_ajout DATETIME DEFAULT CURRENT_TIMESTAMP,
        description TEXT,
        FOREIGN KEY (id_dossier) REFERENCES dossiers(id)
    )
    """)

    #  des données d'exemple pour faciliter les tests
    try:
        # Utilisateurs d'exemple avec rôles
        cursor.execute("""
        INSERT OR IGNORE INTO utilisateurs (id, nom, fonction, contact, role, permissions) VALUES 
        (1, 'Admin Principal', 'Administrateur', 'admin@entreprise.com', 'RH', '["read", "write", "manage_users"]'),
        (2, 'Ahmed Hassan', 'Archiviste', 'ahmed.hassan@entreprise.com', 'Archiviste', '["read", "write", "delete"]')
        """)
        
        # Comptes d'exemple avec matricules
        cursor.execute("""
        INSERT OR IGNORE INTO comptes (username, matricule, id_utilisateur) VALUES 
        ('admin', 'EMP001', 1),
        ('ahmed.hassan', 'EMP002', 2)
        """)
        
        # Dossiers d'exemple
        cursor.execute("""
        INSERT OR IGNORE INTO dossiers (nom_personne, etat_personne, localisation, date_creation, commentaire) VALUES 
        ('Dossier Test 1', 'Actif', 'Rayon A - Étagère 1', '2024-01-15', 'Dossier de test pour démonstration'),
        ('Dossier Test 2', 'Archivé', 'Archives - Boîte 5', '2024-01-10', 'Dossier archivé')
        """)
        
    except sqlite3.IntegrityError:
        # Les données existent déjà, pas de problème
        pass

    # Ajouter la colonne date_retour_effective si elle n'existe pas
    try:
        cursor.execute("ALTER TABLE mouvements ADD COLUMN date_retour_effective DATETIME")
        print("Colonne date_retour_effective ajoutée à la table mouvements.")
    except sqlite3.OperationalError:
        # La colonne existe déjà
        pass

    conn.commit()
    conn.close()
    print("Base de données et tables créées avec succès.")
    print("Comptes d'exemple créés :")
    print("- admin / EMP001 (RH)")
    print("- ahmed.hassan / EMP002 (Archiviste)")

if __name__ == "__main__":
    create_tables() 