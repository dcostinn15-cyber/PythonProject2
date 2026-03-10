


produse = ["espresso", "latte", "cappuccino", "ceai", "ciocolata calda", "croissant"]
preturi = [8.0, 12.0, 11.0, 7.0, 10.0, 9.0]
stoc = [20, 15, 18, 30, 12, 10]
cant_comanda = [0, 0, 0, 0, 0, 0]

reducere_curenta = 0
tip_reducere = None


# 1 Afisare meniu produse
def afisare_meniu(produse, preturi, stoc):
    print("\n--- MENIU ---")
    for i in range(len(produse)):
        print(i, produse[i], "-", preturi[i], "lei | stoc:", stoc[i])


# 2 Adaugare produs
def adauga_produs(cant_comanda, stoc, index, cantitate):
    if index < 0 or index >= len(stoc):
        print("Index invalid")
        return

    if cantitate <= 0:
        print("Cantitate invalida")
        return

    disponibil = stoc[index] - cant_comanda[index]

    if cantitate > disponibil:
        print("Stoc insuficient")
        return

    cant_comanda[index] += cantitate
    print("Produs adaugat")


# 3 Scadere produs
def scade_produs(cant_comanda, index, cantitate):

    if index < 0 or index >= len(cant_comanda):
        print("Index invalid")
        return

    if cantitate <= 0:
        print("Cantitate invalida")
        return

    if cantitate > cant_comanda[index]:
        print("Nu exista atatea produse in comanda")
        return

    cant_comanda[index] -= cantitate
    print("Produs scazut")


# 4 Calcul total
def calcul_total(cant_comanda, preturi):

    total = 0

    for i in range(len(cant_comanda)):
        total += cant_comanda[i] * preturi[i]

    return total


# 5 Stabilire reducere
def stabilire_reducere(total, tip):

    reducere = 0

    if tip == "student":
        if total >= 30:
            reducere = 0.10 * total
        else:
            print("Total insuficient pentru reducere student")

    elif tip == "happy":
        if total >= 50:
            reducere = 0.15 * total
        else:
            print("Total insuficient pentru happy hour")

    elif tip == "cupon":
        if total >= 25:
            reducere = 7
        else:
            print("Total insuficient pentru cupon")

    if reducere > total:
        reducere = total

    return reducere


# 6 Afisare bon
def afisare_bon(produse, preturi, cant_comanda, reducere):

    total = calcul_total(cant_comanda, preturi)

    print("\n--- BON ---")

    for i in range(len(produse)):
        if cant_comanda[i] > 0:
            subtotal = cant_comanda[i] * preturi[i]
            print(produse[i], "x", cant_comanda[i], "=", subtotal)

    print("Total:", total)
    print("Reducere:", reducere)
    print("Total final:", total - reducere)


# 7 Finalizare comanda
def finalizare_comanda(stoc, cant_comanda):

    for i in range(len(stoc)):
        stoc[i] -= cant_comanda[i]
        cant_comanda[i] = 0


# 8 Anulare comanda
def anulare_comanda(cant_comanda):

    for i in range(len(cant_comanda)):
        cant_comanda[i] = 0


# MENIU PRINCIPAL
while True:

    print("""
1 Afisare meniu
2 Adauga produs
3 Scade produs
4 Aplicare reducere
5 Finalizare comanda
6 Anulare comanda
0 Iesire
""")

    opt = input("Alege optiunea: ")

    if opt == "1":
        afisare_meniu(produse, preturi, stoc)

    elif opt == "2":
        index = int(input("Index produs: "))
        cant = int(input("Cantitate: "))
        adauga_produs(cant_comanda, stoc, index, cant)

    elif opt == "3":
        index = int(input("Index produs: "))
        cant = int(input("Cantitate de scazut: "))
        scade_produs(cant_comanda, index, cant)

    elif opt == "4":

        total = calcul_total(cant_comanda, preturi)

        if total == 0:
            print("Comanda este goala")
        else:
            print("""
1 student
2 happy
3 cupon
4 fara reducere
5 inapoi
""")

            r = input("Alege reducerea: ")

            if r == "1":
                reducere_curenta = stabilire_reducere(total, "student")

            elif r == "2":
                reducere_curenta = stabilire_reducere(total, "happy")

            elif r == "3":
                reducere_curenta = stabilire_reducere(total, "cupon")

            elif r == "4":
                reducere_curenta = 0

    elif opt == "5":

        total = calcul_total(cant_comanda, preturi)

        if total == 0:
            print("Nu exista produse in comanda")
        else:
            afisare_bon(produse, preturi, cant_comanda, reducere_curenta)
            finalizare_comanda(stoc, cant_comanda)
            reducere_curenta = 0

    elif opt == "6":
        anulare_comanda(cant_comanda)
        reducere_curenta = 0
        print("Comanda anulata")

    elif opt == "0":
        print("Program inchis")
        break

    else:
        print("Optiune invalida")

