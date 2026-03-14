import csv

glosar = {}


def adauga_termen():
    termen = input("Introdu termenul: ")

    if termen in glosar:
        print("Termenul există deja.")
        return

    definitie = input("Definiție: ")
    categorie = input("Categorie: ")
    exemplu = input("Exemplu: ")

    glosar[termen] = {
        "definitie": definitie,
        "categorie": categorie,
        "exemplu": exemplu
    }

    print("Termen adăugat cu succes.")


def cautare_exacta():
    termen = input("Introdu termenul căutat: ")

    if termen in glosar:
        print(glosar[termen])
    else:
        print("Termenul nu există.")


def cautare_fragment():
    fragment = input("Introdu fragmentul: ")

    gasit = False
    for termen in glosar:
        if fragment.lower() in termen.lower():
            print(termen, ":", glosar[termen])
            gasit = True

    if not gasit:
        print("Nu s-au găsit rezultate.")


def actualizare():
    termen = input("Termenul de actualizat: ")

    if termen not in glosar:
        print("Termenul nu există.")
        return

    camp = input("Ce vrei să modifici? (definitie/categorie/exemplu): ")

    if camp not in glosar[termen]:
        print("Câmp invalid.")
        return

    valoare = input("Noua valoare: ")
    glosar[termen][camp] = valoare

    print("Actualizare realizată.")


def stergere():
    termen = input("Termenul de șters: ")

    if termen in glosar:
        del glosar[termen]
        print("Termen șters.")
    else:
        print("Termenul nu există.")


def afisare():
    if not glosar:
        print("Glosarul este gol.")
        return

    for termen, info in glosar.items():
        print("\nTermen:", termen)
        print("Definiție:", info["definitie"])
        print("Categorie:", info["categorie"])
        print("Exemplu:", info["exemplu"])


def statistici():
    total = len(glosar)
    categorii = {}

    for termen in glosar:
        cat = glosar[termen]["categorie"]

        if cat not in categorii:
            categorii[cat] = 0

        categorii[cat] += 1

    print("Total termeni:", total)
    print("Termeni pe categorii:")

    for cat, nr in categorii.items():
        print(cat, ":", nr)


def salvare_csv():
    with open("glosar.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["termen", "definitie", "categorie", "exemplu"])

        for termen, info in glosar.items():
            writer.writerow([
                termen,
                info["definitie"],
                info["categorie"],
                info["exemplu"]
            ])

    print("Glosar salvat în glosar.csv")


def incarcare_csv():
    try:
        with open("glosar.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                glosar[row["termen"]] = {
                    "definitie": row["definitie"],
                    "categorie": row["categorie"],
                    "exemplu": row["exemplu"]
                }

        print("Glosar încărcat.")
    except FileNotFoundError:
        print("Fișierul nu există.")


def meniu():
    while True:
        print("\n--- MENIU ---")
        print("1. Adaugă termen")
        print("2. Căutare exactă")
        print("3. Căutare fragment")
        print("4. Actualizare termen")
        print("5. Ștergere termen")
        print("6. Afișare glosar")
        print("7. Statistici")
        print("8. Salvare CSV")
        print("9. Încărcare CSV")
        print("0. Ieșire")

        opt = input("Alege opțiunea: ")

        if opt == "1":
            adauga_termen()
        elif opt == "2":
            cautare_exacta()
        elif opt == "3":
            cautare_fragment()
        elif opt == "4":
            actualizare()
        elif opt == "5":
            stergere()
        elif opt == "6":
            afisare()
        elif opt == "7":
            statistici()
        elif opt == "8":
            salvare_csv()
        elif opt == "9":
            incarcare_csv()
        elif opt == "0":
            print("Program închis.")
            break
        else:
            print("Opțiune invalidă.")


meniu()


