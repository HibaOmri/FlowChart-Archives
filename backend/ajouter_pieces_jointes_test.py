#!/usr/bin/env python3
"""
Script pour ajouter des pièces jointes de test à certains dossiers
"""

import db
import os
import shutil
from datetime import datetime
import random

def creer_fichier_test(chemin_fichier, contenu="Contenu de test"):
    """Crée un fichier de test"""
    try:
        with open(chemin_fichier, 'w', encoding='utf-8') as f:
            f.write(contenu)
        return True
    except Exception as e:
        print(f"Erreur création fichier {chemin_fichier}: {e}")
        return False

def ajouter_pieces_jointes_test():
    """Ajoute des pièces jointes de test à certains dossiers"""
    
    try:
        # Récupérer tous les dossiers
        dossiers = db.lister_dossiers()
        
        if not dossiers:
            print("❌ Erreur : Aucun dossier trouvé dans la base.")
            return
        
        print(f"📊 Dossiers disponibles : {len(dossiers)}")
        
        # Types de fichiers possibles
        types_fichiers = [
            (".pdf", "Document PDF"),
            (".doc", "Document Word"),
            (".docx", "Document Word"),
            (".xls", "Document Excel"),
            (".xlsx", "Document Excel"),
            (".txt", "Document texte"),
            (".jpg", "Image JPEG"),
            (".png", "Image PNG"),
            (".gif", "Image GIF"),
            (".mp4", "Vidéo MP4"),
            (".avi", "Vidéo AVI"),
            (".mov", "Vidéo MOV")
        ]
        
        # Noms de fichiers possibles
        noms_fichiers = [
            "rapport_annuel",
            "contrat_emploi",
            "fiche_paie",
            "evaluation_performance",
            "formation_complete",
            "audit_interne",
            "certification_qualite",
            "plan_securite",
            "etude_environnementale",
            "projet_innovation",
            "budget_exercice",
            "compte_rendu_reunion",
            "analyse_technique",
            "document_historique",
            "photo_equipe",
            "video_presentation",
            "manuel_procedure",
            "rapport_audit",
            "plan_formation",
            "etude_marketing"
        ]
        
        pieces_ajoutees = 0
        
        # Pour chaque dossier, ajouter 1-3 pièces jointes
        for dossier in dossiers:
            dossier_id = dossier[0]
            nom_dossier = dossier[1]
            
            # Nombre de pièces jointes aléatoire entre 1 et 3
            nb_pieces = random.randint(1, 3)
            
            # Créer le dossier d'archives s'il n'existe pas
            archives_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'archives')
            if not os.path.exists(archives_dir):
                os.makedirs(archives_dir)
            
            # Créer le sous-dossier pour ce dossier
            dossier_dir = os.path.join(archives_dir, f'dossier_{dossier_id}')
            if not os.path.exists(dossier_dir):
                os.makedirs(dossier_dir)
            
            for i in range(nb_pieces):
                # Type de fichier aléatoire
                type_fichier, description_type = random.choice(types_fichiers)
                
                # Nom de fichier aléatoire
                nom_base = random.choice(noms_fichiers)
                nom_fichier = f"{nom_base}_{dossier_id}_{i+1}{type_fichier}"
                
                # Chemin complet du fichier
                chemin_fichier = os.path.join(dossier_dir, nom_fichier)
                
                # Contenu du fichier
                contenu = f"""
Document de test pour le dossier {nom_dossier}
ID Dossier: {dossier_id}
Date de création: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
Type: {description_type}
Description: {nom_base.replace('_', ' ').title()}

Ce fichier a été généré automatiquement pour les tests du système d'archives OCP Khouribga.
                """
                
                # Créer le fichier de test
                if creer_fichier_test(chemin_fichier, contenu):
                    try:
                        # Ajouter à la base de données
                        db.ajouter_piece_jointe(
                            id_dossier=dossier_id,
                            nom_fichier=nom_fichier,
                            chemin_fichier=chemin_fichier,
                            type_fichier=type_fichier,
                            description=f"{description_type} - {nom_base.replace('_', ' ').title()} - Dossier {nom_dossier}"
                        )
                        pieces_ajoutees += 1
                        
                        if pieces_ajoutees % 10 == 0:
                            print(f"✅ {pieces_ajoutees} pièces jointes ajoutées...")
                            
                    except Exception as e:
                        print(f"❌ Erreur lors de l'ajout de la pièce jointe pour le dossier {nom_dossier}: {e}")
        
        print(f"\n🎉 Résumé :")
        print(f"- {pieces_ajoutees} pièces jointes ajoutées avec succès")
        print(f"- {len(dossiers)} dossiers traités")
        
        # Statistiques par type de fichier
        print(f"\n📊 Statistiques par type de fichier :")
        for type_fichier, description in types_fichiers:
            count = db.compter_pieces_jointes_par_type(type_fichier)
            print(f"- {description}: {count} fichiers")
        
    except Exception as e:
        print(f"❌ Erreur générale lors de l'ajout des pièces jointes : {e}")

def compter_pieces_jointes_par_type(type_fichier):
    """Compte les pièces jointes par type de fichier"""
    try:
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM pieces_jointes WHERE type_fichier = ?", (type_fichier,))
        count = cur.fetchone()[0]
        conn.close()
        return count
    except:
        return 0

if __name__ == "__main__":
    print("🚀 Ajout de pièces jointes de test...")
    ajouter_pieces_jointes_test()
    print("\n✅ Script terminé !") 