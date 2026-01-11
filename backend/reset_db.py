
import db

def reset_database():
    print("🗑️  Suppression complète de la base de données...")
    try:
        # Supprimer tous les noeuds et les relations
        db.get_db().query("MATCH (n) DETACH DELETE n")
        print("✅ Base de données vidée avec succès.")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la suppression : {e}")
        return False

if __name__ == "__main__":
    confirm = input("ATTENTION : Cela va supprimer TOUTES les données de Neo4j. Continuer ? (o/n) ")
    if confirm.lower() == 'o':
        reset_database()
