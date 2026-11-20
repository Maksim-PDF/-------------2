from openpyxl import Workbook
from app.models import Order
from app.logic import calculate_total

def export_to_excel(order: Order, filename="check.xlsx"):
    wb = Workbook()
    ws = wb.active
    ws.title = "Чек"

    ws.append(["Блюдо", "Цена", "Время готовки"])
    for item in order.items:
        ws.append([item.name, item.price, item.cooking_time])
        
    ws.append(["Итого со скидкой:", calculate_total(order)])
    wb.save(filename)
    print(f"Чек сохранен в файл {filename}")
