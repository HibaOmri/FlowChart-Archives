from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, QComboBox, 
                             QTextEdit, QDateEdit, QHBoxLayout, QPushButton, 
                             QListWidget, QListWidgetItem, QFileDialog, QFrame,
                             QScrollArea, QWidget, QMessageBox, QProgressBar)
from PyQt5.QtCore import QDate, Qt, QMimeData, QThread, pyqtSignal
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QPixmap, QIcon
from .styles import STYLE_SHEET, ETATS_DOSSIERS, NIVEAUX_CONFIDENTIALITE
import os
import sys
import shutil
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '../backend'))
import db

class FileDropWidget(QFrame):
    """Widget pour le drag & drop de fichiers"""
    files_dropped = pyqtSignal(list)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setMinimumHeight(120)
        self.setStyleSheet("""
            QFrame {
                border: 2px dashed #ccc;
                border-radius: 8px;
                background-color: #f8f9fa;
                padding: 20px;
            }
            QFrame:hover {
                border-color: #1976D2;
                background-color: #e3f2fd;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Icône et texte
        icon_label = QLabel("📁")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 32px; margin-bottom: 10px;")
        layout.addWidget(icon_label)
        
        text_label = QLabel("Glissez-déposez vos fichiers ici\nou cliquez pour sélectionner")
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setStyleSheet("color: #666; font-size: 14px;")
        text_label.setWordWrap(True)
        layout.addWidget(text_label)
        
        self.setLayout(layout)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setStyleSheet("""
                QFrame {
                    border: 2px dashed #1976D2;
                    border-radius: 8px;
                    background-color: #e3f2fd;
                    padding: 20px;
                }
            """)
    
    def dragLeaveEvent(self, event):
        self.setStyleSheet("""
            QFrame {
                border: 2px dashed #ccc;
                border-radius: 8px;
                background-color: #f8f9fa;
                padding: 20px;
            }
            QFrame:hover {
                border-color: #1976D2;
                background-color: #e3f2fd;
            }
        """)
    
    def dropEvent(self, event: QDropEvent):
        files = []
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if os.path.isfile(file_path):
                files.append(file_path)
        
        if files:
            self.files_dropped.emit(files)
        
        self.setStyleSheet("""
            QFrame {
                border: 2px dashed #ccc;
                border-radius: 8px;
                background-color: #f8f9fa;
                padding: 20px;
            }
            QFrame:hover {
                border-color: #1976D2;
                background-color: #e3f2fd;
            }
        """)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            files, _ = QFileDialog.getOpenFileNames(
                self, 
                "Sélectionner des fichiers",
                "",
                "Tous les fichiers (*);;Documents (*.pdf *.doc *.docx);;Images (*.jpg *.jpeg *.png *.gif);;Textes (*.txt *.rtf)"
            )
            if files:
                self.files_dropped.emit(files)

class FileListWidget(QListWidget):
    """Widget pour afficher la liste des fichiers sélectionnés"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMaximumHeight(150)
        self.setStyleSheet("""
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eee;
                background-color: #f8f9fa;
                border-radius: 4px;
                margin: 2px;
            }
            QListWidget::item:hover {
                background-color: #e3f2fd;
            }
        """)
    
    def add_file(self, file_path):
        """Ajoute un fichier à la liste"""
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        
        # Formater la taille
        if file_size < 1024:
            size_str = f"{file_size} B"
        elif file_size < 1024 * 1024:
            size_str = f"{file_size / 1024:.1f} KB"
        else:
            size_str = f"{file_size / (1024 * 1024):.1f} MB"
        
        # Créer l'item avec icône selon le type de fichier
        item = QListWidgetItem()
        item.setText(f"📄 {file_name} ({size_str})")
        item.setData(Qt.UserRole, file_path)
        
        # Ajouter un bouton de suppression
        item.setData(Qt.UserRole + 1, True)  # Marquer comme supprimable
        
        self.addItem(item)
    
    def get_files(self):
        """Retourne la liste des chemins de fichiers"""
        files = []
        for i in range(self.count()):
            item = self.item(i)
            file_path = item.data(Qt.UserRole)
            if file_path:
                files.append(file_path)
        return files
    
    def remove_selected_files(self):
        """Supprime les fichiers sélectionnés"""
        for item in self.selectedItems():
            self.takeItem(self.row(item))

class AddDossierDialog(QDialog):
    def __init__(self, parent=None, dossier_data=None):
        super().__init__(parent)
        self.dossier_data = dossier_data  # Pour la modification
        self.files_to_upload = []  # Liste des fichiers à uploader
        
        if dossier_data:
            self.setWindowTitle("✏️ Modifier le dossier")
            self.is_editing = True
        else:
            self.setWindowTitle("📁 Ajouter un dossier")
            self.is_editing = False
            
        self.setModal(True)
        self.setStyleSheet(STYLE_SHEET)
        self.resize(600, 700)
        self.setup_ui()
        
        if dossier_data:
            self.fill_form_with_data(dossier_data)

    def setup_ui(self):
        layout = QVBoxLayout()

        # Titre
        title_label = QLabel("📁 Nouveau dossier" if not self.is_editing else "✏️ Modifier le dossier")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-weight: bold; font-size: 16px; margin: 10px; color: #1976D2;")
        layout.addWidget(title_label)

        # Scroll Area pour le contenu
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        
        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_widget.setLayout(content_layout)

        # Champs du dossier
        self.nom_input = QLineEdit()
        self.nom_input.setPlaceholderText("Entrez le nom de la personne")
        self.etat_input = QComboBox()
        self.etat_input.addItems(ETATS_DOSSIERS)
        self.localisation_input = QLineEdit()
        self.localisation_input.setPlaceholderText("Entrez la localisation")
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        self.commentaire_input = QTextEdit()
        self.commentaire_input.setPlaceholderText("Entrez un commentaire...")
        self.commentaire_input.setMaximumHeight(100)
        
        # Nouveaux champs pour la responsabilité et confidentialité
        self.responsable_input = QComboBox()
        self.charger_utilisateurs()
        self.niveau_confidentialite_input = QComboBox()
        self.niveau_confidentialite_input.addItems(NIVEAUX_CONFIDENTIALITE)

        content_layout.addWidget(QLabel("👤 Nom de la personne :"))
        content_layout.addWidget(self.nom_input)
        content_layout.addWidget(QLabel("📊 État :"))
        content_layout.addWidget(self.etat_input)
        content_layout.addWidget(QLabel("📍 Localisation :"))
        content_layout.addWidget(self.localisation_input)
        content_layout.addWidget(QLabel("📅 Date de création :"))
        content_layout.addWidget(self.date_input)
        content_layout.addWidget(QLabel("👨‍💼 Responsable :"))
        content_layout.addWidget(self.responsable_input)
        content_layout.addWidget(QLabel("🔒 Niveau de confidentialité :"))
        content_layout.addWidget(self.niveau_confidentialite_input)
        content_layout.addWidget(QLabel("💬 Commentaire :"))
        content_layout.addWidget(self.commentaire_input)

        # Séparateur
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        content_layout.addWidget(separator)

        # Section Pièces jointes
        pieces_label = QLabel("📎 Pièces jointes")
        pieces_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #1976D2; margin-top: 10px;")
        content_layout.addWidget(pieces_label)

        # Zone de drag & drop
        self.drop_widget = FileDropWidget()
        self.drop_widget.files_dropped.connect(self.on_files_dropped)
        content_layout.addWidget(self.drop_widget)

        # Liste des fichiers sélectionnés
        files_label = QLabel("📋 Fichiers sélectionnés :")
        content_layout.addWidget(files_label)
        
        self.files_list = FileListWidget()
        content_layout.addWidget(self.files_list)

        # Boutons pour les fichiers
        files_btn_layout = QHBoxLayout()
        self.btn_add_files = QPushButton("📁 Ajouter des fichiers")
        self.btn_remove_files = QPushButton("🗑️ Supprimer la sélection")
        self.btn_add_files.setProperty("success", True)
        self.btn_remove_files.setProperty("warning", True)
        files_btn_layout.addWidget(self.btn_add_files)
        files_btn_layout.addWidget(self.btn_remove_files)
        content_layout.addLayout(files_btn_layout)

        # Barre de progression (cachée par défaut)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        content_layout.addWidget(self.progress_bar)

        # Message d'aide
        help_label = QLabel("💡 Formats acceptés : PDF, Word, Excel, Images, Textes. Taille max : 10 MB par fichier.")
        help_label.setStyleSheet("color: #6c757d; font-size: 11px; font-style: italic; margin: 5px;")
        help_label.setWordWrap(True)
        content_layout.addWidget(help_label)

        scroll.setWidget(content_widget)
        layout.addWidget(scroll)

        # Boutons principaux
        btn_layout = QHBoxLayout()
        if self.is_editing:
            self.btn_ok = QPushButton("✅ Modifier")
        else:
            self.btn_ok = QPushButton("✅ Ajouter")
        self.btn_cancel = QPushButton("❌ Annuler")
        self.btn_ok.setProperty("success", True)
        self.btn_cancel.setProperty("warning", True)
        btn_layout.addWidget(self.btn_ok)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        # Connexions
        self.btn_ok.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_add_files.clicked.connect(self.add_files_manually)
        self.btn_remove_files.clicked.connect(self.files_list.remove_selected_files)

    def on_files_dropped(self, files):
        """Gère les fichiers déposés par drag & drop"""
        for file_path in files:
            if self.validate_file(file_path):
                self.files_list.add_file(file_path)
                self.files_to_upload.append(file_path)

    def add_files_manually(self):
        """Ajoute des fichiers via le dialogue de sélection"""
        files, _ = QFileDialog.getOpenFileNames(
            self, 
            "Sélectionner des fichiers",
            "",
            "Tous les fichiers (*);;Documents (*.pdf *.doc *.docx);;Images (*.jpg *.jpeg *.png *.gif);;Textes (*.txt *.rtf)"
        )
        
        for file_path in files:
            if self.validate_file(file_path):
                self.files_list.add_file(file_path)
                self.files_to_upload.append(file_path)

    def validate_file(self, file_path):
        """Valide un fichier avant l'ajout"""
        # Vérifier la taille (max 10 MB)
        file_size = os.path.getsize(file_path)
        if file_size > 10 * 1024 * 1024:  # 10 MB
            QMessageBox.warning(self, "⚠️ Fichier trop volumineux", 
                              f"Le fichier {os.path.basename(file_path)} dépasse la limite de 10 MB.")
            return False
        
        # Vérifier si le fichier est déjà dans la liste
        if file_path in self.files_to_upload:
            QMessageBox.information(self, "ℹ️ Fichier déjà ajouté", 
                                  f"Le fichier {os.path.basename(file_path)} est déjà dans la liste.")
            return False
        
        return True

    def charger_utilisateurs(self):
        """Charge la liste des utilisateurs dans le combobox"""
        try:
            utilisateurs = db.lister_utilisateurs()
            self.responsable_input.clear()
            self.responsable_input.addItem("-- Sélectionner un responsable --", None)
            for utilisateur in utilisateurs:
                self.responsable_input.addItem(f"{utilisateur[1]} ({utilisateur[2]})", utilisateur[0])
        except Exception as e:
            print(f"Erreur lors du chargement des utilisateurs: {e}")

    def fill_form_with_data(self, dossier_data):
        """Remplit le formulaire avec les données existantes"""
        self.nom_input.setText(dossier_data[1])  # nom_personne
        index = self.etat_input.findText(dossier_data[2])  # etat_personne
        if index >= 0:
            self.etat_input.setCurrentIndex(index)
        self.localisation_input.setText(dossier_data[3])  # localisation
        
        # Date
        try:
            date = QDate.fromString(dossier_data[4], "yyyy-MM-dd")
            self.date_input.setDate(date)
        except:
            self.date_input.setDate(QDate.currentDate())
        
        self.commentaire_input.setPlainText(dossier_data[5] or "")  # commentaire
        
        # Responsable
        if dossier_data[6]:  # responsable_id
            for i in range(self.responsable_input.count()):
                if self.responsable_input.itemData(i) == dossier_data[6]:
                    self.responsable_input.setCurrentIndex(i)
                    break
        
        # Niveau de confidentialité
        if dossier_data[7]:  # niveau_confidentialite
            index = self.niveau_confidentialite_input.findText(dossier_data[7])
            if index >= 0:
                self.niveau_confidentialite_input.setCurrentIndex(index)

    def get_data(self):
        """Retourne les données du formulaire et la liste des fichiers"""
        responsable_id = self.responsable_input.currentData()
        dossier_data = (
            self.nom_input.text(),
            self.etat_input.currentText(),
            self.localisation_input.text(),
            self.date_input.date().toString("yyyy-MM-dd"),
            self.commentaire_input.toPlainText(),
            responsable_id,
            self.niveau_confidentialite_input.currentText()
        )
        
        return dossier_data, self.files_to_upload 