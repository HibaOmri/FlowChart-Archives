from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QHBoxLayout, QPushButton, QLineEdit, QFrame, QComboBox, QTextEdit, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from .styles import STYLE_SHEET
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '../backend'))
import db

class GestionUtilisateursDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("👥 Gestion des utilisateurs")
        self.setModal(True)
        self.resize(900, 600)
        self.setStyleSheet(STYLE_SHEET)
        layout = QVBoxLayout()

        # Titre
        title_label = QLabel("👥 Gestion des utilisateurs")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-weight: bold; font-size: 18px; margin: 10px; color: #1976D2;")
        layout.addWidget(title_label)

        # Tableau des utilisateurs
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "🆔 ID", "👤 Nom", "💼 Fonction", "🔑 Rôle", "📞 Contact", "🆔 Compte"
        ])
        
        # Ajuster les colonnes
        header = self.table.horizontalHeader()
        if header:
            header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # ID
            header.setSectionResizeMode(1, QHeaderView.Stretch)  # Nom
            header.setSectionResizeMode(2, QHeaderView.Stretch)  # Fonction
            header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Rôle
            header.setSectionResizeMode(4, QHeaderView.Stretch)  # Contact
            header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Compte
        
        layout.addWidget(self.table)

        # Boutons
        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("➕ Ajouter un utilisateur")
        self.btn_edit = QPushButton("✏️ Modifier l'utilisateur sélectionné")
        self.btn_delete = QPushButton("🗑️ Supprimer l'utilisateur sélectionné")
        self.btn_close = QPushButton("❌ Fermer")
        self.btn_add.setProperty("success", True)
        self.btn_edit.setProperty("success", True)
        self.btn_delete.setProperty("warning", True)
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_edit)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_close)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        self.btn_add.clicked.connect(self.ajouter_utilisateur)
        self.btn_edit.clicked.connect(self.modifier_utilisateur)
        self.btn_delete.clicked.connect(self.supprimer_utilisateur)
        self.btn_close.clicked.connect(self.accept)

        self.charger_utilisateurs()

    def charger_utilisateurs(self):
        try:
            utilisateurs = db.lister_utilisateurs()
            self.table.setRowCount(len(utilisateurs))
            for row, utilisateur in enumerate(utilisateurs):
                # ID, Nom, Fonction, Rôle, Contact
                for col in range(4):  # Les 4 premières colonnes
                    value = utilisateur[col] if col < len(utilisateur) else ""
                    self.table.setItem(row, col, QTableWidgetItem(str(value)))
                
                # Contact (colonne 5)
                contact = utilisateur[3] if len(utilisateur) > 3 else ""
                self.table.setItem(row, 4, QTableWidgetItem(str(contact)))
                
                # Colonne statut du compte (colonne 6)
                id_utilisateur = utilisateur[0]
                has_account = not db.verifier_utilisateur_sans_compte(id_utilisateur)
                
                status_item = QTableWidgetItem()
                if has_account:
                    status_item.setText("✅ Actif")
                    status_item.setBackground(QColor(200, 255, 200))  # Vert clair
                else:
                    status_item.setText("❌ Aucun")
                    status_item.setBackground(QColor(255, 200, 200))  # Rouge clair
                
                self.table.setItem(row, 5, status_item)
        except Exception as e:
            QMessageBox.warning(self, "❌ Erreur", f"Impossible de charger les utilisateurs :\n{str(e)}")

    def ajouter_utilisateur(self):
        dialog = UtilisateurDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            nom, fonction, contact, username, matricule, role = dialog.get_data()
            if nom and fonction:
                try:
                    # Ajouter l'utilisateur avec le rôle
                    id_utilisateur = db.ajouter_utilisateur(nom, fonction, contact, role)
                    
                    # Créer le compte si un nom d'utilisateur est fourni
                    if username:
                        # Générer un matricule automatiquement si non fourni
                        if not matricule:
                            matricule = db.generer_matricule_auto()
                        
                        # Créer le compte
                        success = db.creer_compte_utilisateur(id_utilisateur, username, matricule)
                        
                        if success:
                            QMessageBox.information(self, "✅ Succès", 
                                f"Utilisateur '{nom}' ajouté avec succès !\n\n"
                                f"🆔 Compte créé automatiquement :\n"
                                f"👤 Nom d'utilisateur: {username}\n"
                                f"🆔 Matricule: {matricule}")
                        else:
                            QMessageBox.warning(self, "⚠️ Attention", 
                                f"Utilisateur '{nom}' ajouté mais impossible de créer le compte.\n"
                                f"Le nom d'utilisateur ou matricule existe peut-être déjà.")
                    else:
                        QMessageBox.information(self, "✅ Succès", 
                            f"Utilisateur '{nom}' ajouté avec succès !\n\n"
                            f"💡 Aucun compte créé. L'utilisateur pourra en créer un lors de sa première connexion.")
                    
                    self.charger_utilisateurs()
                except Exception as e:
                    QMessageBox.warning(self, "❌ Erreur", f"Erreur lors de l'ajout :\n{str(e)}")
            else:
                QMessageBox.warning(self, "⚠️ Erreur", "Veuillez remplir le nom et la fonction.")

    def modifier_utilisateur(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "⚠️ Aucune sélection", "Veuillez sélectionner un utilisateur à modifier.")
            return
        
        id_item = self.table.item(row, 0)
        nom_item = self.table.item(row, 1)
        fonction_item = self.table.item(row, 2)
        role_item = self.table.item(row, 3)
        contact_item = self.table.item(row, 4)
        
        if not id_item:
            QMessageBox.warning(self, "❌ Erreur", "Impossible de récupérer l'identifiant de l'utilisateur.")
            return
        
        id_utilisateur = int(id_item.text())
        
        # Pré-remplir la boîte de dialogue
        dialog = UtilisateurDialog(self)
        dialog.setWindowTitle("✏️ Modifier l'utilisateur")
        dialog.nom_input.setText(nom_item.text() if nom_item else "")
        dialog.fonction_input.setText(fonction_item.text() if fonction_item else "")
        dialog.contact_input.setText(contact_item.text() if contact_item else "")
        
        # Pré-remplir le rôle
        role_text = role_item.text() if role_item else "Archiviste"
        index = dialog.role_input.findText(role_text)
        if index >= 0:
            dialog.role_input.setCurrentIndex(index)
        
        # Vérifier si l'utilisateur a déjà un compte
        has_account = not db.verifier_utilisateur_sans_compte(id_utilisateur)
        if has_account:
            dialog.username_input.setEnabled(False)
            dialog.matricule_input.setEnabled(False)
            dialog.username_input.setPlaceholderText("Compte existant - non modifiable")
            dialog.matricule_input.setPlaceholderText("Compte existant - non modifiable")
        
        if dialog.exec_() == QDialog.Accepted:
            nom, fonction, contact, username, matricule, role = dialog.get_data()
            if nom and fonction:
                try:
                    db.modifier_utilisateur(id_utilisateur, nom, fonction, contact, role)
                    QMessageBox.information(self, "✅ Succès", f"Utilisateur '{nom}' modifié avec succès !")
                    self.charger_utilisateurs()
                except Exception as e:
                    QMessageBox.warning(self, "❌ Erreur", f"Erreur lors de la modification :\n{str(e)}")
            else:
                QMessageBox.warning(self, "⚠️ Erreur", "Veuillez remplir le nom et la fonction.")

    def supprimer_utilisateur(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "⚠️ Aucune sélection", "Veuillez sélectionner un utilisateur à supprimer.")
            return
        
        id_item = self.table.item(row, 0)
        nom_item = self.table.item(row, 1)
        
        if not id_item:
            QMessageBox.warning(self, "❌ Erreur", "Impossible de récupérer l'identifiant de l'utilisateur.")
            return
        
        id_utilisateur = int(id_item.text())
        nom_utilisateur = nom_item.text() if nom_item else f"ID {id_utilisateur}"
        
        reply = QMessageBox.question(self, "⚠️ Confirmation", 
                                   f"Voulez-vous vraiment supprimer l'utilisateur '{nom_utilisateur}' ?\n\nCette action est irréversible !", 
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                db.supprimer_utilisateur(id_utilisateur)
                QMessageBox.information(self, "✅ Succès", f"Utilisateur '{nom_utilisateur}' supprimé avec succès !")
                self.charger_utilisateurs()
            except Exception as e:
                QMessageBox.warning(self, "❌ Erreur", f"Erreur lors de la suppression :\n{str(e)}")

class UtilisateurDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("👤 Utilisateur")
        self.setModal(True)
        self.setStyleSheet(STYLE_SHEET)
        layout = QVBoxLayout()

        # Titre
        title_label = QLabel("👤 Informations utilisateur")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-weight: bold; font-size: 16px; margin: 10px; color: #1976D2;")
        layout.addWidget(title_label)

        self.nom_input = QLineEdit()
        self.nom_input.setPlaceholderText("Entrez le nom complet")
        self.fonction_input = QLineEdit()
        self.fonction_input.setPlaceholderText("Entrez la fonction/le poste")
        self.contact_input = QLineEdit()
        self.contact_input.setPlaceholderText("Entrez les informations de contact")

        layout.addWidget(QLabel("👤 Nom complet :"))
        layout.addWidget(self.nom_input)
        layout.addWidget(QLabel("💼 Fonction :"))
        layout.addWidget(self.fonction_input)
        layout.addWidget(QLabel("📞 Contact :"))
        layout.addWidget(self.contact_input)

        # Champ rôle limité à RH et Archiviste
        layout.addWidget(QLabel("🔑 Rôle :"))
        self.role_input = QComboBox()
        self.role_input.addItems(["RH", "Archiviste"])
        layout.addWidget(self.role_input)
        
        # Message d'information sur les rôles
        role_info = QLabel("💡 Seuls les rôles 'RH' et 'Archiviste' sont autorisés pour la gestion des dossiers.")
        role_info.setStyleSheet("color: #1976D2; font-size: 11px; font-style: italic; margin: 5px;")
        role_info.setWordWrap(True)
        layout.addWidget(role_info)

        # Séparateur
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator)

        # Section compte
        compte_label = QLabel("🆔 Création du compte")
        compte_label.setStyleSheet("font-weight: bold; color: #1976D2; margin-top: 10px;")
        layout.addWidget(compte_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nom d'utilisateur pour la connexion")
        layout.addWidget(QLabel("👤 Nom d'utilisateur :"))
        layout.addWidget(self.username_input)

        self.matricule_input = QLineEdit()
        self.matricule_input.setPlaceholderText("Numéro de matricule (ex: EMP001) ou laissez vide pour auto-génération")
        layout.addWidget(QLabel("🆔 Numéro de matricule :"))
        layout.addWidget(self.matricule_input)

        # Message d'aide
        help_label = QLabel("💡 Le compte sera créé automatiquement avec ces identifiants.")
        help_label.setStyleSheet("color: #666; font-size: 11px; font-style: italic; margin: 5px;")
        help_label.setWordWrap(True)
        layout.addWidget(help_label)

        btn_layout = QHBoxLayout()
        self.btn_ok = QPushButton("✅ OK")
        self.btn_cancel = QPushButton("❌ Annuler")
        self.btn_ok.setProperty("success", True)
        self.btn_cancel.setProperty("warning", True)
        btn_layout.addWidget(self.btn_ok)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        self.btn_ok.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)

    def get_data(self):
        return (
            self.nom_input.text(),
            self.fonction_input.text(),
            self.contact_input.text(),
            self.username_input.text(),
            self.matricule_input.text(),
            self.role_input.currentText()
        ) 