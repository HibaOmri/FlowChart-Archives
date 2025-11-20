#!/usr/bin/env python3
"""
Script pour ajouter plus de dossiers variés dans la base de données
"""

import db
from datetime import datetime, timedelta
import random

def ajouter_plus_de_dossiers():
    """Ajoute des dossiers supplémentaires variés dans la base de données"""
    
    # Dossiers supplémentaires variés pour OCP Khouribga
    dossiers_supplementaires = [
        # Dossiers historiques
        ("Ahmed Bennani", "Décédé", "Archives Historiques - Khouribga Administration", "2022-01-10", "Ancien directeur des mines - Période 1980-1995"),
        ("Fatima El Khadiri", "Décédé", "Archives Historiques - Khouribga Administration", "2022-02-15", "Ancienne responsable archives - Période 1975-2000"),
        ("Mohammed Benjelloun", "Décédé", "Archives Historiques - Khouribga Administration", "2022-03-20", "Ancien ingénieur principal - Période 1965-1990"),
        ("Amina Tazi", "Décédé", "Archives Historiques - Khouribga Administration", "2022-04-25", "Ancienne chef comptabilité - Période 1970-2005"),
        
        # Dossiers actifs - Direction
        ("Hassan Mansouri", "Actif", "Archives Direction - Khouribga Administration", "2023-09-01", "Directeur adjoint - Documents de direction"),
        ("Nadia El Fassi", "Actif", "Archives Direction - Khouribga Administration", "2023-09-15", "Directrice financière - Documents financiers"),
        ("Karim Benali", "Actif", "Archives Direction - Khouribga Administration", "2023-10-01", "Directeur technique - Documents techniques"),
        ("Leila Bennani", "Actif", "Archives Direction - Khouribga Administration", "2023-10-15", "Directrice RH - Documents ressources humaines"),
        
        # Dossiers actifs - RH
        ("Samira Tazi", "Actif", "Archives RH - Khouribga Administration", "2023-11-01", "Responsable recrutement - Documents recrutement"),
        ("Youssef Mansouri", "Actif", "Archives RH - Khouribga Administration", "2023-11-15", "Responsable formation - Documents formation"),
        ("Fatima Benjelloun", "Actif", "Archives RH - Khouribga Administration", "2023-12-01", "Responsable paie - Documents paie"),
        ("Omar El Khadiri", "Actif", "Archives RH - Khouribga Administration", "2023-12-15", "Responsable sécurité sociale - Documents sécurité sociale"),
        
        # Dossiers actifs - Technique
        ("Rachid Bennani", "Actif", "Archives Techniques - Khouribga Technique", "2024-01-01", "Chef service maintenance - Documents maintenance"),
        ("Amina Mansouri", "Actif", "Archives Techniques - Khouribga Technique", "2024-01-15", "Ingénieure mines - Documents exploitation"),
        ("Hassan Tazi", "Actif", "Archives Techniques - Khouribga Technique", "2024-02-01", "Responsable sécurité - Documents sécurité"),
        ("Nadia Benali", "Actif", "Archives Techniques - Khouribga Technique", "2024-02-15", "Responsable qualité - Documents qualité"),
        
        # Dossiers actifs - Finances
        ("Karim El Fassi", "Actif", "Archives Finances - Khouribga Administration", "2024-03-01", "Responsable comptabilité - Documents comptables"),
        ("Leila Benjelloun", "Actif", "Archives Finances - Khouribga Administration", "2024-03-15", "Responsable trésorerie - Documents trésorerie"),
        ("Samira Mansouri", "Actif", "Archives Finances - Khouribga Administration", "2024-04-01", "Responsable budget - Documents budgétaires"),
        ("Youssef Tazi", "Actif", "Archives Finances - Khouribga Administration", "2024-04-15", "Responsable audit - Documents audit"),
        
        # Dossiers actifs - Logistique
        ("Omar Bennani", "Actif", "Archives Logistique - Khouribga Technique", "2024-05-01", "Responsable approvisionnement - Documents approvisionnement"),
        ("Fatima El Khadiri", "Actif", "Archives Logistique - Khouribga Technique", "2024-05-15", "Responsable transport - Documents transport"),
        ("Rachid Mansouri", "Actif", "Archives Logistique - Khouribga Technique", "2024-06-01", "Responsable stock - Documents stock"),
        ("Amina Benali", "Actif", "Archives Logistique - Khouribga Technique", "2024-06-15", "Responsable maintenance préventive - Documents maintenance"),
        
        # Dossiers actifs - Communication
        ("Hassan El Fassi", "Actif", "Archives Communication - Khouribga Administration", "2024-07-01", "Responsable communication - Documents communication"),
        ("Nadia Benjelloun", "Actif", "Archives Communication - Khouribga Administration", "2024-07-15", "Responsable relations publiques - Documents RP"),
        ("Karim Mansouri", "Actif", "Archives Communication - Khouribga Administration", "2024-08-01", "Responsable événementiel - Documents événements"),
        ("Leila Tazi", "Actif", "Archives Communication - Khouribga Administration", "2024-08-15", "Responsable presse - Documents presse"),
        
        # Dossiers actifs - Recherche et Développement
        ("Samira Bennani", "Actif", "Archives R&D - Khouribga Technique", "2024-09-01", "Responsable R&D - Documents recherche"),
        ("Youssef El Khadiri", "Actif", "Archives R&D - Khouribga Technique", "2024-09-15", "Chef projet innovation - Documents innovation"),
        ("Omar Benali", "Actif", "Archives R&D - Khouribga Technique", "2024-10-01", "Responsable brevets - Documents brevets"),
        ("Fatima Mansouri", "Actif", "Archives R&D - Khouribga Technique", "2024-10-15", "Responsable partenariats - Documents partenariats"),
        
        # Dossiers actifs - Environnement
        ("Rachid El Fassi", "Actif", "Archives Environnement - Khouribga Technique", "2024-11-01", "Responsable environnement - Documents environnement"),
        ("Amina Benjelloun", "Actif", "Archives Environnement - Khouribga Technique", "2024-11-15", "Responsable développement durable - Documents DD"),
        ("Hassan Tazi", "Actif", "Archives Environnement - Khouribga Technique", "2024-12-01", "Responsable conformité - Documents conformité"),
        ("Nadia Mansouri", "Actif", "Archives Environnement - Khouribga Technique", "2024-12-15", "Responsable impact environnemental - Documents impact"),
        
        # Dossiers retraités récents
        ("Mohammed Benali", "Retraité", "Archives Historiques - Khouribga Administration", "2023-12-01", "Ancien directeur technique - Retraite 2023"),
        ("Fatima El Fassi", "Retraité", "Archives Historiques - Khouribga Administration", "2024-01-01", "Ancienne responsable RH - Retraite 2024"),
        ("Karim Benjelloun", "Retraité", "Archives Historiques - Khouribga Administration", "2024-02-01", "Ancien chef comptable - Retraite 2024"),
        ("Leila Mansouri", "Retraité", "Archives Historiques - Khouribga Administration", "2024-03-01", "Ancienne responsable communication - Retraite 2024"),
        
        # Dossiers spéciaux
        ("Ahmed Tazi", "Actif", "Archives Spéciales - Khouribga Administration", "2024-04-01", "Responsable archives confidentielles - Documents confidentiels"),
        ("Samira El Khadiri", "Actif", "Archives Spéciales - Khouribga Administration", "2024-04-15", "Responsable archives numériques - Documents numériques"),
        ("Youssef Bennani", "Actif", "Archives Spéciales - Khouribga Administration", "2024-05-01", "Responsable archives historiques - Documents historiques"),
        ("Omar Mansouri", "Actif", "Archives Spéciales - Khouribga Administration", "2024-05-15", "Responsable archives légales - Documents légaux"),
        
        # Dossiers internationaux
        ("Fatima Benali", "Actif", "Archives Internationales - Khouribga Administration", "2024-06-01", "Responsable relations internationales - Documents internationaux"),
        ("Rachid El Fassi", "Actif", "Archives Internationales - Khouribga Administration", "2024-06-15", "Responsable export - Documents export"),
        ("Amina Tazi", "Actif", "Archives Internationales - Khouribga Administration", "2024-07-01", "Responsable import - Documents import"),
        ("Hassan Benjelloun", "Actif", "Archives Internationales - Khouribga Administration", "2024-07-15", "Responsable partenariats internationaux - Documents partenariats"),
        
        # Dossiers formation
        ("Nadia Mansouri", "Actif", "Archives Formation - Khouribga Administration", "2024-08-01", "Responsable formation continue - Documents formation"),
        ("Karim El Khadiri", "Actif", "Archives Formation - Khouribga Administration", "2024-08-15", "Responsable apprentissage - Documents apprentissage"),
        ("Leila Benali", "Actif", "Archives Formation - Khouribga Administration", "2024-09-01", "Responsable développement compétences - Documents compétences"),
        ("Samira Tazi", "Actif", "Archives Formation - Khouribga Administration", "2024-09-15", "Responsable évaluation - Documents évaluation"),
        
        # Dossiers sécurité
        ("Youssef Bennani", "Actif", "Archives Sécurité - Khouribga Technique", "2024-10-01", "Responsable sécurité physique - Documents sécurité"),
        ("Omar El Fassi", "Actif", "Archives Sécurité - Khouribga Technique", "2024-10-15", "Responsable cybersécurité - Documents cybersécurité"),
        ("Fatima Mansouri", "Actif", "Archives Sécurité - Khouribga Technique", "2024-11-01", "Responsable prévention - Documents prévention"),
        ("Rachid Benjelloun", "Actif", "Archives Sécurité - Khouribga Technique", "2024-11-15", "Responsable contrôle accès - Documents contrôle"),
        
        # Dossiers qualité
        ("Amina El Khadiri", "Actif", "Archives Qualité - Khouribga Technique", "2024-12-01", "Responsable assurance qualité - Documents qualité"),
        ("Hassan Benali", "Actif", "Archives Qualité - Khouribga Technique", "2024-12-15", "Responsable certification - Documents certification"),
        ("Nadia Tazi", "Actif", "Archives Qualité - Khouribga Technique", "2025-01-01", "Responsable audit qualité - Documents audit"),
        ("Karim Mansouri", "Actif", "Archives Qualité - Khouribga Technique", "2025-01-15", "Responsable amélioration continue - Documents amélioration")
    ]
    
    try:
        # Ajouter les dossiers
        dossiers_ajoutes = 0
        for nom, etat, localisation, date_creation, commentaire in dossiers_supplementaires:
            try:
                db.ajouter_dossier(nom, etat, localisation, date_creation, commentaire)
                print(f"✅ Dossier ajouté : {nom}")
                dossiers_ajoutes += 1
            except Exception as e:
                print(f"❌ Erreur lors de l'ajout du dossier {nom}: {e}")
        
        print(f"\n🎉 Résumé :")
        print(f"- {dossiers_ajoutes} nouveaux dossiers ajoutés avec succès")
        print(f"- {len(dossiers_supplementaires) - dossiers_ajoutes} dossiers en erreur")
        
        # Afficher les statistiques par catégorie
        categories = {}
        for nom, etat, localisation, date_creation, commentaire in dossiers_supplementaires:
            if "Archives" in localisation:
                categorie = localisation.split(" - ")[0]
                categories[categorie] = categories.get(categorie, 0) + 1
        
        print(f"\n📊 Répartition par catégorie :")
        for categorie, count in categories.items():
            print(f"- {categorie}: {count} dossiers")
        
        # Afficher les statistiques par état
        etats = {}
        for nom, etat, localisation, date_creation, commentaire in dossiers_supplementaires:
            etats[etat] = etats.get(etat, 0) + 1
        
        print(f"\n📈 Répartition par état :")
        for etat, count in etats.items():
            print(f"- {etat}: {count} dossiers")
        
    except Exception as e:
        print(f"❌ Erreur générale lors de l'ajout des dossiers : {e}")

if __name__ == "__main__":
    print("🚀 Ajout de dossiers supplémentaires...")
    ajouter_plus_de_dossiers()
    print("\n✅ Script terminé !") 