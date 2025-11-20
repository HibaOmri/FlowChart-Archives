from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QHBoxLayout, QPushButton, QTextEdit, QComboBox, QDateTimeEdit, QMessageBox, QLineEdit, QDateEdit, QWidget
from PyQt5.QtCore import Qt, QDateTime, QDate
from PyQt5.QtGui import QColor
from .styles import STYLE_SHEET, TYPES_MOUVEMENTS
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '../backend'))
import db

class HistoriqueMouvementsDialog(QDialog):
    def __init__(self, id_dossier, nom_dossier, parent=None):
        super().__init__(parent)
        self.id_dossier = id_dossier
        self.setWindowTitle(f"📋 Historique des mouvements - {nom_dossier}")
        self.setModal(True)
        self.resize(800, 500)
        self.setStyleSheet(STYLE_SHEET)
        layout = QVBoxLayout()

        # Titre
        title_label = QLabel(f"📋 Historique des mouvements - {nom_dossier}")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-weight: bold; font-size: 16px; margin: 10px; color: #1976D2;")
        layout.addWidget(title_label)

        # Tableau des mouvements
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "📁 Dossier", "👤 Donné par", "👥 Donné à", "📅 Date", "📋 Motif", "📅 Retour prévu", "⚙️ Actions"
        ])
        
        # Ajuster les colonnes
        header = self.table.horizontalHeader()
        if header:
            header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Dossier
            header.setSectionResizeMode(1, QHeaderView.Stretch)  # Donné par
            header.setSectionResizeMode(2, QHeaderView.Stretch)  # Donné à
            header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Date
            header.setSectionResizeMode(4, QHeaderView.Stretch)  # Motif
            header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Retour prévu
            header.setSectionResizeMode(6, QHeaderView.Fixed)  # Actions
            header.resizeSection(6, 140)  # Largeur fixe pour Actions
        
        layout.addWidget(self.table)

        # Boutons
        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("➕ Ajouter un mouvement")
        self.btn_close = QPushButton("❌ Fermer")
        self.btn_add.setProperty("success", True)
        btn_layout.addWidget(self.btn_add)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_close)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        self.btn_add.clicked.connect(self.ajouter_mouvement)
        self.btn_close.clicked.connect(self.accept)

        # Connecter le clic sur la colonne Actions
        self.table.cellClicked.connect(self.on_cell_clicked)

        self.charger_mouvements()

    def charger_mouvements(self):
        mouvements = db.historique_mouvements(self.id_dossier)
        self.table.setRowCount(len(mouvements))
        for row, mouvement in enumerate(mouvements):
            # Structure des colonnes retournées par historique_mouvements :
            # id, id_dossier, id_utilisateur, type_mouvement, date_mouvement, 
            # date_retour_prevue, destinataire_nom, destinataire_fonction, motif, remarques, signature_utilisateur, nom_utilisateur
            
            # Dossier (numéro du dossier - colonne 1)
            numero_dossier = mouvement[1] if len(mouvement) > 1 else "N/A"
            self.table.setItem(row, 0, QTableWidgetItem(str(numero_dossier)))
            
            # Donné par (nom de l'utilisateur qui donne - dernière colonne)
            donne_par = mouvement[11] if len(mouvement) > 11 else "N/A"
            self.table.setItem(row, 1, QTableWidgetItem(str(donne_par)))
            
            # Donné à (destinataire - colonne 6)
            donne_a = mouvement[6] if len(mouvement) > 6 else "N/A"
            self.table.setItem(row, 2, QTableWidgetItem(str(donne_a)))
            
            # Date (colonne 4) - formater pour l'affichage
            date_mouvement = mouvement[4] if len(mouvement) > 4 else "N/A"
            if date_mouvement != "N/A":
                try:
                    from datetime import datetime
                    dt = datetime.strptime(str(date_mouvement), '%Y-%m-%d %H:%M:%S')
                    date_mouvement = dt.strftime('%d/%m/%Y')
                except:
                    pass
            self.table.setItem(row, 3, QTableWidgetItem(str(date_mouvement)))
            
            # Motif (colonne 8)
            motif = mouvement[8] if len(mouvement) > 8 else "N/A"
            self.table.setItem(row, 4, QTableWidgetItem(str(motif)))
            
            # Retour prévu (colonne 5)
            date_retour_prevue = mouvement[5] if len(mouvement) > 5 else "N/A"
            if date_retour_prevue != "N/A":
                try:
                    from datetime import datetime
                    dt = datetime.strptime(str(date_retour_prevue), '%Y-%m-%d')
                    date_retour_prevue = dt.strftime('%d/%m/%Y')
                except:
                    pass
            self.table.setItem(row, 5, QTableWidgetItem(str(date_retour_prevue)))
            
            # Actions : Statut simple avec couleur de fond
            id_mouvement = mouvement[0] if len(mouvement) > 0 else None
            
            # Vérifier si le mouvement a été retourné
            est_retourne = db.verifier_mouvement_retourne(id_mouvement) if id_mouvement else False
            
            if est_retourne:
                # Si retourné, afficher "Retour" en vert
                status_text = "Retour"
                status_color = "#4CAF50"  # Vert
            else:
                # Si pas retourné, afficher "Prise" en bleu
                status_text = "Prise"
                status_color = "#2196F3"  # Bleu
            
            # Créer un item de tableau avec couleur de fond
            action_item = QTableWidgetItem(status_text)
            action_item.setBackground(QColor(status_color))
            action_item.setForeground(QColor("white"))
            action_item.setTextAlignment(Qt.AlignCenter)
            
            # Stocker l'ID du mouvement dans les données de l'item
            action_item.setData(Qt.UserRole, id_mouvement)
            action_item.setData(Qt.UserRole + 1, est_retourne)
            
            self.table.setItem(row, 6, action_item)

    def on_cell_clicked(self, row, column):
        """Gère les clics sur les cellules du tableau."""
        if column == 6:  # Colonne Actions
            item = self.table.item(row, column)
            if item:
                id_mouvement = item.data(Qt.UserRole)
                est_retourne = item.data(Qt.UserRole + 1)
                
                if not est_retourne:
                    # Si pas retourné, proposer de marquer comme retourné
                    reply = QMessageBox.question(self, "📤 Confirmation de retour", 
                                               "Voulez-vous marquer ce dossier comme retourné ?\n\n"
                                               "Cette action enregistrera la date de retour effective.", 
                                               QMessageBox.Yes | QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        try:
                            db.marquer_mouvement_retourne(id_mouvement)
                            self.charger_mouvements()
                            QMessageBox.information(self, "✅ Succès", "Dossier marqué comme retourné avec succès !")
                        except Exception as e:
                            QMessageBox.warning(self, "❌ Erreur", f"Erreur lors du marquage du retour :\n{str(e)}")
                else:
                    # Si déjà retourné, proposer de supprimer
                    reply = QMessageBox.question(self, "⚠️ Confirmation", 
                                               "Ce dossier est déjà retourné.\n\n"
                                               "Voulez-vous supprimer ce mouvement ?\n\n"
                                               "Cette action est irréversible !", 
                                               QMessageBox.Yes | QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        try:
                            db.supprimer_mouvement(id_mouvement)
                            self.charger_mouvements()
                            QMessageBox.information(self, "✅ Succès", "Mouvement supprimé avec succès !")
                        except Exception as e:
                            QMessageBox.warning(self, "❌ Erreur", f"Erreur lors de la suppression :\n{str(e)}")

    def ajouter_mouvement(self):
        dialog = AjouterMouvementDialog(self.id_dossier, self)
        if dialog.exec_() == QDialog.Accepted:
            self.charger_mouvements()



class AjouterMouvementDialog(QDialog):
    def __init__(self, id_dossier, parent=None):
        super().__init__(parent)
        self.id_dossier = id_dossier
        self.setWindowTitle("➕ Ajouter un mouvement")
        self.setModal(True)
        self.setStyleSheet(STYLE_SHEET)
        layout = QVBoxLayout()

        # Titre
        title_label = QLabel("➕ Ajouter un nouveau mouvement")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-weight: bold; font-size: 16px; margin: 10px; color: #1976D2;")
        layout.addWidget(title_label)



        # Destinataire (employé OCP ou Autre)
        layout.addWidget(QLabel("👤 Destinataire du dossier :"))
        self.destinataire_input = QComboBox()
        self.destinataire_map = {}  # id_utilisateur -> (nom, fonction)
        self.charger_destinataires()
        self.destinataire_input.currentIndexChanged.connect(self.toggle_autre_destinataire)
        layout.addWidget(self.destinataire_input)

        # Champ pour nom/prénom si 'Autre'
        self.autre_nom_input = QLineEdit()
        self.autre_nom_input.setPlaceholderText("Nom et prénom du destinataire externe")
        self.autre_nom_input.setVisible(False)
        layout.addWidget(self.autre_nom_input)

        # Motif du mouvement
        self.motif_input = QLineEdit()
        self.motif_input.setPlaceholderText("Motif de la demande (ex: Audit interne, Consultation, etc.)")
        layout.addWidget(QLabel("📋 Motif :"))
        layout.addWidget(self.motif_input)

        # Date de retour prévue
        self.date_retour_input = QDateEdit()
        self.date_retour_input.setCalendarPopup(True)
        self.date_retour_input.setDate(QDate.currentDate().addDays(7))  # Par défaut +7 jours
        layout.addWidget(QLabel("📅 Date de retour prévue :"))
        layout.addWidget(self.date_retour_input)

        # Date et heure du mouvement
        self.date_input = QDateTimeEdit()
        self.date_input.setDateTime(QDateTime.currentDateTime())
        self.date_input.setCalendarPopup(True)
        layout.addWidget(QLabel("📅 Date et heure du mouvement :"))
        layout.addWidget(self.date_input)

        # Remarques
        self.remarques_input = QTextEdit()
        self.remarques_input.setMaximumHeight(100)
        self.remarques_input.setPlaceholderText("Remarques supplémentaires...")
        layout.addWidget(QLabel("💬 Remarques :"))
        layout.addWidget(self.remarques_input)

        # Boutons
        btn_layout = QHBoxLayout()
        self.btn_ok = QPushButton("✅ Ajouter")
        self.btn_cancel = QPushButton("❌ Annuler")
        self.btn_ok.setProperty("success", True)
        self.btn_cancel.setProperty("warning", True)
        btn_layout.addWidget(self.btn_ok)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        self.btn_ok.clicked.connect(self.ajouter_mouvement)
        self.btn_cancel.clicked.connect(self.reject)

    def charger_destinataires(self):
        self.destinataire_input.clear()
        self.destinataire_map = {}
        
        # Liste des destinataires autorisés (personnes qui peuvent recevoir des dossiers)
        destinataires_autorises = [
            # Chefs de départements
            ("Chef du département juridique", "Chef Département Juridique"),
            ("Chef du département logistique", "Chef Département Logistique"),
            ("Chef du département production", "Chef Département Production"),
            ("Chef du département maintenance", "Chef Département Maintenance"),
            ("Chef du département sécurité", "Chef Département Sécurité"),
            ("Chef du département environnement", "Chef Département Environnement"),
            ("Chef du département qualité", "Chef Département Qualité"),
            ("Chef du département finances", "Chef Département Finances"),
            ("Chef du département informatique", "Chef Département Informatique"),
            
            # Assistants de direction
            ("Assistant directeur général", "Assistant Direction Générale"),
            ("Assistant directeur technique", "Assistant Direction Technique"),
            ("Assistant directeur administratif", "Assistant Direction Administrative"),
            ("Assistant directeur commercial", "Assistant Direction Commerciale"),
            ("Assistant directeur RH", "Assistant Direction RH"),
            
            # Employés autorisés par RH (avec validation)
            ("Employé autorisé - Audit interne", "Employé Audit"),
            ("Employé autorisé - Contrôle qualité", "Employé Contrôle"),
            ("Employé autorisé - Formation", "Employé Formation"),
            ("Employé autorisé - Sécurité", "Employé Sécurité"),
            ("Employé autorisé - Maintenance", "Employé Maintenance"),
            ("Employé autorisé - Logistique", "Employé Logistique"),
            ("Employé autorisé - Juridique", "Employé Juridique"),
            ("Employé autorisé - Finances", "Employé Finances"),
            ("Employé autorisé - Informatique", "Employé Informatique"),
            ("Employé autorisé - Environnement", "Employé Environnement"),
        ]
        
        # Ajouter les destinataires autorisés
        for nom, fonction in destinataires_autorises:
            self.destinataire_input.addItem(f"{nom} ({fonction})", nom)
            self.destinataire_map[nom] = (nom, fonction)
        
        # Ajouter l'option "Autre" pour les cas spéciaux
        self.destinataire_input.addItem("Autre (préciser)", -1)

    def toggle_autre_destinataire(self):
        if self.destinataire_input.currentData() == -1:
            self.autre_nom_input.setVisible(True)
        else:
            self.autre_nom_input.setVisible(False)

    def get_data(self):
        destinataire_id = self.destinataire_input.currentData()
        destinataire_nom = None
        destinataire_fonction = None
        if destinataire_id == -1:
            destinataire_nom = self.autre_nom_input.text().strip()
            destinataire_fonction = "Externe"
        else:
            destinataire_nom, destinataire_fonction = self.destinataire_map.get(destinataire_id, ("", ""))
        
        return (
            self.id_dossier,
            destinataire_id,
            self.motif_input.text().strip(),
            self.date_input.dateTime().toString("yyyy-MM-dd hh:mm:ss"),
            self.date_retour_input.date().toString("yyyy-MM-dd"),
            destinataire_nom,
            destinataire_fonction,
            self.remarques_input.toPlainText()
        )

    def ajouter_mouvement(self):
        id_dossier, destinataire_id, motif, date_mouvement, date_retour_prevue, destinataire_nom, destinataire_fonction, remarques = self.get_data()
        
        if not motif:
            QMessageBox.warning(self, "⚠️ Erreur", "Veuillez saisir le motif du mouvement.")
            return
        
        if destinataire_id == -1 and not destinataire_nom:
            QMessageBox.warning(self, "⚠️ Erreur", "Veuillez saisir le nom et prénom du destinataire externe.")
            return
        
        # Pour l'instant, on utilise un id_utilisateur par défaut (l'utilisateur connecté)
        # TODO: Récupérer l'id de l'utilisateur connecté
        id_utilisateur = 1  # Temporaire
        
        # Utiliser le motif comme type de mouvement (plus simple)
        type_mouvement = "Transfert"  # Par défaut
        
        try:
            db.ajouter_mouvement(id_dossier, id_utilisateur, type_mouvement, motif, date_mouvement, date_retour_prevue, destinataire_nom, destinataire_fonction, remarques)
            QMessageBox.information(self, "✅ Succès", f"Mouvement ajouté avec succès !")
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, "❌ Erreur", f"Erreur lors de l'ajout du mouvement :\n{str(e)}") 