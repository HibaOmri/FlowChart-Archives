#!/usr/bin/env python3
"""
Script de test pour les fonctions de pièces jointes
"""

import db
import os

def test_pieces_jointes():
    print("🧪 Test des fonctions de pièces jointes...")
    
    try:
        # Test 1: Vérifier que la table existe
        print("\n1. Vérification de la table pieces_jointes...")
        import sqlite3
        conn = sqlite3.connect('archives.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='pieces_jointes'")
        result = cursor.fetchone()
        if result:
            print("✅ Table pieces_jointes existe")
        else:
            print("❌ Table pieces_jointes n'existe pas")
        conn.close()
        
        # Test 2: Lister les dossiers
        print("\n2. Test de lister_dossiers...")
        dossiers = db.lister_dossiers()
        print(f"📁 {len(dossiers)} dossiers trouvés")
        
        if dossiers:
            id_dossier = dossiers[0][0]  # Premier dossier
            print(f"📋 Test avec le dossier ID: {id_dossier}")
            
            # Test 3: Lister les pièces jointes
            print("\n3. Test de lister_pieces_jointes...")
            pieces = db.lister_pieces_jointes(id_dossier)
            print(f"📎 {len(pieces)} pièces jointes trouvées")
            
            # Test 4: Test de formater_taille_fichier
            print("\n4. Test de formater_taille_fichier...")
            tailles = [1024, 1024*1024, 1024*1024*1024]
            for taille in tailles:
                formatted = db.formater_taille_fichier(taille)
                print(f"   {taille} bytes = {formatted}")
        
        print("\n✅ Tests terminés avec succès !")
        
    except Exception as e:
        print(f"\n❌ Erreur lors des tests : {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_pieces_jointes() 