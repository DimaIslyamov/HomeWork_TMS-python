import customtkinter
from task_2.calculation_of_payments import calculation_of_payments
from task_3.interstellar_calculation import calculate_planets_year

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

app = customtkinter.CTk()
app.geometry("500x450")
app.title("Home Work")

planet_one = None


# Button functions
def calculation_payment_button_clicked():
    try:
        i = float(tab_one_entry_i.get())
        s = float(tab_one_entry_s.get())
        n = int(tab_one_entry_n.get())

        (monthly_payment,
         user_total_count,
         overpayment_amount) = calculation_of_payments(interest_rate=i,
                                                       loan_amount=s,
                                                       months_count=n)
        tab_oneLabel.configure(
            text=f"Ежемесячный платёж: {monthly_payment:.2f}\n"
            f"Всего выплат: {user_total_count:.2f}\n"
            f"Переплата: {overpayment_amount:.2f}")

        tab_one_entry_i.delete(0, "end")
        tab_one_entry_s.delete(0, "end")
        tab_one_entry_n.delete(0, "end")

    except ValueError:
        tab_oneLabel.configure(text="Пожалуйста введите 'Цифры'")


def calculation_of_interstellar_button_clicked():
    global planet_one

    try:
        r = float(tab_two_r.get())
        v = float(tab_two_v.get())

        if planet_one is None:
            planet_one = (r, v)

            tab_two_r.delete(0, "end")
            tab_two_v.delete(0, "end")

            tab_two_label.configure(text="Первая планета сохранена. Введите данные второй")

        else:
            r1, v1 = planet_one

            planet_1 = calculate_planets_year(orbital_radius=r1, orbital_velocity=v1)
            planet_2 = calculate_planets_year(orbital_radius=r, orbital_velocity=v)

            tab_two_label.configure(
                text=f"Длинна года на первой планете: {planet_1:.4f}\n"
                     f"Длинна года на второй планете: {planet_2:.4f}\n"
                     f"На первой планете год длинна чем на второй? : {"Да" if planet_1 > planet_2 else "Нет"}")

            tab_two_r.delete(0, "end")
            tab_two_v.delete(0, "end")

            planet_one = None

    except ValueError:
        print("Ошибка ввода!")


# Root of tkinter
root = customtkinter.CTkFrame(master=app, corner_radius=10)
root.pack(pady=10, padx=10, fill="both", expand=True)

# Create table View
table_view = customtkinter.CTkTabview(master=root,
                                      width=400, height=200,
                                      corner_radius=10,)
table_view.pack(pady=15, padx=15)

# adds table names
tab_one = table_view.add("Подсчет Кредитования ")
tab_two = table_view.add("Интерстеллар ")

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
                                         text="Ввод",
                                         command=calculation_of_interstellar_button_clicked)
tab_two_button.pack(pady=20)

app.mainloop()
