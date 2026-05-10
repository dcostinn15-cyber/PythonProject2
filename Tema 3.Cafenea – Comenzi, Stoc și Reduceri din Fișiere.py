import csv
import json

# 1 Citire fisiere
def citeste_produse_csv(fisier):
    produse = {}
    with open(fisier, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            produse[row["id"]] = {
                "nume": row["nume"],
                "pret": float(row["pret"]),
                "stoc": int(row["stoc"])
            }
        return produse


def citeste_reduceri_json(fisier):
    with open(fisier, encoding='utf-8') as f:
        return json.load(f)


# 2 Afisare meniu produse
def afiseaza_meniu(produse):
    print("\n--- MENIU ---")
    for id_produs, produs in produse.items():
        print(f"{id_produs}. {produs['nume']} - {produs['pret']} lei (stoc: {produs['stoc']})")


# 3 Adaugare produs
def adauga_produs(comanda, produse, id_produs, cantitate):
    if id_produs not in produse:
        print("Produs invalid!")
        return

    if cantitate <= 0:
        print("Cantitate invalida!")
        return

    deja = comanda.get(id_produs, 0)
    stoc_real = produse[id_produs]["stoc"] - deja

    if cantitate > stoc_real:
        print("Stoc insuficient!")
        return

    comanda[id_produs] = deja + cantitate
    print("Produs adaugat!")


# 4 Scadere produs
def scade_produs(comanda, id_produs, cantitate):
    if id_produs not in comanda:
        print("Produsul nu este in comanda!")
        return

    if cantitate <= 0:
        print("Cantitate invalida!")
        return

    if cantitate >= comanda[id_produs]:
        del comanda[id_produs]
    else:
        comanda[id_produs] -= cantitate

    print("Produs actualizat!")


# 5 Calcul total
def calculeaza_total(comanda, produse):
    total = 0
    for id_produs, cant in comanda.items():
        total += produse[id_produs]["pret"] * cant
    return total


# 6 Calcul total si reducere
def calculeaza_reducere(total, tip, reduceri):
    if tip == "" or tip not in reduceri:
        return 0

    regula = reduceri[tip]

    if total < regula["prag"]:
        print("Nu ai atins pragul pentru reducere!")
        return 0

    if regula["tip"] == "procent":
        return total * regula["valoare"] / 100
    else:
        return regula["valoare"]


# 7 Bon
def genereaza_bon(comanda, produse, total, reducere):
    text = "\n--- BON ---\n"
    for id_produs, cantitate in comanda.items():
        p = produse[id_produs]
        subtotal = p["pret"] * cantitate
        text += f"{p['nume']} x{cantitate} = {subtotal:.2f} lei\n"

    text += f"\nTotal: {total:.2f} lei\n"
    text += f"Reducere: {reducere:.2f} lei\n"
    text += f"Total final: {total - reducere:.2f} lei\n"

    return text


def scrie_bon_txt(fisier, text):
    with open(fisier, "w", encoding="utf-8") as f:
        f.write(text)


# 8 Anulare comanda
def goleste_comanda(comanda):
    comanda.clear()


# 9 Program principal
def main():
    produse = citeste_produse_csv("produse.csv")
    reduceri = citeste_reduceri_json("reduceri.json")
    comanda = {}
    reducere_curenta = ""

    while True:
        print("\n ---- MENIU --- ")
        print("1 - Afisare meniu")
        print("2 - Adauga produs")
        print("3 - Scade produs")
        print("4 - Aplicare reducere")
        print("5 - Finalizare comanda")
        print("6 - Anulare comanda")
        print("0 - Iesire")

        opt = input("Alege optiune: ")

        if opt == "1":
            afiseaza_meniu(produse)

        elif opt == "2":
            id_produs = input("ID produs: ")
            cant = int(input("Cantitate: "))
            adauga_produs(comanda, produse, id_produs, cant)

        elif opt == "3":
            id_produs = input("ID produs: ")
            cant = int(input("Cantitate de scazut: "))
            scade_produs(comanda, id_produs, cant)

        elif opt == "4":
            total = calculeaza_total(comanda, produse)

            if total == 0:
                print("Comanda este goala!")
                continue

            print("1-student 2-happy 3-cupon 4-fara")
            alegere = input("Alege: ")

            if alegere == "1":
                reducere_curenta = "student"
            elif alegere == "2":
                reducere_curenta = "happy"
            elif alegere == "3":
                reducere_curenta = "cupon"
            elif alegere == "4":
                reducere_curenta = ""

        elif opt == "5":
            total = calculeaza_total(comanda, produse)
            if total == 0:
                print("Comanda este goala!")
                continue
            reducere = calculeaza_reducere(total, reducere_curenta, reduceri)


            bon = genereaza_bon(comanda, produse, total, reducere)
            print(bon)

            scrie_bon_txt("bon.txt", bon)

# 10 Actualizare stoc
            for id_produs, cantitate in comanda.items():
                produse[id_produs]["stoc"] -= cantitate

            goleste_comanda(comanda)
            reducere_curenta = ""

            print("Comanda finalizata!")

        elif opt == "6":
            goleste_comanda(comanda)
            reducere_curenta = ""
            print("Comanda anulata!")

        elif opt == "0":
            print("Program inchis")
            break

        else:
            print("Optiune invalida!")


if __name__ == "__main__":
    main()