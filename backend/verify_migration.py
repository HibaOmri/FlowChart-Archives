
import sys
import os
import json

# Add backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from db import (
        ajouter_dossier, lister_dossiers, obtenir_dossier_par_id,
        ajouter_utilisateur, lister_utilisateurs,
        ajouter_mouvement, historique_mouvements,
        get_db
    )
    from init_db import init_db
except ImportError as e:
    print(f"CRITICAL: Could not import backend modules. Make sure you are running from the backend directory or correct path. {e}")
    sys.exit(1)

def test_migration():
    print("--- 1. Initializing DB ---")
    try:
        init_db()
        print("PASS: init_db executed.")
    except Exception as e:
        print(f"FAIL: init_db raised {e}")
        return

    print("\n--- 2. Testing Users ---")
    try:
        # Add User
        uid = ajouter_utilisateur("Test User", "Tester", "test@test.com", "Archiviste")
        print(f"PASS: User added with ID {uid} (Type: {type(uid)})")
        
        # List Users
        users = lister_utilisateurs()
        print(f"Users found: {len(users)}")
        if isinstance(users, list) and (len(users) == 0 or isinstance(users[0], (list, tuple))):
            print("PASS: lister_utilisateurs returns list of tuples/lists")
        else:
            print(f"FAIL: lister_utilisateurs returned {type(users)} with elements {type(users[0]) if users else 'unknown'}")
            
    except Exception as e:
        print(f"FAIL: User operations raised {e}")
        # import traceback
        # traceback.print_exc()

    print("\n--- 3. Testing Dossiers ---")
    try:
        # Add Dossier
        did = ajouter_dossier("Jean Dupont", "Actif", "B12", "2024-01-01")
        print(f"PASS: Dossier added with ID {did}")

        # Get Dossier
        d = obtenir_dossier_par_id(did)
        if d and isinstance(d, (list, tuple)):
             print(f"PASS: obtenir_dossier_par_id returns tuple/list: {d}")
        else:
             print(f"FAIL: Invalid dossier return format: {d}")

    except Exception as e:
        print(f"FAIL: Dossier operations raised {e}")

    print("\n--- 4. Testing Mouvements ---")
    try:
        mid = ajouter_mouvement(did, uid, "Prise", "Consultation")
        print(f"PASS: Mouvement added with ID {mid}")

        hist = historique_mouvements(did)
        print(f"History length: {len(hist)}")
        if len(hist) > 0:
            print(f"PASS: History retrieved. First item: {hist[0]}")
        else:
            print("WARN: History empty?")

    except Exception as e:
        print(f"FAIL: Mouvement operations raised {e}")
        
    print("\n--- Verification Complete ---")

if __name__ == "__main__":
    test_migration()
