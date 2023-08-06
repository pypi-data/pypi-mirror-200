import pandas

from mimeo import utils
from mimeo.database.exc import InvalidIndex


class City:

    def __init__(self, identifier: str, name: str, name_ascii: str, country: str):
        self.id = int(identifier)
        self.name = name
        self.name_ascii = name_ascii
        self.country = country

    def __str__(self) -> str:
        return str({
            "id": self.id,
            "name": self.name,
            "name_ascii": self.name_ascii,
            "country": self.country
        })

    def __repr__(self) -> str:
        return f"City('{self.id}', '{self.name}', '{self.name_ascii}', '{self.country}')"


class CitiesDB:

    NUM_OF_RECORDS = 42905
    __CITIES_DB = "cities.csv"
    __CITIES_DF = None
    __CITIES = None
    __COUNTRY_CITIES = {}

    def get_city_at(self, index: int) -> City:
        cities = self.__get_cities()
        try:
            return cities[index]
        except IndexError:
            raise InvalidIndex(f"Provided index [{index}] is out or the range: 0-{CitiesDB.NUM_OF_RECORDS-1}!")

    def get_cities_of(self, country_iso3: str) -> list:
        return self.__get_country_cities(country_iso3).copy()

    @classmethod
    def get_cities(cls) -> list:
        return cls.__get_cities().copy()

    @classmethod
    def __get_country_cities(cls, country_iso3: str) -> list:
        if country_iso3 not in cls.__COUNTRY_CITIES:
            cities = cls.__get_cities()
            cls.__COUNTRY_CITIES[country_iso3] = list(filter(lambda city: city.country == country_iso3, cities))
        return cls.__COUNTRY_CITIES[country_iso3]

    @classmethod
    def __get_cities(cls) -> list:
        if cls.__CITIES is None:
            cls.__CITIES = [City(row.ID, row.CITY, row.CITY_ASCII, row.COUNTRY)
                            for row in cls.__get_cities_df().itertuples()]
        return cls.__CITIES

    @classmethod
    def __get_cities_df(cls) -> pandas.DataFrame:
        if cls.__CITIES_DF is None:
            cls.__CITIES_DF = pandas.read_csv(utils.get_resource(CitiesDB.__CITIES_DB))
        return cls.__CITIES_DF
