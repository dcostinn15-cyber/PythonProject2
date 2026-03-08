produse = ["espresso", "latte", "cappuccino", "ceai", "ciocolata calda", "croissant"]
preturi = [8.0, 12.0, 11.0, 7.0, 10.0, 9.0]
stoc = [20, 15, 18, 30, 12, 10]
cant_comanda = [0, 0, 0, 0, 0, 0]
#1
def afisare_meniu(produse, preturi, stoc):
    for i in range(len(produse)):
        print(i, produse[i], "- Pret:", preturi[i], "lei - Stoc:", stoc[i])
#2
def adauga_in_comanda(cant_comanda, stoc, index, cantitate):

    if index < 0 or index >= len(stoc):
        print("Index invalid")
        return

    if cantitate <= 0:
        print("Cantitate invalida")
        return

    stoc_disponibil = stoc[index] - cant_comanda[index]

    if cantitate > stoc_disponibil:
        print("Stoc insuficient")
        return

    cant_comanda[index] += cantitate
    print("Produs adaugat in comanda")
#3
def scade_din_comanda(cant_comanda, index, cantitate):

    if index < 0 or index >= len(cant_comanda):
        print("Index invalid")
        return

    if cantitate <= 0:
        print("Cantitate invalida")
        return

    if cantitate > cant_comanda[index]:
        print("Nu poti scadea mai mult decat exista in comanda")
        return

    cant_comanda[index] -= cantitate
    print("Produs scazut din comanda")
#4
def calculeaza_total(cant_comanda, preturi):

    total = 0

    for i in range(len(cant_comanda)):
        total += cant_comanda[i] * preturi[i]

    return total
#5
def stabilire_reducere(total, tip):

    reducere = 0

    if tip == "student" and total >= 30:
        reducere = total * 0.10

    elif tip == "fidelitate" and total >= 50:
        reducere = total * 0.15

    if reducere > total:
        reducere = total

    return reducere
#6
def afisare_bon(produse, preturi, cant_comanda, total, reducere):

    print("----- BON -----")

    for i in range(len(produse)):
        if cant_comanda[i] > 0:
            subtotal = cant_comanda[i] * preturi[i]
            print(produse[i], "x", cant_comanda[i], "=", subtotal, "lei")

    print("----------------")
    print("Total:", total, "lei")
    print("Reducere:", reducere, "lei")
    print("Total final:", total - reducere, "lei")
#7
def finalizare_comanda(stoc, cant_comanda):

    for i in range(len(stoc)):
        stoc[i] -= cant_comanda[i]
        cant_comanda[i] = 0

    print("Comanda finalizata")
#8
def anulare_comanda(cant_comanda):

    for i in range(len(cant_comanda)):
        cant_comanda[i] = 0

    print("Comanda anulata")

