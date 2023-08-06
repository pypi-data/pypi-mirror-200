import pandas

from mimeo import utils
from mimeo.database.exc import InvalidIndex


class Country:

    def __init__(self, iso_3: str, iso_2: str, name: str):
        self.iso_3 = iso_3
        self.iso_2 = iso_2
        self.name = name

    def __str__(self) -> str:
        return str({
            "iso_3": self.iso_3,
            "iso_2": self.iso_2,
            "name": self.name
        })

    def __repr__(self) -> str:
        return f"Country('{self.iso_3}', '{self.iso_2}', '{self.name}')"


class CountriesDB:

    NUM_OF_RECORDS = 239
    __COUNTRIES_DB = "countries.csv"
    __COUNTRIES_DF = None
    __COUNTRIES = None

    def get_country_at(self, index: int) -> Country:
        countries = self.__get_countries()
        try:
            return countries[index]
        except IndexError:
            raise InvalidIndex(f"Provided index [{index}] is out or the range: 0-{len(countries)-1}!")

    def get_country_by_iso_3(self, iso_3: str) -> Country:
        countries = self.__get_countries()
        return next(filter(lambda country: country.iso_3 == iso_3, countries), None)

    def get_country_by_iso_2(self, iso_2: str) -> Country:
        countries = self.__get_countries()
        return next(filter(lambda country: country.iso_2 == iso_2, countries), None)

    def get_country_by_name(self, name: str) -> Country:
        countries = self.__get_countries()
        return next(filter(lambda country: country.name == name, countries), None)

    @classmethod
    def get_countries(cls) -> list:
        return cls.__get_countries().copy()

    @classmethod
    def __get_countries(cls) -> list:
        if cls.__COUNTRIES is None:
            cls.__COUNTRIES = [Country(row.ISO_3, row.ISO_2, row.NAME)
                               for row in cls.__get_countries_df().itertuples()]
        return cls.__COUNTRIES

    @classmethod
    def __get_countries_df(cls) -> pandas.DataFrame:
        if cls.__COUNTRIES_DF is None:
            cls.__COUNTRIES_DF = pandas.read_csv(utils.get_resource(CountriesDB.__COUNTRIES_DB))
        return cls.__COUNTRIES_DF
