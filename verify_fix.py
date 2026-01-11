
import sys
import os
import datetime

# Setup path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))
import db

print("--- VERIFY FIX START ---")
try:
    # 1. Get a valid dossier ID
    dossier = db.get_db().query_single("MATCH (d:Dossier) RETURN d.id LIMIT 1")
    if not dossier:
        print("No dossier found! Creating one...")
        db.get_db().query("CREATE (d:Dossier {id: 1, nom_personne: 'SystemTest'})")
        did = 1
    else:
        did = dossier[0]
    
    print(f"Using Dossier ID: {did}")

    # 2. Insert Movement
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Inserting movement at {ts}...")
    
    mid = db.ajouter_mouvement(
        id_dossier=did,
        id_utilisateur=1, 
        type_mouvement='VERIFY',
        motif='VERIFY_LOGIC',
        date_mouvement=ts,
        date_retour_prevue='2030-01-01',
        destinataire_nom='Verifier',
        destinataire_fonction='Bot',
        remarques='Auto',
        signature_utilisateur=None # Should become ""
    )
    print(f"Inserted ID: {mid}")

    # 3. Check List
    print("Checking list...")
    lst = db.historique_mouvements(did)
    found = False
    for r in lst:
        if r[0] == mid:
            found = True
            print(f"✅ FOUND Movement {mid}. Date: {r[4]}")
            # Check signature
            sig = r[10] # 10 is signature
            print(f"   Signature: '{sig}'")
            break
            
    if not found:
        print("❌ CRITICAL: Movement NOT found in list.")
    else:
        print("✅ SUCCESS: Logic is working.")

except Exception as e:
    print(f"❌ ERROR: {e}")
print("--- VERIFY FIX END ---")
