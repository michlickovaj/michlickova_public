from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

Baze = declarative_base()
engine = create_engine('sqlite:///pojistenci.db')
Session = sessionmaker(bind=engine)


class Pojistenec(Baze):
    """Třída reprezentující entitu pojištěnce v databázi."""

    __tablename__ = 'pojistenci'
    id = Column(Integer, primary_key=True)
    jmeno = Column(String)
    prijmeni = Column(String)
    vek = Column(Integer)
    telefon = Column(String)

    def __str__(self):
        """Vrátí textovou reprezentaci instance."""
        return f"{self.id:<5}\t{self.jmeno:<12}\t{self.prijmeni:<20}\t{self.vek:<4}\t{self.telefon:<12}"
Baze.metadata.create_all(engine)