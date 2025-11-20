#!/usr/bin/env python3
"""
Script de test pour diagnostiquer le problème avec l'ajout de fichiers
"""

import os
import sys
import shutil
from datetime import datetime

# Ajouter le chemin du backend
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))
import db

def test_file_upload():
    """Test de l'ajout de fichiers"""
    print("=== Test d'ajout de fichiers ===")
    
    # 1. Test de création d'un dossier
    print("\n1. Création d'un dossier de test...")
    try:
        dossier_id = db.ajouter_dossier(
            nom_personne="Test Fichiers",
            etat_personne="Actif",
            localisation="Test",
            date_creation="2024-01-01",
            commentaire="Dossier de test pour fichiers"
        )
        print(f"✅ Dossier créé avec ID: {dossier_id}")
    except Exception as e:
        print(f"❌ Erreur création dossier: {e}")
        return
    
    # 2. Test de création du dossier d'archives
    print("\n2. Création du dossier d'archives...")
    try:
        archives_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'archives')
        if not os.path.exists(archives_dir):
            os.makedirs(archives_dir)
            print(f"✅ Dossier archives créé: {archives_dir}")
        else:
            print(f"✅ Dossier archives existe déjà: {archives_dir}")
    except Exception as e:
        print(f"❌ Erreur création dossier archives: {e}")
        return
    
    # 3. Test de création du sous-dossier
    print("\n3. Création du sous-dossier pour le dossier...")
    try:
        dossier_dir = os.path.join(archives_dir, f'dossier_{dossier_id}')
        if not os.path.exists(dossier_dir):
            os.makedirs(dossier_dir)
            print(f"✅ Sous-dossier créé: {dossier_dir}")
        else:
            print(f"✅ Sous-dossier existe déjà: {dossier_dir}")
    except Exception as e:
        print(f"❌ Erreur création sous-dossier: {e}")
        return
    
    # 4. Test de création d'un fichier de test
    print("\n4. Création d'un fichier de test...")
    try:
        test_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_file.txt')
        with open(test_file_path, 'w', encoding='utf-8') as f:
            f.write("Ceci est un fichier de test pour l'upload.")
        print(f"✅ Fichier de test créé: {test_file_path}")
    except Exception as e:
        print(f"❌ Erreur création fichier test: {e}")
        return
    
    # 5. Test de copie du fichier
    print("\n5. Test de copie du fichier...")
    try:
        file_name = os.path.basename(test_file_path)
        dest_path = os.path.join(dossier_dir, file_name)
        
        # Éviter les doublons
        counter = 1
        base_name, ext = os.path.splitext(file_name)
        while os.path.exists(dest_path):
            file_name = f"{base_name}_{counter}{ext}"
            dest_path = os.path.join(dossier_dir, file_name)
            counter += 1
        
        shutil.copy2(test_file_path, dest_path)
        print(f"✅ Fichier copié vers: {dest_path}")
    except Exception as e:
        print(f"❌ Erreur copie fichier: {e}")
        return
    
    # 6. Test d'ajout en base de données
    print("\n6. Test d'ajout en base de données...")
    try:
        piece_id = db.ajouter_piece_jointe(
            id_dossier=dossier_id,
            nom_fichier=file_name,
            chemin_fichier=dest_path,
            type_fichier=os.path.splitext(file_name)[1].lower(),
            description=f"Fichier de test ajouté le {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        )
        print(f"✅ Pièce jointe ajoutée avec ID: {piece_id}")
    except Exception as e:
        print(f"❌ Erreur ajout en base: {e}")
        return
    
    # 7. Test de récupération des pièces jointes
    print("\n7. Test de récupération des pièces jointes...")
    try:
        pieces = db.lister_pieces_jointes(dossier_id)
        print(f"✅ Pièces jointes récupérées: {len(pieces)} fichier(s)")
        for piece in pieces:
            print(f"   - {piece[1]} ({piece[3]}) - {piece[4]} bytes")
    except Exception as e:
        print(f"❌ Erreur récupération pièces jointes: {e}")
        return
    
    # 8. Nettoyage
    print("\n8. Nettoyage...")
    try:
        # Supprimer le fichier de test
        if os.path.exists(test_file_path):
            os.remove(test_file_path)
            print("✅ Fichier de test supprimé")
        
        # Supprimer le dossier de test
        if os.path.exists(dossier_dir):
            shutil.rmtree(dossier_dir)
            print("✅ Dossier de test supprimé")
        
        # Supprimer le dossier d'archives s'il est vide
        if os.path.exists(archives_dir) and not os.listdir(archives_dir):
            os.rmdir(archives_dir)
            print("✅ Dossier archives supprimé (vide)")
        
        # Supprimer le dossier de test de la base
        db.supprimer_dossier(dossier_id)
        print("✅ Dossier supprimé de la base de données")
        
    except Exception as e:
        print(f"⚠️ Erreur lors du nettoyage: {e}")
    
    print("\n=== Test terminé ===")

if __name__ == "__main__":
    test_file_upload() 