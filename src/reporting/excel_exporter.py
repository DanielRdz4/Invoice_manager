
from openpyxl import Workbook
from datetime import datetime
from src.persistence.database import get_connection
from src.core.paths import XLSX_PATH

def db_to_xlsx():
    """Reads .db file ando converts it to xlsx"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM invoices")
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]

    wb = Workbook()
    ws = wb.active
    ws.title = "Invoices"

    ws.append(column_names)

    date_col_index = column_names.index("fecha")  # nombre real de tu columna

    for row in rows:
        row = list(row)

        raw_date = row[date_col_index]
        if raw_date:
            dt = datetime.fromisoformat(raw_date)
            row[date_col_index] = dt.date()  # ← elimina la hora

        ws.append(row)

    # formato de fecha en Excel
    for cell in ws.iter_cols(min_col=date_col_index+1, max_col=date_col_index+1, min_row=2):
        for c in cell:
            c.number_format = "yyyy-mm-dd"

    wb.save(XLSX_PATH)
    conn.close()