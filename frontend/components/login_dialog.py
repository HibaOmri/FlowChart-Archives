import sys
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QPushButton, QMessageBox, QFrame, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from .styles import STYLE_SHEET
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '../backend'))
import db

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🔐 Connexion - SGAU")
        self.setModal(True)
        self.setFixedSize(450, 600)
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
            }
        """)
        
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(0)
        
        # Carte de connexion
        login_card = QFrame()
        login_card.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 15px;
            }
        """)
        login_layout = QVBoxLayout()
        login_layout.setContentsMargins(30, 30, 30, 30)
        login_layout.setSpacing(20)
        
        # Titre principal
        title_label = QLabel("Système de Gestion d'Archives")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-weight: bold;
            font-size: 20px;
            color: #2c3e50;
            margin-bottom: 5px;
        """)
        login_layout.addWidget(title_label)
        
        # Sous-titre
        subtitle_label = QLabel("Connexion")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("""
            font-size: 14px;
            color: #7f8c8d;
            margin-bottom: 25px;
        """)
        login_layout.addWidget(subtitle_label)
        
        # Nom d'utilisateur
        username_label = QLabel("Nom d'utilisateur")
        username_label.setStyleSheet("""
            font-weight: bold;
            font-size: 13px;
            color: #2c3e50;
        """)
        login_layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Entrez votre nom d'utilisateur")
        self.username_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #bdc3c7;
                border-radius: 8px;
                padding: 10px 12px;
                font-size: 13px;
                background: white;
                color: #2c3e50;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        login_layout.addWidget(self.username_input)
        
        # Numéro de matricule
        matricule_label = QLabel("Numéro de matricule")
        matricule_label.setStyleSheet("""
            font-weight: bold;
            font-size: 13px;
            color: #2c3e50;
        """)
        login_layout.addWidget(matricule_label)
        
        self.matricule_input = QLineEdit()
        self.matricule_input.setPlaceholderText("Ex: EMP001")
        self.matricule_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #bdc3c7;
                border-radius: 8px;
                padding: 10px 12px;
                font-size: 13px;
                background: white;
                color: #2c3e50;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        login_layout.addWidget(self.matricule_input)
        
        # Message d'aide
        help_label = QLabel("Nouvel utilisateur ? Contactez l'administrateur pour obtenir vos identifiants.")
        help_label.setStyleSheet("""
            color: #95a5a6;
            font-size: 11px;
            font-style: italic;
            padding: 8px;
            background: #f8f9fa;
            border-radius: 6px;
            border: 1px solid #ecf0f1;
        """)
        help_label.setWordWrap(True)
        help_label.setAlignment(Qt.AlignCenter)
        login_layout.addWidget(help_label)
        
        # Bouton de connexion
        self.btn_login = QPushButton("Se connecter")
        self.btn_login.setStyleSheet("""
            QPushButton {
                background: #3498db;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
                color: white;
            }
            QPushButton:hover {
                background: #2980b9;
            }
            QPushButton:pressed {
                background: #1f5f8b;
            }
        """)
        login_layout.addWidget(self.btn_login)
        
        # Bouton annuler
        self.btn_cancel = QPushButton("Annuler")
        self.btn_cancel.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: 1px solid #e74c3c;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
                font-weight: bold;
                color: #e74c3c;
            }
            QPushButton:hover {
                background: #e74c3c;
                color: white;
            }
        """)
        login_layout.addWidget(self.btn_cancel)
        
        login_card.setLayout(login_layout)
        main_layout.addWidget(login_card)
        
        self.setLayout(main_layout)

        self.btn_login.clicked.connect(self.try_login)
        self.btn_cancel.clicked.connect(self.reject)
        self.matricule_input.returnPressed.connect(self.try_login)

        self.current_user = None

    def try_login(self):
        username = self.username_input.text().strip()
        matricule = self.matricule_input.text().strip()
        
        if not username or not matricule:
            QMessageBox.warning(self, "⚠️ Erreur", "Veuillez remplir tous les champs.\n\nNom d'utilisateur et numéro de matricule sont requis.")
            return
        
        try:
            # Vérifier l'authentification avec le matricule
            user_data = db.verifier_authentification(username, matricule)
            
            if user_data:
                self.current_user = user_data
                QMessageBox.information(self, "✅ Connexion réussie", 
                    f"Bienvenue, {user_data['nom']} !\n\n"
                    f"👤 Utilisateur: {user_data['username']}\n"
                    f"🆔 Matricule: {user_data['matricule']}\n"
                    f"💼 Fonction: {user_data['fonction']}\n\n"
                    f"Vous êtes maintenant connecté au système.")
                self.accept()
            else:
                # Vérifier si l'utilisateur existe mais n'a pas de compte
                self.verifier_utilisateur_sans_compte(username)
                
        except Exception as e:
            QMessageBox.warning(self, "❌ Erreur", f"Erreur lors de la connexion :\n{str(e)}")

    def verifier_utilisateur_sans_compte(self, username):
        """Vérifie si l'utilisateur existe mais n'a pas encore de compte"""
        try:
            utilisateurs = db.lister_utilisateurs()
            for utilisateur in utilisateurs:
                if utilisateur[1] == username:  # Nom d'utilisateur trouvé
                    reply = QMessageBox.question(self, "🆕 Nouvel utilisateur détecté", 
                        f"L'utilisateur '{username}' existe mais n'a pas encore de compte.\n\n"
                        f"Voulez-vous créer un compte maintenant ?\n\n"
                        f"Un numéro de matricule sera généré automatiquement.",
                        QMessageBox.Yes | QMessageBox.No)
                    
                    if reply == QMessageBox.Yes:
                        self.creer_compte_utilisateur(utilisateur[0], username)
                    return
            
            # Si on arrive ici, l'utilisateur n'existe pas du tout
            QMessageBox.warning(self, "❌ Utilisateur non trouvé", 
                f"L'utilisateur '{username}' n'existe pas dans le système.\n\n"
                f"Veuillez vérifier le nom d'utilisateur ou contacter l'administrateur.")
                
        except Exception as e:
            QMessageBox.warning(self, "❌ Erreur", f"Erreur lors de la vérification :\n{str(e)}")

    def creer_compte_utilisateur(self, id_utilisateur, username):
        """Crée un compte pour un utilisateur existant"""
        try:
            # Générer un matricule automatiquement
            matricule = db.generer_matricule_auto()
            
            # Créer le compte
            success = db.creer_compte_utilisateur(id_utilisateur, username, matricule)
            
            if success:
                QMessageBox.information(self, "✅ Compte créé", 
                    f"Compte créé avec succès pour '{username}' !\n\n"
                    f"🆔 Votre numéro de matricule: {matricule}\n\n"
                    f"Vous pouvez maintenant vous connecter avec ces identifiants.")
                
                # Pré-remplir les champs
                self.matricule_input.setText(matricule)
            else:
                QMessageBox.warning(self, "❌ Erreur", 
                    "Impossible de créer le compte.\n"
                    "Le nom d'utilisateur ou le matricule existe peut-être déjà.")
                
        except Exception as e:
            QMessageBox.warning(self, "❌ Erreur", f"Erreur lors de la création du compte :\n{str(e)}")

    def get_current_user(self):
        return self.current_user

    def get_credentials(self):
        username = self.username_input.text().strip()
        matricule = self.matricule_input.text().strip()
        return username, matricule 