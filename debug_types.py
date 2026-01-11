
import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'backend'))
import db

def check_types():
    print("Checking Dossier ID types...")
    dossiers = db.get_db().query("MATCH (d:Dossier) RETURN d.id LIMIT 5")
    for d in dossiers:
        val = d[0]
        print(f"Value: {val}, Type: {type(val)}")

    print("\nChecking Mouvement creation logic...")
    # Try to simulate the match used in ajouter_mouvement
    # Pick the first ID found
    if dossiers:
        first_id = dossiers[0][0]
        print(f"Testing MATCH with ID: {first_id} (Type: {type(first_id)})")
        
        # Test exact match
        query = "MATCH (d:Dossier {id: $did}) RETURN d"
        res = db.get_db().query(query, {'did': first_id})
        print(f"Match with original type result count: {len(res)}")
        
        # Test forced int
        try:
            int_id = int(first_id)
            res_int = db.get_db().query(query, {'did': int_id})
            print(f"Match with INT cast result count: {len(res_int)}")
        except:
            print("Cannot cast to int")
            
        # Test forced str
        str_id = str(first_id)
        res_str = db.get_db().query(query, {'did': str_id})
        print(f"Match with STR cast result count: {len(res_str)}")

if __name__ == "__main__":
    check_types()
