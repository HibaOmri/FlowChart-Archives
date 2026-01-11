# Styles et constantes globales pour l'interface PyQt5

STYLE_SHEET = """
QMainWindow {
    background-color: #f5f7fa;
}

/* --- Boutons Généraux --- */
QPushButton {
    background-color: #2196F3;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 6px;
    font-weight: bold;
    min-width: 80px;
}
QPushButton:hover {
    background-color: #1976D2;
}
QPushButton:pressed {
    background-color: #0D47A1;
}

/* Boutons Warning (Supprimer/Annuler) */
QPushButton[warning="true"] {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #F44336, stop:1 #D32F2F);
}
QPushButton[warning="true"]:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #D32F2F, stop:1 #C62828);
}

/* Boutons Success (Valider/Ajouter) */
QPushButton[success="true"] {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #4CAF50, stop:1 #388E3C);
}
QPushButton[success="true"]:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #388E3C, stop:1 #2E7D32);
}

/* --- Champs de saisie --- */
QLineEdit, QComboBox, QTextEdit, QDateEdit, QDateTimeEdit {
    padding: 8px 12px;
    border: 2px solid #E0E0E0;
    border-radius: 8px;
    background-color: white;
    color: #333;
    font-size: 13px;
}

QLineEdit:focus, QComboBox:focus, QTextEdit:focus, QDateEdit:focus, QDateTimeEdit:focus {
    border-color: #1976D2;
    background-color: #FFFFFF;
}

QLineEdit:hover, QComboBox:hover {
    border-color: #BDBDBD;
}

/* --- Tableaux --- */
QTableWidget {
    background-color: white;
    alternate-background-color: #f8f9fa;
    gridline-color: #f0f0f0;
    border: 1px solid #E0E0E0;
    border-radius: 8px;
    selection-background-color: #E3F2FD;
    selection-color: #1976D2;
}

QTableWidget::item {
    padding: 8px;
    border-bottom: 1px solid #F5F5F5;
}

QHeaderView::section {
    background-color: #F8F9FA;
    color: #444;
    padding: 10px;
    border: none;
    border-bottom: 2px solid #ddd;
    font-weight: bold;
    font-size: 13px;
}

/* --- Labels et Textes --- */
QLabel {
    color: #333;
}

.title-label {
    font-size: 18px;
    font-weight: bold;
    color: #2c3e50;
    margin: 15px 0 10px 0;
}

.section-label {
    font-weight: bold;
    color: #1976D2;
    font-size: 14px;
}

/* --- Composants Spécifiques --- */
.user-info {
    background-color: white;
    color: #2c3e50;
    padding: 8px 15px;
    border-radius: 20px;
    border: 1px solid #e0e0e0;
    font-weight: bold;
}

.stats-label {
    color: #555;
    font-size: 12px;
    font-weight: bold;
    padding: 6px 15px;
    background: #fff;
    border-radius: 15px;
    border: 1px solid #E0E0E0;
}

/* --- ComboBox Dropdown --- */
QComboBox::drop-down {
    border: none;
    width: 30px;
}
QComboBox::down-arrow {
    image: none;
    border: none;
    color: #555;
}

/* --- ScrollBar --- */
QScrollBar:vertical {
    border: none;
    background: #f1f1f1;
    width: 10px;
    margin: 0px 0px 0px 0px;
}
QScrollBar::handle:vertical {
    background: #c1c1c1;
    min-height: 20px;
    border-radius: 5px;
}
QScrollBar::handle:vertical:hover {
    background: #a8a8a8;
}
"""

# Couleurs pour les statuts
STATUS_COLORS = {
    'actif': {'bg': '#E8F5E8', 'text': '#2E7D32', 'border': '#4CAF50'},
    'retraité': {'bg': '#FFF3E0', 'text': '#E65100', 'border': '#FF9800'},
    'décédé': {'bg': '#F3E5F5', 'text': '#7B1FA2', 'border': '#9C27B0'},
    'non-actif': {'bg': '#F5F5F5', 'text': '#616161', 'border': '#9E9E9E'}
}

# Styles pour les cartes d'action (boutons)
ACTION_CARD_STYLE = """
QPushButton {
    background-color: white;
    border: 1px solid #E0E0E0;
    border-radius: 12px;
    text-align: center;
}
QPushButton:hover {
    background-color: #F8F9FA;
    border-color: %s;
}
QPushButton:pressed {
    background-color: #E3F2FD;
}
"""

ETATS_DOSSIERS = ["Actif", "Retraité", "Décédé", "Archivé", "En cours", "Terminé", "Suspendu"]
TYPES_MOUVEMENTS = ["Prise", "Retour", "Transfert", "Consultation", "Archivage", "Modification"]
NIVEAUX_CONFIDENTIALITE = ["Public", "Interne", "Confidentiel", "Secret"] 