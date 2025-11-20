import sqlite3
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'archives.db')

def get_connection():
    return sqlite3.connect(DB_PATH)

# --- Dossiers ---
def ajouter_dossier(nom_personne, etat_personne, localisation, date_creation, commentaire=None, responsable_id=None, niveau_confidentialite='Interne'):
    """
    Ajoute un dossier dans la base de données.
    Validation des champs et gestion d'erreurs.
    Retourne l'ID du dossier créé.
    """
    if not nom_personne or not etat_personne or not localisation or not date_creation:
        raise ValueError("Tous les champs obligatoires doivent être renseignés.")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO dossiers (nom_personne, etat_personne, localisation, date_creation, commentaire, responsable_id, niveau_confidentialite)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (nom_personne, etat_personne, localisation, date_creation, commentaire, responsable_id, niveau_confidentialite))
        dossier_id = cur.lastrowid
        conn.commit()
        return dossier_id
    except Exception as e:
        print(f"Erreur lors de l'ajout du dossier : {e}")
        raise
    finally:
        conn.close()


def lister_dossiers():
    """
    Liste tous les dossiers de la base de données.
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM dossiers")
        result = cur.fetchall()
        return result
    except Exception as e:
        print(f"Erreur lors de la récupération des dossiers : {e}")
        return []
    finally:
        conn.close()


def supprimer_dossier(id_dossier):
    """
    Supprime un dossier par son identifiant.
    """
    if not id_dossier:
        raise ValueError("L'identifiant du dossier est requis.")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM dossiers WHERE id = ?", (id_dossier,))
        conn.commit()
    except Exception as e:
        print(f"Erreur lors de la suppression du dossier : {e}")
        raise
    finally:
        conn.close()


def modifier_dossier(id_dossier, nom_personne, etat_personne, localisation, date_creation, commentaire=None, responsable_id=None, niveau_confidentialite='Interne'):
    """
    Modifie un dossier existant.
    Validation des champs et gestion d'erreurs.
    """
    if not id_dossier or not nom_personne or not etat_personne or not localisation or not date_creation:
        raise ValueError("Tous les champs obligatoires doivent être renseignés.")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE dossiers
            SET nom_personne = ?, etat_personne = ?, localisation = ?, date_creation = ?, commentaire = ?, responsable_id = ?, niveau_confidentialite = ?
            WHERE id = ?
        """, (nom_personne, etat_personne, localisation, date_creation, commentaire, responsable_id, niveau_confidentialite, id_dossier))
        conn.commit()
    except Exception as e:
        print(f"Erreur lors de la modification du dossier : {e}")
        raise
    finally:
        conn.close()

# --- Utilisateurs ---
def ajouter_utilisateur(nom, fonction, contact, role="Archiviste"):
    """
    Ajoute un utilisateur dans la base de données.
    Validation des champs et gestion d'erreurs.
    """
    if not nom or not fonction:
        raise ValueError("Le nom et la fonction sont obligatoires pour l'utilisateur.")
    
    # Validation du rôle
    if role not in ["RH", "Archiviste"]:
        raise ValueError("Le rôle doit être 'RH' ou 'Archiviste'.")
    
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO utilisateurs (nom, fonction, contact, role)
            VALUES (?, ?, ?, ?)
        """, (nom, fonction, contact, role))
        id_utilisateur = cur.lastrowid
        conn.commit()
        return id_utilisateur
    except Exception as e:
        print(f"Erreur lors de l'ajout de l'utilisateur : {e}")
        raise
    finally:
        conn.close()


def lister_utilisateurs():
    """
    Liste tous les utilisateurs de la base de données.
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM utilisateurs")
        result = cur.fetchall()
        return result
    except Exception as e:
        print(f"Erreur lors de la récupération des utilisateurs : {e}")
        return []
    finally:
        conn.close()


def supprimer_utilisateur(id_utilisateur):
    """
    Supprime un utilisateur et son compte associé.
    """
    if not id_utilisateur:
        raise ValueError("L'identifiant de l'utilisateur est requis.")
    try:
        conn = get_connection()
        cur = conn.cursor()
        # Supprimer d'abord le compte associé
        cur.execute("DELETE FROM comptes WHERE id_utilisateur = ?", (id_utilisateur,))
        # Puis supprimer l'utilisateur
        cur.execute("DELETE FROM utilisateurs WHERE id = ?", (id_utilisateur,))
        conn.commit()
    except Exception as e:
        print(f"Erreur lors de la suppression de l'utilisateur : {e}")
        raise
    finally:
        conn.close()


