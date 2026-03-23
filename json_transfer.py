"""
Muunnoskerros yritysApi:n tuottaman datan ja sisäisen formaatin välillä
"""
from dict_transformer import DictTransformer, DictTreeTrans, DeletePatterns, TransPattern
import json

class YritysRekisteriMuutos(DictTransformer):
    API_VERSION = "V3"

    @staticmethod
    def voimassaoleva(data:dict):
        """Yritys ei ole lakkautettu"""
        if data["tradeRegisterStatus"] == "4":
            return False
        else:
            return True
        
    @staticmethod
    def Toimialanimi(data:dict, path:str):
        for lan in data[path]["descriptions"]:
            if lan["languageCode"] == "1":
                return lan["description"]
    @staticmethod
    def main_name(data:dict, path:str) -> str:
        names: list[dict] = data[path]
        return names[0]["name"]

    @staticmethod
    def yhtiomuoto(data:dict, path:str) -> str:

        for lan in data[path][0]["descriptions"]:
            if lan["languageCode"] == "1":
                return lan["description"]
    @staticmethod
    def osoite(data:dict, path:str) -> str:
        osoite = data[path][0]
        try:
            comps = DictTreeTrans.ignore_absent_field(osoite,["street","buildingNumber","entrance","apartmentNumber" , "apartmentIdSuffix"],"")
            full_osoite = " ".join(comps).rstrip()
            return full_osoite
        except TypeError as e:
            print("Osoite typeError: ", data["names"][0]["name"])
            return None
        
    @staticmethod
    def kaupunki(data:dict, path:str) -> str:
        offices = data[path][0]["postOffices"]
        for office in offices:
            if office["languageCode"] == "1":
                return office["city"]
        return None

    KAUPUNKI = TransPattern("addresses", "Kaupunki", kaupunki)
    OSOITE = TransPattern("addresses", "Osoite", osoite)
    YHTIOMUOTO = TransPattern("companyForms", "Yhtiomuoto", yhtiomuoto)
    TOIMIALA = TransPattern("mainBusinessLine", "Toimiala", Toimialanimi)
    REMOVE_BSN_DETAIL = TransPattern("mainBusinessLine.type","Toimialakoodi", lambda d, path: DictTreeTrans.data_from_path(d, path ))
    MAIN_NAME = TransPattern("names", "Nimi", main_name, True)
    REGISTER_DATE = TransPattern("registrationDate", "Rekisterointi_pvm",lambda d, path: DictTreeTrans.data_from_path(d, path ) )
    WEBSITE = TransPattern("website.url", "Website", lambda d, path: DictTreeTrans.data_from_path(d, path, None ))
    POISTETTAVAT_KENTÄT = DeletePatterns(["website","mainBusinessLine", "addresses", "euId", "businessId", "companyForms", "companySituations", "registeredEntries", "registrationDate"])
    Y_TUNNUS = TransPattern("businessId.value", "Y_tunnus", lambda d, path: DictTreeTrans.data_from_path(d, path))
    
    validation = [voimassaoleva]
    trans_functions = [WEBSITE, KAUPUNKI, OSOITE,YHTIOMUOTO, Y_TUNNUS,TOIMIALA, MAIN_NAME, REMOVE_BSN_DETAIL, REGISTER_DATE, POISTETTAVAT_KENTÄT]


ALAKOODIT = ["62100", # Ohjelmointi 
             "71127", # Kone ja prosessisuunnittelu.
             "71129" # Muu tekninen palvelu
             ]
ALA_KOMBINAATIOT = ("62", "621", "6210", "63", "72","71")
ALAKOODIT_BLACKLIST = ["71202", #Autokatsastus
                       "71110" # Arkitehtipalvelut
                       ]
class OHJELMATEKNINEN(YritysRekisteriMuutos):

    @staticmethod
    def tekninen_ala(data:dict):
        try:
            bussinesline = data["mainBusinessLine"]
            if bussinesline == None:
                return False
            alakoodi:str = bussinesline["type"]
            
            if alakoodi in ALAKOODIT:
                if alakoodi == "71202": 
                    print("tieteelline", data["names"][0]["name"])
                return True
            else:
                if alakoodi.startswith(ALA_KOMBINAATIOT):
                    if alakoodi not in ALAKOODIT_BLACKLIST:
                        return True
        except KeyError as e:
            return False

        return False

    validation = []
    validation.extend(YritysRekisteriMuutos.validation)
    validation.extend([tekninen_ala])

