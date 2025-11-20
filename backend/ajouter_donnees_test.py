#!/usr/bin/env python3
"""
Script pour ajouter des dossiers et mouvements de test dans la base de données
"""

import db
from datetime import datetime, timedelta

def ajouter_donnees_test():
    """Ajoute des dossiers et mouvements de test dans la base de données"""
    
    # Ajouter des dossiers de test pour OCP Khouribga
    dossiers_test = [
        ("Mohammed V", "Décédé", "Archives Historiques - Khouribga Administration", "2023-01-15", "Dossier historique - Roi du Maroc, période OCP Khouribga"),
        ("Hassan II", "Décédé", "Archives Historiques - Khouribga Administration", "2023-02-20", "Dossier historique - Roi du Maroc, développement OCP Khouribga"),
        ("Mohammed VI", "Actif", "Archives Direction - Khouribga Administration", "2023-03-10", "Dossier actuel - Roi du Maroc, modernisation OCP Khouribga"),
        ("Karim El Khadiri", "Actif", "Archives Direction - Khouribga Administration", "2023-04-05", "Directeur site Khouribga - Documents de direction"),
        ("Nadia Benslimane", "Actif", "Archives RH - Khouribga Administration", "2023-05-12", "Responsable RH Khouribga - Documents RH"),
        ("Omar Tazi", "Actif", "Archives Techniques - Khouribga Technique", "2023-06-01", "Chef service technique - Documents techniques"),
        ("Youssef Benali", "Retraité", "Archives Historiques - Khouribga Administration", "2023-06-15", "Ancien directeur des mines - Khouribga"),
        ("Fatima Zahra Bennani", "Retraité", "Archives Historiques - Khouribga Administration", "2023-07-01", "Ancienne responsable archives - Khouribga"),
        ("Rachid Benjelloun", "Actif", "Archives Techniques - Khouribga Technique", "2023-07-15", "Ingénieur mines - Documents techniques"),
        ("Leila Mansouri", "Actif", "Archives Sécurité - Khouribga Technique", "2023-08-01", "Responsable sécurité - Documents sécurité"),
        ("Samira El Fassi", "Actif", "Archives Formation - Khouribga Administration", "2023-08-15", "Responsable formation - Documents formation")
    ]
    
    try:
        # Ajouter les dossiers
        for nom, etat, localisation, date_creation, commentaire in dossiers_test:
            db.ajouter_dossier(nom, etat, localisation, date_creation, commentaire)
            print(f"Dossier ajouté : {nom}")
        
        # Récupérer les IDs des dossiers et utilisateurs
        dossiers = db.lister_dossiers()
        utilisateurs = db.lister_utilisateurs()
        
        if not dossiers or not utilisateurs:
            print("Erreur : Aucun dossier ou utilisateur trouvé dans la base.")
            return
        
        # Ajouter des mouvements de test pour OCP Khouribga
        mouvements_test = [
            # Mouvements pour le premier dossier (Mohammed V)
            (dossiers[0][0], utilisateurs[0][0], "Prise", "2023-06-01 09:00:00", "Consultation pour recherche historique OCP Khouribga"),
            (dossiers[0][0], utilisateurs[1][0], "Transfert", "2023-06-02 14:30:00", "Transfert vers service numérisation - Khouribga Technique"),
            (dossiers[0][0], utilisateurs[2][0], "Retour", "2023-06-03 16:45:00", "Retour après numérisation - Archives Historiques Khouribga"),
            
            # Mouvements pour le deuxième dossier (Hassan II)
            (dossiers[1][0], utilisateurs[3][0], "Prise", "2023-06-05 10:15:00", "Consultation pour exposition - Musée OCP Khouribga"),
            (dossiers[1][0], utilisateurs[0][0], "Transfert", "2023-06-06 11:20:00", "Transfert vers laboratoire - Khouribga Technique"),
            (dossiers[1][0], utilisateurs[1][0], "Retour", "2023-06-07 15:30:00", "Retour après analyse - Archives Historiques Khouribga"),
            
            # Mouvements pour le troisième dossier (Mohammed VI)
            (dossiers[2][0], utilisateurs[4][0], "Prise", "2023-06-10 08:45:00", "Consultation pour rapport annuel OCP Khouribga"),
            (dossiers[2][0], utilisateurs[2][0], "Transfert", "2023-06-11 13:15:00", "Transfert vers service restauration - Khouribga Technique"),
            (dossiers[2][0], utilisateurs[0][0], "Retour", "2023-06-12 17:00:00", "Retour après restauration - Archives Direction Khouribga"),
            
            # Mouvements pour le quatrième dossier (Karim El Khadiri)
            (dossiers[3][0], utilisateurs[7][0], "Prise", "2023-06-15 09:30:00", "Consultation documents direction - Conseil d'administration Khouribga"),
            (dossiers[3][0], utilisateurs[8][0], "Transfert", "2023-06-16 14:00:00", "Transfert vers service RH - Khouribga Administration"),
            (dossiers[3][0], utilisateurs[1][0], "Retour", "2023-06-17 16:00:00", "Retour après validation RH - Archives Direction Khouribga"),
        ]
        
        for id_dossier, id_utilisateur, type_mouvement, date_mouvement, remarques in mouvements_test:
            db.ajouter_mouvement(id_dossier, id_utilisateur, type_mouvement, date_mouvement, remarques)
            print(f"Mouvement ajouté : {type_mouvement} pour le dossier {id_dossier}")
        
        print("\nToutes les données de test ont été ajoutées avec succès !")
        
        # Afficher un résumé
        print(f"\nRésumé :")
        print(f"- {len(dossiers_test)} dossiers ajoutés")
        print(f"- {len(mouvements_test)} mouvements ajoutés")
        print(f"- {len(utilisateurs)} utilisateurs disponibles")
        
    except Exception as e:
        print(f"Erreur lors de l'ajout des données : {e}")

if __name__ == "__main__":
    ajouter_donnees_test() 