from pojistenec import Pojistenec, Session


class DatabazePojistencu:
    """Třída reprezentující databázi pojistenců a operace s ní spojené."""
    def __init__(self):
        """Inicializační metoda pro vytvoření instance."""
        self.session = Session()

    def nacti_udaj(self, text_zadani, typ_vstupu):
        """Metoda pro načítání uživatelského vstupu s validací.
            :param text_zadani: Textový popis zadání uživatele.
            :param typ_vstupu: Typ očekávaného vstupu ("text", "telefon", "vek").
            :return: Načtený a validovaný uživatelský vstup.
        """

        while True:
            spatne = False
            udaj = input(text_zadani).strip()

            if not udaj:
                print("Vstup nesmí být prázdný.")
                spatne = True
            elif typ_vstupu == "text":
                udaj = udaj.lower().capitalize()
            elif typ_vstupu == "telefon" and not all(znak.isdigit() or znak == "+" for znak in udaj):
                print("Telefon může obsahovat pouze čísla a znak +.")
                spatne = True
            elif typ_vstupu == "vek":
                try:
                    udaj = int(udaj)
                except ValueError:
                    print("Věk musí být pouze číslo.")
                    spatne = True

            if not spatne:
                break

        return udaj

    def vytvor_a_uloz_pojistence(self, jmeno, prijmeni, vek, telefon):
        """
        Metoda pro vytvoření a uložení nového pojistence do databáze.

        :param jmeno: Křestní jméno pojistence.
        :param prijmeni: Příjmení pojistence.
        :param vek: Věk pojistence.
        :param telefon: Telefonní číslo pojistence.
        """
        novy_pojistenec = Pojistenec(jmeno=jmeno, prijmeni=prijmeni, vek=vek, telefon=telefon)
        self.session.add(novy_pojistenec)
        self.session.commit()
        print("Data byla uložena.")

    def vyhledej_pojistence(self, jmeno, prijmeni):
        """
        Metoda pro vyhledání pojistenců dle křestního jména a příjmení.

        :param jmeno: Křestní jméno pro vyhledání.
        :param prijmeni: Příjmení pro vyhledání.
        :return: Seznam nalezených pojistenců.
        """
        nalezeni = self.session.query(Pojistenec).filter(
            Pojistenec.jmeno.startswith(jmeno),
            Pojistenec.prijmeni.startswith(prijmeni)
        ).all()
        return nalezeni

    def vyhledej_pojistence_presne(self, id_pojistence):
        """
       Metoda pro vyhledání pojistence dle konkrétního identifikátoru.

       :param id_pojistence: Identifikátor hledaného pojistence.
       :return: Nalezený pojistenec nebo None, pokud není nalezen.
       """
        hledany_pojistenec = self.session.query(Pojistenec).filter(
            Pojistenec.id == id_pojistence
        ).first()
        return hledany_pojistenec

    def edituj_pojistence(self):
        """ Metoda pro editaci existujícího pojistence v databázi."""
        for pojisteny in self.session.query(Pojistenec).all():
            print(pojisteny)
        editovany_pojistenec = self.vyhledej_pojistence_presne(
            input("Zadejte číslo pojištěnce, kterého chcete editovat:"))

        if editovany_pojistenec:
            spatne = True
            while spatne:
                editovana_polozka = input("Jakou hodnotu chcete změnit? jméno/příjmení/telefon/věk: ")
                if editovana_polozka not in ["jméno", "příjmení", "telefon", "věk"]:
                    print("Neplatná volba, zadejte volbu znovu s jednou z hodnot: jméno/příjmení/telefon/věk.")
                else:
                    if editovana_polozka == "jméno":
                        editovany_pojistenec.jmeno = self.nacti_udaj("Zadejte nové křestní jméno:", "text")
                    elif editovana_polozka == "příjmení":
                        editovany_pojistenec.prijmeni = self.nacti_udaj("Zadejte nové příjmení:", "text")
                    elif editovana_polozka == "telefon":
                        editovany_pojistenec.telefon = self.nacti_udaj("Zadejte nový telefon:", "telefon")
                    elif editovana_polozka == "věk":
                        editovany_pojistenec.vek = self.nacti_udaj("Zadejte nový věk:", "vek")
                    spatne = False
            self.session.commit()
            print("Pojištěnec byl aktualizován.")

        else:
            print("Pojištěnce se nepodařilo najít. Zkuste to znovu.")

    def smaz_pojistence(self):
        """ Metoda pro smazání existujícího pojistence z databáze. """
        for pojisteny in self.session.query(Pojistenec).all():
            print(pojisteny)
        pojistenec_k_vymazani = self.vyhledej_pojistence_presne(
            input("Zadejte číslo pojištěnce, kterého chcete smazat:"))

        if pojistenec_k_vymazani:
            self.session.delete(pojistenec_k_vymazani)
            self.session.commit()
            print(f"Pojištěnec byl smazán.")
        else:
            print("Pojištěnec s danými kritérii nebyl nalezen.")
