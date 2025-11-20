#!/usr/bin/env python3
"""
Script pour afficher un résumé complet du système d'archives
"""

import db
import os
from datetime import datetime

def afficher_resume_systeme():
    """Affiche un résumé complet du système d'archives"""
    
    print("=" * 60)
    print("📊 RÉSUMÉ COMPLET DU SYSTÈME D'ARCHIVES OCP KHOURIBGA")
    print("=" * 60)
    
    try:
        # Récupérer toutes les données
        dossiers = db.lister_dossiers()
        utilisateurs = db.lister_utilisateurs()
        
        # Compter les mouvements
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM mouvements")
        total_mouvements = cur.fetchone()[0]
        
        # Compter les pièces jointes
        cur.execute("SELECT COUNT(*) FROM pieces_jointes")
        total_pieces_jointes = cur.fetchone()[0]
        
        # Compter par état
        cur.execute("SELECT etat_personne, COUNT(*) FROM dossiers GROUP BY etat_personne")
        etats = cur.fetchall()
        
        # Compter par localisation
        cur.execute("SELECT localisation, COUNT(*) FROM dossiers GROUP BY localisation")
        localisations = cur.fetchall()
        
        conn.close()
        
        print(f"\n📁 DOSSIERS :")
        print(f"   • Total : {len(dossiers)} dossiers")
        
        print(f"\n   📈 Répartition par état :")
        for etat, count in etats:
            print(f"      - {etat} : {count} dossiers")
        
        print(f"\n   📍 Répartition par localisation :")
        for localisation, count in localisations:
            print(f"      - {localisation} : {count} dossiers")
        
        print(f"\n👥 UTILISATEURS :")
        print(f"   • Total : {len(utilisateurs)} utilisateurs")
        
        print(f"\n   👤 Détail des utilisateurs :")
        for user in utilisateurs:
            print(f"      - {user[1]} ({user[2]}) - {user[4]}")
        
        print(f"\n📋 MOUVEMENTS :")
        print(f"   • Total : {total_mouvements} mouvements")
        
        # Statistiques par type de mouvement
        types_mouvements = ["Prise", "Transfert", "Retour", "Consultation", "Archivage", "Numérisation"]
        print(f"\n   📊 Répartition par type :")
        for type_mvt in types_mouvements:
            count = db.compter_mouvements_par_type(type_mvt)
            print(f"      - {type_mvt} : {count} mouvements")
        
        print(f"\n📎 PIÈCES JOINTES :")
        print(f"   • Total : {total_pieces_jointes} fichiers")
        
        # Statistiques par type de fichier
        types_fichiers = [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".txt", ".jpg", ".png", ".gif", ".mp4", ".avi", ".mov"]
        print(f"\n   📊 Répartition par type de fichier :")
        for type_fichier in types_fichiers:
            count = db.compter_pieces_jointes_par_type(type_fichier)
            if count > 0:
                print(f"      - {type_fichier} : {count} fichiers")
        
        print(f"\n💾 STOCKAGE :")
        
        # Vérifier les dossiers physiques
        archives_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'archives')
        if os.path.exists(archives_dir):
            dossiers_physiques = [d for d in os.listdir(archives_dir) if d.startswith('dossier_')]
            print(f"   • Dossiers physiques créés : {len(dossiers_physiques)}")
            
            # Compter les fichiers physiques
            total_fichiers_physiques = 0
            for dossier in dossiers_physiques:
                dossier_path = os.path.join(archives_dir, dossier)
                if os.path.isdir(dossier_path):
                    fichiers = [f for f in os.listdir(dossier_path) if os.path.isfile(os.path.join(dossier_path, f))]
                    total_fichiers_physiques += len(fichiers)
            
            print(f"   • Fichiers physiques : {total_fichiers_physiques}")
        else:
            print(f"   • Dossier archives non trouvé")
        
        # Vérifier les dossiers frontend
        frontend_archives_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend', 'archives')
        if os.path.exists(frontend_archives_dir):
            dossiers_frontend = [d for d in os.listdir(frontend_archives_dir) if d.startswith('dossier_')]
            print(f"   • Dossiers frontend créés : {len(dossiers_frontend)}")
        
        print(f"\n🎯 STATISTIQUES GÉNÉRALES :")
        print(f"   • Ratio mouvements/dossier : {total_mouvements/len(dossiers):.1f}")
        print(f"   • Ratio pièces jointes/dossier : {total_pieces_jointes/len(dossiers):.1f}")
        print(f"   • Dossiers actifs : {sum(1 for etat, _ in etats if etat == 'Actif')}")
        print(f"   • Dossiers retraités : {sum(1 for etat, _ in etats if etat == 'Retraité')}")
        print(f"   • Dossiers décédés : {sum(1 for etat, _ in etats if etat == 'Décédé')}")
        
        print(f"\n📅 DERNIÈRE MISE À JOUR :")
        print(f"   • {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}")
        
        print(f"\n" + "=" * 60)
        print("✅ Système d'archives OCP Khouribga opérationnel !")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération du résumé : {e}")

if __name__ == "__main__":
    afficher_resume_systeme() 