from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                             QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
                             QFileDialog, QLineEdit, QTextEdit, QFrame, QSplitter, QWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from .styles import STYLE_SHEET
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '../backend'))
import db
import shutil

class GestionPiecesJointesDialog(QDialog):
    def __init__(self, id_dossier, nom_dossier, parent=None):
        super().__init__(parent)
        self.id_dossier = id_dossier
        self.nom_dossier = nom_dossier
        self.setWindowTitle(f"Pièces jointes - {nom_dossier}")
        self.setModal(True)
        self.resize(800, 600)
        self.setStyleSheet(STYLE_SHEET)
        
        # Créer le dossier pour les pièces jointes s'il n'existe pas
        self.dossier_pieces = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'pieces_jointes', str(id_dossier))
        os.makedirs(self.dossier_pieces, exist_ok=True)
        
        self.setup_ui()
        self.charger_pieces_jointes()

    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Titre
        title_label = QLabel(f"📎 Pièces jointes - {self.nom_dossier}")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-weight: bold; font-size: 18px; margin: 10px; color: #1976D2;")
        layout.addWidget(title_label)
        
        # Section d'ajout de fichiers
        add_section = QFrame()
        add_section.setStyleSheet("""
            QFrame {
                background: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        add_layout = QVBoxLayout()
        
        add_title = QLabel("Ajouter un fichier")
        add_title.setStyleSheet("font-weight: bold; font-size: 14px; color: #495057; margin-bottom: 10px;")
        add_layout.addWidget(add_title)
        
        # Boutons d'ajout
        btn_layout = QHBoxLayout()
        self.btn_ajouter_fichier = QPushButton("📁 Sélectionner un fichier")
        self.btn_ajouter_fichier.setStyleSheet("""
            QPushButton {
                background: #28a745;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #218838;
            }
        """)
        self.btn_ajouter_fichier.clicked.connect(self.ajouter_fichier)
        
        self.btn_ajouter_dossier = QPushButton("📂 Sélectionner un dossier")
        self.btn_ajouter_dossier.setStyleSheet("""
            QPushButton {
                background: #17a2b8;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #138496;
            }
        """)
        self.btn_ajouter_dossier.clicked.connect(self.ajouter_dossier)
        
        btn_layout.addWidget(self.btn_ajouter_fichier)
        btn_layout.addWidget(self.btn_ajouter_dossier)
        btn_layout.addStretch()
        add_layout.addLayout(btn_layout)
        
        add_section.setLayout(add_layout)
        layout.addWidget(add_section)
        
        # Tableau des pièces jointes
        table_label = QLabel("📋 Fichiers attachés")
        table_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #495057; margin: 10px 0;")
        layout.addWidget(table_label)
        
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "📄 Nom", "📊 Taille", "📅 Date ajout", "📝 Description", "🔗 Chemin", "⚙️ Actions"
        ])
        
        # Ajuster les colonnes
        header = self.table.horizontalHeader()
        if header:
            header.setSectionResizeMode(0, QHeaderView.Stretch)  # Nom
            header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Taille
            header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Date
            header.setSectionResizeMode(3, QHeaderView.Stretch)  # Description
            header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Chemin
            header.setSectionResizeMode(5, QHeaderView.Fixed)  # Actions
            header.resizeSection(5, 120)
        
        layout.addWidget(self.table)
        
        # Boutons de fermeture
        btn_close_layout = QHBoxLayout()
        self.btn_fermer = QPushButton("❌ Fermer")
        self.btn_fermer.setStyleSheet("""
            QPushButton {
                background: #6c757d;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #5a6268;
            }
        """)
        self.btn_fermer.clicked.connect(self.accept)
        btn_close_layout.addStretch()
        btn_close_layout.addWidget(self.btn_fermer)
        layout.addLayout(btn_close_layout)
        
        self.setLayout(layout)

    def ajouter_fichier(self):
        """Ajoute un fichier au dossier"""
        fichier, _ = QFileDialog.getOpenFileName(
            self, 
            "Sélectionner un fichier", 
            "", 
            "Tous les fichiers (*.*);;Documents (*.pdf *.doc *.docx);;Images (*.jpg *.jpeg *.png *.gif);;Vidéos (*.mp4 *.avi *.mov)"
        )
        
        if fichier:
            self.copier_fichier(fichier)

    def ajouter_dossier(self):
        """Ajoute tous les fichiers d'un dossier"""
        dossier = QFileDialog.getExistingDirectory(self, "Sélectionner un dossier")
        
        if dossier:
            fichiers_ajoutes = 0
            for root, dirs, files in os.walk(dossier):
                for file in files:
                    chemin_complet = os.path.join(root, file)
                    if self.copier_fichier(chemin_complet, silent=True):
                        fichiers_ajoutes += 1
            
            if fichiers_ajoutes > 0:
                QMessageBox.information(self, "✅ Succès", f"{fichiers_ajoutes} fichier(s) ajouté(s) avec succès !")
                self.charger_pieces_jointes()

    def copier_fichier(self, chemin_source, silent=False):
        """Copie un fichier vers le dossier des pièces jointes"""
        try:
            nom_fichier = os.path.basename(chemin_source)
            extension = os.path.splitext(nom_fichier)[1].lower()
            
            # Générer un nom unique si le fichier existe déjà
            nom_destination = nom_fichier
            compteur = 1
            while os.path.exists(os.path.join(self.dossier_pieces, nom_destination)):
                nom_sans_ext = os.path.splitext(nom_fichier)[0]
                nom_destination = f"{nom_sans_ext}_{compteur}{extension}"
                compteur += 1
            
            chemin_destination = os.path.join(self.dossier_pieces, nom_destination)
            
            # Copier le fichier
            shutil.copy2(chemin_source, chemin_destination)
            
            # Ajouter à la base de données
            type_fichier = self.determiner_type_fichier(extension)
            db.ajouter_piece_jointe(
                self.id_dossier, 
                nom_destination, 
                chemin_destination, 
                type_fichier
            )
            
            if not silent:
                QMessageBox.information(self, "✅ Succès", f"Fichier '{nom_destination}' ajouté avec succès !")
                self.charger_pieces_jointes()
            
            return True
            
        except Exception as e:
            if not silent:
                QMessageBox.warning(self, "❌ Erreur", f"Erreur lors de l'ajout du fichier :\n{str(e)}")
            return False

    def determiner_type_fichier(self, extension):
        """Détermine le type de fichier basé sur l'extension"""
        types = {
            '.pdf': 'Document PDF',
            '.doc': 'Document Word',
            '.docx': 'Document Word',
            '.xls': 'Document Excel',
            '.xlsx': 'Document Excel',
            '.jpg': 'Image JPEG',
            '.jpeg': 'Image JPEG',
            '.png': 'Image PNG',
            '.gif': 'Image GIF',
            '.mp4': 'Vidéo MP4',
            '.avi': 'Vidéo AVI',
            '.mov': 'Vidéo MOV',
            '.txt': 'Fichier texte',
            '.zip': 'Archive ZIP',
            '.rar': 'Archive RAR'
        }
        return types.get(extension.lower(), 'Fichier')

    def charger_pieces_jointes(self):
        """Charge la liste des pièces jointes"""
        try:
            pieces = db.lister_pieces_jointes(self.id_dossier)
            self.table.setRowCount(len(pieces))
            
            for row, piece in enumerate(pieces):
                # Nom du fichier
                nom_item = QTableWidgetItem(piece[1])
                self.table.setItem(row, 0, nom_item)
                
                # Taille
                taille = db.formater_taille_fichier(piece[4]) if piece[4] else "0 B"
                taille_item = QTableWidgetItem(taille)
                self.table.setItem(row, 1, taille_item)
                
                # Date d'ajout
                date_ajout = piece[5] if piece[5] else "N/A"
                date_item = QTableWidgetItem(str(date_ajout))
                self.table.setItem(row, 2, date_item)
                
                # Description
                description = piece[6] if piece[6] else ""
                desc_item = QTableWidgetItem(description)
                self.table.setItem(row, 3, desc_item)
                
                # Chemin (caché mais accessible)
                chemin_item = QTableWidgetItem(piece[2])
                self.table.setItem(row, 4, chemin_item)
                
                # Actions
                actions_widget = QWidget()
                actions_layout = QHBoxLayout()
                actions_layout.setContentsMargins(2, 2, 2, 2)
                
                btn_ouvrir = QPushButton("👁️")
                btn_ouvrir.setToolTip("Ouvrir le fichier")
                btn_ouvrir.setStyleSheet("""
                    QPushButton {
                        background: #007bff;
                        color: white;
                        border: none;
                        border-radius: 3px;
                        padding: 4px 8px;
                        font-size: 10px;
                    }
                    QPushButton:hover {
                        background: #0056b3;
                    }
                """)
                btn_ouvrir.clicked.connect(lambda checked, p=piece: self.ouvrir_fichier(p))
                
                btn_supprimer = QPushButton("🗑️")
                btn_supprimer.setToolTip("Supprimer le fichier")
                btn_supprimer.setStyleSheet("""
                    QPushButton {
                        background: #dc3545;
                        color: white;
                        border: none;
                        border-radius: 3px;
                        padding: 4px 8px;
                        font-size: 10px;
                    }
                    QPushButton:hover {
                        background: #c82333;
                    }
                """)
                btn_supprimer.clicked.connect(lambda checked, p=piece: self.supprimer_fichier(p))
                
                actions_layout.addWidget(btn_ouvrir)
                actions_layout.addWidget(btn_supprimer)
                actions_layout.addStretch()
                actions_widget.setLayout(actions_layout)
                
                self.table.setCellWidget(row, 5, actions_widget)
                
        except Exception as e:
            QMessageBox.warning(self, "❌ Erreur", f"Erreur lors du chargement des pièces jointes :\n{str(e)}")

    def ouvrir_fichier(self, piece):
        """Ouvre un fichier avec l'application par défaut"""
        try:
            import subprocess
            import platform
            
            chemin_fichier = piece[2]
            if os.path.exists(chemin_fichier):
                if platform.system() == "Windows":
                    os.startfile(chemin_fichier)
                elif platform.system() == "Darwin":  # macOS
                    subprocess.run(["open", chemin_fichier])
                else:  # Linux
                    subprocess.run(["xdg-open", chemin_fichier])
            else:
                QMessageBox.warning(self, "❌ Erreur", "Le fichier n'existe plus sur le disque.")
        except Exception as e:
            QMessageBox.warning(self, "❌ Erreur", f"Impossible d'ouvrir le fichier :\n{str(e)}")

    def supprimer_fichier(self, piece):
        """Supprime une pièce jointe"""
        nom_fichier = piece[1]
        id_piece = piece[0]
        
        reply = QMessageBox.question(
            self, 
            "⚠️ Confirmation", 
            f"Voulez-vous vraiment supprimer le fichier '{nom_fichier}' ?\n\nCette action est irréversible !",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                db.supprimer_piece_jointe(id_piece)
                QMessageBox.information(self, "✅ Succès", f"Fichier '{nom_fichier}' supprimé avec succès !")
                self.charger_pieces_jointes()
            except Exception as e:
                QMessageBox.warning(self, "❌ Erreur", f"Erreur lors de la suppression :\n{str(e)}") 