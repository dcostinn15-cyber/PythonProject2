import json
import os
from collections import Counter


# 1. INCARCAREA SI VALIDAREA DATELOR

def incarca_investitii(nume_fisier):
    if not os.path.exists(nume_fisier):
        print("Fisierul nu exista.")
        return []

    try:
        with open(nume_fisier, "r", encoding="utf-8") as f:
            investitii = json.load(f)

        if not investitii:
            print("Fisierul este gol.")
            return []

        campuri_obligatorii = ["nume", "cost", "profit", "categorie", "risc"]

        for inv in investitii:
            for camp in campuri_obligatorii:
                if camp not in inv:
                    print(f"Lipseste campul {camp} intr-o investitie.")
                    return []

        return investitii

    except json.JSONDecodeError:
        print("Fisier JSON invalid.")
        return []


# 2. AFISAREA INVESTITIILOR

def afiseaza_investitii(investitii):
    print("\nLISTA INVESTITIILOR\n")

    for inv in investitii:
        print(f"Nume: {inv['nume']}")
        print(f"Cost: {inv['cost']}")
        print(f"Profit: {inv['profit']}")
        print(f"Categorie: {inv['categorie']}")
        print(f"Risc: {inv['risc']}")
        print("-" * 40)


# 3. ANALIZA DESCRIPTIVA

def analiza_investitii(investitii):
    print("\nANALIZA INVESTITIILOR\n")

    print(f"Numar total investitii: {len(investitii)}")

    min_cost = min(investitii, key=lambda x: x["cost"])
    max_cost = max(investitii, key=lambda x: x["cost"])
    max_profit = max(investitii, key=lambda x: x["profit"])

    print(f"Investitia cu cost minim: {min_cost['nume']} ({min_cost['cost']})")
    print(f"Investitia cu cost maxim: {max_cost['nume']} ({max_cost['cost']})")
    print(f"Investitia cu profit maxim: {max_profit['nume']} ({max_profit['profit']})")

    categorii = Counter(inv["categorie"] for inv in investitii)
    riscuri = Counter(inv["risc"] for inv in investitii)

    print("\nDistributie pe categorii:")
    for cat, nr in categorii.items():
        print(f"{cat}: {nr}")

    print("\nDistributie pe niveluri de risc:")
    for risc, nr in riscuri.items():
        print(f"{risc}: {nr}")


# 4. FILTRARE SI SORTARE

def filtreaza_dupa_categorie(investitii, categorie):
    return [inv for inv in investitii if inv["categorie"] == categorie]


def filtreaza_dupa_risc(investitii, risc):
    return [inv for inv in investitii if inv["risc"] == risc]


def sorteaza_dupa_cost(investitii):
    return sorted(investitii, key=lambda x: x["cost"])


def sorteaza_dupa_profit(investitii):
    return sorted(investitii, key=lambda x: x["profit"], reverse=True)


def sorteaza_dupa_raport(investitii):
    return sorted(
        investitii,
        key=lambda x: x["profit"] / x["cost"],
        reverse=True
    )


# 5. VALIDAREA BUGETULUI

def citeste_buget():
    while True:
        try:
            buget = int(input("\nIntroduceti bugetul maxim: "))

            if buget <= 0:
                print("Bugetul trebuie sa fie pozitiv.")
            else:
                return buget

        except ValueError:
            print("Introduceti o valoare valida.")


# 6. PROGRAMARE DINAMICA

def optimizare_investitii(investitii, buget):

# RESTRICTIE SUPLIMENTARA: eliminam investitiile cu risc ridicat

    investitii_filtrate = [
        inv for inv in investitii
        if inv["risc"] != "ridicat"
    ]

    n = len(investitii_filtrate)

    # Tabel DP
    dp = [[0 for _ in range(buget + 1)] for _ in range(n + 1)]

# Construirea tabelului
    for i in range(1, n + 1):

        cost = investitii_filtrate[i - 1]["cost"]
        profit = investitii_filtrate[i - 1]["profit"]

        for b in range(buget + 1):

            # nu luam investitia
            dp[i][b] = dp[i - 1][b]

            # luam investitia daca exista buget
            if cost <= b:
                dp[i][b] = max(
                    dp[i][b],
                    profit + dp[i - 1][b - cost]
                )

 # RECONSTRUIREA SOLUTIEI

    investitii_selectate = []

    b = buget

    for i in range(n, 0, -1):

        if dp[i][b] != dp[i - 1][b]:

            investitii_selectate.append(
                investitii_filtrate[i - 1]
            )

            b -= investitii_filtrate[i - 1]["cost"]

    investitii_selectate.reverse()

    profit_total = dp[n][buget]
    cost_total = sum(inv["cost"] for inv in investitii_selectate)
    buget_ramas = buget - cost_total

    return (
        profit_total,
        cost_total,
        buget_ramas,
        investitii_selectate,
        dp
    )


# 7. AFISAREA TABELULUI DP (Dynamic Programming)

def afiseaza_tabel_dp(dp, buget):
    print("\nTABEL DP (partial)\n")

    for i in range(len(dp)):
        print(dp[i][:min(buget + 1, 20)])


# 8. AFISAREA REZULTATULUI FINAL

def afiseaza_rezultat(
        buget,
        profit_total,
        cost_total,
        buget_ramas,
        investitii_selectate):

    print("\nREZULTAT FINAL")
    print("=" * 40)

    print(f"Buget disponibil: {buget}")
    print(f"Profit optim: {profit_total}")
    print(f"Cost total utilizat: {cost_total}")
    print(f"Buget ramas: {buget_ramas}")

    print("\nInvestitii selectate:")

    if not investitii_selectate:
        print("Nu exista investitii selectate.")
    else:
        for inv in investitii_selectate:
            print(f"- {inv['nume']}")


# FUNCTIA PRINCIPALA

def main():

    nume_fisier = "investitii.json"

    investitii = incarca_investitii(nume_fisier)

    if not investitii:
        return

    afiseaza_investitii(investitii)

    analiza_investitii(investitii)

    while True:

        buget = citeste_buget()

        (
            profit_total,
            cost_total,
            buget_ramas,
            investitii_selectate,
            dp
        ) = optimizare_investitii(investitii, buget)

        afiseaza_tabel_dp(dp, buget)

        afiseaza_rezultat(
            buget,
            profit_total,
            cost_total,
            buget_ramas,
            investitii_selectate
        )

        raspuns = input(
            "\nDoriti o noua analiza? (da/nu): "
        ).lower()

        if raspuns != "da":
            break



if __name__ == "__main__":
    main()