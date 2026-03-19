
import math
import time
import sys
import requests 
from  dataclasses import dataclass, asdict

@dataclass
class YritysQuery:
    BASE_URL = "https://avoindata.prh.fi/opendata-ytj-api/v3/"
    API_PER_PAGE = 100
    VERSION = "v3"

    """Validit parametrit"""
    name:str = None
    """Toiminimen mukaan"""
    location: str= None
    """Sijainti, joko alue tai postinumero int[len(5)]"""
    companyForm:str = None
    """Yritysmuotojen koodit"""
    businessId: str|int = None
    """Y-tunnus"""
    mainBusinessLine: str|int = None
    """Päätoimiala kuvaus tai alanumero int[len(5)]"""
    postCode: str|int = None
    """Käynti osoitteen postinumero"""
    registrationDateStart:str = None
    registrationDateEnd:str = None
    businessIdRegistrationStart: str = None
    businessIdRegistrationEnd:str = None

    def build_url_query(self):
        """Muodosta http-url"""
        query = self.BASE_URL + "companies" "?"
        for (a, l) in asdict(self).items() :
            if l is not None:
                query += f"{a}={l}&"
        query = query[:-1] # Pop last &-symbol
        return query
    
    def url_with_page(self, page:int):
        q = self.build_url_query()
        return q + f"&page={page}"


class YRITYSApi :
    BASE_URL = "https://avoindata.prh.fi/opendata-ytj-api/v3/"
    API_PER_PAGE = 100

    def __init__(self):
        pass

    def request(self, request) -> dict[str, dict, list]:
        res = requests.get(request, timeout=5, headers={"accept": "application/json"})
        res.raise_for_status()
        return res.json()

    ## TODO Tämä methodi ei palauta json muotoista dataa vaan zip-tiedoston
    # def all_companies(self, ytunnus:str) :
    #     return self.request(self.BASE_URL + "all_companies")

    
    def get_query(self, components:YritysQuery) -> dict[str, dict]:
        """Hae yhden kyselyn mukaiset tulokset"""
        result = self.request(components.build_url_query())
        return result["companies"]
  
    def get_pages(self, components:YritysQuery, start_page = 1, all = True):
        """Kun tuloksena on enemmän kuin 100 oliota,
        palautetaan tulokset 100 sarjojen sivuissa.
        """
        t0 = time.perf_counter()
        first_page  = self.request(components.url_with_page(1))
        request_time = time.perf_counter()- t0
        total = first_page["totalResults"]
        data:list = first_page["companies"]
        print("Tulokset haulla", total)

        if all and total > 100 :
            max_pages = math.ceil(total / self.API_PER_PAGE) 
            pages_left = max_pages - start_page
            print("Datan sivumäärä: ", max_pages)
            print("Sivuja jäljellä haettavaksi", pages_left, "aloittaen sivusta: ", start_page)
            minutes, seconds = divmod(request_time * pages_left , 60)
            print(f"Arvioitu aika: {minutes} min {seconds:.1f} s")

            for i in range(start_page, max_pages +1):

                print("|", end="", flush=True)
                query = components.url_with_page(i)
                try:
                    res = self.request(query)
                except requests.HTTPError as e:
                    if e.response.status_code == 429:
                        time.sleep(1.0)
                        res = self.request(query)
                    else:
                        raise e
                result_data = res["companies"]

                if len(result_data) == 0:
                    print("\nEnding before end at page",i, "got empty result" )
                    break
                data.extend(result_data)
                
        return data

