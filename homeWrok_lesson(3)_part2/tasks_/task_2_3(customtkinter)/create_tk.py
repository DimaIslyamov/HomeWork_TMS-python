import customtkinter
from task_2.calculation_of_payments import calculation_of_payments

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

app = customtkinter.CTk()
app.geometry("500x450")
app.title("Home Work")


# Button functions
def calculation_payment_button_clicked():
    try:
        i = float(tab_one_entry_i.get())
        s = float(tab_one_entry_s.get())
        n = int(tab_one_entry_n.get())

        m, user_total_count, overpayment_amount = calculation_of_payments(i=i, s=s, n=n)
        tab_oneLabel.configure(text=f"Ежемесячный платёж: {m:.2f}\n"
                                    f"Всего выплат: {user_total_count:.2f}\n"
                                    f"Переплата: {overpayment_amount:.2f}")

        tab_one_entry_i.delete(0, "end")
        tab_one_entry_s.delete(0, "end")
        tab_one_entry_n.delete(0, "end")

    except ValueError:
        tab_oneLabel.configure(text="Пожалуйста введите 'Цифры'")


root = customtkinter.CTkFrame(master=app, corner_radius=10)
root.pack(pady=10, padx=10, fill="both", expand=True)

# Create table View
table_view = customtkinter.CTkTabview(master=root,
                                      width=400,
                                      height=200,
                                      corner_radius=10,
                                      )
table_view.pack(pady=15, padx=15)

# adds table names
tab_one = table_view.add(" Подсчет Кредитования ")
tab_two = table_view.add(" Интерстеллар ")

# Create table one inputs, label and button
tab_oneLabel = customtkinter.CTkLabel(master=tab_one,
                                      text="Играл с кредитами – проиграл")
tab_oneLabel.pack(pady=10)
tab_one_entry_i = customtkinter.CTkEntry(master=tab_one,
                                         placeholder_text="Введите годовую ставку",
                                         width=200)
tab_one_entry_i.pack(pady=10, padx=10)
tab_one_entry_s = customtkinter.CTkEntry(master=tab_one,
                                         placeholder_text="Сумма займа",
                                         width=200)
tab_one_entry_s.pack(pady=10, padx=10)
tab_one_entry_n = customtkinter.CTkEntry(master=tab_one,
                                         placeholder_text="На сколько месяцев кредит",
                                         width=200)
tab_one_entry_n.pack(pady=10, padx=10)
tab_one_button = customtkinter.CTkButton(master=tab_one,
                                         text="Подсчитать",
                                         command=calculation_payment_button_clicked)
tab_one_button.pack(pady=20)

# Get values
user_value_i = tab_one_entry_i.get()
user_value_s = tab_one_entry_s.get()
user_value_n = tab_one_entry_n.get()

# Create table two label,inputs and button
tab_two_label = customtkinter.CTkLabel(master=tab_two,
                                       text="Введите данные первой планеты")
tab_two_label.pack(pady=10)
tab_two_r = customtkinter.CTkEntry(master=tab_two,
                                   placeholder_text="Радиус планеты",
                                   width=200)
tab_two_r.pack(pady=10, padx=10)
tab_two_v = customtkinter.CTkEntry(master=tab_two,
                                   placeholder_text="Орбитальная скорость",
                                   width=200)
tab_two_v.pack(pady=10, padx=10)

tab_two_button = customtkinter.CTkButton(master=tab_two,
                                         text="Ввод",)
tab_two_button.pack(pady=20)

app.mainloop()
