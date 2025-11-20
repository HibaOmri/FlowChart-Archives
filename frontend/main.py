import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from components.login_dialog import LoginDialog
from components.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    login_dialog = LoginDialog()
    if login_dialog.exec_() == 1:
        username, matricule = login_dialog.get_credentials()
        import os
        sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../backend'))
        import db
        user_info = db.verifier_authentification(username, matricule)
        if user_info:
            window = MainWindow(user_info)
            window.show()
            sys.exit(app.exec_())
        else:
            QMessageBox.critical(None, "❌ Erreur de connexion", 
                "Nom d'utilisateur ou matricule incorrect.\n\nComptes de test :\n• marie.martin / EMP001 (RH)\n• jean.dupont / EMP002 (Archiviste)\n• ahmed.hassan / EMP003 (Archiviste)")
            sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main() 