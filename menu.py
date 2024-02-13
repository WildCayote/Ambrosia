from fastapi import FastAPI , Request, Header, APIRouter
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
    tags = ["menu"]
)

templates = Jinja2Templates(directory="./menu/menu")

router.mount("/static" , StaticFiles(directory="./menu/menu") , name="static")




@router.get("/menu/{id}")
def getMenu(request: Request, id : int ,  tableId : int = None):
    fetchedMenu = Menu.getMenu(menuId=id)
    if fetchedMenu:
        menuItems = Item.getMenuItems(menuId=id)
        itemResponse = []
        if menuItems:
            for menuItem in menuItems:
                itemResponse.append(
                    {
                    "id" : menuItem[0],
                    "menuId" : menuItem[1],
                    "name" : menuItem[2],
                    "description" : menuItem[3],
                    "price" : menuItem[4]
                    }
                )
            if fetchedMenu[5] == 2:
                return templates.TemplateResponse("expensiveMenu.html" , {"request":request ,"seq" : itemResponse , "table_id":tableId , "menu_Id" : fetchedMenu[0]})
            return templates.TemplateResponse("cheapMenu.html" , {"request":request ,"seq" : itemResponse})
            
        else:
            return{
                "success" : False,
                "message" : "Sorry the menu is currently empty"
            }
    else:
        return {
            "success" : False,
            "message" : "menu not found"
        }
    
    

#order from a menu
@router.post("/menu/order")
def orderFromMenu(payload : models.OrderFromMenu):
    orderedMenu = Menu.getMenu(menuId = payload.menuId)

    #check if the menu exists
    if orderedMenu:
        
        #check whether the menu has order functionality
        if orderedMenu[5] == 2:
            orderdTable = HotelTable.getTableNum(tableNum = payload.tableNum , ownerId=orderedMenu[1])     
        
            #check if the table orderd from exists 
            if orderdTable:
                #loop through each item
                acceptedItems = []
                for item in payload.items:
                    orderdItem = Item.getMenuItem(itemId=item.itemId)
                    #check if the item exists
                    if orderdItem:
                        acceptedItems.append(
                            {
                                "itemId" : orderdItem[0],
                                "tableId" : orderdTable[0],
                                "amount" : item.amount,
                                "price" : orderdItem[4] * item.amount,
                                "menuId" : orderedMenu[0]
                            }
                        )
                    else:
                        acceptedItems = []
                        return{
                            "success" : False,
                            "message" : "Item doesn't exist"
                        }
                
                #loop through each accepted item
                for item in acceptedItems:
                    #create orders for each item
                    Order.createOrder(itemId=item['itemId'] , tableId=item['tableId'] , menuId=item['menuId'] , price=item['price'] , amount=item['amount'])
                
                return {
                    "success" : True,
                    "message" : "Order is placed"
                }    
            else:
                return{
                    "success" : False,
                    "message" : "Table doesn't exists"
                }
        else:
            return{
                "success" : False,
                "message" : "This functionality isn't availbale for this menu"
            }
    else:
        return{
            "success" : False,
            "message" : "Couldn't find the menu"
        }


####################################################################################3

@router.post("/menus")
def createMenu(menu: models.menuCreate):
    token = menu.token
    token = JWT.verify(token)
    if not token['valid']:
        return {
            'success': False,
            'message': token['error']
        }
    ownerId = token['payload']['user-id']
    paymentClass = token['payload']['user-class']
    return (Menu.createMenu(ownerId, menu.name, menu.description, Timestamp.now(), paymentClass))


@router.put("/menus")
def updateMenu(menu: models.menuUpdate):
    token = JWT.verify(menu.token)
    if not token['valid']:
        return {
            'success': False,
            'message': token['error']
        }

    id = token['payload']['user-id']
    return Menu.updateMenu(id, **menu.dict())
    


@router.delete("/menus")
def deleteMenu(menu: models.menuDelete):
    token = JWT.verify(menu.token)
    if not token['valid']:
        return {
            'success': False,
            'message': token['error']
        }

    userId = token['payload']['user-id']
    return Menu.deleteMenu(menu.menuId, userId)


@router.get("/menus")
def getMenus(token: str = Header()):
    token = JWT.verify(token)
    # print(token)
    if token['valid']:
        ownerId = token['payload']['user-id']
        return Menu.getUserMenuDescription(ownerId)
        
    else:
        return {
            "success": False,
            "message": "Access Unauthorized"
        }


