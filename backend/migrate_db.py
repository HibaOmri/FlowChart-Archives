#!/usr/bin/env python3
"""
Script de migration pour mettre à jour les rôles utilisateurs
Remplace tous les anciens rôles par 'RH' ou 'Archiviste'
"""

import sqlite3
import os

def migrate_roles():
    """Migre les rôles utilisateurs vers les nouveaux rôles autorisés"""
    
    # Chemin vers la base de données
    db_path = os.path.join(os.path.dirname(__file__), 'archives.db')
    
    if not os.path.exists(db_path):
        print("❌ Base de données non trouvée. Veuillez d'abord initialiser la base de données.")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Mapping des anciens rôles vers les nouveaux
        role_mapping = {
            'Admin': 'RH',
            'Archiviste_Principal': 'Archiviste',
            'Assistant': 'Archiviste',
            'Consultant': 'Archiviste'
        }
        
        # Récupérer tous les utilisateurs
        cursor.execute("SELECT id, nom, role FROM utilisateurs")
        utilisateurs = cursor.fetchall()
        
        print(f"📋 Migration des rôles pour {len(utilisateurs)} utilisateurs...")
        
        updated_count = 0
        for id_utilisateur, nom, role in utilisateurs:
            if role in role_mapping:
                nouveau_role = role_mapping[role]
                cursor.execute("UPDATE utilisateurs SET role = ? WHERE id = ?", (nouveau_role, id_utilisateur))
                print(f"✅ {nom}: {role} → {nouveau_role}")
                updated_count += 1
            elif role not in ['RH', 'Archiviste']:
                # Rôle inconnu, le convertir en Archiviste par défaut
                cursor.execute("UPDATE utilisateurs SET role = ? WHERE id = ?", ('Archiviste', id_utilisateur))
                print(f"⚠️ {nom}: {role} → Archiviste (rôle inconnu)")
                updated_count += 1
            else:
                print(f"ℹ️ {nom}: {role} (déjà correct)")
        
        conn.commit()
        print(f"\n✅ Migration terminée ! {updated_count} utilisateurs mis à jour.")
        
        # Afficher le résumé final
        cursor.execute("SELECT role, COUNT(*) FROM utilisateurs GROUP BY role")
        roles_finaux = cursor.fetchall()
        
        print("\n📊 Répartition finale des rôles :")
        for role, count in roles_finaux:
            print(f"• {role}: {count} utilisateur(s)")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la migration : {e}")
        return False

if __name__ == "__main__":
    print("🔄 Migration des rôles utilisateurs...")
    print("Anciens rôles → Nouveaux rôles :")
    print("• Admin → RH")
    print("• Archiviste_Principal → Archiviste")
    print("• Assistant → Archiviste")
    print("• Consultant → Archiviste")
    print("• RH → RH (inchangé)")
    print("• Archiviste → Archiviste (inchangé)")
    print()
    
    success = migrate_roles()
    if success:
        print("\n🎉 Migration réussie !")
    else:
        print("\n💥 Migration échouée !") 