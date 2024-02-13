from pydantic import BaseModel
from typing  import Optional , Union , List
from security import hash , JWT

class OwnerLogin(BaseModel):
    email : str
    password : str


class OwnerCreateAccount(BaseModel):
    email : str
    password : str
    firstName : str
    lastName : str
    hotelName : str
    birthDate : str
    phoneNum : str
    paymentClass : int = 1


class AdminLogin(BaseModel):
    adminName : str
    password : str


class WaiterLogin(BaseModel):
    userName : int
    password : str


class CreateWaiter(BaseModel):
    token : str
    userName : str
    password : str


class DeleteWaiter(BaseModel):
    token : str
    waiterId : int


class UpdateServicePrice(BaseModel):
    token : str
    id : int
    price : float


class UpdateServiceDescription(BaseModel):
    token : str
    id : int
    description : str       


class MenuItem(BaseModel):
    itemId : int
    amount : int


class OrderFromMenu(BaseModel):
    menuId : int
    tableNum : int
    items : List[MenuItem]


class GetUplacedOrders(BaseModel):
    token : str


class WaiterPlaceOrder(BaseModel):
    token : str
    menuId : int


###################################################################

class menuCreate(BaseModel):
    name: str
    description: str 
    token: str

class menuUpdate(BaseModel):
    description: str 
    name: str
    token: str
    menuId: int
    paymentClass: int = None

class menuDelete(BaseModel):
    token: str
    menuId: int

class itemUpdate(BaseModel):
    itemId: int
    description: str = None
    price: int = None
    token: str

class itemAdd(BaseModel):
    description: str
    menuId: int
    name: str
    price: int
    token: str

class QRcreate(BaseModel):
    menuId: int
    string: str
    token: str

class QRget(BaseModel):
    token: str
    string: str
    

class itemDelete(BaseModel):
    token: str
    itemId: int

class Table(BaseModel):
    token: str
    tablenum: int

class AdminAcc(BaseModel):
    adminName: str
    password: str