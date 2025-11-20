# Styles et constantes globales pour l'interface PyQt5

STYLE_SHEET = """
QMainWindow {
    background-color: #f5f5f5;
}

QPushButton {
    background-color: #2196F3;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
    min-width: 80px;
}

QPushButton:hover {
    background-color: #1976D2;
}

QPushButton:pressed {
    background-color: #0D47A1;
}

QPushButton[warning="true"] {
    background-color: #f44336;
}

QPushButton[warning="true"]:hover {
    background-color: #d32f2f;
}

QPushButton[success="true"] {
    background-color: #4CAF50;
}

QPushButton[success="true"]:hover {
    background-color: #388E3C;
}

QLineEdit, QComboBox, QTextEdit, QDateEdit, QDateTimeEdit {
    padding: 6px;
    border: 2px solid #ddd;
    border-radius: 4px;
    background-color: white;
}

QLineEdit:focus, QComboBox:focus, QTextEdit:focus, QDateEdit:focus, QDateTimeEdit:focus {
    border-color: #2196F3;
}

QTableWidget {
    background-color: white;
    alternate-background-color: #f9f9f9;
    gridline-color: #ddd;
    border: 1px solid #ddd;
    border-radius: 4px;
}

QTableWidget::item {
    padding: 8px;
    border-bottom: 1px solid #eee;
}

QTableWidget::item:selected {
    background-color: #e3f2fd;
    color: black;
}

QHeaderView::section {
    background-color: #2196F3;
    color: white;
    padding: 8px;
    border: none;
    font-weight: bold;
}

QLabel {
    color: #333;
    font-weight: bold;
}

QDialog {
    background-color: #f5f5f5;
}

.user-info {
    background-color: #e8f5e8;
    color: #2e7d32;
    padding: 8px;
    border-radius: 4px;
    border: 1px solid #4caf50;
    font-weight: bold;
}

.search-box {
    background-color: white;
    border: 2px solid #ddd;
    border-radius: 4px;
    padding: 8px;
}

.title-label {
    font-size: 16px;
    font-weight: bold;
    color: #1976D2;
    margin: 10px 0;
}
"""

ETATS_DOSSIERS = ["Actif", "Retraité", "Décédé", "Archivé", "En cours", "Terminé", "Suspendu"]
TYPES_MOUVEMENTS = ["Prise", "Retour", "Transfert", "Consultation", "Archivage", "Modification"]
NIVEAUX_CONFIDENTIALITE = ["Public", "Interne", "Confidentiel", "Secret"] 