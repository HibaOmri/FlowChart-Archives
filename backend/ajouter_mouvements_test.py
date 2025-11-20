#!/usr/bin/env python3
"""
Script pour ajouter des mouvements de test pour tous les dossiers
"""

import db
from datetime import datetime, timedelta
import random

def ajouter_mouvements_test():
    """Ajoute des mouvements de test pour tous les dossiers"""
    
    try:
        # Récupérer tous les dossiers et utilisateurs
        dossiers = db.lister_dossiers()
        utilisateurs = db.lister_utilisateurs()
        
        if not dossiers or not utilisateurs:
            print("❌ Erreur : Aucun dossier ou utilisateur trouvé dans la base.")
            return
        
        print(f"📊 Dossiers disponibles : {len(dossiers)}")
        print(f"👥 Utilisateurs disponibles : {len(utilisateurs)}")
        
        # Types de mouvements possibles
        types_mouvements = ["Prise", "Transfert", "Retour", "Consultation", "Archivage", "Numérisation"]
        
        # Motifs possibles
        motifs_possibles = [
            "Consultation pour recherche historique",
            "Transfert vers service numérisation",
            "Retour après traitement",
            "Consultation pour audit",
            "Transfert vers archives centrales",
            "Consultation pour rapport annuel",
            "Transfert vers service restauration",
            "Consultation pour exposition",
            "Transfert vers laboratoire d'analyse",
            "Consultation pour formation",
            "Transfert vers service qualité",
            "Consultation pour projet R&D",
            "Transfert vers service environnement",
            "Consultation pour conformité",
            "Transfert vers service sécurité",
            "Consultation pour partenariat",
            "Transfert vers service international",
            "Consultation pour certification",
            "Transfert vers service formation",
            "Consultation pour amélioration continue"
        ]
        
        # Localisations possibles
        localisations = [
            "Archives Historiques - Khouribga Administration",
            "Archives Direction - Khouribga Administration", 
            "Archives RH - Khouribga Administration",
            "Archives Techniques - Khouribga Technique",
            "Archives Finances - Khouribga Administration",
            "Archives Logistique - Khouribga Technique",
            "Archives Communication - Khouribga Administration",
            "Archives R&D - Khouribga Technique",
            "Archives Environnement - Khouribga Technique",
            "Archives Spéciales - Khouribga Administration",
            "Archives Internationales - Khouribga Administration",
            "Archives Formation - Khouribga Administration",
            "Archives Sécurité - Khouribga Technique",
            "Archives Qualité - Khouribga Technique"
        ]
        
        mouvements_ajoutes = 0
        
        # Pour chaque dossier, ajouter 2-4 mouvements
        for dossier in dossiers:
            dossier_id = dossier[0]
            nom_dossier = dossier[1]
            
            # Nombre de mouvements aléatoire entre 2 et 4
            nb_mouvements = random.randint(2, 4)
            
            # Date de base pour ce dossier
            date_base = datetime.strptime(dossier[4], "%Y-%m-%d")  # date_creation
            
            for i in range(nb_mouvements):
                # Utilisateur aléatoire
                utilisateur = random.choice(utilisateurs)
                utilisateur_id = utilisateur[0]
                
                # Type de mouvement aléatoire
                type_mouvement = random.choice(types_mouvements)
                
                # Date du mouvement (après la date de création)
                jours_apres_creation = random.randint(1, 365)
                date_mouvement = date_base + timedelta(days=jours_apres_creation)
                
                # Motif aléatoire
                motif = random.choice(motifs_possibles)
                
                # Localisation aléatoire
                localisation = random.choice(localisations)
                
                # Remarques détaillées
                remarques = f"{motif} - {localisation} - Dossier {nom_dossier}"
                
                try:
                    db.ajouter_mouvement(
                        dossier_id, 
                        utilisateur_id, 
                        type_mouvement, 
                        date_mouvement.strftime("%Y-%m-%d %H:%M:%S"),
                        remarques
                    )
                    mouvements_ajoutes += 1
                    
                    if mouvements_ajoutes % 10 == 0:
                        print(f"✅ {mouvements_ajoutes} mouvements ajoutés...")
                        
                except Exception as e:
                    print(f"❌ Erreur lors de l'ajout du mouvement pour le dossier {nom_dossier}: {e}")
        
        print(f"\n🎉 Résumé :")
        print(f"- {mouvements_ajoutes} mouvements ajoutés avec succès")
        print(f"- {len(dossiers)} dossiers traités")
        print(f"- {len(utilisateurs)} utilisateurs impliqués")
        
        # Statistiques par type de mouvement
        print(f"\n📊 Statistiques par type de mouvement :")
        for type_mvt in types_mouvements:
            count = db.compter_mouvements_par_type(type_mvt)
            print(f"- {type_mvt}: {count} mouvements")
        
    except Exception as e:
        print(f"❌ Erreur générale lors de l'ajout des mouvements : {e}")

def compter_mouvements_par_type(type_mouvement):
    """Compte les mouvements par type"""
    try:
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM mouvements WHERE type_mouvement = ?", (type_mouvement,))
        count = cur.fetchone()[0]
        conn.close()
        return count
    except:
        return 0

if __name__ == "__main__":
    print("🚀 Ajout de mouvements de test...")
    ajouter_mouvements_test()
    print("\n✅ Script terminé !") 