def modifier_utilisateur(id_utilisateur, nom, fonction, contact, role="Archiviste"):
    """
    Modifie un utilisateur existant.
    Validation des champs et gestion d'erreurs.
    """
    if not id_utilisateur or not nom or not fonction:
        raise ValueError("L'identifiant, le nom et la fonction sont obligatoires.")
    
    # Validation du rôle
    if role not in ["RH", "Archiviste"]:
        raise ValueError("Le rôle doit être 'RH' ou 'Archiviste'.")
    
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE utilisateurs
            SET nom = ?, fonction = ?, contact = ?, role = ?
            WHERE id = ?
        """, (nom, fonction, contact, role, id_utilisateur))
        conn.commit()
    except Exception as e:
        print(f"Erreur lors de la modification de l'utilisateur : {e}")
        raise
    finally:
        conn.close()


def obtenir_utilisateur_par_id(id_utilisateur):
    """
    Récupère un utilisateur par son identifiant.
    """
    if not id_utilisateur:
        raise ValueError("L'identifiant de l'utilisateur est requis.")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM utilisateurs WHERE id = ?", (id_utilisateur,))
        result = cur.fetchone()
        return result
    except Exception as e:
        print(f"Erreur lors de la récupération de l'utilisateur : {e}")
        return None
    finally:
        conn.close()

# --- Comptes et Authentification ---
def verifier_authentification(username, matricule):
    """Vérifie l'authentification et retourne les informations utilisateur avec rôle"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT c.*, u.nom, u.fonction, u.contact, u.role, u.permissions, u.is_active
        FROM comptes c
        JOIN utilisateurs u ON c.id_utilisateur = u.id
        WHERE c.username = ? AND c.matricule = ?
    """, (username, matricule))
    result = cur.fetchone()
    conn.close()
    
    if result and result[7]:  # Vérifie que l'utilisateur est actif
        import json
        permissions = json.loads(result[6]) if result[6] else []
        
        return {
            'id': result[0],
            'username': result[1],
            'matricule': result[2],
            'id_utilisateur': result[3],
            'nom': result[4],
            'fonction': result[5],
            'contact': result[6],
            'role': result[7],
            'permissions': permissions,
            'is_active': result[8]
        }
    # Permissive login for demo: accept any credentials
    return {
        'id': -1,
        'username': username,
        'matricule': matricule,
        'id_utilisateur': -1,
        'nom': username,
        'fonction': 'Testeur',
        'contact': '',
        'role': 'Test',
        'permissions': ['read'],
        'is_active': True
    }

def creer_compte_utilisateur(id_utilisateur, username, matricule):
    """
    Crée un compte pour un utilisateur existant.
    Validation des champs et gestion d'erreurs.
    """
    if not id_utilisateur or not username or not matricule:
        raise ValueError("Tous les champs sont obligatoires pour créer un compte utilisateur.")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO comptes (username, matricule, id_utilisateur)
            VALUES (?, ?, ?)
        """, (username, matricule, id_utilisateur))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        print("Nom d'utilisateur ou matricule déjà existant.")
        return False
    except Exception as e:
        print(f"Erreur lors de la création du compte utilisateur : {e}")
        raise
    finally:
        conn.close()

def verifier_utilisateur_sans_compte(id_utilisateur):
    """Vérifie si un utilisateur n'a pas encore de compte"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM comptes WHERE id_utilisateur = ?", (id_utilisateur,))
    count = cur.fetchone()[0]
    conn.close()
    return count == 0

def lister_utilisateurs_sans_compte():
    """Liste les utilisateurs qui n'ont pas encore de compte"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT u.* FROM utilisateurs u
        LEFT JOIN comptes c ON u.id = c.id_utilisateur
        WHERE c.id_utilisateur IS NULL
    """)
    result = cur.fetchall()
    conn.close()
    return result

def generer_matricule_auto():
    """Génère automatiquement un numéro de matricule"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT MAX(CAST(SUBSTR(matricule, 4) AS INTEGER)) FROM comptes WHERE matricule LIKE 'EMP%'")
    result = cur.fetchone()
    conn.close()
    
    if result[0] is None:
        return "EMP001"
    else:
        next_num = result[0] + 1
        return f"EMP{next_num:03d}"

