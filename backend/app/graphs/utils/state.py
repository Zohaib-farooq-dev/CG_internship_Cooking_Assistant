from typing_extensions import TypedDict
class MyState(TypedDict):
    query : str
    classifier : str 
    content : dict
    evaluate: dict
