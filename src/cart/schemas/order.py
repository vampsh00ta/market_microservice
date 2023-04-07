from pydantic import BaseModel
from pydantic import BaseModel
from datetime import datetime
from src.cart.schemas.item import Item
from pydantic.typing import ForwardRef
from typing import List

class MakeOrder(BaseModel):
    email:str = 'test'
    street:str = 'test'



class Order(BaseModel):
    id:int
    date:datetime
    items:List[Item]
    class Config:
        orm_mode = True

# ListOrder= ForwardRef("List[Order]")
