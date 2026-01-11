import os
import sys

# Ensure backend directory is in path if run from root
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db import (
    get_db, 
    get_next_id,
    ajouter_utilisateur, 
    creer_compte_utilisateur,
    ajouter_dossier
)

def init_db():
    print("Initialisation de la base de données Neo4j...")
    conn = get_db()
    
    # 1. Création des contraintes (Unicité)
    try:
        # Neo4j 5.x syntax for constraints
        constraints = [
            "CREATE CONSTRAINT IF NOT EXISTS FOR (c:Compte) REQUIRE c.username IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (c:Compte) REQUIRE c.matricule IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (u:Utilisateur) REQUIRE u.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (d:Dossier) REQUIRE d.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (p:PieceJointe) REQUIRE p.id IS UNIQUE",
            # Counter constraint
            "CREATE CONSTRAINT IF NOT EXISTS FOR (c:Counter) REQUIRE c.name IS UNIQUE"
        ]
        
        for const in constraints:
            conn.query(const)
        print("Contraintes vérifiées/créées.")
    except Exception as e:
        print(f"Erreur lors de la création des contraintes : {e}")

    # 2. Initialisation des compteurs (si inexistants)
    labels = ['Dossier', 'Utilisateur', 'Compte', 'Mouvement', 'PieceJointe']
    for label in labels:
        try:
            # On ne reset pas si existe, on s'assure juste qu'il existe
            query = "MERGE (c:Counter {name: $name}) ON CREATE SET c.count = 0"
            conn.query(query, {'name': label})
        except Exception as e:
            print(f"Erreur init compteur {label}: {e}")
    print("Compteurs initialisés.")

    # 3. Données d'exemple
    # On vérifie s'il y a des utilisateurs
    users = conn.query("MATCH (u:Utilisateur) RETURN count(u)")
    if users[0][0] == 0:
        print("Base vide, ajout des données d'exemple...")
        try:
            # Admin RH
            id_admin = ajouter_utilisateur(
                nom="Admin Principal",
                fonction="Administrateur",
                contact="admin@entreprise.com",
                role="RH"
            )
            # Donne des permissions (json string comme dans l'original) via une update manuelle ou via le code (code ne gère pas permissions en écriture explicite dans ajouter_utilisateur, on va faire un patch)
            conn.query("MATCH (u:Utilisateur {id: $id}) SET u.permissions = $p", 
                      {'id': id_admin, 'p': '["read", "write", "manage_users"]'})
            
            creer_compte_utilisateur(id_admin, "admin", "EMP001")
            
            # Archiviste
            id_archiviste = ajouter_utilisateur(
                nom="Ahmed Hassan",
                fonction="Archiviste",
                contact="ahmed.hassan@entreprise.com",
                role="Archiviste"
            )
            conn.query("MATCH (u:Utilisateur {id: $id}) SET u.permissions = $p", 
                      {'id': id_archiviste, 'p': '["read", "write", "delete"]'})
            creer_compte_utilisateur(id_archiviste, "ahmed.hassan", "EMP002")
            
            # Dossiers
            ajouter_dossier(
                nom_personne='Dossier Test 1',
                etat_personne='Actif',
                localisation='Rayon A - Étagère 1',
                date_creation='2024-01-15',
                commentaire='Dossier de test pour démonstration',
                responsable_id=id_archiviste,
                niveau_confidentialite='Interne'
            )
            
            ajouter_dossier(
                nom_personne='Dossier Test 2',
                etat_personne='Archivé',
                localisation='Archives - Boîte 5',
                date_creation='2024-01-10',
                commentaire='Dossier archivé',
                niveau_confidentialite='Interne'
            )
            
            print("Données d'exemple ajoutées.")
            print("- admin / EMP001 (RH)")
            print("- ahmed.hassan / EMP002 (Archiviste)")
            
        except Exception as e:
            print(f"Erreur lors de l'ajout des données d'exemple : {e}")
    else:
        print("La base contient déjà des données.")

    conn.close()

if __name__ == "__main__":
    init_db()