import os
from datetime import datetime
from neo4j import GraphDatabase, basic_auth

# --- Configuration Neo4j ---
# Ces valeurs peuvent être surchargées par des variables d'environnement ou modifiées ici
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://127.0.0.1:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

class Neo4jConnection:
    _instance = None
    
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=basic_auth(NEO4J_USER, NEO4J_PASSWORD))

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Neo4jConnection()
        return cls._instance
    
    def close(self):
        if self.driver:
            self.driver.close()

    def query(self, query, parameters=None):
        if parameters is None:
            parameters = {}
        with self.driver.session() as session:
            result = session.run(query, parameters)
            # Convert to list of lists/tuples to mimic SQLite fetchall
            return [record.values() for record in result]
            
    def query_single(self, query, parameters=None):
        if parameters is None:
            parameters = {}
        with self.driver.session() as session:
            result = session.run(query, parameters)
            record = result.single()
            if record:
                return record.values()
            return None

def get_db():
    return Neo4jConnection.get_instance()

def get_next_id(label):
    """
    Simule l'auto-incrément pour un label donné (Dossier, Utilisateur, etc.)
    """
    query = """
    MERGE (c:Counter {name: $label})
    ON CREATE SET c.count = 0
    SET c.count = c.count + 1
    RETURN c.count as next_id
    """
    result = get_db().query_single(query, {'label': label})
    return result[0] if result else 1

# --- Dossiers ---
def ajouter_dossier(nom_personne, etat_personne, localisation, date_creation, commentaire=None, responsable_id=None, niveau_confidentialite='Interne'):
    """
    Ajoute un dossier dans la base de données.
    """
    if not nom_personne or not etat_personne or not localisation or not date_creation:
        raise ValueError("Tous les champs obligatoires doivent être renseignés.")
    
    try:
        new_id = get_next_id('Dossier')
        
        query = """
        CREATE (d:Dossier {
            id: $id,
            nom_personne: $nom_personne,
            etat_personne: $etat_personne,
            localisation: $localisation,
            date_creation: $date_creation,
            commentaire: $commentaire,
            responsable_id: $responsable_id,
            niveau_confidentialite: $niveau_confidentialite
        })
        RETURN d.id
        """
        params = {
            'id': new_id,
            'nom_personne': nom_personne,
            'etat_personne': etat_personne,
            'localisation': localisation,
            'date_creation': date_creation,
            'commentaire': commentaire,
            'responsable_id': responsable_id,
            'niveau_confidentialite': niveau_confidentialite
        }
        
        # Link responsible if exists
        if responsable_id:
             link_query = """
             MATCH (d:Dossier {id: $d_id}), (u:Utilisateur {id: $u_id})
             MERGE (u)-[:RESPONSABLE_DE]->(d)
             """
             get_db().query(link_query, {'d_id': new_id, 'u_id': responsable_id})

        get_db().query(query, params)
        return new_id
    except Exception as e:
        print(f"Erreur lors de l'ajout du dossier : {e}")
        raise

def lister_dossiers():
    """
    Liste tous les dossiers. Ordre des champs doit correspondre à la table SQL originale:
    id, nom_personne, etat_personne, localisation, date_creation, commentaire, responsable_id, niveau_confidentialite
    """
    try:
        query = """
        MATCH (d:Dossier)
        RETURN d.id, d.nom_personne, d.etat_personne, d.localisation, d.date_creation, d.commentaire, d.responsable_id, d.niveau_confidentialite
        ORDER BY d.id
        """
        return get_db().query(query)
    except Exception as e:
        print(f"Erreur lors de la récupération des dossiers : {e}")
        return []

def supprimer_dossier(id_dossier):
    if not id_dossier:
        raise ValueError("L'identifiant du dossier est requis.")
    try:
        query = "MATCH (d:Dossier {id: $id}) DETACH DELETE d"
        get_db().query(query, {'id': id_dossier})
    except Exception as e:
        print(f"Erreur lors de la suppression du dossier : {e}")
        raise