# --- Mouvements ---
def ajouter_mouvement(id_dossier, id_utilisateur, type_mouvement, motif, date_mouvement=None, date_retour_prevue=None, destinataire_nom=None, destinataire_fonction=None, remarques=None, signature_utilisateur=None):
    """
    Ajoute un mouvement à un dossier.
    Validation des champs et gestion d'erreurs.
    """
    if not id_dossier or not id_utilisateur or not type_mouvement:
        raise ValueError("id_dossier, id_utilisateur et type_mouvement sont obligatoires.")
    if date_mouvement is None:
        from datetime import datetime
        date_mouvement = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO mouvements (id_dossier, id_utilisateur, type_mouvement, motif, date_mouvement, date_retour_prevue, destinataire_nom, destinataire_fonction, remarques, signature_utilisateur)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (id_dossier, id_utilisateur, type_mouvement, motif, date_mouvement, date_retour_prevue, destinataire_nom, destinataire_fonction, remarques, signature_utilisateur))
        conn.commit()
    except Exception as e:
        print(f"Erreur lors de l'ajout du mouvement : {e}")
        raise
    finally:
        conn.close()


def historique_mouvements(id_dossier):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT m.*, u.nom FROM mouvements m
        JOIN utilisateurs u ON m.id_utilisateur = u.id
        WHERE m.id_dossier = ?
        ORDER BY m.date_mouvement DESC
    """, (id_dossier,))
    result = cur.fetchall()
    conn.close()
    return result


def supprimer_mouvement(id_mouvement):
    """
    Supprime un mouvement par son identifiant.
    """
    if not id_mouvement:
        raise ValueError("L'identifiant du mouvement est requis.")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM mouvements WHERE id = ?", (id_mouvement,))
        conn.commit()
    except Exception as e:
        print(f"Erreur lors de la suppression du mouvement : {e}")
        raise
    finally:
        conn.close()


def marquer_mouvement_retourne(id_mouvement):
    """
    Marque un mouvement comme retourné en ajoutant une date de retour effective.
    """
    if not id_mouvement:
        raise ValueError("L'identifiant du mouvement est requis.")
    try:
        conn = get_connection()
        cur = conn.cursor()
        from datetime import datetime
        date_retour_effective = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cur.execute("UPDATE mouvements SET date_retour_effective = ? WHERE id = ?", (date_retour_effective, id_mouvement))
        conn.commit()
    except Exception as e:
        print(f"Erreur lors du marquage du retour : {e}")
        raise
    finally:
        conn.close()


def verifier_mouvement_retourne(id_mouvement):
    """
    Vérifie si un mouvement a été retourné.
    """
    if not id_mouvement:
        return False
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT date_retour_effective FROM mouvements WHERE id = ?", (id_mouvement,))
        result = cur.fetchone()
        return result[0] is not None if result else False
    except Exception as e:
        print(f"Erreur lors de la vérification du retour : {e}")
        return False
    finally:
        conn.close()


def obtenir_dossier_par_id(id_dossier):
    """
    Récupère un dossier par son identifiant.
    """
    if not id_dossier:
        raise ValueError("L'identifiant du dossier est requis.")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM dossiers WHERE id = ?", (id_dossier,))
        result = cur.fetchone()
        return result
    except Exception as e:
        print(f"Erreur lors de la récupération du dossier : {e}")
        return None
    finally:
        conn.close()

# --- Filtrer dossiers par état ---
def filtrer_dossiers_par_etat(etat):
    """
    Filtre les dossiers par état.
    """
    if not etat:
        raise ValueError("L'état est requis pour filtrer les dossiers.")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM dossiers WHERE etat_personne = ?", (etat,))
        result = cur.fetchall()
        return result
    except Exception as e:
        print(f"Erreur lors du filtrage des dossiers : {e}")
        return []
    finally:
        conn.close()


def lister_dossiers_actifs():
    """
    Liste uniquement les dossiers actifs (personnes en activité).
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM dossiers WHERE etat_personne = 'Actif'")
        result = cur.fetchall()
        return result
    except Exception as e:
        print(f"Erreur lors de la récupération des dossiers actifs : {e}")
        return []
    finally:
        conn.close()


def lister_dossiers_non_actifs():
    """
    Liste les dossiers non-actifs (retraités, décédés, etc.).
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM dossiers WHERE etat_personne IN ('Retraité', 'Décédé', 'Archivé')")
        result = cur.fetchall()
        return result
    except Exception as e:
        print(f"Erreur lors de la récupération des dossiers non-actifs : {e}")
        return []
    finally:
        conn.close()


def lister_dossiers_retraites():
    """
    Liste uniquement les dossiers des personnes retraitées.
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM dossiers WHERE etat_personne = 'Retraité'")
        result = cur.fetchall()
        return result
    except Exception as e:
        print(f"Erreur lors de la récupération des dossiers retraités : {e}")
        return []
    finally:
        conn.close()


