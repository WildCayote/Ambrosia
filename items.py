from fastapi import APIRouter
from fastapi import FastAPI , Request, Header
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from sqlite3 import Timestamp
import time

import qrcodegen
import models  
from security import JWT , hash
from databaseService import Owner , Admin , Waiter , PaymentTypes , Menu , Item , HotelTable , Order
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse


router = APIRouter(
    tags = ["items"]
)


templates = Jinja2Templates(directory="./menu/menu")

router.mount("/static" , StaticFiles(directory="./menu/menu") , name="static")



@router.get("/menus/items")
def getItems(token: str = Header()):
    token = JWT.verify(token)
    if not token['valid']:
        return {
            'success': False,
            'message': token['error']
        }
    userId = token['payload']['user-id']
    res = Menu.getUserMenu(userId)
    menuId = res[0]
    items = Item.getMenuItems(menuId)
    result = []

    if items:
        for i in items:
            result.append(
                {
                    "itemId": i[0],
                    "name": i[2],
                    "description": i[3],
                    "price": i[4]
                }
            )
        return result
    else:
         return{
            "success" : False,
            "message" : "none"
        }


@router.post("/menus/items/update")
def updateItems(item: models.itemUpdate):
    item.itemId = int(item.itemId)
    token = JWT.verify(item.token)
    if not token['valid']:
        return {
            'success': False,
            'message': token['error']
        }

    userId = token['payload']['user-id']
    return Item.updateItem(**item.dict())


@router.post("/menus/items")
def addItems(item: models.itemAdd):
    token = JWT.verify(item.token)
    if not token['valid']:
        return {
            'success': False,
            'message': token['error']
        }
    return Item.createMenuItems(**item.dict())


@router.delete("/menus/items")
def deleteItems(item: models.itemDelete):
    token = JWT.verify(item.token)
    if not token['valid']:
        return {
            'success': False,
            'message': token['error']
        }
    return Item.removeMenuItem(**item.dict())


