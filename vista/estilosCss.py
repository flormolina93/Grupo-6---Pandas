
estiloBoton = """
    QPushButton {
    background-color: #e0a7a7;
    color: white;
    font-size: 14px;
    font-weight: bold;
    padding: 10px 20px;
    border: 2px solid #d473cf;
    border-radius: 12px;
    min-width: 120px;
    min-height: 40px;
    text-align: center;
    }

    QPushButton:hover {
        background-color: #c88d8d;
        }
    """

estiloTitulo = """
        font-size: 18px;
        font-weight: bold;
        color: #a15c5c;
        text-align: center;
    """

estilosContenedorPrincipal ="""
        background-color: #f1d7d8;
        border-radius: 20px;
        padding: 30px;
        margin: 20px;
        border: 2px solid #e0a7a7;
    """

estiloTabla = """
    QTableWidget {
        background-color: #f9f5f6;
        border: 1px solid #e0a7a7;
        border-radius: 10px;
        gridline-color: #e0a7a7;
        font-size: 20px;
    }

    QHeaderView::section {
        background-color: #e0a7a7;
        color: white;
        padding: 8px;
        font-weight: bold;
        font-size: 20px;
        border: 1px solid #d39595;
    }

    QTableWidget::item {
        padding: 5px;
        border: none;
    }

    QTableWidget::item:selected {
        background-color: #f1d7d8;
        color: black;
    }

    QTableCornerButton::section {
        background-color: #e0a7a7;
        border: 1px solid #d39595;
    }
"""

estiloInput = """
    QLineEdit {
        background-color: #f9f5f6;
        border: 2px solid #e0a7a7;
        border-radius: 12px;
        padding: 8px 12px;
        font-size: 14px;
        color: #2f2933;
    }

    QLineEdit:focus {
        border: 2px solid #a15c5c;
        background-color: #ffffff;
    }
"""

estilosForm = """
    QWidget {
        background-color: #f0f4f8;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 14px;
        color: #333333;
    }

    QLineEdit, QComboBox, QDateEdit, QTimeEdit {
        border: 2px solid #a1c4fd;
        border-radius: 8px;
        padding: 6px 10px;
        background-color: white;
        selection-background-color: #74a9ff;
        selection-color: white;
        font-size: 14px;
    }
    QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QTimeEdit:focus {
        border-color: #3a8dde;
        background-color: #e6f0ff;
    }

    QPushButton {
        background-color: #3a8dde;
        color: white;
        border-radius: 10px;
        padding: 10px;
        font-weight: bold;
        font-size: 16px;
    }
    QPushButton:hover {
        background-color: #2c6cc9;
    }
    QPushButton:pressed {
        background-color: #1e4f96;
    }

    QLabel {
        font-size: 13px;
        color: #555555;
    }
"""