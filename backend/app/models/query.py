from pydantic import BaseModel
class QueryRequest(BaseModel):
    """
    Pydantic model for validating incoming API requests.

    Attributes:
        query (str): The user's input text to be processed.
    """
    query: str