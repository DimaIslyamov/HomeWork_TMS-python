import customtkinter
from task_2.calculation_of_payments import calculation_of_payments
from task_3.interstellar_calculation import calculate_planets_year

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

app = customtkinter.CTk()
app.geometry("500x450")
app.title("Home Work")

planet_one = None


# get and clean_entry for def
def get_tale_one_entris():
    return (float(tab_one_entry_i.get()),
            float(tab_one_entry_s.get()),
            int(tab_one_entry_n.get()))

def clean_table_one_entris():
    return (tab_one_entry_i.delete(0, "end"),
            tab_one_entry_s.delete(0, "end"),
            tab_one_entry_n.delete(0, "end"))


def get_table_two_entris():
    return (float(tab_two_r.get()),
            float(tab_two_v.get()))

def clean_table_two_entris():
    return (tab_two_r.delete(0, "end"),
            tab_two_v.delete(0, "end"))


# Button functions
def calculation_payment_button_clicked():
    try:
        i, s, n = get_tale_one_entris()

        (monthly_payment,
         user_total_count,
         overpayment_amount) = calculation_of_payments(interest_rate=i,
                                                       loan_amount=s,
                                                       months_count=n)
        tab_one_label.configure(
            text=f"Ежемесячный платёж: {monthly_payment:.2f}\n"
            f"Всего выплат: {user_total_count:.2f}\n"
            f"Переплата: {overpayment_amount:.2f}")

        clean_table_one_entris()

    except ValueError:
        tab_one_label.configure(text="Введите числовые значения")


def calculation_of_interstellar_button_clicked():
    global planet_one

    try:
        r, v = get_table_two_entris()

        if planet_one is None:
            planet_one = (r, v)

            clean_table_two_entris()

            tab_two_label.configure(text="Первая планета сохранена. Введите данные второй")

        else:
            r1, v1 = planet_one

            planet_1 = calculate_planets_year(orbital_radius=r1, orbital_velocity=v1)
            planet_2 = calculate_planets_year(orbital_radius=r, orbital_velocity=v)

            tab_two_label.configure(
                text=f"Длинна года на первой планете: {planet_1:.4f}\n"
                     f"Длинна года на второй планете: {planet_2:.4f}\n"
                     f"На первой планете год длинна чем на второй? : {'Да' if planet_1 > planet_2 else 'Нет'}")

            clean_table_two_entris()

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

# === Create TAB 1 ===
tab_one_label = customtkinter.CTkLabel(master=tab_one,
                                       text="Играл с кредитами – проиграл")
tab_one_entry_i = customtkinter.CTkEntry(master=tab_one,
                                         placeholder_text="Введите годовую ставку",
                                         width=200)
tab_one_entry_s = customtkinter.CTkEntry(master=tab_one,
                                         placeholder_text="Сумма займа",
                                         width=200)
tab_one_entry_n = customtkinter.CTkEntry(master=tab_one,
                                         placeholder_text="На сколько месяцев кредит",
                                         width=200)
tab_one_button = customtkinter.CTkButton(master=tab_one,
                                         text="Подсчитать",
                                         command=calculation_payment_button_clicked)

for entry_one in (tab_one_label, tab_one_entry_i,
                  tab_one_entry_s, tab_one_entry_n,
                  tab_one_button):
    entry_one.pack(pady=10, padx=10)

# === Create TAB 2 ===
tab_two_label = customtkinter.CTkLabel(master=tab_two,
                                       text="Введите данные первой планеты")
tab_two_r = customtkinter.CTkEntry(master=tab_two,
                                   placeholder_text="Радиус планеты",
                                   width=200)
tab_two_v = customtkinter.CTkEntry(master=tab_two,
                                   placeholder_text="Орбитальная скорость",
                                   width=200)
tab_two_button = customtkinter.CTkButton(master=tab_two,
                                         text="Ввод",
                                         command=calculation_of_interstellar_button_clicked)

for entry_two in (tab_two_label, tab_two_r, tab_two_v,
                  tab_two_button):
    entry_two.pack(pady=10, padx=10)

app.mainloop()
