#!/usr/bin/env python3
"""
Script de test pour l'interface d'ajout de fichiers
"""

import os
import sys
import tempfile
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt

# Ajouter le chemin du frontend
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frontend'))
from components.add_dossier_dialog import AddDossierDialog

def test_add_dossier_dialog():
    """Test de l'interface AddDossierDialog"""
    print("=== Test de l'interface AddDossierDialog ===")
    
    app = QApplication(sys.argv)
    
    # Créer un fichier de test temporaire
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
        f.write("Fichier de test pour l'interface")
        test_file_path = f.name
    
    print(f"Fichier de test créé: {test_file_path}")
    
    try:
        # Créer le dialogue
        dialog = AddDossierDialog()
        print("✅ Dialogue AddDossierDialog créé")
        
        # Simuler l'ajout de fichiers
        print("\nTest d'ajout de fichiers...")
        dialog.on_files_dropped([test_file_path])
        
        # Vérifier que les fichiers ont été ajoutés
        files_in_list = dialog.files_list.get_files()
        print(f"Fichiers dans la liste: {files_in_list}")
        
        if test_file_path in files_in_list:
            print("✅ Fichier ajouté avec succès à la liste")
        else:
            print("❌ Fichier non ajouté à la liste")
        
        # Vérifier les données retournées
        dossier_data, files_to_upload = dialog.get_data()
        print(f"Données du dossier: {dossier_data}")
        print(f"Fichiers à uploader: {files_to_upload}")
        
        if test_file_path in files_to_upload:
            print("✅ Fichier correctement retourné par get_data()")
        else:
            print("❌ Fichier non retourné par get_data()")
        
        # Afficher le dialogue (optionnel)
        print("\nAffichage du dialogue (fermez-le pour continuer)...")
        dialog.show()
        
        # Attendre que l'utilisateur ferme le dialogue
        app.exec_()
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Nettoyage
        try:
            os.unlink(test_file_path)
            print("✅ Fichier de test supprimé")
        except:
            pass
    
    print("=== Test terminé ===")

if __name__ == "__main__":
    test_add_dossier_dialog() 