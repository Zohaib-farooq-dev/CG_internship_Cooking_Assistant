"""
Defines the Pydantic model for handling incoming API requests.

`QueryRequest` validates that each request contains a single field:
    - query (str): The user’s input text to be processed.
"""
from pydantic import BaseModel
class QueryRequest(BaseModel):
    query: str