def modifier_dossier(id_dossier, nom_personne, etat_personne, localisation, date_creation, commentaire=None, responsable_id=None, niveau_confidentialite='Interne'):
    if not id_dossier or not nom_personne or not etat_personne or not localisation or not date_creation:
        raise ValueError("Tous les champs obligatoires doivent être renseignés.")
    try:
        query = """
        MATCH (d:Dossier {id: $id})
        SET d.nom_personne = $nom_personne,
            d.etat_personne = $etat_personne,
            d.localisation = $localisation,
            d.date_creation = $date_creation,
            d.commentaire = $commentaire,
            d.responsable_id = $responsable_id,
            d.niveau_confidentialite = $niveau_confidentialite
        """
        params = {
            'id': id_dossier,
            'nom_personne': nom_personne,
            'etat_personne': etat_personne,
            'localisation': localisation,
            'date_creation': date_creation,
            'commentaire': commentaire,
            'responsable_id': responsable_id,
            'niveau_confidentialite': niveau_confidentialite
        }
        get_db().query(query, params)

        # Update responsibility relationship
        # First delete old
        del_rel_query = "MATCH (u:Utilisateur)-[r:RESPONSABLE_DE]->(d:Dossier {id: $id}) DELETE r"
        get_db().query(del_rel_query, {'id': id_dossier})

        # Create new
        if responsable_id:
             link_query = """
             MATCH (d:Dossier {id: $d_id}), (u:Utilisateur {id: $u_id})
             MERGE (u)-[:RESPONSABLE_DE]->(d)
             """
             get_db().query(link_query, {'d_id': id_dossier, 'u_id': responsable_id})

    except Exception as e:
        print(f"Erreur lors de la modification du dossier : {e}")
        raise

# --- Utilisateurs ---
def ajouter_utilisateur(nom, fonction, contact, role="Archiviste"):
    if not nom or not fonction:
        raise ValueError("Le nom et la fonction sont obligatoires.")
    if role not in ["RH", "Archiviste"]:
        raise ValueError("Le rôle doit être 'RH' ou 'Archiviste'.")
    
    try:
        new_id = get_next_id('Utilisateur')
        query = """
        CREATE (u:Utilisateur {
            id: $id,
            nom: $nom,
            fonction: $fonction,
            contact: $contact,
            role: $role,
            is_active: 1
        })
        RETURN u.id
        """
        get_db().query(query, {'id': new_id, 'nom': nom, 'fonction': fonction, 'contact': contact, 'role': role})
        return new_id
    except Exception as e:
        print(f"Erreur lors de l'ajout de l'utilisateur : {e}")
        raise

def lister_utilisateurs():
    # id, nom, fonction, contact, role, permissions, is_active
    try:
        query = """
        MATCH (u:Utilisateur)
        RETURN u.id, u.nom, u.fonction, u.contact, u.role, u.permissions, u.is_active
        ORDER BY u.id
        """
        return get_db().query(query)
    except Exception as e:
        print(f"Erreur lors de la récupération des utilisateurs : {e}")
        return []

def supprimer_utilisateur(id_utilisateur):
    if not id_utilisateur:
        raise ValueError("L'identifiant de l'utilisateur est requis.")
    try:
        # Also delete linked account nodes if any (though typically we map account to attributes or separate node linked)
        # SQL: DELETE FROM comptes... DELETE FROM utilisateurs
        query = """
        MATCH (u:Utilisateur {id: $id}) 
        OPTIONAL MATCH (u)-[:POSSEDE_COMPTE]->(c:Compte)
        DETACH DELETE u, c
        """
        get_db().query(query, {'id': id_utilisateur})
    except Exception as e:
        print(f"Erreur lors de la suppression de l'utilisateur : {e}")
        raise

