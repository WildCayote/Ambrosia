from fastapi import FastAPI , Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse


import qrcodegen
import models  
from security import JWT
import waiters, menu, items, services, auth

from databaseService import HotelTable

templates = Jinja2Templates(directory="./menu/menu")

app = FastAPI()
app.mount("/static" , StaticFiles(directory="./menu/menu") , name="static")

origins = [ 
    "*" 
]

app.add_middleware( 
    CORSMiddleware, 
    allow_origins = origins, 
    allow_credentials =True, 
    allow_methods = ["*"], 
    allow_headers = ["*"] 
)



# open docs if ur confused where whatever function ur looking for is


@app.get("/testMenu")
def getmenu(request : Request):
    return templates.TemplateResponse("testMenu.html" , {"request":request ,"seq" : [2]})



@app.post("/menus/qrcode")
def getQRcode(payload: models.QRget):
    token = JWT.verify(payload.token)
    if not token['valid']:
        return {
            'success': False,
            'message': token['error']
        }

    qr0 = qrcodegen.QrCode.encode_text("{string}".format(string = payload.string), qrcodegen.QrCode.Ecc.MEDIUM)
    # print_qr(qr0)       #just prints it to console, the image not the string
    svg = qrcodegen.to_svg_str(qr0, 4) 
    qr0 = svg.replace("\n", "")
    qr0 = qr0.replace("\\", "")
    
    # print(qr0)
    # return {"QRstring": qr0}
    return HTMLResponse(content=qr0, media_type="application/svg+xml")


@app.patch("/tables")
def createtable(table: models.Table):
    token = JWT.verify(table.token)
    if not token['valid']:
        return {
            'success': False,
            'message': token['error']
        }
    ownerId = token['payload']['user-id']
    return HotelTable.createTable(ownerId, table.tablenum)


app.include_router(waiters.router)
app.include_router(menu.router)
app.include_router(items.router)
app.include_router(services.router)
app.include_router(auth.router)

























# ####################################################################################3

# @app.post("/menus")
# def createMenu(menu: models.menuCreate):
#     token = menu.token
#     token = JWT.verify(token)
#     ownerId = token['payload']['user-id']
#     if not token['valid']:
#         return {
#             'success': False,
#             'message': token['error']
#         }
    
#     #check if user has already created a menu
#     ownerMenu = Menu.getUserMenu(ownerId)
#     if not ownerMenu:
#         return Menu.createMenu(creationDate=Timestamp.now(), ownerId=ownerId, description=menu.description , name=menu.name , paymentClass=menu.paymentClass)
#     else:
#         return {
#             "success" : False,
#             "message" : "You can only create one menu with a single account"
#         }

# @app.patch("/menus")
# def updateMenu(menu: models.menuUpdate):
#     token = JWT.verify(menu.token)
#     if not token['valid']:
#         return {
#             'success': False,
#             'message': token['error']
#         }

#     id = token['payload']['user-id']
#     return Menu.updateMenu(id, **menu.dict())
    

# @app.delete("/menus", status_code=401)
# def deleteMenu(menu: models.menuDelete):
#     token = JWT.verify(menu.token)
#     if not token['valid']:
#         return {
#             'success': False,
#             'message': token['error']
#         }

#     userId = token['payload']['user-id']
#     return Menu.deleteMenu(menu.menuId, userId)


# @app.patch("/menus/items")
# def updateItems(item: models.itemUpdate):
#     item.itemId = int(item.itemId)
#     token = JWT.verify(item.token)
#     if not token['valid']:
#         return {
#             'success': False,
#             'message': token['error']
#         }

#     userId = token['payload']['user-id']
#     return Item.updateItem(**item.dict())


# @app.post("/menus/items")
# def addItems(item: models.itemAdd):
#     token = JWT.verify(item.token)
#     if not token['valid']:
#         return {
#             'success': False,
#             'message': token['error']
#         }
#     return Item.createMenuItems(**item.dict())


# @app.delete("/menus/items")
# def deleteItems(item: models.itemDelete):
#     token = JWT.verify(item.token)
#     if not token['valid']:
#         return {
#             'success': False,
#             'message': token['error']
#         }
#     return Item.removeMenuItem(**item.dict())


# # ````````````````````````````````````````````````````````````````````````````````







