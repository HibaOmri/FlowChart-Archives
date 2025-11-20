import db
from datetime import datetime

print("--- Test ajout utilisateur ---")
db.ajouter_utilisateur("Test User", "Agent", "test@example.com")

print("--- Test ajout dossier ---")
db.ajouter_dossier("Fatima Benhaddou", "Actif", "Bâtiment A", "2024-06-01", "Dossier test")

print("--- Liste des utilisateurs ---")
utilisateurs = db.lister_utilisateurs()
for u in utilisateurs:
    print(u)

print("--- Liste des dossiers ---")
dossiers = db.lister_dossiers()
for d in dossiers:
    print(d)

print("--- Test ajout mouvement ---")
# On suppose que le premier utilisateur et le premier dossier existent
db.ajouter_mouvement(1, 1, "Prise", remarques="Premier mouvement de test")

print("--- Historique des mouvements pour le dossier 1 ---")
hist = db.historique_mouvements(1)
for m in hist:
    print(m) 