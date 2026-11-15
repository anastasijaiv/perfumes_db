import tkinter as tk
from tkinter import ttk

from funkcijas import (
    add_brand,
    add_perfume,
    add_wear,
    add_rating,
    add_note,
    add_perfume_note,
    add_perfume_season,
    get_brand,
    get_perfume,
    get_wear,
    get_note,
    get_season,
    get_rating,
    get_perfume_note,
    get_perfume_season,
)
#Krāsa
BG = "#A4EAFF"
ACCENT = "#1BAEF1"
ACCENT_DARK = "#0C88C2"
ACCENT_LIGHT = "#75CBF3"
ERROR = "#E23D3D"


window = tk.Tk()
window.title("Mana Parfīmu Kolekcija")
window.geometry("800x900")
window.config(bg=BG)

window.update_idletasks()
screen_w = window.winfo_screenwidth()
screen_h = window.winfo_screenheight()
x = (screen_w - 800) // 2
y = max(0, (screen_h - 900) // 2)
window.geometry("800x900+" + str(x) + "+" + str(y))

main_canvas = tk.Canvas(window, bg=BG, highlightthickness=0)
scrollbar = tk.Scrollbar(window, orient="vertical", command=main_canvas.yview)
main_canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
main_canvas.pack(side="left", fill="both", expand=True)

main_frame = tk.Frame(main_canvas, bg=BG)
content_window = main_canvas.create_window((0, 0), window=main_frame, anchor="nw")
#Lai būtu centrā
def center_content(event=None):
    canvas_w = main_canvas.winfo_width()
    content_w = main_frame.winfo_reqwidth()
    if canvas_w > content_w:
        x = (canvas_w - content_w) // 2
    else:
        x = 0
    main_canvas.coords(content_window, x, 0)


def on_configure(event):

    main_canvas.configure(scrollregion=main_canvas.bbox("all"))
    center_content()


main_frame.bind("<Configure>", on_configure)
main_canvas.bind("<Configure>", center_content)


def on_mousewheel(event):

    steps = max(1, abs(event.delta) // 120)
    if event.delta > 0:
        main_canvas.yview_scroll(-steps, "units")
    else:
        main_canvas.yview_scroll(steps, "units")


main_canvas.bind_all("<MouseWheel>", on_mousewheel)

header = tk.Label(main_frame, text="Mana Parfīmu Kolekcija",
                  font=("Arial", 20, "bold"), bg=BG, fg=ACCENT)
header.pack(pady=(15, 5))

try:
    logo_big = tk.PhotoImage(file="perfumebgg.png")
    logo = logo_big.subsample(2)
    logo_label = tk.Label(main_frame, image=logo, bg=BG)
    logo_label.pack(pady=5)
except Exception:
    pass
tabs = ttk.Notebook(main_frame)
tabs.pack(fill="both", expand=True, padx=10, pady=10)

brand_tab = tk.Frame(tabs, bg=BG)
tabs.add(brand_tab, text="Brendi")

perfume_tab = tk.Frame(tabs, bg=BG)
tabs.add(perfume_tab, text="Parfīmi")

def create_table(parent, headers, widths, height):
    columns = []
    for i in range(len(headers)):
        columns.append("c" + str(i))
    table = ttk.Treeview(parent, columns=columns, show="headings", height=height)
    for i in range(len(headers)):
        table.heading("c" + str(i), text=headers[i])
        table.column("c" + str(i), width=widths[i], anchor="center")
    table.pack(fill="x", padx=5, pady=5)
    return table

def eu_datums(datums):
    parts = str(datums).split("-")
    if len(parts) == 3:
        return parts[2] + "-" + parts[1] + "-" + parts[0]
    return str(datums)

def iso_datums(datums):
    parts = str(datums).strip().split("-")
    if len(parts) == 3 and len(parts[0]) == 2:
        return parts[2] + "-" + parts[1] + "-" + parts[0]
    return str(datums)


def showBrands():
    for row in brand_table.get_children():
        brand_table.delete(row)
    for brand in get_brand():
        brand_table.insert("", "end", values=brand)


def showPerfumes():
    for row in perfume_table.get_children():
        perfume_table.delete(row)
    for perfume in get_perfume():
        perfume_table.insert("", "end", values=perfume)


def showWears():
    for row in wear_table.get_children():
        wear_table.delete(row)
    for wear in get_wear():
        rinda = (wear[0], wear[1], eu_datums(wear[2]), wear[3])
        wear_table.insert("", "end", values=rinda)


def showRatings():
    for row in rating_table.get_children():
        rating_table.delete(row)
    for rating in get_rating():
        rating_table.insert("", "end", values=rating)


def showNotes():
    for row in note_table.get_children():
        note_table.delete(row)
    for note in get_note():
        note_table.insert("", "end", values=note)


def showPerfumeNotes():
    for row in pn_table.get_children():
        pn_table.delete(row)
    for link in get_perfume_note():
        pn_table.insert("", "end", values=link)


def showSeasons():
    for row in season_table.get_children():
        season_table.delete(row)
    for season in get_season():                      
        season_table.insert("", "end", values=season)


def showPerfumeSeasons():
    for row in ps_table.get_children():
        ps_table.delete(row)
    for link in get_perfume_season():
        ps_table.insert("", "end", values=link)



def addBrandFromWindow():
    name = brand_name_input.get()
    country = brand_country_input.get()
    year = brand_year_input.get()

    brand_id = add_brand(name, country, year)

    brand_name_input.delete(0, tk.END)
    brand_country_input.delete(0, tk.END)
    brand_year_input.delete(0, tk.END)
    brand_result.config(text="Brends pievienots! ID = " + str(brand_id))
    showBrands()


def addPerfumeFromWindow():
    brand_id = brand_id_input.get()
    name = perfume_name_input.get()
    price = price_input.get()

    try:
        perfume_id = add_perfume(brand_id, name, price)
    except Exception:
        # ja brenda ID neeksistē
        perfume_result.config(text="Brenda ID neekstistē.", fg=ERROR)
        return

    brand_id_input.delete(0, tk.END)
    perfume_name_input.delete(0, tk.END)
    price_input.delete(0, tk.END)

    perfume_result.config(text="Parfīms pievienots! ID = " + str(perfume_id), fg=ACCENT_DARK)
    showPerfumes()


def addWearFromWindow():
    perfume_id = perfume_id_input.get()
    date = iso_datums(wear_date_input.get())
    occasion = occasion_input.get()

    try:
        wear_id = add_wear(perfume_id, date, occasion)
    except Exception:
        # ja parfīma ID neeksistē ziņo
        wear_result.config(text="Parfīma ID neekstistē.", fg=ERROR)
        return

    perfume_id_input.delete(0, tk.END)
    wear_date_input.delete(0, tk.END)
    occasion_input.delete(0, tk.END)

    wear_result.config(text="Ieraksts pievienots! ID = " + str(wear_id), fg=ACCENT_DARK)
    showWears()


def addRatingFromWindow():
    perfume_id = rating_perfume_id_input.get()  # parfīma ID
    scent = scent_input.get()                   # smaržas vērtējums 1-10
    longevity = longevity_input.get()           # izturības vērtējums 1-10
    projection = projection_input.get()         # projekcijas vērtējums 1-10
    overall = overall_input.get()               # kopējais vērtējums 1-10
    review = review_input.get()                 # brīvā teksta atsauksme

    try:
        rating_id = add_rating(perfume_id, scent, longevity, projection, overall, review)
    except Exception:
        rating_result.config(text="Kļūda! Pārbaudi Parfīma ID.", fg=ERROR)
        return

    rating_perfume_id_input.delete(0, tk.END)
    scent_input.delete(0, tk.END)
    longevity_input.delete(0, tk.END)
    projection_input.delete(0, tk.END)
    overall_input.delete(0, tk.END)
    review_input.delete(0, tk.END)

    rating_result.config(text="Vērtējums pievienots! ID = " + str(rating_id), fg=ACCENT_DARK)
    showRatings()


def addNoteFromWindow():
    name = note_name_input.get()
    category = note_category_input.get()

    note_id = add_note(name, category)

    note_name_input.delete(0, tk.END) 
    note_category_input.delete(0, tk.END)

    note_result.config(text="Nota pievienota! ID = " + str(note_id), fg=ACCENT_DARK)
    showNotes()


def addPerfumeNoteFromWindow():
    perfume_id = pn_perfume_id_input.get()  # kurš parfīms
    note_id = pn_note_id_input.get()        # kura nota

    try:
        add_perfume_note(perfume_id, note_id)
    except Exception:
        pn_result.config(text="Kļūda! Pārbaudi Parfīma un Notas ID.", fg=ERROR)
        return

    pn_perfume_id_input.delete(0, tk.END)  
    pn_note_id_input.delete(0, tk.END)

    pn_result.config(text="Sasaiste pievienota!", fg=ACCENT_DARK)
    showPerfumeNotes()  # atjauno sasaistes tabulu


def addPerfumeSeasonFromWindow():
    perfume_id = ps_perfume_id_input.get()  # kurš parfīms
    season_id = ps_season_id_input.get()    # kura sezona

    try:
        add_perfume_season(perfume_id, season_id)
    except Exception:
        ps_result.config(text="Kļūda! Pārbaudi Parfīma un Sezonas ID.", fg=ERROR)
        return

    ps_perfume_id_input.delete(0, tk.END)
    ps_season_id_input.delete(0, tk.END)

    ps_result.config(text="Sasaiste pievienota!", fg=ACCENT_DARK)
    showPerfumeSeasons()


# ================= BRENDI CILNE =================

# ---------- Pievienot brendu ----------
brand_block = tk.LabelFrame(brand_tab, text="Pievienot brendu", bg=BG, fg=ACCENT_DARK,
                            font=("Arial", 11, "bold"), padx=10, pady=8)
brand_block.pack(fill="x", padx=10, pady=(10, 5))

tk.Label(brand_block, text="Nosaukums:", bg=BG, fg=ACCENT_DARK).pack(anchor="w")
brand_name_input = tk.Entry(brand_block, width=40)
brand_name_input.pack(pady=(2, 6), fill="x")

tk.Label(brand_block, text="Valsts:", bg=BG, fg=ACCENT_DARK).pack(anchor="w")
brand_country_input = tk.Entry(brand_block, width=40)
brand_country_input.pack(pady=(2, 6), fill="x")

tk.Label(brand_block, text="Dibināšanas gads:", bg=BG, fg=ACCENT_DARK).pack(anchor="w")
brand_year_input = tk.Entry(brand_block, width=40)
brand_year_input.pack(pady=(2, 6), fill="x")


brand_button = tk.Button(brand_block, text="Pievienot brendu", command=addBrandFromWindow,
                         bg=ACCENT_DARK, fg="white", activebackground=ACCENT_LIGHT,
                         font=("Arial", 10, "bold"), cursor="hand2")
brand_button.pack(fill="x", pady=(4, 2))

brand_result = tk.Label(brand_block, text="", bg=BG, fg=ACCENT_DARK,
                        font=("Arial", 9, "bold"))
brand_result.pack()

# ---------- visi brendi ----------
brand_table_block = tk.LabelFrame(brand_tab, text="Visi brendi", bg=BG, fg=ACCENT,
                                  font=("Arial", 11, "bold"), padx=10, pady=8)
brand_table_block.pack(fill="x", padx=10, pady=5)

brand_table = create_table(brand_table_block,
                           ["ID", "Nosaukums", "Valsts", "Gads"],
                           [60, 280, 220, 100], 6)                

# ================= PARFĪMI =================

# ---------- Pievienot parfīmu ----------
perfume_block = tk.LabelFrame(perfume_tab, text="Pievienot parfīmu", bg=BG, fg=ACCENT_DARK,
                              font=("Arial", 11, "bold"), padx=10, pady=8)
perfume_block.pack(fill="x", padx=10, pady=(10, 5))

tk.Label(perfume_block, text="Brenda ID:", bg=BG, fg=ACCENT_DARK).pack(anchor="w")
brand_id_input = tk.Entry(perfume_block, width=40) 
brand_id_input.pack(pady=(2, 6), fill="x")

tk.Label(perfume_block, text="Nosaukums:", bg=BG, fg=ACCENT_DARK).pack(anchor="w")
perfume_name_input = tk.Entry(perfume_block, width=40)
perfume_name_input.pack(pady=(2, 6), fill="x")

tk.Label(perfume_block, text="Cena (EUR):", bg=BG, fg=ACCENT_DARK).pack(anchor="w")
price_input = tk.Entry(perfume_block, width=40)
price_input.pack(pady=(2, 6), fill="x")

perfume_button = tk.Button(perfume_block, text="Pievienot parfīmu", command=addPerfumeFromWindow,
                           bg=ACCENT, fg="white", activebackground=ACCENT_LIGHT,
                           font=("Arial", 10, "bold"), cursor="hand2")
perfume_button.pack(fill="x", pady=(4, 2))

perfume_result = tk.Label(perfume_block, text="", bg=BG, fg=ACCENT_DARK,
                          font=("Arial", 9, "bold"))
perfume_result.pack()

# ---------- visi parfīmi ----------
perfume_table_block = tk.LabelFrame(perfume_tab, text="Visi parfīmi", bg=BG, fg=ACCENT,
                                    font=("Arial", 11, "bold"), padx=10, pady=8)
perfume_table_block.pack(fill="x", padx=10, pady=5)

perfume_table = create_table(perfume_table_block,
                             ["ID", "Nosaukums", "Brends", "Cena (EUR)"],  # "Brends" nāk no JOIN
                             [60, 250, 250, 130], 6)

# ---------- Pievienot valkāšanas ierakstu ----------
wear_block = tk.LabelFrame(perfume_tab, text="Pievienot valkāšanas ierakstu", bg=BG, fg=ACCENT_DARK,
                           font=("Arial", 11, "bold"), padx=10, pady=8)
wear_block.pack(fill="x", padx=10, pady=5)

tk.Label(wear_block, text="Parfīma ID:", bg=BG, fg=ACCENT_DARK).pack(anchor="w")
perfume_id_input = tk.Entry(wear_block, width=40)
perfume_id_input.pack(pady=(2, 6), fill="x")


tk.Label(wear_block, text="Datums (DD-MM-GGGG):", bg=BG, fg=ACCENT_DARK).pack(anchor="w")
wear_date_input = tk.Entry(wear_block, width=40)
wear_date_input.pack(pady=(2, 6), fill="x")

tk.Label(wear_block, text="Pasākums (School / Work / Everyday / etc):", bg=BG, fg=ACCENT_DARK).pack(anchor="w")
occasion_input = tk.Entry(wear_block, width=40)
occasion_input.pack(pady=(2, 6), fill="x")

wear_button = tk.Button(wear_block, text="Pievienot ierakstu", command=addWearFromWindow,
                        bg=ACCENT, fg="white", activebackground=ACCENT_LIGHT,
                        font=("Arial", 10, "bold"), cursor="hand2")
wear_button.pack(fill="x", pady=(4, 2))

wear_result = tk.Label(wear_block, text="", bg=BG, fg=ACCENT_DARK,
                       font=("Arial", 9, "bold"))
wear_result.pack()

# ---------- valkāšanas žurnāls ----------
wear_table_block = tk.LabelFrame(perfume_tab, text="Valkāšanas žurnāls", bg=BG, fg=ACCENT,
                                 font=("Arial", 11, "bold"), padx=10, pady=8)
wear_table_block.pack(fill="x", padx=10, pady=5)

wear_table = create_table(wear_table_block,
                          ["ID", "Parfīms", "Datums", "Pasākums"],  # datums rādīsies DD-MM-GGGG
                          [60, 240, 130, 280], 5)

# ---------- Pievienot vērtējumu ----------
rating_block = tk.LabelFrame(perfume_tab, text="Pievienot vērtējumu", bg=BG, fg=ACCENT_DARK,
                             font=("Arial", 11, "bold"), padx=10, pady=8)
rating_block.pack(fill="x", padx=10, pady=5)

tk.Label(rating_block, text="Parfīma ID:", bg=BG, fg=ACCENT_DARK).pack(anchor="w")
rating_perfume_id_input = tk.Entry(rating_block, width=40)
rating_perfume_id_input.pack(pady=(2, 6), fill="x")

tk.Label(rating_block, text="Smarža (1-10):", bg=BG, fg=ACCENT_DARK).pack(anchor="w")
scent_input = tk.Entry(rating_block, width=40)
scent_input.pack(pady=(2, 6), fill="x")

tk.Label(rating_block, text="Izturība (1-10):", bg=BG, fg=ACCENT_DARK).pack(anchor="w")
longevity_input = tk.Entry(rating_block, width=40)
longevity_input.pack(pady=(2, 6), fill="x")

tk.Label(rating_block, text="Projekcija (1-10):", bg=BG, fg=ACCENT_DARK).pack(anchor="w")
projection_input = tk.Entry(rating_block, width=40)
projection_input.pack(pady=(2, 6), fill="x")

tk.Label(rating_block, text="Kopējais vērtējums (1-10):", bg=BG, fg=ACCENT_DARK).pack(anchor="w")
overall_input = tk.Entry(rating_block, width=40)
overall_input.pack(pady=(2, 6), fill="x")

tk.Label(rating_block, text="Atsauksme:", bg=BG, fg=ACCENT_DARK).pack(anchor="w")
review_input = tk.Entry(rating_block, width=40)
review_input.pack(pady=(2, 6), fill="x")

rating_button = tk.Button(rating_block, text="Pievienot vērtējumu", command=addRatingFromWindow,
                          bg=ACCENT, fg="white", activebackground=ACCENT_LIGHT,
                          font=("Arial", 10, "bold"), cursor="hand2")
rating_button.pack(fill="x", pady=(4, 2))

rating_result = tk.Label(rating_block, text="", bg=BG, fg=ACCENT_DARK,
                         font=("Arial", 9, "bold"))
rating_result.pack()

# ---------- vērtējumi ----------
rating_table_block = tk.LabelFrame(perfume_tab, text="Vērtējumi", bg=BG, fg=ACCENT,
                                   font=("Arial", 11, "bold"), padx=10, pady=8)
rating_table_block.pack(fill="x", padx=10, pady=5)

rating_table = create_table(rating_table_block,
                            ["ID", "Parfīms", "Smarža", "Izturība", "Projekcija", "Kopā", "Atsauksme"],
                            [45, 130, 60, 65, 80, 55, 280], 5)

# ---------- Pievienot smaržu notu ----------
note_block = tk.LabelFrame(perfume_tab, text="Pievienot smaržu notu", bg=BG, fg=ACCENT_DARK,
                           font=("Arial", 11, "bold"), padx=10, pady=8)
note_block.pack(fill="x", padx=10, pady=5)

tk.Label(note_block, text="Nosaukums:", bg=BG, fg=ACCENT_DARK).pack(anchor="w")
note_name_input = tk.Entry(note_block, width=40)
note_name_input.pack(pady=(2, 6), fill="x")


tk.Label(note_block, text="Kategorija (top / heart / base):", bg=BG, fg=ACCENT_DARK).pack(anchor="w")
note_category_input = tk.Entry(note_block, width=40)
note_category_input.pack(pady=(2, 6), fill="x")

note_button = tk.Button(note_block, text="Pievienot notu", command=addNoteFromWindow,
                        bg=ACCENT, fg="white", activebackground=ACCENT_LIGHT,
                        font=("Arial", 10, "bold"), cursor="hand2")
note_button.pack(fill="x", pady=(4, 2))

note_result = tk.Label(note_block, text="", bg=BG, fg=ACCENT_DARK,
                       font=("Arial", 9, "bold"))
note_result.pack()

# ---------- visas smaržu notas ----------
note_list_block = tk.LabelFrame(perfume_tab, text="Visas smaržu notas", bg=BG, fg=ACCENT,
                                font=("Arial", 11, "bold"), padx=10, pady=8)
note_list_block.pack(fill="x", padx=10, pady=5)



note_table = create_table(note_list_block,
                          ["ID", "Nota", "Kategorija"],
                          [60, 300, 300], 5)

# ---------- Sasaistīt parfīmu ar notu ----------
perfume_note_block = tk.LabelFrame(perfume_tab, text="Sasaistīt parfīmu ar notu", bg=BG, fg=ACCENT_DARK,
                                   font=("Arial", 11, "bold"), padx=10, pady=8)
perfume_note_block.pack(fill="x", padx=10, pady=5)

tk.Label(perfume_note_block, text="Parfīma ID:", bg=BG, fg=ACCENT_DARK).pack(anchor="w")
pn_perfume_id_input = tk.Entry(perfume_note_block, width=40)
pn_perfume_id_input.pack(pady=(2, 6), fill="x")

tk.Label(perfume_note_block, text="Notas ID:", bg=BG, fg=ACCENT_DARK).pack(anchor="w")
pn_note_id_input = tk.Entry(perfume_note_block, width=40)
pn_note_id_input.pack(pady=(2, 6), fill="x")

pn_button = tk.Button(perfume_note_block, text="Sasaistīt", command=addPerfumeNoteFromWindow,
                      bg=ACCENT, fg="white", activebackground=ACCENT_LIGHT,
                      font=("Arial", 10, "bold"), cursor="hand2")
pn_button.pack(fill="x", pady=(4, 2))

pn_result = tk.Label(perfume_note_block, text="", bg=BG, fg=ACCENT_DARK,
                     font=("Arial", 9, "bold"))
pn_result.pack()

# ---------- parfīmu notas ----------
pn_table_block = tk.LabelFrame(perfume_tab, text="Parfīmu notas", bg=BG, fg=ACCENT,
                               font=("Arial", 11, "bold"), padx=10, pady=8)
pn_table_block.pack(fill="x", padx=10, pady=5)

pn_table = create_table(pn_table_block,
                        ["Parfīms", "Nota"],
                        [350, 350], 5)

# ---------- Sasaistīt parfīmu ar sezonu ----------
perfume_season_block = tk.LabelFrame(perfume_tab, text="Sasaistīt parfīmu ar sezonu", bg=BG, fg=ACCENT_DARK,
                                     font=("Arial", 11, "bold"), padx=10, pady=8)
perfume_season_block.pack(fill="x", padx=10, pady=5)

tk.Label(perfume_season_block, text="Parfīma ID:", bg=BG, fg=ACCENT_DARK).pack(anchor="w")
ps_perfume_id_input = tk.Entry(perfume_season_block, width=40)
ps_perfume_id_input.pack(pady=(2, 6), fill="x")


tk.Label(perfume_season_block, text="Sezonas ID:", bg=BG, fg=ACCENT_DARK).pack(anchor="w")
ps_season_id_input = tk.Entry(perfume_season_block, width=40)
ps_season_id_input.pack(pady=(2, 6), fill="x")

ps_button = tk.Button(perfume_season_block, text="Sasaistīt", command=addPerfumeSeasonFromWindow,
                      bg=ACCENT, fg="white", activebackground=ACCENT_LIGHT,
                      font=("Arial", 10, "bold"), cursor="hand2")
ps_button.pack(fill="x", pady=(4, 2))

ps_result = tk.Label(perfume_season_block, text="", bg=BG, fg=ACCENT_DARK,
                     font=("Arial", 9, "bold"))
ps_result.pack()

# ---------- parfīmu sezonas ----------
ps_table_block = tk.LabelFrame(perfume_tab, text="Parfīmu sezonas", bg=BG, fg=ACCENT,
                               font=("Arial", 11, "bold"), padx=10, pady=8)
ps_table_block.pack(fill="x", padx=10, pady=5)

ps_table = create_table(ps_table_block,
                        ["Parfīms", "Sezona"],  # rāda NOSAUKUMUS, nevis ID (JOIN no 3 tabulām)
                        [350, 350], 5)

# ---------- visas sezonas ----------
season_list_block = tk.LabelFrame(perfume_tab, text="Visas sezonas", bg=BG, fg=ACCENT,
                                  font=("Arial", 11, "bold"), padx=10, pady=8)
season_list_block.pack(fill="x", padx=10, pady=(5, 15))



season_table = create_table(season_list_block,
                            ["ID", "Sezona"],
                            [80, 500], 4)


showBrands()
showPerfumes()
showWears()
showRatings()
showNotes()
showPerfumeNotes()
showSeasons()
showPerfumeSeasons()

window.mainloop()