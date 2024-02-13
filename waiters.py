from fastapi import Header, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import models  
from security import JWT , hash
from databaseService import  Waiter , Menu , Item  , Order


router = APIRouter(
    tags = ["waiters"]
)

templates = Jinja2Templates(directory="./menu/menu")

router.mount("/static" , StaticFiles(directory="./menu/menu") , name="static")



#creating Waiters account for a hotel
@router.post("/owner/waiter")
def createWaiter(payload : models.CreateWaiter):
    # print("SDFSFSFSF")
    token = JWT.verify(payload.token)
    if token['valid']:
        if token['payload']['user-class'] == 2:
            waiterCreated = Waiter.createWaiter(ownerId=token['payload']['user-id'] , userName=payload.userName , password=hash(payload.password))
            if waiterCreated == True:
                return{
                    'success' : True,
                    'message' : 'Waiter created'
                }
            else:
                return{
                    'success' : False,
                    'messgae' : waiterCreated
                }
        else:
            return{
                'success' : False,
                'message' : "This feature isn't available for your paymentClass"
            }
 
    else:
        return {
            'success' : False,
            'message' : token['error']
        }


#deleting waiters accound for a hotel
@router.delete("/owner/waiter")
def deleteWaiter(payload : models.DeleteWaiter):
    token = JWT.verify(payload.token)
    if token['valid']:
        if token['payload']['user-class'] == 2:
            waiterDeleted = Waiter.deleteWaiter(ownerId=token['payload']['user-id'] , waiterId=payload.waiterId)
            if waiterDeleted == True:
                return{
                    'success' : True,
                    'message' : 'Waiter account has been deleted'
                }
            else:
                return{
                    'success' : False,
                    'message' : waiterDeleted 
                }
        else:
            return{
                'success' : False,
                'message' : "This feature isn't available for your paymentClass"
            }
 
    else:
        return {
            'success' : False,
            'message' : token['error']
        }



#get new orders
@router.get("/waiter/order")
def getUnplacedOrders(token : str = Header()):
    Token = JWT.verify(token)   
    if Token['valid']:
        loggedInWaiter = Waiter.getWaiterById(Token['payload']['user-id'])
        requestedMenu = Menu.getMenu(Token['payload']['menu-id'])

        #if the menu doesn't exist
        if not requestedMenu or not loggedInWaiter:
            return{
                "success" : False,
                "message" : "menu doesn't exist"
            }

        #check if the waiter is requested the menu of the hotel he/she works for
        if loggedInWaiter[1] == requestedMenu[1]:
            fetchedOrders = Order.waiterGetUnplacedOrderes(Token['payload']["menu-id"])
            unplacedOrders = []
            for order in fetchedOrders:
                orderItem = Item.getMenuItem(order[1])
                unplacedOrders.append(
                    {
                        "order_id" : order[0],
                        "item_id" : order[1],
                        "table_id" : order[3],
                        "amount" : order[2],
                        "price" : order[4],
                        "item_name" : orderItem[2] 
                    }
                )
            return{
                "success" : True,
                "message" : "You can now get the orders",
                "items" : unplacedOrders
            }
        else:
            return{
                "success" : False,
                "message" : "You are not autherized to access this menu"
            }
    else:
        return {
            "success" : False,
            "message": Token['error']
        }
    

#place order to kitchen
@router.post("/waiter/order/{orderId}")
def acceptOrder(payload : models.WaiterPlaceOrder , orderId : int):
    token = JWT.verify(token= payload.token)
    if token['valid']:
        loggedInWaiter = Waiter.getWaiterById(token['payload']['user-id'])
        requestedMenu = Menu.getMenu(token['payload']['menu-id'])

        #check if the waiter is requested the menu of the hotel he/she works for
        if loggedInWaiter[1] == requestedMenu[1]:
            placedOrder = Order.waiterPlaceOrder(menuId=token["payload"]['menu-id'] , orderId=orderId)
            if placedOrder:
                return{
                    "success" : True,
                    "message" : "Order has been placed"
                }
            else:
                return{
                    "success" : False,
                    "message" : placedOrder
                }
        else:
            return{
                "success" : False,
                "message" : "You can't access this menu"
            } 
    else:
        return{
            "success" : False,
            "message" : token['error']
        }

@router.get("/owner/waiters")
def getWaiters(token: str = Header()):
    token = JWT.verify(token)
    if not token['valid']:
        return {
            'success': False,
            'message': token['error']
        }
    userId = token['payload']['user-id']
    res = Waiter.getWaiters(userId)
    result = []

    if res:
        # print(res)
        for i in res:
            result.append(
                {
                    "waiterId": i[0],
                    "username": i[2]
                }
            )
        return result
    else:
         return{
            "success" : False,
            "message" : "none"
        }
