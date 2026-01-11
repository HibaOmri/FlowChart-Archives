from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox, QComboBox, QFrame, QGridLayout, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QColor
from .styles import STYLE_SHEET, STATUS_COLORS, ACTION_CARD_STYLE
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
            'id': 1,
            'nom': 'Utilisateur Test',
            'role': 'Archiviste',
            'permissions': ['read']
        }
        self.setup_ui()

    def apply_shadow(self, widget, color=QColor(0, 0, 0, 50), blur=15, offset=(0, 2)):
        """Helper to apply a drop shadow effect to a widget"""
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(blur)
        shadow.setColor(color)
        shadow.setOffset(*offset)
        widget.setGraphicsEffect(shadow)

    def setup_ui(self):
        self.setWindowTitle(f"Gestion des Archives - SGAU - Connecté: {self.user_info['nom']}")
        self.resize(1200, 750)
        self.setStyleSheet(STYLE_SHEET)
        
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        central.setLayout(layout)

        # === Header: User Info & Actions ===
        header_layout = QHBoxLayout()
        
        # User Info Badge
        user_info = QLabel(f"Utilisateur: {self.user_info['nom']} | {self.user_info.get('fonction', self.user_info.get('role', 'Archiviste'))}")
        user_info.setProperty("class", "user-info")
        user_info.setStyleSheet("background-color: white; color: #2c3e50; padding: 8px 15px; border-radius: 20px; border: 1px solid #e0e0e0; font-weight: bold;")
        self.apply_shadow(user_info, QColor(0, 0, 0, 20), 10, (0, 2))
        header_layout.addWidget(user_info)
        
        header_layout.addStretch()
        
        # Bouton Users (pour Admin)
        self.btn_users = QPushButton("Gérer les utilisateurs")
        self.btn_users.setStyleSheet("""
            QPushButton {
                background-color: #607D8B;
                padding: 8px 20px;
                border-radius: 20px;
            }
            QPushButton:hover { background-color: #546E7A; }
        """)
        self.apply_shadow(self.btn_users)
        header_layout.addWidget(self.btn_users)
        
        # Bouton Logout
        self.btn_logout = QPushButton("Déconnexion")
        self.btn_logout.setProperty("warning", True)
        self.btn_logout.setStyleSheet("border-radius: 20px; padding: 8px 20px;")
        self.apply_shadow(self.btn_logout, QColor(244, 67, 54, 80))
        header_layout.addWidget(self.btn_logout)
        
        layout.addLayout(header_layout)

        # === Barre de Recherche & Filtres ===
        search_frame = QFrame()
        search_frame.setStyleSheet("background-color: white; border-radius: 12px;")
        self.apply_shadow(search_frame, QColor(0, 0, 0, 30))
        search_layout = QHBoxLayout(search_frame)
        search_layout.setContentsMargins(15, 10, 15, 10)
        
        # Recherche
        search_label = QLabel("🔍")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Rechercher par nom, matricule ou état...")
        self.search_input.setStyleSheet("border: none; background: transparent; font-size: 14px;")
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        
        # Séparateur vertical
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("color: #eee;")
        search_layout.addWidget(line)
        
        # Filtre
        filter_label = QLabel("Filtrer par:")
        filter_label.setStyleSheet("color: #666; margin-left: 10px;")
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["Tous les dossiers", "Dossiers actifs", "Dossiers retraités", "Dossiers décédés", "Dossiers non-actifs"])
        self.filter_map = {
            0: "tous", 1: "actifs", 2: "retraites", 3: "decedes", 4: "non_actifs"
        }
        self.filter_combo.setStyleSheet("border: none; background: transparent; font-weight: bold; color: #1976D2;")
        
        search_layout.addWidget(filter_label)
        search_layout.addWidget(self.filter_combo)
        
        layout.addWidget(search_frame)

        # === Statistiques Rapides ===
        self.stats_label = QLabel("Chargement des statistiques...")
        self.stats_label.setStyleSheet("color: #666; font-style: italic; margin-left: 10px;")
        layout.addWidget(self.stats_label)

        # === Actions Rapides ===
        actions_label = QLabel("Actions rapides")
        actions_label.setProperty("class", "section-label")
        actions_label.setStyleSheet("font-weight: bold; font-size: 16px; color: #1976D2; margin: 15px 0 10px 0;")
        layout.addWidget(actions_label)
        
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(15)
        
        self.card_add = self.create_action_card("+", "Ajouter", "Créer un nouveau dossier", "#4CAF50")
        self.card_edit = self.create_action_card("✎", "Modifier", "Modifier le dossier sélectionné", "#2196F3")
        self.card_delete = self.create_action_card("x", "Supprimer", "Supprimer le dossier sélectionné", "#F44336")
        self.card_history = self.create_action_card("H", "Historique", "Voir l'historique des mouvements", "#FF9800")
        
        actions_layout.addWidget(self.card_add)
        actions_layout.addWidget(self.card_edit)
        actions_layout.addWidget(self.card_delete)
        actions_layout.addWidget(self.card_history)
        actions_layout.addStretch()
        
        layout.addLayout(actions_layout)

        # === Tableau des Dossiers ===
        table_path_label = QLabel("Liste des dossiers")
        table_path_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #1976D2; margin-top: 15px;")
        layout.addWidget(table_path_label)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Nom", "État", "Localisation", "Date création", "Commentaire", "Pièces jointes"
        ])
        
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        
        self.apply_shadow(self.table, QColor(0,0,0,30))
        
        layout.addWidget(self.table)

        # Connexions
        self.search_input.textChanged.connect(self.charger_dossiers)
        self.filter_combo.currentIndexChanged.connect(self.charger_dossiers)
        
        self.card_add.clicked.connect(self.ouvrir_dialog_ajout)
        self.card_delete.clicked.connect(self.supprimer_dossier_selectionne)
        self.card_edit.clicked.connect(self.modifier_dossier_selectionne)
        self.card_history.clicked.connect(self.ouvrir_historique_mouvements)
        self.btn_users.clicked.connect(self.ouvrir_gestion_utilisateurs)
        self.btn_logout.clicked.connect(self.logout)
        
        self.table.cellDoubleClicked.connect(self.on_dossier_double_click)
        self.table.cellClicked.connect(self.on_cell_clicked)

        # Chargement initial
        self.charger_dossiers()

    def charger_dossiers(self):
        """Charge et filtre les dossiers en une seule passe"""
        tous_dossiers = db.lister_dossiers()
        search_text = self.search_input.text().lower()
        filter_index = self.filter_combo.currentIndex()
        filter_status_code = self.filter_map.get(filter_index, "tous")
        
        filtered_dossiers = []
        for dossier in tous_dossiers:
            nom = str(dossier[1]).lower()
            etat = str(dossier[2]).lower()
            
            if search_text and (search_text not in nom and search_text not in etat):
                continue
                
            if filter_status_code != "tous":
                target = ""
                if filter_status_code == "actifs": target = "actif"
                elif filter_status_code == "retraites": target = "retraité"
                elif filter_status_code == "decedes": target = "décédé"
                elif filter_status_code == "non_actifs": target = "non-actif"
                
                if target and target != etat:
                    continue

            filtered_dossiers.append(dossier)
            
        self.update_table(filtered_dossiers)
        self.update_stats(filtered_dossiers)

    def update_table(self, dossiers):
        self.table.setRowCount(len(dossiers))
        for row, dossier in enumerate(dossiers):
            for col in [0, 1, 3, 4, 5]:
                self.table.setItem(row, col, QTableWidgetItem(str(dossier[col])))
            
            etat = str(dossier[2])
            self.table.setCellWidget(row, 2, self.create_status_badge(etat))
            
            try:
                pieces_count = len(db.lister_pieces_jointes(dossier[0]))
            except:
                pieces_count = 0
            pieces_item = QTableWidgetItem(f"{pieces_count} PJ")
            pieces_item.setData(Qt.UserRole, dossier[0])
            self.table.setItem(row, 6, pieces_item)
            
        self.table.resizeColumnsToContents()

    def update_stats(self, dossiers_affiches):
        total_visible = len(dossiers_affiches)
        try:
            all_dossiers = db.lister_dossiers()
            total = len(all_dossiers)
            actifs = sum(1 for d in all_dossiers if str(d[2]).lower() == 'actif')
        except:
            total = 0
            actifs = 0
            
        self.stats_label.setText(f"Affichés: {total_visible} | Total Base: {total} ( Dont {actifs} Actifs )")

    def ouvrir_dialog_ajout(self):
        dialog = AddDossierDialog(self)
        if dialog.exec_() == QMessageBox.Accepted:
            dossier_data, files_to_upload = dialog.get_data()
            nom, etat, localisation, date_creation, commentaire, responsable_id, niveau_confidentialite = dossier_data
            
            if nom and etat and localisation and date_creation:
                try:
                    # Ajouter le dossier
                    id_dossier = db.ajouter_dossier(nom, etat, localisation, date_creation, commentaire, responsable_id, niveau_confidentialite)
                    if files_to_upload:
                        self.upload_files_to_dossier(id_dossier, files_to_upload)
                    QMessageBox.information(self, "Succès", f"Dossier '{nom}' ajouté avec succès !")
                    self.charger_dossiers()
                except Exception as e:
                    QMessageBox.warning(self, "Erreur", f"Erreur lors de l'ajout du dossier : {str(e)}")
            else:
                QMessageBox.warning(self, "⚠️ Erreur", "Veuillez remplir tous les champs obligatoires.")

    def supprimer_dossier_selectionne(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Aucune sélection", "Veuillez sélectionner un dossier à supprimer.")
            return
        id_item = self.table.item(row, 0)
        nom_item = self.table.item(row, 1)
        if not id_item:
            QMessageBox.warning(self, "Erreur", "Impossible de récupérer l'identifiant du dossier.")
            return
        id_dossier = int(id_item.text())
        nom_dossier = nom_item.text() if nom_item else f"ID {id_dossier}"
        
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Confirmation de suppression")
        msg_box.setText(f"<h3>Supprimer le dossier ?</h3>")
        msg_box.setInformativeText(f"<p><b>Dossier :</b> {nom_dossier}</p><p><b>ID :</b> {id_dossier}</p><p style='color: #D32F2F;'>Cette action est irréversible !</p>")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        
        reply = msg_box.exec_()
        if reply == QMessageBox.Yes:
            try:
                db.supprimer_dossier(id_dossier)
                QMessageBox.information(self, "Succès", "Dossier supprimé avec succès !")
                self.charger_dossiers()
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de la suppression : {str(e)}")

    def modifier_dossier_selectionne(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Aucune sélection", "Veuillez sélectionner un dossier à modifier.")
            return
        id_item = self.table.item(row, 0)
        id_dossier = int(id_item.text())
        
        try:
            dossier_data = db.obtenir_dossier_par_id(id_dossier)
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Impossible de récupérer les données du dossier : {str(e)}")
            return
        
        dialog = AddDossierDialog(self, dossier_data)
        if dialog.exec_() == QMessageBox.Accepted:
            dossier_data, files_to_upload = dialog.get_data()
            nom, etat, localisation, date_creation, commentaire, responsable_id, niveau_confidentialite = dossier_data
            if nom and etat and localisation and date_creation:
                try:
                    db.modifier_dossier(id_dossier, nom, etat, localisation, date_creation, commentaire, responsable_id, niveau_confidentialite)
                    if files_to_upload:
                        self.upload_files_to_dossier(id_dossier, files_to_upload)
                    QMessageBox.information(self, "Succès", f"Dossier '{nom}' modifié avec succès !")
                    self.charger_dossiers()
                except Exception as e:
                    QMessageBox.warning(self, "Erreur", f"Erreur lors de la modification : {str(e)}")
            else:
                QMessageBox.warning(self, "⚠️ Erreur", "Veuillez remplir tous les champs obligatoires.")

    def ouvrir_historique_mouvements(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Aucune sélection", "Veuillez sélectionner un dossier.")
            return
        id_item = self.table.item(row, 0)
        nom_item = self.table.item(row, 1)
        dialog = HistoriqueMouvementsDialog(int(id_item.text()), nom_item.text(), self, user_info=self.user_info)
        dialog.exec_()

    def ouvrir_gestion_pieces_jointes(self):
        self.on_cell_clicked(self.table.currentRow(), 6)

    def ouvrir_gestion_utilisateurs(self):
        dialog = GestionUtilisateursDialog(self)
        dialog.exec_()
    
    def on_dossier_double_click(self, row, column):
        self.ouvrir_historique_mouvements()

    def on_cell_clicked(self, row, column):
        if column == 6: # Pièces jointes column
            id_item = self.table.item(row, 0)
            nom_item = self.table.item(row, 1)
            if id_item and nom_item:
                dialog = GestionPiecesJointesDialog(int(id_item.text()), nom_item.text(), self)
                dialog.exec_()

    def create_status_badge(self, status):
        """Crée un badge coloré pour l'état du dossier"""
        badge = QLabel(status)
        badge.setAlignment(Qt.AlignCenter)
        badge.setFixedHeight(24)
        
        status_lower = status.lower()
        colors = STATUS_COLORS.get(status_lower, STATUS_COLORS['non-actif'])
        
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
        """Crée une carte d'action plus compacte"""
        card = QPushButton()
        self.apply_shadow(card, QColor(0,0,0,10), blur=10, offset=(0, 2))
        card.setFixedSize(210, 75)
        card.setCursor(Qt.PointingHandCursor)
        
        # Style compact
        card.setStyleSheet(f"""
            QPushButton {{
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 12px;
                text-align: left;
            }}
            QPushButton:hover {{
                background-color: #F8FDFF;
                border: 1px solid {color}50;
            }}
            QPushButton:pressed {{
                background-color: #F0F5FA;
            }}
        """)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(10)
        
        # 1. Petit Icone (Cercle)
        icon_container = QLabel()
        icon_container.setFixedSize(38, 38)
        icon_container.setAlignment(Qt.AlignCenter)
        icon_container.setStyleSheet(f"""
            background-color: {color}15;
            color: {color};
            border-radius: 19px;
            font-size: 18px;
        """)
        icon_container.setText(icon)
        layout.addWidget(icon_container)
        
        # 2. Textes ajustés
        text_layout = QVBoxLayout()
        text_layout.setSpacing(0)
        text_layout.setContentsMargins(0, 2, 0, 2)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-family: 'Segoe UI', sans-serif;
            font-size: 13px;
            font-weight: bold;
            color: #2c3e50;
        """)
        
        desc_label = QLabel(description)
        desc_label.setStyleSheet("""
            font-family: 'Segoe UI', sans-serif;
            font-size: 10px;
            color: #95a5a6;
        """)
        desc_label.setWordWrap(True)
        
        text_layout.addWidget(title_label)
        text_layout.addWidget(desc_label)
        text_layout.addStretch()
        
        layout.addLayout(text_layout)
        card.setLayout(layout)
        
        return card

    def upload_files_to_dossier(self, id_dossier, files_to_upload):
        if not files_to_upload: return
        try:
            archives_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'archives')
            if not os.path.exists(archives_dir): os.makedirs(archives_dir)
            dossier_dir = os.path.join(archives_dir, f'dossier_{id_dossier}')
            if not os.path.exists(dossier_dir): os.makedirs(dossier_dir)
            
            uploaded_count = 0
            for file_path in files_to_upload:
                try:
                    file_name = os.path.basename(file_path)
                    dest_path = os.path.join(dossier_dir, file_name)
                    counter = 1
                    base_name, ext = os.path.splitext(file_name)
                    while os.path.exists(dest_path):
                        file_name = f"{base_name}_{counter}{ext}"
                        dest_path = os.path.join(dossier_dir, file_name)
                        counter += 1
                    shutil.copy2(file_path, dest_path)
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
            if uploaded_count > 0:
                QMessageBox.information(self, "Succès", f"{uploaded_count} fichier(s) ajouté(s) au dossier avec succès !")
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur lors de l'upload des fichiers : {str(e)}")

    def logout(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle("Déconnexion")
        msg_box.setText(f"<h3>Se déconnecter ?</h3>")
        msg_box.setInformativeText(f"<p>Voulez-vous vraiment vous déconnecter de l'application ?</p><p><b>Utilisateur :</b> {self.user_info['nom']}</p>")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        reply = msg_box.exec_()
        if reply == QMessageBox.Yes:
            self.close()