def modifier_utilisateur(id_utilisateur, nom, fonction, contact, role="Archiviste"):
    if not id_utilisateur or not nom or not fonction:
        raise ValueError("L'identifiant, le nom et la fonction sont obligatoires.")
    if role not in ["RH", "Archiviste"]:
        raise ValueError("Le rôle doit être 'RH' ou 'Archiviste'.")
    try:
        query = """
        MATCH (u:Utilisateur {id: $id})
        SET u.nom = $nom, u.fonction = $fonction, u.contact = $contact, u.role = $role
        """
        get_db().query(query, {'id': id_utilisateur, 'nom': nom, 'fonction': fonction, 'contact': contact, 'role': role})
    except Exception as e:
        print(f"Erreur lors de la modification de l'utilisateur : {e}")
        raise

def obtenir_utilisateur_par_id(id_utilisateur):
    if not id_utilisateur:
        raise ValueError("L'identifiant de l'utilisateur est requis.")
    try:
        query = """
        MATCH (u:Utilisateur {id: $id})
        RETURN u.id, u.nom, u.fonction, u.contact, u.role, u.permissions, u.is_active
        """
        result = get_db().query_single(query, {'id': id_utilisateur})
        return result
    except Exception as e:
        print(f"Erreur lors de la récupération de l'utilisateur : {e}")
        return None

# --- Comptes ---
def verifier_authentification(username, matricule):
    # SQL returns: c.*, u.nom, u.fonction, u.contact, u.role, u.permissions, u.is_active
    # c.* is id, username, matricule, id_utilisateur
    try:
        query = """
        MATCH (c:Compte {username: $username, matricule: $matricule})<-[:POSSEDE_COMPTE]-(u:Utilisateur)
        RETURN c.id, c.username, c.matricule, c.id_utilisateur, u.nom, u.fonction, u.contact, u.role, u.permissions, u.is_active
        """
        result = get_db().query_single(query, {'username': username, 'matricule': matricule})
        
        if result and result[9]: # u.is_active is at index 9
             import json
             permissions = json.loads(result[8]) if result[8] else []
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
                'is_active': result[9]
             }
         
        # Backup/Permissive logic similar to original file
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
    except Exception:
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
    if not id_utilisateur or not username or not matricule:
        raise ValueError("Tous les champs sont obligatoires.")
    try:
        # Check uniqueness
        check = get_db().query_single("MATCH (c:Compte) WHERE c.username = $u OR c.matricule = $m RETURN count(c)", {'u':username, 'm':matricule})
        if check and check[0] > 0:
            print("Nom d'utilisateur ou matricule déjà existant.")
            return False

        new_id = get_next_id('Compte')
        query = """
        MATCH (u:Utilisateur {id: $uid})
        CREATE (c:Compte {id: $id, username: $username, matricule: $matricule, id_utilisateur: $uid})
        CREATE (u)-[:POSSEDE_COMPTE]->(c)
        """
        get_db().query(query, {'id': new_id, 'username': username, 'matricule': matricule, 'uid': id_utilisateur})
        return True
    except Exception as e:
        print(f"Erreur lors de la création du compte : {e}")
        raise

def verifier_utilisateur_sans_compte(id_utilisateur):
    try:
        query = "MATCH (u:Utilisateur {id: $id})-[:POSSEDE_COMPTE]->(c:Compte) RETURN count(c)"
        res = get_db().query_single(query, {'id': id_utilisateur})
        return res[0] == 0 if res else True
    except Exception:
        return False

def lister_utilisateurs_sans_compte():
    query = """
    MATCH (u:Utilisateur)
    WHERE NOT (u)-[:POSSEDE_COMPTE]->(:Compte)
    RETURN u.id, u.nom, u.fonction, u.contact, u.role, u.permissions, u.is_active
    """
    return get_db().query(query)

def generer_matricule_auto():
    # Simple simulation logic, querying max ID isn't as efficient in Neo4j but works for small sets
    # Or just keep string logic
    query = "MATCH (c:Compte) WHERE c.matricule STARTS WITH 'EMP' RETURN c.matricule"
    results = get_db().query(query)
    max_num = 0
    for row in results:
        mat = row[0]
        try:
             num = int(mat[3:])
             if num > max_num:
                 max_num = num
        except:
             pass
    
    next_num = max_num + 1
    return f"EMP{next_num:03d}"

