import json
import hashlib
import os
import secrets
#bibliotecile folosite

#1fișierul unde se salvează datele
FILE_NAME = "parole.json"


#2clasa Nod
class Nod:
    def __init__(self, site, username, parola):
        self.site = site
        self.username = username
        self.parola = parola
        self.next = None
        #reprezintă un cont salvat


#3clasa ListaParole
class ListaParole:
    def __init__(self):
        self.head = None
        #aceasta este o listă simplu înlănțuită
        #la început lista este goala
        #head=primul element din lista

#4funcția de adăugare
    def adauga(self, site, username, parola):
        nod = Nod(site, username, parola)
        #creeaza un nod nou

        if self.head is None:
            self.head = nod
            return
        #daca lista este goala nodul devine primul element

        curent = self.head
        while curent.next:
            curent = curent.next
        curent.next = nod
        #daca lista nu este goala, programul merge pana la ultimul nod si adauga contul nou la final

#5functia de afisare
    def afiseaza(self):
        if self.head is None:
            print("Nu exista parole salvate.")
            return
        #daca nu exista conturi, afiseaza mesajul....

        curent = self.head
        while curent:
            print(f"\nSite: {curent.site}")
            print(f"Username: {curent.username}")
            print(f"Parola: {curent.parola}")
            curent = curent.next
            #daca exista conturi, parcurge lsita si afiseaza fiecare cont

#6functia de cautare
    def cauta(self, site):
        curent = self.head
        #pornim de la primul cont

        while curent:
            if curent.site.lower() == site.lower():
                return curent
            curent = curent.next
            # compara site ul introdus cu fiecare site salvat
            # lower ca sa nu conteze literele mari sau mici
        return None
    #daca nu gaseste nimic


#7functia de stergere
    def sterge(self, site):
        curent = self.head #nodul verificat acum
        anterior = None #nodul dineaintea lui

        while curent:
            if curent.site.lower() == site.lower():

                if anterior is None:
                    self.head = curent.next
                    #daca nodul de sters este primul mutam inceputul liste la urmatorul nod
                else:
                    anterior.next = curent.next
                    #daca nodul este in mijloc sau la final sarim peste nodul sters

                return True
            #daca stergerea a reusit

            anterior = curent
            curent = curent.next

        return False
    #daca nu s a gasit site ul

#8tranformarea listei in lista normala
    def in_lista(self):
        date = []
        #tranforma lista inlantuita in lista normala python
        curent = self.head

        while curent:
            date.append({
                "site": curent.site,
                "username": curent.username,
                "parola": curent.parola
            })
            #salvat in fisier json
            curent = curent.next

        return date

#9incarcarea datelor in lista
    def incarca(self, date):
        for item in date:
            self.adauga(
                item["site"],
                item["username"],
                item["parola"]
            )
            #ia datele din fisierul json si le pune inapoi in lista inlantuita


#10functia de hashing
def hash_parola(parola, salt):
    return hashlib.sha256((parola + salt).encode()).hexdigest()
#face hashing ul parolei principale
#parola este combinata cu un salt
#apoi il transforma intr un hash
#in fisier nu se salveaza parola reala


#11functia initializare
def initializare():

        parola_master = input("Seteaza parola principala: ")
        #daca nu exista cere parola principala

        salt = secrets.token_hex(16)
        hash_master = hash_parola(parola_master, salt)

        date = {
            "salt": salt,
            "master_hash": hash_master,
            "parole": []
        }

        with open(FILE_NAME, "w") as f:
            json.dump(date, f, indent=4)
            #o salveaza in fisier

        print("Parola principala a fost salvata.")


#12functia autentificare
def autentificare():
    print("Caut fisierul aici:", os.path.abspath(FILE_NAME))
    with open(FILE_NAME, "r") as f:
        date = json.load(f)
        #citeste datele din fisier

    parola = input("Introdu parola principala: ")

    if hash_parola(parola, date["salt"]) == date["master_hash"]:
        #comapara cu hash ul salvat

        print("Autentificare reusita.")
        return True

    print("Parola incorecta!")
    return False
#daca sunt egale parola este corecta, daca nu, nu


#13incarcarea si salvarea fisierelor
def incarca_date():
    with open(FILE_NAME, "r") as f:
        return json.load(f)
    #citeste fisierul json


def salveaza_date(date):
    with open(FILE_NAME, "w") as f:
        json.dump(date, f, indent=4) #ident=4 face fisierul mai frumos aranjat
        #salveaza datele in fisier

#14functia principala meniu
def meniu():
    initializare()
    #verifica daca aplicatia trebuie initializata

    if not autentificare():
        return
    #cere autentificare
    #daca parola este gresita programul se opreste

    date = incarca_date()
#daca este corecta citeste datele
    lista = ListaParole()
    #creaza lista
    lista.incarca(date["parole"])
    #incarca parolele salvate

#16meniul aplicatiei.
    while True:

        print("\n===== MANAGER DE PAROLE =====")
        print("1. Adauga cont")
        print("2. Afiseaza conturi")
        print("3. Cauta cont")
        print("4. Sterge cont")
        print("5. Salveaza")
        print("0. Iesire")

        opt = input("Alege optiunea: ")

#optiunea 1 adaugare cont.
        if opt == "1":

            site = input("Site: ")
            username = input("Username: ")
            parola = input("Parola: ")

            lista.adauga(site, username, parola)
            #se adauga contul in lista inlantuita

            print("Cont adaugat.")

#optiunea 2 afisare conturi
        elif opt == "2":

            lista.afiseaza()

#optiunea 3 cautare cont
        elif opt == "3":

            site = input("Site cautat: ")

            rezultat = lista.cauta(site)
            #cauta contul dupa site

            if rezultat:
                print("\nGasit:")
                print("Site:", rezultat.site)
                print("Username:", rezultat.username)
                print("Parola:", rezultat.parola)
            else:
                print("Nu exista.")

#optiunea 4 stergere cont
        elif opt == "4":

            site = input("Site de sters: ")

            if lista.sterge(site):
                print("Sters cu succes.")
            else:
                print("Nu exista.")

#optiunea 5 salvare.
        elif opt == "5":

            date["parole"] = lista.in_lista()
            salveaza_date(date)
            #tranforma lista inlantuita intr o lista normala si o salveaza in json

            print("Date salvate.")

#optiunea o iesire.
        elif opt == "0":

            date["parole"] = lista.in_lista()
            salveaza_date(date)

            print("La revedere!")
            break

        else:
            print("Optiune invalida.")
            #salveaza datele si opreste programul.

#pornirea programului.
if __name__ == "__main__":
    meniu()