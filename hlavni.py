from databaze import DatabazePojistencu
from pojistenec import Pojistenec


class Hlavni:
    """Hlavní třída pro interakci s programem Evidence pojistěných."""

    def __init__(self):
        """Inicializační metoda pro vytvoření instance."""
        self.databaze = DatabazePojistencu()

    def zobraz_menu(self):
        """Metoda pro zobrazení hlavního menu programu."""
        print("—————————————————————————————————")
        print("Evidence pojistěných")
        print("—————————————————————————————————")
        print("Vyberte si akci:")
        print("1 — Přidat nového pojištěného")
        print("2 — Vypsat všechny pojištěné")
        print("3 — Vyhledat pojištěného")
        print("4 — Editovat pojištěného")
        print("5 — Smazat pojištěného")
        print("6 — Konec")

    def volba(self):
        """Metoda pro zpracování volby uživatele."""
        pokracovat = True
        while pokracovat:
            self.zobraz_menu()
            volba = input("Zvolte číslo operace: ").strip()
            if volba == "1":
                jmeno = self.databaze.nacti_udaj("Zadejte křestní jméno nového pojištěnce:", "text")
                prijmeni = self.databaze.nacti_udaj("Zadejte příjmení nového pojištěnce:", "text")
                vek = self.databaze.nacti_udaj("Zadejte věk nového pojištěnce:", "vek")
                telefon = self.databaze.nacti_udaj("Zadejte telefon nového pojištěnce:", "telefon")

                self.databaze.vytvor_a_uloz_pojistence(jmeno, prijmeni, vek, telefon)
                print("Stiskněte enter pro pokračování...")
                input()
            elif volba == "2":
                if not self.databaze.session.query(Pojistenec).all():
                    print("Databáze je prázdná.")
                    print("Stiskněte enter pro pokračování...")
                    input()
                else:
                    for pojisteny in self.databaze.session.query(Pojistenec).all():
                        print(pojisteny)
                    print("Stiskněte enter pro pokračování...")
                    input()

            elif volba == "3":
                if not self.databaze.session.query(Pojistenec).all():
                    print("Databáze je prázdná.")
                    print("Stiskněte enter pro pokračování...")
                    input()
                else:
                    jmeno = self.databaze.nacti_udaj("Zadejte počáteční písmena jména:", "text")
                    prijmeni = self.databaze.nacti_udaj("Zadejte počáteční písmena příjmení:", "text")
                    nalezeny = self.databaze.vyhledej_pojistence(jmeno, prijmeni)
                    if not nalezeny:
                        print("Pojištěnci s tímto jménem a příjmením nebyli nalezeni.")
                    else:
                        for nalezeny_pojisteny in nalezeny:
                            print(nalezeny_pojisteny)
                    print("Stiskněte enter pro pokračování...")
                    input()
            elif volba == "4":
                self.databaze.edituj_pojistence()
                print("Stiskněte enter pro pokračování...")
                input()
            elif volba == "5":
                self.databaze.smaz_pojistence()
                print("Stiskněte enter pro pokračování...")
                input()
            elif volba == "6":
                print("Konec")
                pokracovat = False
            else:
                print("Neplatná volba, zadejte číslo 1-6.")
                print("Stiskněte enter pro pokračování...")
                input()


hlavni = Hlavni()
hlavni.volba()
