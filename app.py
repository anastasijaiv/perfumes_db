import tkinter as tk
from tkinter import ttk


from funkcijas import (
    add_brand,
    add_perfume,
    add_wear,
)

def addBrandFromWindow():
    name = brand_name_input.get()
    country = brand_country_input.get()
    year = brand_year_input.get()

    add_brand(name, country, year)

    brand_name_input.delete(0, tk.END)
    brand_country_input.delete(0, tk.END)
    brand_year_input.delete(0, tk.END)

    brand_result.config(text = "Brends pievienots")


def addPerfumeFromWindow():
    brand_id = brand_id_input.get()
    name = perfume_name_input.get()
    price = price_input.get()

    add_perfume(brand_id, name, price)

    brand_id_input.delete(0, tk.END)
    perfume_name_input.delete(0, tk.END)
    price_input.delete(0, tk.END)

    perfume_result.config(text = "Parfīms pievienots")


def addWearFromWindow():
    perfume_id = perfume_id_input.get()
    date = wear_date_input.get()
    occasion = occasion_input.get()

    add_wear(perfume_id, date, occasion)

    perfume_id_input.delete(0, tk.END)
    wear_date_input.delete(0, tk.END)
    occasion_input.delete(0, tk.END)

    wear_result.config(text = "Ieraksts pievienots")




window = tk.Tk()

window.title("Parfīmu kolekcijas datubāze")
window.geometry("800x800")

tabs = ttk.Notebook(window)
tabs.pack(fill="both", expand= True)

perfume_tab = ttk.Frame(tabs)
brand_tab = ttk.Frame(tabs)

tabs.add(perfume_tab, text="Parfīmi")
tabs.add(brand_tab, text="Brendi")

header = tk.Label(
    window,
    text = "Parfīmu kolekcijas datubāze",
    font = ("Arial", 20, "bold")
)
header.pack(pady=20)

brand_block = tk.LabelFrame(
    window,
    text="Pievienot brendu",
    padx = 10,
    pady = 10
)
brand_block.pack(fill="x", padx = 20, pady = 10)

tk.Label(brand_block, text = "Nosaukums").pack()
brand_name_input = tk.Entry(brand_block, width=40)
brand_name_input.pack(pady = 5)

tk.Label(brand_block, text = "Valsts").pack()
brand_country_input = tk.Entry(brand_block, width=40)
brand_country_input.pack(pady = 5)

tk.Label(brand_block, text = "Dibināšanas gads").pack()
brand_year_input = tk.Entry(brand_block, width=40)
brand_year_input.pack(pady = 5)

brand_button = tk.Button(brand_block, text = "Pievienot brendu", command=addBrandFromWindow)
brand_button.pack(pady=5)

brand_result = tk.Label(
    brand_block, text = "", fg="green"
)
brand_result.pack(pady=5)



perfume_block = tk.LabelFrame(
    window,
    text="Pievienot parfīmu",
    padx = 10,
    pady = 10
)
perfume_block.pack(fill="x", padx = 20, pady = 10)

tk.Label(perfume_block, text = "Brenda ID").pack()
brand_id_input = tk.Entry(perfume_block, width=40)
brand_id_input.pack(pady = 5)

tk.Label(perfume_block, text = "Nosaukums").pack()
perfume_name_input = tk.Entry(perfume_block, width=40)
perfume_name_input.pack(pady = 5)

tk.Label(perfume_block, text = "Cena").pack()
price_input = tk.Entry(perfume_block, width=40)
price_input.pack(pady = 5)

perfume_button = tk.Button(perfume_block, text = "Pievienot parfīmu", command=addPerfumeFromWindow)
perfume_button.pack(pady=5)

perfume_result = tk.Label(
    perfume_block, text = "", fg="green"
)
perfume_result.pack(pady=5)



wear_block = tk.LabelFrame(
    window,
    text="Pievienot valkāšanas ierakstu",
    padx = 10,
    pady = 10
)
wear_block.pack(fill="x", padx = 20, pady = 10)

tk.Label(wear_block, text = "Parfīma ID").pack()
perfume_id_input = tk.Entry(wear_block, width=40)
perfume_id_input.pack(pady = 5)

tk.Label(wear_block, text = "Datums").pack()
wear_date_input = tk.Entry(wear_block, width=40)
wear_date_input.pack(pady = 5)

tk.Label(wear_block, text = "Pasākums (School / Work / Everyday)").pack()
occasion_input = tk.Entry(wear_block, width=40)
occasion_input.pack(pady = 5)

wear_button = tk.Button(wear_block, text = "Pievienot ierakstu", command=addWearFromWindow)
wear_button.pack(pady=5)

wear_result = tk.Label(
    wear_block, text = "", fg="green"
)
wear_result.pack(pady=5)


window.mainloop()