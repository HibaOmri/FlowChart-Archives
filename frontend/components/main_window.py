from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox, QComboBox, QFrame, QGridLayout
from PyQt5.QtCore import Qt, QDate
from .styles import STYLE_SHEET
from .add_dossier_dialog import AddDossierDialog
from .gestion_utilisateurs import GestionUtilisateursDialog
from .historique_mouvements import HistoriqueMouvementsDialog
from .gestion_pieces_jointes import GestionPiecesJointesDialog
import os
import sys
import shutil
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '../backend'))
import db

class MainWindow(QMainWindow):
    def __init__(self, user_info=None):
        super().__init__()
        self.user_info = user_info or {
            'nom': 'Utilisateur Test',
            'role': 'Archiviste',
            'permissions': ['read']
        }
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle(f"📚 Gestion des Archives - SGAU - {self.user_info['nom']} ({self.user_info['role']})")
        self.resize(1200, 700)
        self.setStyleSheet(STYLE_SHEET)
        self.setWindowTitle(f"📚 Gestion des Archives - SGAU - Connecté: {self.user_info['nom']}")
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()
        central.setLayout(layout)

        # Barre d'information utilisateur
        user_layout = QHBoxLayout()
        user_info = QLabel(f"👤 Utilisateur connecté: {self.user_info['nom']} ({self.user_info.get('fonction', self.user_info.get('role', ''))})")
        user_info.setStyleSheet("user-info")
        user_layout.addWidget(user_info)
        user_layout.addStretch()
        
        # Bouton gérer utilisateur (moderne avec ombres)
        self.btn_users = QPushButton("👥")
        self.btn_users.setFixedSize(45, 45)
        self.btn_users.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #607D8B, stop:1 #455A64);
                border: none;
                border-radius: 22px;
                color: white;
                font-size: 18px;
                font-weight: bold;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #455A64, stop:1 #37474F);
                transform: translateY(-1px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #37474F, stop:1 #263238);
                transform: translateY(0px);
                box-shadow: 0 1px 2px rgba(0,0,0,0.2);
            }
        """)
        user_layout.addWidget(self.btn_users)
        
        # Bouton déconnexion moderne
        self.btn_logout = QPushButton("🚪 Déconnexion")
        self.btn_logout.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #F44336, stop:1 #D32F2F);
                border: none;
                border-radius: 8px;
                color: white;
                font-weight: bold;
                font-size: 13px;
                padding: 8px 16px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #D32F2F, stop:1 #C62828);
                transform: translateY(-1px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #C62828, stop:1 #B71C1C);
                transform: translateY(0px);
                box-shadow: 0 1px 2px rgba(0,0,0,0.2);
            }
        """)
        user_layout.addWidget(self.btn_logout)
        layout.addLayout(user_layout)

        # Barre de recherche moderne
        search_layout = QHBoxLayout()
        search_label = QLabel("🔍 Recherche :")
        search_label.setStyleSheet("""
            font-weight: bold;
            font-size: 14px;
            color: #1976D2;
            margin-right: 10px;
        """)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Rechercher par nom ou état...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 10px 15px;
                font-size: 13px;
                background: white;
                color: #333;
            }
            QLineEdit:focus {
                border-color: #1976D2;
                background: #F8F9FA;
            }
            QLineEdit:hover {
                border-color: #BDBDBD;
            }
        """)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        self.search_input.textChanged.connect(self.filtrer_dossiers)

        # Tableau des dossiers
        table_label = QLabel("📋 Liste des dossiers")
        table_label.setStyleSheet("title-label")
        layout.addWidget(table_label)
        
        self.table = QTableWidget()
        self.table.setColumnCount(7)  # Augmenté de 6 à 7 colonnes
        self.table.setHorizontalHeaderLabels([
            "🆔 ID", "👤 Nom", "📊 État", "📍 Localisation", "📅 Date création", "💬 Commentaire", "📎 Pièces jointes"
        ])
        
        # Style moderne pour le tableau avec hover effects
        self.table.setStyleSheet("""
            QTableWidget {
                background: white;
                border: 2px solid #E0E0E0;
                border-radius: 12px;
                gridline-color: #F0F0F0;
                selection-background-color: #E3F2FD;
                selection-color: #1976D2;
                font-size: 13px;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #F5F5F5;
            }
            QTableWidget::item:hover {
                background: #F8F9FA;
                border-radius: 6px;
            }
            QTableWidget::item:selected {
                background: #E3F2FD;
                color: #1976D2;
                font-weight: bold;
            }
            QHeaderView::section {
                background: #F8F9FA;
                color: #333;
                font-weight: bold;
                font-size: 14px;
                padding: 12px 8px;
                border: none;
                border-bottom: 2px solid #E0E0E0;
            }
            QHeaderView::section:hover {
                background: #E3F2FD;
                color: #1976D2;
            }
        """)
        
        # Activer l'alternance des couleurs des lignes
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)

        # Filtre moderne avec ComboBox
        filter_layout = QHBoxLayout()
        filter_label = QLabel("🔍 Filtrer par état :")
        filter_label.setStyleSheet("font-weight: bold; color: #1976D2; margin-right: 10px;")
        
        self.filter_combo = QComboBox()
        self.filter_combo.addItem("📋 Tous les dossiers", "tous")
        self.filter_combo.addItem("✅ Dossiers actifs", "actifs")
        self.filter_combo.addItem("👴 Dossiers retraités", "retraites")
        self.filter_combo.addItem("🕯️ Dossiers décédés", "decedes")
        self.filter_combo.addItem("📦 Dossiers non-actifs", "non_actifs")
        
        # Style moderne pour le ComboBox
        self.filter_combo.setStyleSheet("""
            QComboBox {
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 8px 12px;
                background: white;
                font-size: 14px;
                min-width: 200px;
                color: #333;
            }
            QComboBox:hover {
                border-color: #1976D2;
                background: #F5F5F5;
            }
            QComboBox:focus {
                border-color: #1976D2;
                background: white;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #666;
                margin-right: 10px;
            }
            QComboBox QAbstractItemView {
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                background: white;
                selection-background-color: #1976D2;
                selection-color: white;
                padding: 5px;
            }
        """)
        
        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.filter_combo)
        filter_layout.addStretch()  # Espace à droite
        
        # Statistiques rapides
        self.stats_label = QLabel("📊 Chargement...")
        self.stats_label.setStyleSheet("""
            color: #666;
            font-size: 12px;
            font-style: italic;
            padding: 5px 10px;
            background: #F8F9FA;
            border-radius: 15px;
            border: 1px solid #E0E0E0;
        """)
        filter_layout.addWidget(self.stats_label)
        
        layout.addLayout(filter_layout)

        # Actions modernes avec cartes
        actions_label = QLabel("🎯 Actions rapides")
        actions_label.setStyleSheet("font-weight: bold; font-size: 16px; color: #1976D2; margin: 15px 0 10px 0;")
        layout.addWidget(actions_label)
        
        # Replace the grid layout with horizontal layout
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(15)
        
        # Create action buttons in a single line
        self.card_add = self.create_action_card("➕", "Ajouter", "Créer un nouveau dossier", "#4CAF50")
        self.card_edit = self.create_action_card("✏️", "Modifier", "Modifier le dossier sélectionné", "#2196F3")
        self.card_delete = self.create_action_card("🗑️", "Supprimer", "Supprimer le dossier sélectionné", "#F44336")
        self.card_history = self.create_action_card("📋", "Historique", "Voir l'historique des mouvements", "#FF9800")
        
        # Add buttons to horizontal layout
        actions_layout.addWidget(self.card_add)
        actions_layout.addWidget(self.card_edit)
        actions_layout.addWidget(self.card_delete)
        actions_layout.addWidget(self.card_history)
        actions_layout.addStretch()  # This will push buttons to the left
        
        layout.addLayout(actions_layout)

        # Connexion du filtre ComboBox
        self.filter_combo.currentIndexChanged.connect(self.on_filter_changed)
        
        # Connexions des cartes d'action
        self.card_add.clicked.connect(self.ouvrir_dialog_ajout)
        self.card_delete.clicked.connect(self.supprimer_dossier_selectionne)
        self.card_edit.clicked.connect(self.modifier_dossier_selectionne)
        self.card_history.clicked.connect(self.ouvrir_historique_mouvements)
        self.btn_users.clicked.connect(self.ouvrir_gestion_utilisateurs)
        self.btn_logout.clicked.connect(self.logout)
        
        # Double-clic sur un dossier pour ouvrir l'historique
        self.table.cellDoubleClicked.connect(self.on_dossier_double_click)
        
        # Clic simple sur la colonne des pièces jointes
        self.table.cellClicked.connect(self.on_cell_clicked)

        self.charger_dossiers()

    def on_filter_changed(self):
        """Gère le changement de filtre dans le ComboBox"""
        filter_value = self.filter_combo.currentData()
        
        if filter_value == "tous":
            self.charger_dossiers()
        elif filter_value == "actifs":
            self.charger_dossiers_actifs()
        elif filter_value == "retraites":
            self.charger_dossiers_retraites()
        elif filter_value == "decedes":
            self.charger_dossiers_decedes()
        elif filter_value == "non_actifs":
            self.charger_dossiers_non_actifs()
    
    def update_stats(self, dossiers):
        """Met à jour les statistiques affichées"""
        total = len(dossiers)
        actifs = sum(1 for d in dossiers if str(d[2]).lower() == 'actif')
        retraites = sum(1 for d in dossiers if str(d[2]).lower() == 'retraité')
        decedes = sum(1 for d in dossiers if str(d[2]).lower() == 'décédé')
        non_actifs = sum(1 for d in dossiers if str(d[2]).lower() == 'non-actif')
        
        # Mise à jour de la barre de statistiques rapides
        self.stats_label.setText(f"📊 Total: {total} | ✅ Actifs: {actifs} | 👴 Retraités: {retraites} | 🕯️ Décédés: {decedes} | 📦 Non-actifs: {non_actifs}")

    def filtrer_dossiers(self):
        texte = self.search_input.text().lower()
        dossiers = db.lister_dossiers()
        filtered = []
        for dossier in dossiers:
            nom = str(dossier[1]).lower()
            etat = str(dossier[2]).lower()
            if texte in nom or texte in etat:
                filtered.append(dossier)
        self.table.setRowCount(len(filtered))
        for row, dossier in enumerate(filtered):
            # Colonnes 0, 1, 3, 4, 5 (ID, Nom, Localisation, Date, Commentaire)
            for col in [0, 1, 3, 4, 5]:
                value = dossier[col]
                self.table.setItem(row, col, QTableWidgetItem(str(value)))
            
            # Colonne État (2) avec badge coloré
            etat = str(dossier[2])
            etat_item = QTableWidgetItem()
            badge = self.create_status_badge(etat)
            self.table.setItem(row, 2, etat_item)
            self.table.setCellWidget(row, 2, badge)
            
            # Nouvelle colonne : Pièces jointes (colonne 6)
            pieces_count = len(db.lister_pieces_jointes(dossier[0]))
            pieces_item = QTableWidgetItem(f"📎 {pieces_count} fichier(s)")
            pieces_item.setData(Qt.UserRole, dossier[0])  # Stocker l'ID du dossier
            self.table.setItem(row, 6, pieces_item)
            
        self.table.resizeColumnsToContents()
        
        # Mettre à jour les statistiques avec les dossiers filtrés
        self.update_stats(filtered)

    def charger_dossiers(self):
        dossiers = db.lister_dossiers()
        dossiers_filtres = self.filtrer_dossiers_selon_permissions(dossiers)
        self.table.setRowCount(len(dossiers_filtres))
        for row, dossier in enumerate(dossiers_filtres):
            # Colonnes 0, 1, 3, 4, 5 (ID, Nom, Localisation, Date, Commentaire)
            for col in [0, 1, 3, 4, 5]:
                value = dossier[col]
                self.table.setItem(row, col, QTableWidgetItem(str(value)))
            
            # Colonne État (2) avec badge coloré
            etat = str(dossier[2])
            etat_item = QTableWidgetItem()
            badge = self.create_status_badge(etat)
            self.table.setItem(row, 2, etat_item)
            self.table.setCellWidget(row, 2, badge)
            
            # Nouvelle colonne : Pièces jointes (colonne 6)
            pieces_count = len(db.lister_pieces_jointes(dossier[0]))
            pieces_item = QTableWidgetItem(f"📎 {pieces_count} fichier(s)")
            pieces_item.setData(Qt.UserRole, dossier[0])  # Stocker l'ID du dossier
            self.table.setItem(row, 6, pieces_item)
            
        self.table.resizeColumnsToContents()
        self.update_stats(dossiers_filtres)
        self.search_input.clear()

    def filtrer_dossiers_selon_permissions(self, dossiers):
        return dossiers

    def charger_dossiers_actifs(self):
        dossiers = db.lister_dossiers_actifs()
        self.table.setRowCount(len(dossiers))
        for row, dossier in enumerate(dossiers):
            # Colonnes 0, 1, 3, 4, 5 (ID, Nom, Localisation, Date, Commentaire)
            for col in [0, 1, 3, 4, 5]:
                value = dossier[col]
                self.table.setItem(row, col, QTableWidgetItem(str(value)))
            
            # Colonne État (2) avec badge coloré
            etat = str(dossier[2])
            etat_item = QTableWidgetItem()
            badge = self.create_status_badge(etat)
            self.table.setItem(row, 2, etat_item)
            self.table.setCellWidget(row, 2, badge)
            
            # Nouvelle colonne : Pièces jointes (colonne 6)
            pieces_count = len(db.lister_pieces_jointes(dossier[0]))
            pieces_item = QTableWidgetItem(f"📎 {pieces_count} fichier(s)")
            pieces_item.setData(Qt.UserRole, dossier[0])  # Stocker l'ID du dossier
            self.table.setItem(row, 6, pieces_item)
            
        self.table.resizeColumnsToContents()
        self.update_stats(dossiers)
        self.search_input.clear()

    def charger_dossiers_retraites(self):
        dossiers = db.lister_dossiers_retraites()
        self.table.setRowCount(len(dossiers))
        for row, dossier in enumerate(dossiers):
            # Colonnes 0, 1, 3, 4, 5 (ID, Nom, Localisation, Date, Commentaire)
            for col in [0, 1, 3, 4, 5]:
                value = dossier[col]
                self.table.setItem(row, col, QTableWidgetItem(str(value)))
            
            # Colonne État (2) avec badge coloré
            etat = str(dossier[2])
            etat_item = QTableWidgetItem()
            badge = self.create_status_badge(etat)
            self.table.setItem(row, 2, etat_item)
            self.table.setCellWidget(row, 2, badge)
            
            # Nouvelle colonne : Pièces jointes (colonne 6)
            pieces_count = len(db.lister_pieces_jointes(dossier[0]))
            pieces_item = QTableWidgetItem(f"📎 {pieces_count} fichier(s)")
            pieces_item.setData(Qt.UserRole, dossier[0])  # Stocker l'ID du dossier
            self.table.setItem(row, 6, pieces_item)
            
        self.table.resizeColumnsToContents()
        self.update_stats(dossiers)
        self.search_input.clear()

    def charger_dossiers_decedes(self):
        dossiers = db.lister_dossiers_decedes()
        self.table.setRowCount(len(dossiers))
        for row, dossier in enumerate(dossiers):
            # Colonnes 0, 1, 3, 4, 5 (ID, Nom, Localisation, Date, Commentaire)
            for col in [0, 1, 3, 4, 5]:
                value = dossier[col]
                self.table.setItem(row, col, QTableWidgetItem(str(value)))
            
            # Colonne État (2) avec badge coloré
            etat = str(dossier[2])
            etat_item = QTableWidgetItem()
            badge = self.create_status_badge(etat)
            self.table.setItem(row, 2, etat_item)
            self.table.setCellWidget(row, 2, badge)
            
            # Nouvelle colonne : Pièces jointes (colonne 6)
            pieces_count = len(db.lister_pieces_jointes(dossier[0]))
            pieces_item = QTableWidgetItem(f"📎 {pieces_count} fichier(s)")
            pieces_item.setData(Qt.UserRole, dossier[0])  # Stocker l'ID du dossier
            self.table.setItem(row, 6, pieces_item)
            
        self.table.resizeColumnsToContents()
        self.update_stats(dossiers)
        self.search_input.clear()

    def charger_dossiers_non_actifs(self):
        dossiers = db.lister_dossiers_non_actifs()
        self.table.setRowCount(len(dossiers))
        for row, dossier in enumerate(dossiers):
            # Colonnes 0, 1, 3, 4, 5 (ID, Nom, Localisation, Date, Commentaire)
            for col in [0, 1, 3, 4, 5]:
                value = dossier[col]
                self.table.setItem(row, col, QTableWidgetItem(str(value)))
            
            # Colonne État (2) avec badge coloré
            etat = str(dossier[2])
            etat_item = QTableWidgetItem()
            badge = self.create_status_badge(etat)
            self.table.setItem(row, 2, etat_item)
            self.table.setCellWidget(row, 2, badge)
            
            # Nouvelle colonne : Pièces jointes (colonne 6)
            pieces_count = len(db.lister_pieces_jointes(dossier[0]))
            pieces_item = QTableWidgetItem(f"📎 {pieces_count} fichier(s)")
            pieces_item.setData(Qt.UserRole, dossier[0])  # Stocker l'ID du dossier
            self.table.setItem(row, 6, pieces_item)
            
        self.table.resizeColumnsToContents()
        self.update_stats(dossiers)
        self.search_input.clear()

    def ouvrir_dialog_ajout(self):
        dialog = AddDossierDialog(self)
        if dialog.exec_() == QMessageBox.Accepted:
            dossier_data, files_to_upload = dialog.get_data()
            nom, etat, localisation, date_creation, commentaire, responsable_id, niveau_confidentialite = dossier_data
            
            if nom and etat and localisation and date_creation:
                try:
                    # Ajouter le dossier
                    id_dossier = db.ajouter_dossier(nom, etat, localisation, date_creation, commentaire, responsable_id, niveau_confidentialite)
                    
                    # Ajouter les pièces jointes si des fichiers sont sélectionnés
                    if files_to_upload:
                        self.upload_files_to_dossier(id_dossier, files_to_upload)
                    
                    QMessageBox.information(self, "✅ Succès", f"Dossier '{nom}' ajouté avec succès !")
                    self.charger_dossiers()
                except Exception as e:
                    QMessageBox.warning(self, "❌ Erreur", f"Erreur lors de l'ajout du dossier : {str(e)}")
            else:
                QMessageBox.warning(self, "⚠️ Erreur", "Veuillez remplir tous les champs obligatoires.")

    def supprimer_dossier_selectionne(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "⚠️ Aucune sélection", 
                "Veuillez sélectionner un dossier à supprimer.")
            return
            
        id_item = self.table.item(row, 0)
        nom_item = self.table.item(row, 1)
        if not id_item:
            QMessageBox.warning(self, "❌ Erreur", 
                "Impossible de récupérer l'identifiant du dossier.")
            return
            
        id_dossier = int(id_item.text())
        nom_dossier = nom_item.text() if nom_item else f"ID {id_dossier}"
        
        # Confirmation moderne avec icônes et couleurs
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("🗑️ Confirmation de suppression")
        msg_box.setText(f"<h3>⚠️ Supprimer le dossier ?</h3>")
        msg_box.setInformativeText(f"<p><b>Dossier :</b> {nom_dossier}</p>"
                                  f"<p><b>ID :</b> {id_dossier}</p>"
                                  f"<p style='color: #D32F2F; font-weight: bold;'>"
                                  f"⚠️ Cette action est irréversible !</p>")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        
        # Style moderne pour la boîte de dialogue
        msg_box.setStyleSheet("""
            QMessageBox {
                background: white;
                border: 2px solid #E0E0E0;
                border-radius: 12px;
            }
            QMessageBox QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #F44336, stop:1 #D32F2F);
                border: none;
                border-radius: 6px;
                color: white;
                font-weight: bold;
                padding: 8px 16px;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #D32F2F, stop:1 #C62828);
            }
            QMessageBox QPushButton[text="&Non"] {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #607D8B, stop:1 #455A64);
            }
            QMessageBox QPushButton[text="&Non"]:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #455A64, stop:1 #37474F);
            }
        """)
        
        reply = msg_box.exec_()
        if reply == QMessageBox.Yes:
            try:
                db.supprimer_dossier(id_dossier)
                
                # Message de succès moderne
                success_msg = QMessageBox()
                success_msg.setIcon(QMessageBox.Information)
                success_msg.setWindowTitle("✅ Suppression réussie")
                success_msg.setText(f"<h3>✅ Dossier supprimé avec succès !</h3>")
                success_msg.setInformativeText(f"<p>Le dossier <b>'{nom_dossier}'</b> a été supprimé de la base de données.</p>")
                success_msg.setStandardButtons(QMessageBox.Ok)
                success_msg.setStyleSheet("""
                    QMessageBox {
                        background: white;
                        border: 2px solid #4CAF50;
                        border-radius: 12px;
                    }
                    QMessageBox QPushButton {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #4CAF50, stop:1 #388E3C);
                        border: none;
                        border-radius: 6px;
                        color: white;
                        font-weight: bold;
                        padding: 8px 16px;
                        min-width: 80px;
                    }
                    QMessageBox QPushButton:hover {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #388E3C, stop:1 #2E7D32);
                    }
                """)
                success_msg.exec_()
                self.charger_dossiers()
                
            except Exception as e:
                QMessageBox.critical(self, "❌ Erreur", 
                    f"Erreur lors de la suppression : {str(e)}")

    def modifier_dossier_selectionne(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "⚠️ Aucune sélection", "Veuillez sélectionner un dossier à modifier.")
            return
        id_item = self.table.item(row, 0)
        nom_item = self.table.item(row, 1)
        etat_item = self.table.item(row, 2)
        localisation_item = self.table.item(row, 3)
        date_item = self.table.item(row, 4)
        commentaire_item = self.table.item(row, 5)
        if not id_item:
            QMessageBox.warning(self, "❌ Erreur", "Impossible de récupérer l'identifiant du dossier.")
            return
        id_dossier = int(id_item.text())
        
        # Récupérer les données complètes du dossier
        try:
            dossier_data = db.obtenir_dossier_par_id(id_dossier)
        except Exception as e:
            QMessageBox.warning(self, "❌ Erreur", f"Impossible de récupérer les données du dossier : {str(e)}")
            return
        
        dialog = AddDossierDialog(self, dossier_data)
        if dialog.exec_() == QMessageBox.Accepted:
            dossier_data, files_to_upload = dialog.get_data()
            nom, etat, localisation, date_creation, commentaire, responsable_id, niveau_confidentialite = dossier_data
            
            if nom and etat and localisation and date_creation:
                try:
                    # Modifier le dossier
                    db.modifier_dossier(id_dossier, nom, etat, localisation, date_creation, commentaire, responsable_id, niveau_confidentialite)
                    
                    # Ajouter les nouvelles pièces jointes si des fichiers sont sélectionnés
                    if files_to_upload:
                        self.upload_files_to_dossier(id_dossier, files_to_upload)
                    
                    QMessageBox.information(self, "✅ Succès", f"Dossier '{nom}' modifié avec succès !")
                    self.charger_dossiers()
                except Exception as e:
                    QMessageBox.warning(self, "❌ Erreur", f"Erreur lors de la modification du dossier : {str(e)}")
            else:
                QMessageBox.warning(self, "⚠️ Erreur", "Veuillez remplir tous les champs obligatoires.")

    def ouvrir_historique_mouvements(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "⚠️ Aucune sélection", "Veuillez sélectionner un dossier pour voir son historique.")
            return
        id_item = self.table.item(row, 0)
        nom_item = self.table.item(row, 1)
        if not id_item or not nom_item:
            QMessageBox.warning(self, "❌ Erreur", "Impossible de récupérer les informations du dossier.")
            return
        id_dossier = int(id_item.text())
        nom_dossier = nom_item.text()
        dialog = HistoriqueMouvementsDialog(id_dossier, nom_dossier, self)
        dialog.exec_()

    def ouvrir_gestion_pieces_jointes(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "⚠️ Aucune sélection", "Veuillez sélectionner un dossier pour gérer ses pièces jointes.")
            return
        
        id_item = self.table.item(row, 0)
        nom_item = self.table.item(row, 1)
        
        if not id_item or not nom_item:
            QMessageBox.warning(self, "❌ Erreur", "Impossible de récupérer les informations du dossier.")
            return
        
        id_dossier = int(id_item.text())
        nom_dossier = nom_item.text()
        
        dialog = GestionPiecesJointesDialog(id_dossier, nom_dossier, self)
        dialog.exec_()

    def ouvrir_gestion_utilisateurs(self):
        dialog = GestionUtilisateursDialog(self)
        dialog.exec_()
    


    def on_dossier_double_click(self, row, column):
        id_item = self.table.item(row, 0)
        nom_item = self.table.item(row, 1)
        if id_item and nom_item:
            id_dossier = int(id_item.text())
            nom_dossier = nom_item.text()
            dialog = HistoriqueMouvementsDialog(id_dossier, nom_dossier, self)
            dialog.exec_()

    def on_cell_clicked(self, row, column):
        if column == 6: # Pièces jointes column
            id_item = self.table.item(row, 0)
            nom_item = self.table.item(row, 1)
            if id_item and nom_item:
                id_dossier = int(id_item.text())
                nom_dossier = nom_item.text()
                dialog = GestionPiecesJointesDialog(id_dossier, nom_dossier, self)
                dialog.exec_()

    def create_status_badge(self, status):
        """Crée un badge coloré pour l'état du dossier"""
        badge = QLabel(status)
        badge.setAlignment(Qt.AlignCenter)
        badge.setFixedHeight(24)
        
        # Palette de couleurs moderne pour les états
        status_colors = {
            'actif': {
                'bg': '#E8F5E8',
                'text': '#2E7D32',
                'border': '#4CAF50'
            },
            'retraité': {
                'bg': '#FFF3E0',
                'text': '#E65100',
                'border': '#FF9800'
            },
            'décédé': {
                'bg': '#F3E5F5',
                'text': '#7B1FA2',
                'border': '#9C27B0'
            },
            'non-actif': {
                'bg': '#F5F5F5',
                'text': '#616161',
                'border': '#9E9E9E'
            }
        }
        
        # Normaliser le statut
        status_lower = status.lower()
        colors = status_colors.get(status_lower, status_colors['non-actif'])
        
        badge.setStyleSheet(f"""
            QLabel {{
                background: {colors['bg']};
                color: {colors['text']};
                border: 1px solid {colors['border']};
                border-radius: 12px;
                padding: 4px 12px;
                font-weight: bold;
                font-size: 11px;
                text-transform: uppercase;
            }}
        """)
        
        return badge

    def create_action_card(self, icon, title, description, color):
        """Crée une carte d'action moderne avec ombres et effets"""
        card = QPushButton()
        card.setFixedSize(130, 90)  # Légèrement plus grand
        card.setCursor(Qt.PointingHandCursor)
        
        # Style moderne avec ombres et effets
        card.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #FFFFFF, stop:1 #F8F9FA);
                border: 2px solid #E0E0E0;
                border-radius: 12px;
                padding: 10px;
                text-align: center;
                font-weight: bold;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #F8F9FA, stop:1 #E3F2FD);
                border-color: {color};
                transform: translateY(-1px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.15);
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #E3F2FD, stop:1 #BBDEFB);
                border-color: {color};
                transform: translateY(0px);
                box-shadow: 0 1px 2px rgba(0,0,0,0.1);
            }}
        """)
        
        # Layout vertical pour la carte
        layout = QVBoxLayout()
        layout.setSpacing(6)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Icône
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"""
            font-size: 24px;
            color: {color};
            margin-bottom: 4px;
        """)
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)
        
        # Titre
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            font-weight: bold;
            font-size: 12px;
            color: #333;
            margin-bottom: 2px;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel(description)
        desc_label.setStyleSheet(f"""
            font-size: 10px;
            color: #666;
            text-align: center;
        """)
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        card.setLayout(layout)
        return card



    def upload_files_to_dossier(self, id_dossier, files_to_upload):
        """Upload les fichiers vers un dossier"""
        if not files_to_upload:
            return
        
        try:
            # Créer le dossier d'archives s'il n'existe pas
            archives_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'archives')
            if not os.path.exists(archives_dir):
                os.makedirs(archives_dir)
            
            # Créer le sous-dossier pour ce dossier
            dossier_dir = os.path.join(archives_dir, f'dossier_{id_dossier}')
            if not os.path.exists(dossier_dir):
                os.makedirs(dossier_dir)
            
            uploaded_count = 0
            for file_path in files_to_upload:
                try:
                    # Copier le fichier vers le dossier d'archives
                    file_name = os.path.basename(file_path)
                    dest_path = os.path.join(dossier_dir, file_name)
                    
                    # Éviter les doublons
                    counter = 1
                    base_name, ext = os.path.splitext(file_name)
                    while os.path.exists(dest_path):
                        file_name = f"{base_name}_{counter}{ext}"
                        dest_path = os.path.join(dossier_dir, file_name)
                        counter += 1
                    
                    shutil.copy2(file_path, dest_path)
                    
                    # Ajouter à la base de données
                    db.ajouter_piece_jointe(
                        id_dossier=id_dossier,
                        nom_fichier=file_name,
                        chemin_fichier=dest_path,
                        type_fichier=os.path.splitext(file_name)[1].lower(),
                        description=f"Fichier ajouté le {datetime.now().strftime('%d/%m/%Y %H:%M')}"
                    )
                    
                    uploaded_count += 1
                    
                except Exception as e:
                    print(f"Erreur lors de l'upload du fichier {file_path}: {e}")
                    continue
            
            if uploaded_count > 0:
                QMessageBox.information(self, "✅ Succès", 
                    f"{uploaded_count} fichier(s) ajouté(s) au dossier avec succès !")
            
        except Exception as e:
            QMessageBox.warning(self, "❌ Erreur", f"Erreur lors de l'upload des fichiers : {str(e)}")

    def logout(self):
        # Confirmation moderne pour la déconnexion
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle("🚪 Déconnexion")
        msg_box.setText(f"<h3>🚪 Se déconnecter ?</h3>")
        msg_box.setInformativeText(f"<p>Voulez-vous vraiment vous déconnecter de l'application ?</p>"
                                  f"<p><b>Utilisateur :</b> {self.user_info['nom']}</p>")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        
        # Style moderne pour la boîte de dialogue
        msg_box.setStyleSheet("""
            QMessageBox {
                background: white;
                border: 2px solid #E0E0E0;
                border-radius: 12px;
            }
            QMessageBox QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #F44336, stop:1 #D32F2F);
                border: none;
                border-radius: 6px;
                color: white;
                font-weight: bold;
                padding: 8px 16px;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #D32F2F, stop:1 #C62828);
            }
            QMessageBox QPushButton[text="&Non"] {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #607D8B, stop:1 #455A64);
            }
            QMessageBox QPushButton[text="&Non"]:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #455A64, stop:1 #37474F);
            }
        """)
        
        reply = msg_box.exec_()
        if reply == QMessageBox.Yes:
            self.close()