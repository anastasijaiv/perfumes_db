import tkinter as tk
from tkinter import ttk

from funkcijas import (
    add_brand, add_perfume, add_wear, add_rating,
    add_note, add_perfume_note, add_perfume_season,
    get_brand, get_perfume, get_wear, get_note,
    get_season, get_rating, get_perfume_note, get_perfume_season,
    delete_brand, delete_perfume, delete_wear,
    delete_rating, delete_note, delete_season,
    delete_perfume_note, delete_perfume_season,
    search_all,  #meklēšana
)

#Krāsas
BG = "#c2f1ff"
ACCENT = "#1BAEF1"
ACCENT_DARK = "#0C88C2"
ACCENT_LIGHT = "#75CBF3"
ERROR = "#0C88C2"

#Galvenais logs
window = tk.Tk()
window.title("Mana Parfīmu Kolekcija")
window.geometry("800x900")
window.config(bg=BG) #loga fona krāsa

#logs ekrāna centrā
window.update_idletasks() #loga nakami vizuāli atjauninājumi
screen_w = window.winfo_screenwidth()
screen_h = window.winfo_screenheight()
x = (screen_w - 800) // 2 #logs centrā pa horizontāli
y = max(0, (screen_h - 900) // 2) #logs centrā pa vertikāli
window.geometry("800x900+" + str(x) + "+" + str(y))

#Scrollbar
main_canvas = tk.Canvas(window, bg=BG, highlightthickness=0)
scrollbar = tk.Scrollbar(window, orient="vertical", command=main_canvas.yview)
main_canvas.configure(yscrollcommand=scrollbar.set)  #saturs un scrollbar kustas kopā
scrollbar.pack(side="right", fill="y")
main_canvas.pack(side="left", fill="both", expand=True)

main_frame = tk.Frame(main_canvas, bg=BG)  #saturs
content_window = main_canvas.create_window((0, 0), window=main_frame, anchor="nw")  #ramis saturā iekšā


#Satura centrēšana
def center_content(event=None):
    canvas_w = main_canvas.winfo_width() #platums
    content_w = main_frame.winfo_reqwidth() #platums
    if canvas_w > content_w:
        x = (canvas_w - content_w) // 2 #no kreisās malas lai būtu centrā
    else:
        x = 0                                #ja saturs ir platāks, bez atkāpes
    main_canvas.coords(content_window, x, 0)


def on_configure(event):
    #kad saturs vai logs maina izmēru
    main_canvas.configure(scrollregion=main_canvas.bbox("all"))  #cik liels ir saturs
    center_content()


main_frame.bind("<Configure>", on_configure) #saturs maina izmēru
main_canvas.bind("<Configure>", center_content) #logs maina izmēru


def on_mousewheel(event):
    steps = max(1, abs(event.delta) // 120) #cik soļu ritināt
    if event.delta > 0:
        main_canvas.yview_scroll(-steps, "units")
    else:
        main_canvas.yview_scroll(steps, "units")

main_canvas.bind_all("<MouseWheel>", on_mousewheel) #darbojas visā logā

#Virsraksts
header = tk.Label(main_frame, text="Mana Parfīmu Kolekcija",
                  font=("Arial", 20, "bold"), bg=BG, fg=ACCENT)
header.pack(pady=(15, 5))

try:
    logo_big = tk.PhotoImage(file="perfumebgg.png")
    logo = logo_big.subsample(2) #samazinat izmēru
    logo_label = tk.Label(main_frame, image=logo, bg=BG)
    logo_label.pack(pady=5)
except Exception:
    pass  #ja bildes nav, vienalga palaižas

#Cilnes
tabs = ttk.Notebook(main_frame)  #cilņu josla
tabs.pack(fill="both", expand=True, padx=10, pady=10)

brand_tab = tk.Frame(tabs, bg=BG)
tabs.add(brand_tab, text="Brendi")

perfume_tab = tk.Frame(tabs, bg=BG)
tabs.add(perfume_tab, text="Parfīmi")

wear_tab = tk.Frame(tabs, bg=BG)
tabs.add(wear_tab, text="Žurnāls")

rating_tab = tk.Frame(tabs, bg=BG)
tabs.add(rating_tab, text="Vērtējumi")

note_tab = tk.Frame(tabs, bg=BG)
tabs.add(note_tab, text="Notas")

pn_tab = tk.Frame(tabs, bg=BG)
tabs.add(pn_tab, text="Parfīmu notas")

season_tab = tk.Frame(tabs, bg=BG)
tabs.add(season_tab, text="Sezonas")

search_tab = tk.Frame(tabs, bg=BG)
tabs.add(search_tab, text="Meklēšana")

#PALĪGFUNKCIJAS

#tabula kura attēlo datus kolonnās un rindās
def create_table(parent, headers, widths, height):
    columns = [] #saraksts kolonnu nosaukumiem
    for i in range(len(headers)):
        columns.append("c" + str(i))
    table = ttk.Treeview(parent, columns=columns, show="headings", height=height)  #izveido tabulas elementu
    for i in range(len(headers)):
        table.heading("c" + str(i), text=headers[i]) #kolonnas redzamais virsraksts
        table.column("c" + str(i), width=widths[i], anchor="center") #kolonnas platums un teksts centrā
    table.pack(fill="x", padx=5, pady=5)
    return table

#datumu funkcijas
#-------------------------------------------------------
def eu_datums(datums):
    parts = str(datums).split("-") #3
    if len(parts) == 3:
        return parts[2] + "-" + parts[1] + "-" + parts[0]  #diena - gads
    return str(datums)


def iso_datums(datums):
    parts = str(datums).strip().split("-")    # noņem atstarpes / 3
    if len(parts) == 3 and len(parts[0]) == 2:
        return parts[2] + "-" + parts[1] + "-" + parts[0]
    return str(datums)
#-------------------------------------------------------

#dzēst rindu no tabulas
def delete_selected(table, delete_function, result_label, show_function):
    selected = table.selection()
    if len(selected) == 0: #ja nav izvēlēts
        result_label.config(text="Uzspied uz rindas tabulā!", fg=ERROR)
        return
    values = table.item(selected[0], "values")
    try:
        total = delete_function(*values) #dzēšanas funkcija
        extra = total - 1 #cik saistītu ierakstu izdzēšās ar pašu ierakstu
        if total == 0:
            result_label.config(text="Ieraksts nav atrasts.", fg=ERROR)
        elif extra == 0:
            result_label.config(text="Ieraksts izdzēsts!", fg=ACCENT_DARK)
        elif extra == 1:
            result_label.config(text="Izdzēsts! Līdz ar to arī 1 saistīts ieraksts.", fg=ACCENT_DARK)
        else:
            result_label.config(text="Izdzēsts! Līdz ar to arī " + str(extra) + " saistīti ieraksti.", fg=ACCENT_DARK)
    except Exception:
        result_label.config(text="Neizdevās dzēst! Pārbaudi vērtības.", fg=ERROR)
    show_function()


#dzēšanas pogu un paziņojums zem tabulas
def add_delete_row(parent, table, delete_function, show_function):
    label = tk.Label(parent, text="", bg=BG, fg=ACCENT_DARK, font=("Arial", 9, "bold"))
    button = tk.Button(parent, text="Dzēst izvēlēto rindu",
                       command=lambda: delete_selected(table, delete_function, label, show_function),
                       bg=ERROR, fg="white", font=("Arial", 9, "bold"), cursor="hand2")
    button.pack(anchor="w", padx=5, pady=(0, 2))
    label.pack(anchor="w", padx=5, pady=(0, 4))


#funkcijas, kuras aizpilda tabulas

def showBrands():
    for row in brand_table.get_children():    #notīra tabulu
        brand_table.delete(row)
    for brand in get_brand():                 #paņem visus no db
        brand_table.insert("", "end", values=brand)  #ieliek katru tabulā


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



#pievienošanas funkcija

def addBrandFromWindow():
    #paņem tekstu no laukiem
    name = brand_name_input.get()
    country = brand_country_input.get()
    year = brand_year_input.get()

    #pievieno db
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

    #vai brenda ID eksistē
    brand_exists = False
    for b in get_brand():
        if str(b[0]) == brand_id:
            brand_exists = True

    if brand_exists == False:
        perfume_result.config(text="Brenda ID neeksistē.", fg=ERROR)
        return

    #pievieno db
    perfume_id = add_perfume(brand_id, name, price)

    brand_id_input.delete(0, tk.END)
    perfume_name_input.delete(0, tk.END)
    price_input.delete(0, tk.END)

    perfume_result.config(text="Parfīms pievienots! ID = " + str(perfume_id), fg=ACCENT_DARK)

    showPerfumes()


def addWearFromWindow():
    perfume_id = perfume_id_input.get()
    date = iso_datums(wear_date_input.get())
    occasion = occasion_input.get()

    #vai parfīma ID eksistē
    perfume_exists = False
    for p in get_perfume():
        if str(p[0]) == perfume_id:
            perfume_exists = True

    if perfume_exists == False:
        wear_result.config(text="Parfīma ID neeksistē.", fg=ERROR)
        return

    #pievieno db
    wear_id = add_wear(perfume_id, date, occasion)

    perfume_id_input.delete(0, tk.END)
    wear_date_input.delete(0, tk.END)
    occasion_input.delete(0, tk.END)

    wear_result.config(text="Ieraksts pievienots! ID = " + str(wear_id), fg=ACCENT_DARK)

    showWears()


def addRatingFromWindow():
    perfume_id = rating_perfume_id_input.get()
    scent = scent_input.get()
    longevity = longevity_input.get()
    projection = projection_input.get()
    overall = overall_input.get()
    review = review_input.get()

    #vai parfīma ID eksistē
    perfume_exists = False
    for p in get_perfume():
        if str(p[0]) == perfume_id:
            perfume_exists = True

    if perfume_exists == False:
        rating_result.config(text="Kļūda! Pārbaudi Parfīma ID.", fg=ERROR)
        return

    rating_id = add_rating(perfume_id, scent, longevity, projection, overall, review)

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

    # pievieno db
    note_id = add_note(name, category)

    note_name_input.delete(0, tk.END)
    note_category_input.delete(0, tk.END)

    note_result.config(text="Nota pievienota! ID = " + str(note_id), fg=ACCENT_DARK)

    showNotes()


def addPerfumeNoteFromWindow():
    perfume_id = pn_perfume_id_input.get()
    note_id = pn_note_id_input.get()

    #vai parfīma ID eksistē
    perfume_exists = False
    for p in get_perfume():
        if str(p[0]) == perfume_id:
            perfume_exists = True

    #vai notas ID eksistē
    note_exists = False
    for n in get_note():
        if str(n[0]) == note_id:
            note_exists = True

    if perfume_exists == False or note_exists == False:
        pn_result.config(text="Kļūda! Pārbaudi Parfīma un Notas ID.", fg=ERROR)
        return

    #sasaista parfīmu ar notu db
    add_perfume_note(perfume_id, note_id)

    pn_perfume_id_input.delete(0, tk.END)
    pn_note_id_input.delete(0, tk.END)

    pn_result.config(text="Sasaiste pievienota!", fg=ACCENT_DARK)

    showPerfumeNotes()


def addPerfumeSeasonFromWindow():
    perfume_id = ps_perfume_id_input.get()
    season_id = ps_season_id_input.get()

    #vai parfīma ID eksistē
    perfume_exists = False
    for p in get_perfume():
        if str(p[0]) == perfume_id:
            perfume_exists = True

    #vai sezonas ID eksistē
    season_exists = False
    for s in get_season():
        if str(s[0]) == season_id:
            season_exists = True

    if perfume_exists == False or season_exists == False:
        ps_result.config(text="Kļūda! Pārbaudi Parfīma un Sezonas ID.", fg=ERROR)
        return

    #sasaista parfīmu ar sezonu db
    add_perfume_season(perfume_id, season_id)

    ps_perfume_id_input.delete(0, tk.END)
    ps_season_id_input.delete(0, tk.END)

    ps_result.config(text="Sasaiste pievienota", fg=ACCENT_DARK)

    showPerfumeSeasons()


def searchFromWindow():
    text = search_input.get().strip() #paņem / noņem atstarpes no malām
    if text == "":
        search_result.config(text="Ievadi meklējamo tekstu!", fg=ERROR)
        return
    for row in search_table.get_children():   #notīra iepriekšējos
        search_table.delete(row)
    results = search_all(text)
    for r in results:
        search_table.insert("", "end", values=r)  #katru rezultātu tabulā
    search_result.config(text=str(len(results)) + " ieraksti", fg=ACCENT_DARK)  #cik atrada


#CILNE: BRENDI


#Pievienot brendu
brand_block = tk.LabelFrame(brand_tab, text="Pievienot brendu", bg=BG, fg=ACCENT_DARK,
                            font=("Arial", 11, "bold"), padx=10, pady=8)
brand_block.pack(fill="x", padx=10, pady=(10, 5))

tk.Label(brand_block, text="Nosaukums:", bg=BG, fg=ACCENT_DARK).pack(anchor="w")
brand_name_input = tk.Entry(brand_block, width=40)  #ievades lauks nosaukumam
brand_name_input.pack(pady=(2, 6), fill="x")

tk.Label(brand_block, text="Valsts:", bg=BG, fg=ACCENT_DARK).pack(anchor="w")
brand_country_input = tk.Entry(brand_block, width=40)  #valstij
brand_country_input.pack(pady=(2, 6), fill="x")

tk.Label(brand_block, text="Dibināšanas gads:", bg=BG, fg=ACCENT_DARK).pack(anchor="w")
brand_year_input = tk.Entry(brand_block, width=40)  #gadam
brand_year_input.pack(pady=(2, 6), fill="x")

brand_button = tk.Button(brand_block, text="Pievienot brendu", command=addBrandFromWindow,  #izsauc funkciju
                         bg=ACCENT_DARK, fg="white", activebackground=ACCENT_LIGHT,
                         font=("Arial", 10, "bold"), cursor="hand2")
brand_button.pack(fill="x", pady=(4, 2))

brand_result = tk.Label(brand_block, text="", bg=BG, fg=ACCENT_DARK,
                        font=("Arial", 9, "bold"))  #paziņojums
brand_result.pack()

#Visi brendi (tabula)
brand_table_block = tk.LabelFrame(brand_tab, text="Visi brendi", bg=BG, fg=ACCENT,
                                  font=("Arial", 11, "bold"), padx=10, pady=8)
brand_table_block.pack(fill="x", padx=10, pady=5)

brand_table = create_table(brand_table_block,
                           ["ID", "Nosaukums", "Valsts", "Gads"],  #virsraksti
                           [60, 280, 220, 100], 6)                 #platumi un rindu skaits

add_delete_row(brand_table_block, brand_table, delete_brand, showBrands)

# CILNE: PARFĪMI

#Pievienot parfīmu
perfume_block = tk.LabelFrame(perfume_tab, text="Pievienot parfīmu", bg=BG, fg=ACCENT_DARK,
                              font=("Arial", 11, "bold"), padx=10, pady=8)
perfume_block.pack(fill="x", padx=10, pady=(10, 5))

tk.Label(perfume_block, text="Brenda ID:", bg=BG, fg=ACCENT_DARK).pack(anchor="w")
brand_id_input = tk.Entry(perfume_block, width=40)  #brenda ID
brand_id_input.pack(pady=(2, 6), fill="x")

tk.Label(perfume_block, text="Nosaukums:", bg=BG, fg=ACCENT_DARK).pack(anchor="w")
perfume_name_input = tk.Entry(perfume_block, width=40)  #nosaukumam
perfume_name_input.pack(pady=(2, 6), fill="x")

tk.Label(perfume_block, text="Cena (EUR):", bg=BG, fg=ACCENT_DARK).pack(anchor="w")
price_input = tk.Entry(perfume_block, width=40)  #cenai
price_input.pack(pady=(2, 6), fill="x")

perfume_button = tk.Button(perfume_block, text="Pievienot parfīmu", command=addPerfumeFromWindow,
                           bg=ACCENT, fg="white", activebackground=ACCENT_LIGHT,
                           font=("Arial", 10, "bold"), cursor="hand2")
perfume_button.pack(fill="x", pady=(4, 2))

perfume_result = tk.Label(perfume_block, text="", bg=BG, fg=ACCENT_DARK,
                          font=("Arial", 9, "bold"))
perfume_result.pack()

#Visi parfīmi (tabula)
perfume_table_block = tk.LabelFrame(perfume_tab, text="Visi parfīmi", bg=BG, fg=ACCENT,
                                    font=("Arial", 11, "bold"), padx=10, pady=8)
perfume_table_block.pack(fill="x", padx=10, pady=5)

perfume_table = create_table(perfume_table_block,
                             ["ID", "Nosaukums", "Brends", "Cena (EUR)"],
                             [60, 250, 250, 130], 6)

add_delete_row(perfume_table_block, perfume_table, delete_perfume, showPerfumes)

# CILNE: ŽURNĀLS

#Pievienot valkāšanas ierakstu
wear_block = tk.LabelFrame(wear_tab, text="Pievienot valkāšanas ierakstu", bg=BG, fg=ACCENT_DARK,
                           font=("Arial", 11, "bold"), padx=10, pady=8)
wear_block.pack(fill="x", padx=10, pady=(10, 5))

tk.Label(wear_block, text="Parfīma ID:", bg=BG, fg=ACCENT_DARK).pack(anchor="w")
perfume_id_input = tk.Entry(wear_block, width=40)  #parfīma ID
perfume_id_input.pack(pady=(2, 6), fill="x")


tk.Label(wear_block, text="Datums (DD-MM-GGGG):", bg=BG, fg=ACCENT_DARK).pack(anchor="w")
wear_date_input = tk.Entry(wear_block, width=40)  #datumam
wear_date_input.pack(pady=(2, 6), fill="x")

tk.Label(wear_block, text="Pasākums (School / Work / Everyday / etc):", bg=BG, fg=ACCENT_DARK).pack(anchor="w")
occasion_input = tk.Entry(wear_block, width=40)  #pasākumam
occasion_input.pack(pady=(2, 6), fill="x")

wear_button = tk.Button(wear_block, text="Pievienot ierakstu", command=addWearFromWindow,
                        bg=ACCENT, fg="white", activebackground=ACCENT_LIGHT,
                        font=("Arial", 10, "bold"), cursor="hand2")
wear_button.pack(fill="x", pady=(4, 2))

wear_result = tk.Label(wear_block, text="", bg=BG, fg=ACCENT_DARK,
                       font=("Arial", 9, "bold"))
wear_result.pack()

#Valkāšanas žurnāls (tabula)
wear_table_block = tk.LabelFrame(wear_tab, text="Valkāšanas žurnāls", bg=BG, fg=ACCENT,
                                 font=("Arial", 11, "bold"), padx=10, pady=8)
wear_table_block.pack(fill="x", padx=10, pady=5)

wear_table = create_table(wear_table_block,
                          ["ID", "Parfīms", "Datums", "Pasākums"],
                          [60, 240, 130, 280], 5)

add_delete_row(wear_table_block, wear_table, delete_wear, showWears)

# CILNE: VĒRTĒJUMI

#Pievienot vērtējumu
rating_block = tk.LabelFrame(rating_tab, text="Pievienot vērtējumu", bg=BG, fg=ACCENT_DARK,
                             font=("Arial", 11, "bold"), padx=10, pady=8)
rating_block.pack(fill="x", padx=10, pady=(10, 5))

tk.Label(rating_block, text="Parfīma ID:", bg=BG, fg=ACCENT_DARK).pack(anchor="w")
rating_perfume_id_input = tk.Entry(rating_block, width=40)  #parfīma ID
rating_perfume_id_input.pack(pady=(2, 6), fill="x")

tk.Label(rating_block, text="Smarža (1-10):", bg=BG, fg=ACCENT_DARK).pack(anchor="w")
scent_input = tk.Entry(rating_block, width=40)  #smaržas vērtējumam
scent_input.pack(pady=(2, 6), fill="x")

tk.Label(rating_block, text="Izturība (1-10):", bg=BG, fg=ACCENT_DARK).pack(anchor="w")
longevity_input = tk.Entry(rating_block, width=40)  #izturības vērtējumam
longevity_input.pack(pady=(2, 6), fill="x")

tk.Label(rating_block, text="Projekcija (1-10):", bg=BG, fg=ACCENT_DARK).pack(anchor="w")
projection_input = tk.Entry(rating_block, width=40)  #projekcijas vērtējumam
projection_input.pack(pady=(2, 6), fill="x")

tk.Label(rating_block, text="Kopējais vērtējums (1-10):", bg=BG, fg=ACCENT_DARK).pack(anchor="w")
overall_input = tk.Entry(rating_block, width=40)  #kopējam vērtējumam
overall_input.pack(pady=(2, 6), fill="x")

tk.Label(rating_block, text="Atsauksme:", bg=BG, fg=ACCENT_DARK).pack(anchor="w")
review_input = tk.Entry(rating_block, width=40)  #atsauksmei
review_input.pack(pady=(2, 6), fill="x")

rating_button = tk.Button(rating_block, text="Pievienot vērtējumu", command=addRatingFromWindow,
                          bg=ACCENT, fg="white", activebackground=ACCENT_LIGHT,
                          font=("Arial", 10, "bold"), cursor="hand2")
rating_button.pack(fill="x", pady=(4, 2))

rating_result = tk.Label(rating_block, text="", bg=BG, fg=ACCENT_DARK,
                         font=("Arial", 9, "bold"))
rating_result.pack()

#Vērtējumi (tabula)
rating_table_block = tk.LabelFrame(rating_tab, text="Vērtējumi", bg=BG, fg=ACCENT,
                                   font=("Arial", 11, "bold"), padx=10, pady=8)
rating_table_block.pack(fill="x", padx=10, pady=5)

rating_table = create_table(rating_table_block,
                            ["ID", "Parfīms", "Smarža", "Izturība", "Projekcija", "Kopā", "Atsauksme"],
                            [45, 130, 60, 65, 80, 55, 280], 5)

add_delete_row(rating_table_block, rating_table, delete_rating, showRatings)

#CILNE: NOTAS

#Pievienot smaržu notu
note_block = tk.LabelFrame(note_tab, text="Pievienot smaržu notu", bg=BG, fg=ACCENT_DARK,
                           font=("Arial", 11, "bold"), padx=10, pady=8)
note_block.pack(fill="x", padx=10, pady=(10, 5))

tk.Label(note_block, text="Nosaukums:", bg=BG, fg=ACCENT_DARK).pack(anchor="w")
note_name_input = tk.Entry(note_block, width=40)  #notas nosaukumam
note_name_input.pack(pady=(2, 6), fill="x")


tk.Label(note_block, text="Kategorija (top / heart / base):", bg=BG, fg=ACCENT_DARK).pack(anchor="w")
note_category_input = tk.Entry(note_block, width=40)  #kategorijai
note_category_input.pack(pady=(2, 6), fill="x")

note_button = tk.Button(note_block, text="Pievienot notu", command=addNoteFromWindow,
                        bg=ACCENT, fg="white", activebackground=ACCENT_LIGHT,
                        font=("Arial", 10, "bold"), cursor="hand2")
note_button.pack(fill="x", pady=(4, 2))

note_result = tk.Label(note_block, text="", bg=BG, fg=ACCENT_DARK,
                       font=("Arial", 9, "bold"))
note_result.pack()

#Visas smaržu notas (tabula)
note_list_block = tk.LabelFrame(note_tab, text="Visas smaržu notas", bg=BG, fg=ACCENT,
                                font=("Arial", 11, "bold"), padx=10, pady=8)
note_list_block.pack(fill="x", padx=10, pady=5)

note_table = create_table(note_list_block,
                          ["ID", "Nota", "Kategorija"],
                          [60, 300, 300], 5)

add_delete_row(note_list_block, note_table, delete_note, showNotes)

# CILNE: PARFĪMU NOTAS (sasaiste parfīms un nota)

#Sasaistīt parfīmu ar notu
perfume_note_block = tk.LabelFrame(pn_tab, text="Sasaistīt parfīmu ar notu", bg=BG, fg=ACCENT_DARK,
                                   font=("Arial", 11, "bold"), padx=10, pady=8)
perfume_note_block.pack(fill="x", padx=10, pady=(10, 5))

tk.Label(perfume_note_block, text="Parfīma ID:", bg=BG, fg=ACCENT_DARK).pack(anchor="w")
pn_perfume_id_input = tk.Entry(perfume_note_block, width=40)  #parfīma ID
pn_perfume_id_input.pack(pady=(2, 6), fill="x")

tk.Label(perfume_note_block, text="Notas ID:", bg=BG, fg=ACCENT_DARK).pack(anchor="w")
pn_note_id_input = tk.Entry(perfume_note_block, width=40)  #notas ID
pn_note_id_input.pack(pady=(2, 6), fill="x")

pn_button = tk.Button(perfume_note_block, text="Sasaistīt", command=addPerfumeNoteFromWindow,
                      bg=ACCENT, fg="white", activebackground=ACCENT_LIGHT,
                      font=("Arial", 10, "bold"), cursor="hand2")
pn_button.pack(fill="x", pady=(4, 2))

pn_result = tk.Label(perfume_note_block, text="", bg=BG, fg=ACCENT_DARK,
                     font=("Arial", 9, "bold"))
pn_result.pack()

#Parfīmu notas (tabula)
pn_table_block = tk.LabelFrame(pn_tab, text="Parfīmu notas", bg=BG, fg=ACCENT,
                               font=("Arial", 11, "bold"), padx=10, pady=8)
pn_table_block.pack(fill="x", padx=10, pady=5)

pn_table = create_table(pn_table_block,
                        ["Parfīms", "Nota"],
                        [350, 350], 5)


add_delete_row(pn_table_block, pn_table, delete_perfume_note, showPerfumeNotes)


# CILNE: SEZONAS (sasaiste parfīms un sezona)

#Sasaistīt parfīmu ar sezonu
perfume_season_block = tk.LabelFrame(season_tab, text="Sasaistīt parfīmu ar sezonu", bg=BG, fg=ACCENT_DARK,
                                     font=("Arial", 11, "bold"), padx=10, pady=8)
perfume_season_block.pack(fill="x", padx=10, pady=(10, 5))

tk.Label(perfume_season_block, text="Parfīma ID:", bg=BG, fg=ACCENT_DARK).pack(anchor="w")
ps_perfume_id_input = tk.Entry(perfume_season_block, width=40)  #parfīma ID
ps_perfume_id_input.pack(pady=(2, 6), fill="x")


tk.Label(perfume_season_block, text="Sezonas ID:", bg=BG, fg=ACCENT_DARK).pack(anchor="w")
ps_season_id_input = tk.Entry(perfume_season_block, width=40)  #sezonas ID
ps_season_id_input.pack(pady=(2, 6), fill="x")

ps_button = tk.Button(perfume_season_block, text="Sasaistīt", command=addPerfumeSeasonFromWindow,
                      bg=ACCENT, fg="white", activebackground=ACCENT_LIGHT,
                      font=("Arial", 10, "bold"), cursor="hand2")
ps_button.pack(fill="x", pady=(4, 2))

ps_result = tk.Label(perfume_season_block, text="", bg=BG, fg=ACCENT_DARK,
                     font=("Arial", 9, "bold"))
ps_result.pack()

# sezonas (tabula)
ps_table_block = tk.LabelFrame(season_tab, text="Parfīmu sezonas", bg=BG, fg=ACCENT,
                               font=("Arial", 11, "bold"), padx=10, pady=8)
ps_table_block.pack(fill="x", padx=10, pady=5)

ps_table = create_table(ps_table_block,
                        ["Parfīms", "Sezona"],
                        [350, 350], 5)

add_delete_row(ps_table_block, ps_table, delete_perfume_season, showPerfumeSeasons)

#Visas sezonas (tabula)
season_list_block = tk.LabelFrame(season_tab, text="Visas sezonas", bg=BG, fg=ACCENT,
                                  font=("Arial", 11, "bold"), padx=10, pady=8)
season_list_block.pack(fill="x", padx=10, pady=(5, 15))

season_table = create_table(season_list_block,
                            ["ID", "Sezona"],
                            [80, 500], 4)

add_delete_row(season_list_block, season_table, delete_season, showSeasons)

# CILNE: MEKLĒŠANA

#"Meklēt visā datubāzē
search_block = tk.LabelFrame(search_tab, text="Meklēt visā datubāzē", bg=BG, fg=ACCENT_DARK,
                             font=("Arial", 11, "bold"), padx=10, pady=8)
search_block.pack(fill="x", padx=10, pady=(10, 5))

tk.Label(search_block, text="Meklē visās tabulās:",
         bg=BG, fg=ACCENT_DARK).pack(anchor="w")
search_input = tk.Entry(search_block, width=40) #meklējamajam tekstam
search_input.pack(pady=(2, 6), fill="x")

search_button = tk.Button(search_block, text="Meklēt", command=searchFromWindow,
                          bg=ACCENT, fg="white", activebackground=ACCENT_LIGHT,
                          font=("Arial", 10, "bold"), cursor="hand2")
search_button.pack(fill="x", pady=(4, 2))

search_result = tk.Label(search_block, text="", bg=BG, fg=ACCENT_DARK,
                         font=("Arial", 9, "bold"))
search_result.pack()

#Rezultāti (tabula)
search_table_block = tk.LabelFrame(search_tab, text="Rezultāti", bg=BG, fg=ACCENT,
                                   font=("Arial", 11, "bold"), padx=10, pady=8)
search_table_block.pack(fill="x", padx=10, pady=5)

search_table = create_table(search_table_block,
                            ["Tabula", "ID", "Informācija"],
                            [120, 60, 500], 10)


showBrands()
showPerfumes()
showWears()
showRatings()
showNotes()
showPerfumeNotes()
showSeasons()
showPerfumeSeasons()

window.mainloop()