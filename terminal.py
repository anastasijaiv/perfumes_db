from funkcijas import (
    add_brand,
    add_wear,
    add_perfume,
    get_brand,
    get_wear,
    get_perfume,
)

while True:
    print("\nPARFĪMU KOLEKCIJA")
    print("1 - Pievienot brendu")
    print("2 - Pievienot parfīmu")
    print("3 - Pievienot valkāšanas ierakstu")
    print("4 - Parādīt valkāšanas žurnālu")
    print("0 - Iziet")

    choice = input("Izvēle: ")

    if choice == "1":
        name = input("Brenda nosaukums: ")
        country = input("Valsts: ")
        year = input("Dibināšanas gads: ")
        brand_id = add_brand(name, country, year)
        print("Brends pievienots. ID: ", brand_id)

    elif choice == "2":
        print("\nBrendu saraksts: ")
        for brand in get_brand():
            print(brand)
        brand_id = input("Brenda ID: ")
        name = input("Parfīma nosaukums: ")
        price = input("Cena: ")
        perfume_id = add_perfume(brand_id, name, price)
        print("Parfīms pievienots. ID: ", perfume_id)

    elif choice == "3":
        print("\nParfīmu saraksts: ")
        for perfume in get_perfume():
            print(perfume)
        perfume_id = input("Parfīma ID: ")
        date = input("Datums (GGGG-MM-DD): ")
        occasion = input("Pasākums: ")
        wear_id = add_wear(perfume_id, date, occasion)
        print("Ieraksts pievienots. ID: ", wear_id)

    elif choice == "4":
        print("\nValkāšanas žurnāls: ")
        for wear in get_wear():
            print(wear)

    if choice == "0":
        break