# --- Mouvements ---
def ajouter_mouvement(id_dossier, id_utilisateur, type_mouvement, motif, date_mouvement=None, date_retour_prevue=None, destinataire_nom=None, destinataire_fonction=None, remarques=None, signature_utilisateur=None):
    if not id_dossier or not id_utilisateur or not type_mouvement:
         raise ValueError("Champs obligatoires manquants.")
    
    if date_mouvement is None:
        date_mouvement = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        new_id = get_next_id('Mouvement') # Actually create a Mouvement ID? 
        # In SQL, Mouvement is a row. In Neo4j w/ Rel, we can put props on Rel.
        # BUT we need an ID to delete/update existing one easily.
        # Relationships in Neo4j have internal IDs but best to use our own for consistency if we need to 'select' it later.
        
        # A relationship cannot be easily targeted by a custom ID property FROM A LIST without 'MATCH ()-[r]-() WHERE r.id=...'. 
        
        query = """
        MATCH (d:Dossier {id: $did})
        MERGE (u:Utilisateur {id: $uid})
        ON CREATE SET u.nom = 'Utilisateur ' + toString($uid), u.role = 'Archiviste'
        CREATE (u)-[r:A_EMPRUNTÉ {
            id: $id,
            type_mouvement: $type,
            motif: $motif,
            date_mouvement: $date,
            date_retour_prevue: $retour,
            destinataire_nom: $dest_nom,
            destinataire_fonction: $dest_fct,
            remarques: $rem,
            signature_utilisateur: $sig,
            id_dossier: $did,        
            id_utilisateur: $uid    
        }]->(d)
        RETURN r.id
        """
        # Note: storing id_dossier/id_user on the rel is redundant but keeps return shape consistent with "SELECT * FROM mouvements" which returns foreign keys.
        
        params = {
            'id': new_id,
            'uid': id_utilisateur,
            'did': id_dossier,
            'type': type_mouvement,
            'motif': motif,
            'date': date_mouvement,
            'retour': date_retour_prevue,
            'dest_nom': destinataire_nom,
            'dest_fct': destinataire_fonction,
            'rem': remarques,
            'sig': signature_utilisateur or ""
        }
        get_db().query(query, params)
        return new_id
    except Exception as e:
        print(f"Erreur ajout mouvement: {e}")
        raise

def historiques_mouvements_query_base(extra_where=""):
    # Helper for select * from mouvements...
    # SQL Order: id, id_dossier, id_usr, type, date, date_ret_prev, dest_nom, dest_fct, motif, rem, sig, date_ret_eff
    return f"""
    MATCH (u:Utilisateur)-[r:A_EMPRUNTÉ]->(d:Dossier)
    {extra_where}
    RETURN r.id, r.id_dossier, r.id_utilisateur, r.type_mouvement, r.date_mouvement, r.date_retour_prevue, r.destinataire_nom, r.destinataire_fonction, r.motif, r.remarques, COALESCE(r.signature_utilisateur, '') as signature_utilisateur, r.date_retour_effective, u.nom
    ORDER BY r.date_mouvement DESC
    """

def historique_mouvements(id_dossier):
    # Returns m.*, u.nom
    query = historiques_mouvements_query_base("WHERE d.id = $did")
    return get_db().query(query, {'did': id_dossier})

def supprimer_mouvement(id_mouvement):
    try:
        query = "MATCH ()-[r:A_EMPRUNTÉ]-() WHERE r.id = $id DELETE r"
        get_db().query(query, {'id': id_mouvement})
    except Exception as e:
        print(f"Erreur suppression mouvement: {e}")
        raise

def marquer_mouvement_retourne(id_mouvement):
    try:
        date_ret = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query = "MATCH ()-[r:A_EMPRUNTÉ]-() WHERE r.id = $id SET r.date_retour_effective = $d"
        get_db().query(query, {'id': id_mouvement, 'd': date_ret})
    except Exception as e:
        print(f"Erreur retour mouvement: {e}")
        raise

def verifier_mouvement_retourne(id_mouvement):
    try:
        query = "MATCH ()-[r:A_EMPRUNTÉ]-() WHERE r.id = $id RETURN r.date_retour_effective"
        res = get_db().query_single(query, {'id': id_mouvement})
        return res[0] is not None if res else False
    except Exception:
        return False