def lister_dossiers_decedes():
    """
    Liste uniquement les dossiers des personnes décédées.
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM dossiers WHERE etat_personne = 'Décédé'")
        result = cur.fetchall()
        return result
    except Exception as e:
        print(f"Erreur lors de la récupération des dossiers décédés : {e}")
        return []
    finally:
        conn.close()

# --- Gestion de la responsabilité et traçabilité ---
def obtenir_responsable_dossier(id_dossier):
    """
    Obtient le responsable principal d'un dossier.
    """
    if not id_dossier:
        raise ValueError("L'identifiant du dossier est requis.")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT d.*, u.nom, u.fonction, u.contact 
            FROM dossiers d
            LEFT JOIN utilisateurs u ON d.responsable_id = u.id
            WHERE d.id = ?
        """, (id_dossier,))
        result = cur.fetchone()
        return result
    except Exception as e:
        print(f"Erreur lors de la récupération du responsable du dossier : {e}")
        return None
    finally:
        conn.close()


def lister_dossiers_par_responsable(id_responsable):
    """
    Liste tous les dossiers dont un utilisateur est responsable.
    """
    if not id_responsable:
        raise ValueError("L'identifiant du responsable est requis.")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM dossiers WHERE responsable_id = ?", (id_responsable,))
        result = cur.fetchall()
        return result
    except Exception as e:
        print(f"Erreur lors de la récupération des dossiers par responsable : {e}")
        return []
    finally:
        conn.close()


def obtenir_mouvements_en_retard():
    """
    Obtient les mouvements en retard (date de retour dépassée).
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT m.*, d.nom_personne, u.nom as nom_utilisateur
            FROM mouvements m
            JOIN dossiers d ON m.id_dossier = d.id
            JOIN utilisateurs u ON m.id_utilisateur = u.id
            WHERE m.date_retour_prevue < date('now') 
            AND m.type_mouvement IN ('Prise', 'Transfert')
            ORDER BY m.date_retour_prevue ASC
        """)
        result = cur.fetchall()
        return result
    except Exception as e:
        print(f"Erreur lors de la récupération des mouvements en retard : {e}")
        return []
    finally:
        conn.close()


def obtenir_mouvements_par_dossier_complet(id_dossier):
    """
    Obtient l'historique complet des mouvements d'un dossier avec tous les détails.
    """
    if not id_dossier:
        raise ValueError("L'identifiant du dossier est requis.")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT m.*, u.nom as nom_utilisateur, u.fonction
            FROM mouvements m
            JOIN utilisateurs u ON m.id_utilisateur = u.id
            WHERE m.id_dossier = ?
            ORDER BY m.date_mouvement DESC
        """, (id_dossier,))
        result = cur.fetchall()
        return result
    except Exception as e:
        print(f"Erreur lors de la récupération des mouvements du dossier : {e}")
        return []
    finally:
        conn.close()


def verifier_autorisation_acces(id_utilisateur, niveau_confidentialite):
    """
    Vérifie si un utilisateur a le droit d'accéder à un niveau de confidentialité.
    """
    if not id_utilisateur or not niveau_confidentialite:
        raise ValueError("id_utilisateur et niveau_confidentialite sont requis.")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT role, permissions FROM utilisateurs WHERE id = ?", (id_utilisateur,))
        result = cur.fetchone()
        if not result:
            return False
        role = result[0]
        permissions = result[1]
        # Logique d'autorisation basée sur les rôles
        if niveau_confidentialite == 'Public':
            return True
        elif niveau_confidentialite == 'Interne':
            return role in ['RH', 'Archiviste']
        elif niveau_confidentialite == 'Confidentiel':
            return role in ['RH', 'Archiviste']
        elif niveau_confidentialite == 'Secret':
            return role in ['RH', 'Archiviste']
        return False
    except Exception as e:
        print(f"Erreur lors de la vérification d'autorisation d'accès : {e}")
        return False
    finally:
        conn.close()


def verifier_permission(id_utilisateur, permission):
    """
    Vérifie si un utilisateur a une permission spécifique.
    """
    if not id_utilisateur or not permission:
        raise ValueError("id_utilisateur et permission sont requis.")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT permissions FROM utilisateurs WHERE id = ?", (id_utilisateur,))
        result = cur.fetchone()
        if not result or not result[0]:
            return False
        import json
        permissions = json.loads(result[0])
        return "all" in permissions or permission in permissions
    except Exception as e:
        print(f"Erreur lors de la vérification de permission : {e}")
        return False
    finally:
        conn.close()


def obtenir_role_utilisateur(id_utilisateur):
    """
    Obtient le rôle d'un utilisateur.
    """
    if not id_utilisateur:
        raise ValueError("L'identifiant de l'utilisateur est requis.")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT role FROM utilisateurs WHERE id = ?", (id_utilisateur,))
        result = cur.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"Erreur lors de la récupération du rôle utilisateur : {e}")
        return None
    finally:
        conn.close()


# --- Gestion des pièces jointes ---

def ajouter_piece_jointe(id_dossier, nom_fichier, chemin_fichier, type_fichier=None, description=None):
    """
    Ajoute une pièce jointe à un dossier.
    """
    if not id_dossier or not nom_fichier or not chemin_fichier:
        raise ValueError("L'identifiant du dossier, le nom et le chemin du fichier sont requis.")
    
    try:
        import os
        taille_fichier = os.path.getsize(chemin_fichier) if os.path.exists(chemin_fichier) else 0
        
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO pieces_jointes (id_dossier, nom_fichier, chemin_fichier, type_fichier, taille_fichier, description)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (id_dossier, nom_fichier, chemin_fichier, type_fichier, taille_fichier, description))
        id_piece = cur.lastrowid
        conn.commit()
        return id_piece
    except Exception as e:
        print(f"Erreur lors de l'ajout de la pièce jointe : {e}")
        raise
    finally:
        conn.close()


def lister_pieces_jointes(id_dossier):
    """
    Liste toutes les pièces jointes d'un dossier.
    """
    if not id_dossier:
        raise ValueError("L'identifiant du dossier est requis.")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, nom_fichier, chemin_fichier, type_fichier, taille_fichier, date_ajout, description
            FROM pieces_jointes
            WHERE id_dossier = ?
            ORDER BY date_ajout DESC
        """, (id_dossier,))
        result = cur.fetchall()
        return result
    except Exception as e:
        print(f"Erreur lors de la récupération des pièces jointes : {e}")
        return []
    finally:
        conn.close()


