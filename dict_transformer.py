"""
Collection of classes to process Abstract dictionary trees.
(like what Python json.parsers offers)
"""
from typing import Callable, Any
from copy import deepcopy
import json
class DictTreeTrans:

    @staticmethod
    def last_dict_of_path(data:dict, path:str) -> list[dict, str]:
        """Search last dictionary from data according the path. Return dictionary and key.
        
        If path is: `"detail.name.surname"` function return `(data.detail.name, "surname")`
        """
        paths = path.split(".")
        if len(paths) > 1:
            last = paths.pop()
            for obj in paths:
                target_obj = data[obj]
            return (target_obj, last) 
        else:
            return (data, paths[0])
        
    @staticmethod
    def remove_path(data:dict, path:str):
        """Delete target path from dictionary.
        
        Ignores `KeyError`: Missing key is intrepret as success.
        """
        try:
            obj, key = DictTreeTrans.last_dict_of_path(data, path)
            obj.pop(key)
            return True
        except KeyError:
            return True

    @staticmethod
    def insert_to_path(data:dict, path:str, insert_data:Any):
        """Insert new data to location of path
        """
        obj, key = DictTreeTrans.last_dict_of_path(data, path)
        obj[key] = insert_data

    @staticmethod
    def data_from_path(data:dict, path:str, fallback:Any = False):
        try:
            parts = path.split(".")
            tree_d = data[parts[0]] 
            for part in parts[1:]:
                tree_d = tree_d[part]
            return tree_d
        except (KeyError, TypeError) as e:
            if fallback is not False:
                return fallback
            else:
                raise e


    @staticmethod
    def ignore_absent_field(data:dict, keys: list[str], fallback:Any)->list[Any]:
        """Iterate trough all keys and ignore all absent fields in data and return fallback value
        Return list of results.
        if value is `None`fallback is used
        """
        results = []
        for field in keys:
            res = data.get(field, fallback)
            if res == None:
                res = fallback
            results.append(res)
        if len(results) > 0:
            return results
        else: return [fallback]
        

    def transform(self, data:dict) :
        """Mutate inserted data according the rules of instance"""
        raise NotImplementedError("Missing interface")
    
class TransPattern(DictTreeTrans):
    path:str ="mainBusinessLine.type"
    target_path:str  = "mainBusinessLine"
    function:Callable
    delete_origin = False
    def __init__(self, path, target, function, delete_origin = False):
        self.path = path
        self.target_path = target
        self.function = function
        self.delete_origin = delete_origin

    def transform(self, data:dict):
        self.insert_to_path(data, self.target_path, self.function(data, self.path))
        if self.delete_origin: self.remove_path(data, self.path)

class DeletePatterns(DictTreeTrans):
    def __init__(self, paths:list[str]):
        self.paths = paths

    def transform(self, data:dict):
        for path in self.paths:
            DeletePatterns.remove_path(data, path)


class DictTransformer:
    """ABC for dictionary transform classes.
    Class interface with DictTreeTrans-type classes that has transform interface
    """
    validation:list[Callable[[dict], bool]]
    """list of functions that took data-dictionary and return `bool` value for validation"""
    trans_functions:list[DictTreeTrans]
    """Transformation object having `.transform(data:dict)` interface """

    @classmethod
    def transform(cls, data:dict):
        cls.rejects = []
        for validator in cls.validation:
            if not validator(data):
                return (False, data)

        new_data = deepcopy(data)
        for trans in cls.trans_functions:
            trans.transform(new_data)
        return ( True, new_data)
