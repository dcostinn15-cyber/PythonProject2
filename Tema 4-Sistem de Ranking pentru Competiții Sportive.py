import json

#1 Citire date din JSON
def incarca_date():
    try:
        with open("competitori.json", "r") as f:
            return json.load(f)
    except:
        return []


#2 Afisare lista
def afiseaza(lista):
    if not lista:
        print("Lista este goala!")
        return

    for c in lista:
        print(c)


#3 Adaugare competitor
def adauga_competitor(lista):
    nume = input("Nume: ").strip()
    if not nume:
        print("Numele nu poate fi gol!")
        return

    punctaj = int(input("Punctaj: "))
    timp = int(input("Timp: "))

    lista.append({
        "nume": nume,
        "punctaj": punctaj,
        "timp": timp
    })


#4 Actualizare competitor
def actualizeaza_competitor(lista):
    nume = input("Numele competitorului: ")

    for c in lista:
        if c["nume"] == nume:
            c["punctaj"] = int(input("Nou punctaj: "))
            c["timp"] = int(input("Nou timp: "))
            return

    print("Competitor inexistent!")


#5 Functie de comparatie
def compara(a, b):
    if a["punctaj"] != b["punctaj"]:
        return a["punctaj"] > b["punctaj"]  # descrescator

    if a["timp"] != b["timp"]:
        return a["timp"] < b["timp"]        # crescator

    return a["nume"] < b["nume"]            # alfabetic


#6 Quicksort
def quicksort(lista):
    if len(lista) <= 1:
        return lista

    pivot = lista[0]
    stanga = []
    dreapta = []

    for x in lista[1:]:
        if compara(x, pivot):
            stanga.append(x)
        else:
            dreapta.append(x)

    return quicksort(stanga) + [pivot] + quicksort(dreapta)


#7 Clasament
def clasament(lista):
    if not lista:
        print("Nu exista competitori!")
        return

    lista_sortata = quicksort(lista)

    print("\nLoc  Nume                Punctaj  Timp")

    loc = 1
    for i in range(len(lista_sortata)):
        if i > 0:
            prev = lista_sortata[i-1]
            curr = lista_sortata[i]

            if not (
                prev["punctaj"] == curr["punctaj"] and
                prev["timp"] == curr["timp"]
            ):
                loc = i + 1

        c = lista_sortata[i]
        print(f"{loc:<4} {c['nume']:<18} {c['punctaj']:<8} {c['timp']}")


#8 Statistici
def statistici(lista):
    if not lista:
        print("Lista este goala!")
        return

    punctaje = [c["punctaj"] for c in lista]
    timpi = [c["timp"] for c in lista]

    print("\nStatistici:")
    print("Numar competitori:", len(lista))
    print("Punctaj maxim:", max(punctaje))
    print("Punctaj minim:", min(punctaje))
    print("Media punctajelor:", sum(punctaje) / len(lista))
    print("Cel mai bun timp:", min(timpi))


#9 Meniu
def meniu():
    lista = incarca_date()

    while True:
        print("\n=== MENIU ===")
        print("1. Afisare competitori")
        print("2. Adaugare competitor")
        print("3. Actualizare competitor")
        print("4. Sortare (Quicksort)")
        print("5. Clasament")
        print("6. Statistici")
        print("0. Iesire")

        opt = input("Alege optiunea: ")

        if opt == "1":
            afiseaza(lista)
        elif opt == "2":
            adauga_competitor(lista)
        elif opt == "3":
            actualizeaza_competitor(lista)
        elif opt == "4":
            lista = quicksort(lista)
            print("Sortare realizata!")
        elif opt == "5":
            clasament(lista)
        elif opt == "6":
            statistici(lista)
        elif opt == "0":
            print("La revedere!")
            break
        else:
            print("Optiune invalida!")


#10 Start program
if __name__ == "__main__":
    meniu()