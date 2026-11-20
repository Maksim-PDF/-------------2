import tkinter as tk
from tkinter import messagebox
from app.models import Dish, Order
from app.logic import calculate_total, calculate_wait_time
from app.exporter import export_to_excel
from app.database import OrderDatabase

class RestaurantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ресторан - Расчет чека")
        self.root.geometry("500x600")

        # Создаем текущий заказ (пока пустой)
        self.current_order = None
        self.db = OrderDatabase()          # ← подключение к SQLite

        # Блок ввода 
        tk.Label(root, text="Введите номер столика:", font=("Arial", 12)).pack(pady=5)
        self.table_entry = tk.Entry(root)
        self.table_entry.pack()
        
        tk.Button(root, text="Создать заказ", command=self.create_order, bg="lightblue").pack(pady=10)

        # Блок меню
        tk.Label(root, text="Меню (нажмите, чтобы добавить):", font=("Arial", 12)).pack(pady=5)
        
        self.menu = [
            Dish("Паста Карбонара", 450, 15, 300),
            Dish("Стейк Рибай", 1200, 25, 400),
            Dish("Салат Цезарь", 350, 10, 200),
            Dish("Суп Том Ям", 500, 20, 350)
        ]

        for dish in self.menu:
            btn = tk.Button(root, text=f"{dish.name} - {dish.price} руб.", command=lambda d=dish: self.add_dish(d))
            btn.pack(pady=2, fill="x", padx=20)

        # Блок вывода
        self.text_area = tk.Text(root, height=10, width=50)
        self.text_area.pack(pady=10)

        # Блок кнопок расчета
        tk.Button(root, text="Рассчитать чек и сохранить", command=self.checkout, bg="lightgreen").pack(pady=10)

    def create_order(self):
        try:
            table_num = int(self.table_entry.get())
            self.current_order = Order(table_num)
            self.text_area.delete(1.0, tk.END) # Очищаем экран
            self.text_area.insert(tk.END, f"Создан заказ для столика {table_num}\n")
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректный номер столика!")

    def add_dish(self, dish):
        if self.current_order is None:
            messagebox.showwarning("Внимание", "Сначала создайте заказ!")
            return
        
        self.current_order.add_item(dish)
        self.text_area.insert(tk.END, f"+ Добавлено: {dish.name} ({dish.price} руб.)\n")

    def checkout(self):
        if not self.current_order or len(self.current_order) == 0:
            messagebox.showwarning("Внимание", "Заказ пуст!")
            return

        # Логика скидки: если блюд 3 и больше - даем 10%
        if len(self.current_order) >= 3 and self.current_order.discount == 0:
            self.current_order.discount = 0.1
            self.text_area.insert(tk.END, "\n*** Применена скидка 10% ***\n")

        total = calculate_total(self.current_order)
        wait_time = calculate_wait_time(self.current_order)

        self.text_area.insert(tk.END, f"\n ИТОГО \n")
        self.text_area.insert(tk.END, f"К оплате: {total} руб.\n")
        self.text_area.insert(tk.END, f"Время ожидания: {wait_time} мин.\n")
        
        # Сохранение в БД
        try:
            order_id = self.db.save_order(self.current_order, total, wait_time)
            self.text_area.insert(tk.END, f"Заказ сохранён в БД (id={order_id})\n")
        except Exception as e:
            messagebox.showerror("Ошибка БД", f"Не удалось сохранить заказ: {e}")

        # Экспорт в Excel
        try:
            export_to_excel(self.current_order, "check_gui.xlsx")
            messagebox.showinfo("Успех", "Чек сохранен в файл check_gui.xlsx!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RestaurantApp(root)
    root.mainloop()