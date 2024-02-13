from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import time

import models  
from security import JWT , hash
from databaseService import Owner , Admin , Waiter , Menu 


router = APIRouter(
    tags = ["auth"]
)

templates = Jinja2Templates(directory="./menu/menu")

router.mount("/static" , StaticFiles(directory="./menu/menu") , name="static")


#createAccount
@router.post("/createAccount")
def create(payload : models.OwnerCreateAccount):
    #previous user with the same email
    previousUser = Owner.getOwner(email=payload.email)
    if previousUser:
        return {
            'success' : False,
            'message' : 'Email is already in use'
        }

    else:

        userCreated = Owner.createOwner(firstName=payload.firstName , lastName=payload.lastName , hotelName=payload.hotelName , email=payload.email , password=hash(payload.password) , phoneNum=payload.phoneNum , birthDate=payload.birthDate , paymentClass=payload.paymentClass)
        if userCreated == True:
            return {
                'success' : True,
                'message' : 'User created'
            }
        else : 
            return{
                'success' : False,
                'message' : userCreated
            }      

@router.post("/admin/createAccount")
def create(payload : models.AdminAcc):
    #previous user with the same email
    previousUser = Admin.getAdmin(adminName=payload.adminName)
    if previousUser:
        return {
            'success' : False,
            'message' : 'Email is already in use'
        }

    else:

        userCreated = Admin.createAdmin(adminName = payload.adminName, password=hash(payload.password))
        if userCreated == True:
            return {
                'success' : True,
                'message' : 'Admin created'
            }
        else : 
            return{
                'success' : False,
                'message' : userCreated
            }      


#OwnerLogin
@router.post("/login")
def ownerLogin(payload : models.OwnerLogin):
    user = Owner.getOwner(payload.email)
    if user:
            if user[6] == hash(payload.password):
                header = {
                    "alg" : 'sha256',
                    "type" : 'jwt'
                }

                payload = {
                    "user-id" : user[0],
                    "user-class" : user[8],
                    "iat" :  int(time.time()),
                    "exp" :  int(time.time())+ 3600
                }

                token = JWT.sign(header=header , payload=payload)

                return{
                     'success' : True,
                     'token' : token
                }
            
            else:
                return{ 
                     'success' : False,
                     'message' : 'Incorrect Credentials'
                    }
                 
    else:
        return{
            'success' : False,
            'message' : 'Incorrect Credentials'
        }
    


#adminLogin
@router.post("/admin/login")
def adminLogin(payload : models.AdminLogin):
    admin = Admin.getAdmin(adminName=payload.adminName)
    if admin:
        print(hash(payload.password))
        if admin[2] == hash(payload.password):
            header = {
                    "alg" : 'sha256',
                    "type" : 'jwt'
                }

            payload = {
                    "user-id" : admin[0],
                    "iat" :  int(time.time()),
                    "exp" :  int(time.time()) + 3600
                }
            
            token = JWT.sign(header=header , payload=payload)
              
            return{
                  "success" : True,
                  "token"  : token
              }

        else:
             return {
                  "success" : False,
                  "message" : "Incorrect Credentials"
             }

    else:
         return{
              "success" : False,
              "message" : "Incorrect Credentials"
         } 


#WaiterLogin
@router.post("/waiter/login")
def waiterLogin(payload : models.WaiterLogin):
    waiter = Waiter.getWaiter(userName=payload.userName)
    print(waiter)
    #check if waiter exists
    if waiter:
        #get the menu
        ownerMenus = Menu.getUserMenu(waiter[1])
        #check if the menu is type 2
        print(ownerMenus)
        if not ownerMenus[5] == 2:
            return{
            "sucess"  : False,
            "message" : "This feature isn't availbale to you"
        }
        
        #check for the password
        print()
        print("``````````````````````````````````````````````````````````")
        print(waiter)
        if waiter[3] == hash(payload.password):
            header = {
                    "alg" : 'sha256',
                    "type" : 'jwt'
                }

            payload = {
                    "user-id" : waiter[0],
                    "owner-id" : waiter[1],
                    "menu-id" : ownerMenus[0],
                    "iat" :  int(time.time()),
                    "exp" :  int(time.time()) + 43200
                }
            
            token = JWT.sign(header=header , payload=payload)
              
            return{
                  "success" : True,
                  "token"  : token
              }
        
        else:
            return{
                "success" : False,
                "message" : "Incorect Credentials"
            }

    else:
        return{
            "success" : False,
            "message" : "Incorect Credentials"
        }