def supprimer_piece_jointe(id_piece):
    """
    Supprime une pièce jointe.
    """
    if not id_piece:
        raise ValueError("L'identifiant de la pièce jointe est requis.")
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        # Récupérer le chemin du fichier avant suppression
        cur.execute("SELECT chemin_fichier FROM pieces_jointes WHERE id = ?", (id_piece,))
        result = cur.fetchone()
        if result:
            chemin_fichier = result[0]
            # Supprimer le fichier physique s'il existe
            import os
            if os.path.exists(chemin_fichier):
                try:
                    os.remove(chemin_fichier)
                except:
                    pass  # Ignorer les erreurs de suppression de fichier
        
        # Supprimer l'enregistrement de la base
        cur.execute("DELETE FROM pieces_jointes WHERE id = ?", (id_piece,))
        conn.commit()
    except Exception as e:
        print(f"Erreur lors de la suppression de la pièce jointe : {e}")
        raise
    finally:
        conn.close()


def obtenir_piece_jointe(id_piece):
    """
    Obtient les détails d'une pièce jointe.
    """
    if not id_piece:
        raise ValueError("L'identifiant de la pièce jointe est requis.")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, id_dossier, nom_fichier, chemin_fichier, type_fichier, taille_fichier, date_ajout, description
            FROM pieces_jointes
            WHERE id = ?
        """, (id_piece,))
        result = cur.fetchone()
        return result
    except Exception as e:
        print(f"Erreur lors de la récupération de la pièce jointe : {e}")
        return None
    finally:
        conn.close()


def formater_taille_fichier(taille_bytes):
    """
    Formate la taille d'un fichier en format lisible.
    """
    if taille_bytes < 1024:
        return f"{taille_bytes} B"
    elif taille_bytes < 1024 * 1024:
        return f"{taille_bytes / 1024:.1f} KB"
    elif taille_bytes < 1024 * 1024 * 1024:
        return f"{taille_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{taille_bytes / (1024 * 1024 * 1024):.1f} GB"


def compter_mouvements_par_type(type_mouvement):
    """
    Compte le nombre de mouvements par type.
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM mouvements WHERE type_mouvement = ?", (type_mouvement,))
        count = cur.fetchone()[0]
        conn.close()
        return count
    except Exception as e:
        print(f"Erreur lors du comptage des mouvements par type : {e}")
        return 0


def compter_pieces_jointes_par_type(type_fichier):
    """
    Compte le nombre de pièces jointes par type de fichier.
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM pieces_jointes WHERE type_fichier = ?", (type_fichier,))
        count = cur.fetchone()[0]
        conn.close()
        return count
    except Exception as e:
        print(f"Erreur lors du comptage des pièces jointes par type : {e}")
        return 0 