# --- Filtres & Getters ---
def obtenir_dossier_par_id(id_dossier):
    if not id_dossier: raise ValueError("ID requis")
    try:
        query = """
        MATCH (d:Dossier {id: $id})
        RETURN d.id, d.nom_personne, d.etat_personne, d.localisation, d.date_creation, d.commentaire, d.responsable_id, d.niveau_confidentialite
        """
        return get_db().query_single(query, {'id': id_dossier})
    except Exception:
        return None

def filtrer_dossiers_par_etat(etat):
    try:
        query = """
        MATCH (d:Dossier {etat_personne: $etat})
        RETURN d.id, d.nom_personne, d.etat_personne, d.localisation, d.date_creation, d.commentaire, d.responsable_id, d.niveau_confidentialite
        """
        return get_db().query(query, {'etat': etat})
    except Exception:
        return []

def lister_dossiers_actifs():
    return filtrer_dossiers_par_etat('Actif')

def lister_dossiers_non_actifs():
    try:
        query = """
        MATCH (d:Dossier) WHERE d.etat_personne IN ['Retraité', 'Décédé', 'Archivé']
        RETURN d.id, d.nom_personne, d.etat_personne, d.localisation, d.date_creation, d.commentaire, d.responsable_id, d.niveau_confidentialite
        """
        return get_db().query(query)
    except Exception:
        return []

def lister_dossiers_retraites():
    return filtrer_dossiers_par_etat('Retraité')

def lister_dossiers_decedes():
    return filtrer_dossiers_par_etat('Décédé')

def obtenir_responsable_dossier(id_dossier):
    # Returns d.*, u.nom, u.fonction, u.contact
    try:
        query = """
        MATCH (d:Dossier {id: $id})
        OPTIONAL MATCH (u:Utilisateur {id: d.responsable_id})
        RETURN d.id, d.nom_personne, d.etat_personne, d.localisation, d.date_creation, d.commentaire, d.responsable_id, d.niveau_confidentialite,
               u.nom, u.fonction, u.contact
        """
        return get_db().query_single(query, {'id': id_dossier})
    except Exception:
        return None

def lister_dossiers_par_responsable(id_responsable):
    try:
        query = """
        MATCH (d:Dossier {responsable_id: $id})
        RETURN d.id, d.nom_personne, d.etat_personne, d.localisation, d.date_creation, d.commentaire, d.responsable_id, d.niveau_confidentialite
        """
        return get_db().query(query, {'id': id_responsable})
    except Exception:
        return []

def obtenir_mouvements_en_retard():
    # m.*, d.nom_personne, u.nom
    # date('now') in Cypher is ISO date, but we stored string 'YYYY-MM-DD HH:MM:SS'. 
    # Comparing strings YYYY-MM-DD works if format is ISO.
    try:
        today = datetime.now().strftime('%Y-%m-%d')
        query = """
        MATCH (u:Utilisateur)-[r:A_EMPRUNTÉ]->(d:Dossier)
        WHERE r.date_retour_prevue < $today AND r.type_mouvement IN ['Prise', 'Transfert']
        RETURN r.id, r.id_dossier, r.id_utilisateur, r.type_mouvement, r.date_mouvement, r.date_retour_prevue, r.destinataire_nom, r.destinataire_fonction, r.motif, r.remarques, r.signature_utilisateur, r.date_retour_effective,
               d.nom_personne, u.nom
        ORDER BY r.date_retour_prevue ASC
        """
        return get_db().query(query, {'today': today})
    except Exception:
        return []

def obtenir_mouvements_par_dossier_complet(id_dossier):
    # m.*, u.nom, u.fonction
    try:
        query = """
        MATCH (u:Utilisateur)-[r:A_EMPRUNTÉ]->(d:Dossier {id: $did})
        RETURN r.id, r.id_dossier, r.id_utilisateur, r.type_mouvement, r.date_mouvement, r.date_retour_prevue, r.destinataire_nom, r.destinataire_fonction, r.motif, r.remarques, r.signature_utilisateur, r.date_retour_effective,
               u.nom, u.fonction
        ORDER BY r.date_mouvement DESC
        """
        return get_db().query(query, {'did': id_dossier})
    except Exception:
        return []

def verifier_autorisation_acces(id_utilisateur, niveau_confidentialite):
    try:
        user = obtenir_utilisateur_par_id(id_utilisateur)
        if not user: return False
        role = user[4]
        if niveau_confidentialite == 'Public': return True
        if role in ['RH', 'Archiviste']: return True
        return False
    except:
        return False

def verifier_permission(id_utilisateur, permission):
    try:
        user = obtenir_utilisateur_par_id(id_utilisateur)
        if not user: return False
        import json
        perms = json.loads(user[5]) if user[5] else []
        return "all" in perms or permission in perms
    except:
        return False

def obtenir_role_utilisateur(id_utilisateur):
    u = obtenir_utilisateur_par_id(id_utilisateur)
    return u[4] if u else None

# --- Pièces Jointes ---
def ajouter_piece_jointe(id_dossier, nom_fichier, chemin_fichier, type_fichier=None, description=None):
    if not id_dossier or not nom_fichier or not chemin_fichier:
        raise ValueError("Champs requis manquants.")
    try:
        new_id = get_next_id('PieceJointe')
        taille = os.path.getsize(chemin_fichier) if os.path.exists(chemin_fichier) else 0
        
        query = """
        MATCH (d:Dossier {id: $did})
        CREATE (p:PieceJointe {
            id: $id,
            id_dossier: $did,
            nom_fichier: $nom,
            chemin_fichier: $path,
            type_fichier: $type,
            taille_fichier: $taille,
            date_ajout: datetime(),
            description: $desc
        })
        CREATE (d)-[:CONTIENT]->(p)
        RETURN p.id
        """
        get_db().query(query, {
            'id': new_id, 'did': id_dossier, 'nom': nom_fichier, 'path': chemin_fichier,
            'type': type_fichier, 'taille': taille, 'desc': description
        })
        return new_id
    except Exception as e:
        print(f"Erreur ajout PJ: {e}")
        raise

def lister_pieces_jointes(id_dossier):
    # SQL: id, nom, chemin, type, taille, date_ajout, description
    try:
        query = """
        MATCH (d:Dossier {id: $did})-[:CONTIENT]->(p:PieceJointe)
        RETURN p.id, p.nom_fichier, p.chemin_fichier, p.type_fichier, p.taille_fichier, toString(p.date_ajout), p.description
        ORDER BY p.date_ajout DESC
        """
        return get_db().query(query, {'did': id_dossier})
    except Exception:
        return []

def supprimer_piece_jointe(id_piece):
    try:
        # Get path first for parsing
        query_sel = "MATCH (p:PieceJointe {id: $id}) RETURN p.chemin_fichier"
        res = get_db().query_single(query_sel, {'id': id_piece})
        if res:
            path = res[0]
            if os.path.exists(path):
                try: os.remove(path)
                except: pass
        
        query_del = "MATCH (p:PieceJointe {id: $id}) DETACH DELETE p"
        get_db().query(query_del, {'id': id_piece})
    except Exception as e:
        print(f"Erreur delete PJ: {e}")
        raise

def obtenir_piece_jointe(id_piece):
    try:
        query = """
        MATCH (p:PieceJointe {id: $id})
        RETURN p.id, p.id_dossier, p.nom_fichier, p.chemin_fichier, p.type_fichier, p.taille_fichier, toString(p.date_ajout), p.description
        """
        return get_db().query_single(query, {'id': id_piece})
    except:
        return None

def formater_taille_fichier(taille_bytes):
    if taille_bytes < 1024:
        return f"{taille_bytes} B"
    elif taille_bytes < 1024 * 1024:
        return f"{taille_bytes / 1024:.1f} KB"
    elif taille_bytes < 1024 * 1024 * 1024:
        return f"{taille_bytes / (1024 * 1024):.1f} MB"
