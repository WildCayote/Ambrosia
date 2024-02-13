from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Double
from sqlalchemy.sql.expression import update
from security import hash

engine = create_engine('sqlite:///qrMenuDB.db', echo=True)
connection = engine.connect()

meta = MetaData()


class Admin:
    model = Table(
        'admin', meta,
        Column('id', Integer, primary_key=True),
        Column('adminName', String),
        Column('password', String)
    )

    @staticmethod
    def getAdmin(adminName):
        query = Admin.model.select().where(Admin.model.c.adminName == adminName)
        return connection.execute(query).fetchone()

    @staticmethod
    def createAdmin(adminName, password):
        query = Admin.model.insert().values(adminName = adminName, password = password)
        try:
            connection.execute(query)
            connection.commit()
            return True
        except Exception as e:
            return e


class Owner:
    model = Table(
        'owner', meta,
        Column('id', Integer, primary_key=True),
        Column('firstName', String),
        Column('lastName', String),
        Column('hotelName', String),
        Column('birthDate', String),
        Column('email', String),
        Column('password', String),
        Column('phoneNum', String),
        Column('paymentClass', Integer)
    )

    @staticmethod
    def createOwner(firstName, lastName, hotelName, birthDate, email, password, phoneNum, paymentClass):
        query = Owner.model.insert().values(firstName=firstName, lastName=lastName, hotelName=hotelName,
                                            birthDate=birthDate, email=email, password=password, phoneNum=phoneNum, paymentClass=paymentClass)
        try:
            connection.execute(query)
            connection.commit()
            return True
        except Exception as e:
            return e

    @staticmethod
    def getOwner(email):
        query = Owner.model.select().where(Owner.model.c.email == email)
        try:
            return connection.execute(query).fetchone()
        except Exception as e:
            return e

    @staticmethod
    def getOwnerById(id):
        query = Owner.model.select().where(Owner.model.c.id == id)
        try:
            return connection.execute(query).fetchone()
        except Exception as e:
            return e


class Waiter:
    model = Table(
        'waiter', meta,
        Column('id', Integer, primary_key=True),
        Column('ownerId', Integer),
        Column('userName', String),
        Column('password', String)
    )

    @staticmethod
    def getWaiter(userName):
        query = Waiter.model.select().where(Waiter.model.c.id == userName)
        try:
            return connection.execute(query).fetchone()
        except Exception as e:
            return e

    @staticmethod
    def getWaiterById(id):
        query = Waiter.model.select().where(Waiter.model.c.id == id)
        try:
            return connection.execute(query).fetchone()
        except Exception as e:
            return e

    @staticmethod
    def createWaiter(ownerId, userName, password):
        query = Waiter.model.insert().values(
            ownerId=ownerId, userName=userName, password=password)
        try:
            connection.execute(query)
            connection.commit()
            return True
        except Exception as e:
            return e

    @staticmethod
    def deleteWaiter(ownerId, waiterId):
        query = Waiter.model.delete().where(Waiter.model.c.ownerId == ownerId,
                                            Waiter.model.c.id == waiterId)
        try:
            connection.execute(query)
            connection.commit()
            return True
        except Exception as e:
            return e

    @staticmethod
    def updateWaiterPassword(ownerId, userName, password):
        query = update(Waiter.model).where(Waiter.model.c.ownerId == ownerId,
                                           Waiter.model.c.userName == userName).values(password=password)
        try:
            connection.execute(query)
            connection.commit()
            return True
        except Exception as e:
            return e

    @staticmethod
    def getWaiters(ownerId):
        query = Waiter.model.select().where(Waiter.model.c.ownerId == ownerId)
        try:
            return connection.execute(query).fetchall()
        except Exception as e:
            return e


class Order:
    model = Table(
        'order', meta,
        Column('id', Integer, primary_key=True),
        Column('itemId', Integer),
        Column('amount', Integer),
        Column('tableId', Integer),
        Column('price', Double),
        Column('placedByWaiter', Integer),
        Column('menuId', Integer)
    )

    @staticmethod
    def getOrders(menuId):
        query = Order.model.select().where(Order.model.menuId == menuId)
        try:
            return connection.execute(query).fetchall()
        except Exception as e:
            return e

    @staticmethod
    def createOrder(itemId, tableId, menuId, price=0.0, amount=1, placedByWaiter=0):
        query = Order.model.insert().values(itemId=itemId, tableId=tableId,
                                            placedByWaiter=placedByWaiter, menuId=menuId, price=price, amount=amount)
        try:
            connection.execute(query)
            connection.commit()
            return True
        except Exception as e:
            return e

    @staticmethod
    def waiterPlaceOrder(menuId, orderId):
        query = update(Order.model).where(Order.model.c.menuId ==
                                          menuId, Order.model.c.id == orderId).values(placedByWaiter=1)
        try:
            connection.execute(query)
            connection.commit()
            return True
        except Exception as e:
            return e

    @staticmethod
    def waiterGetUnplacedOrderes(menuId):
        query = Order.model.select().where(Order.model.c.menuId == menuId,
                                           Order.model.c.placedByWaiter == 0)
        try:
            return connection.execute(query).fetchall()
        except Exception as e:
            return e


class Item:
    model = Table(
        'item', meta,
        Column('id', Integer, primary_key=True),
        Column('menuId', Integer),
        Column('name', String),
        Column('description', String),
        Column('price', Double)
    )

    @staticmethod
    def getMenuItems(menuId):
        query = Item.model.select().where(Item.model.c.menuId == menuId)
        try:
            return connection.execute(query).fetchall()
        except Exception as e:
            return e

    @staticmethod
    def createMenuItems(menuId, name, description, price, token):
        query = Item.model.insert().values(menuId=menuId, name=name,
                                           description=description, price=price)
        try:
            connection.execute(query)
            connection.commit()
            return True
        except Exception as e:
            return e


    @staticmethod
    def getMenuItem(itemId):
        query = Item.model.select().where(Item.model.c.id == itemId)
        try:
            return connection.execute(query).fetchone()
        except Exception as e:
            return e

    @staticmethod
    def updateItem(itemId, token, description=None, price=None):
        if price and description:
            query = update(Item.model).where(Item.model.c.id == itemId).values(
                price=price, description=description)
        elif price:
            query = update(Item.model).where(
                Item.model.c.id == itemId).values(price=price)
        elif description:
            query = update(Item.model).where(Item.model.c.id ==
                                             itemId).values(description=description)
        try:
            connection.execute(query)
            connection.commit()
            return True
        except Exception as e:
            return e

    @staticmethod
    def removeMenuItem(itemId, token):
        query = Item.model.delete().where(Item.model.c.id == itemId)
        try:
            connection.execute(query)
            connection.commit()
            return True
        except Exception as e:
            return e

    @staticmethod
    def removeMenuItems(menuId, token):
        query = Item.model.delete().where(Item.model.c.id == menuId)
        try:
            connection.execute(query)
            connection.commit()
            return True
        except Exception as e:
            return e


class Menu:
    model = Table(
        'menu', meta,
        Column('id', Integer, primary_key=True),
        Column('ownerId', Integer),
        Column('name', String),
        Column('description', String),
        Column('creationDate', String),
        Column('paymentClass', Integer)
    )

    @staticmethod
    def getMenu(menuId):
        query = Menu.model.select().where(Menu.model.c.id == menuId)
        try:
            return connection.execute(query).fetchone()
        except Exception as e:
            return e

    @staticmethod
    def createMenu(ownerId, name, description, creationDate, paymentClass):
        query = Menu.model.insert().values(ownerId=ownerId, name=name, description=description,
                                           creationDate=creationDate, paymentClass=paymentClass)
        query2 = Menu.model.select().where(Menu.model.c.ownerId == ownerId)

        try:
            x = connection.execute(query2).fetchone()
            if x:
                print("Message is imminent")
                return {
                    "Success": False,
                    "Message": "Can not create more than one menu per user"
                }

            connection.execute(query)
            connection.commit()
            print("shouldbeworking")
            return {
                "Success": True,
                "Message": "Menu Created"
            }
        except Exception as e:
            return e

    @staticmethod
    def updateMenu(userId, menuId, token, name, description, paymentClass):
        # print(menu["ownerId"])
        if paymentClass:
            query = update(Menu.model).where(Menu.model.c.id == menuId).values(
                name=name, description=description, paymentClass=paymentClass)
        else:
            query = update(Menu.model).where(Menu.model.c.id == menuId).values(
                name=name, description=description)
        try:
            connection.execute(query)
            connection.commit()
            return True
        except Exception as e:
            return e

    @staticmethod
    def deleteMenu(menuId, userId):
        query = Menu.model.delete().where(Menu.model.c.id == menuId)
        try:
            if Menu.getMenu(menuId)[1] != userId:
                return {
                    "Error": "Unauhtorised User Detected"
                }
            connection.execute(query)
            connection.commit()
            return {
                "Success": True,
                "Message": "Menu deleted successfully"
            }
        except Exception as e:
            return e
    
    @staticmethod
    def getUserMenu(userId):
        query = Menu.model.select().where(Menu.model.c.ownerId == userId)
        try:
            return connection.execute(query).fetchone()
        except Exception as e:
            return e 


    @staticmethod
    def getUserMenuDescription(userId):
        query = Menu.model.select().where(Menu.model.c.ownerId == userId)
        try:
            res = connection.execute(query).fetchone()
            return {
                "menuId": res[0],
                "ownerId": res[1],
                "name": res[2],
                "description": res[3],
                "paymentClass": res[5]
            }
        except Exception as e:
            return e


class PaymentTypes:
    model = Table(
        'paymentTypes', meta,
        Column('id', Integer, primary_key=True),
        Column('descriptionOfService', String),
        Column('price', Double)
    )

    @staticmethod
    def getPaymentTypes():
        query = PaymentTypes.model.select()
        try:
            return connection.execute(query).fetchall()
        except Exception as e:
            return e

    @staticmethod
    def changePrice(id, price):
        query = update(PaymentTypes.model).where(
            PaymentTypes.model.c.id == id).values(price=price)
        try:
            connection.execute(query)
            connection.commit()
            return True
        except Exception as e:
            return e

    @staticmethod
    def changeDescription(id, description):
        query = update(PaymentTypes.model).where(
            PaymentTypes.model.c.id == id).values(descriptionOfService=description)
        try:
            connection.execute(query)
            connection.commit()
            return True
        except Exception as e:
            return e


class HotelTable:
    model = Table(
        'table', meta,
        Column('id', Integer, primary_key=True),
        Column('ownerId', Integer),
        Column('tableNum', Integer)
    )

    # I haven't decided what to do here man
    # The initial purpose of this table was to tell from which table the order came
    # It's a good idea but I don't have a clear idea on how the hotel owner will create and assign the tables in his hotel

    @staticmethod
    def createTable(ownerId, tableNum):
        query = HotelTable.model.insert().values(ownerId=ownerId, tableNum=tableNum)
        query2 = HotelTable.model.select().where((HotelTable.model.c.ownerId == ownerId),
                                                (HotelTable.model.c.tableNum == tableNum))
        try:
            if not connection.execute(query2).fetchone():
                connection.execute(query)
                connection.commit()
                return True
            else:
                return
        except Exception as e:
            return e

    @staticmethod
    def getTableNum(ownerId, tableNum):
        query = HotelTable.model.select().where((HotelTable.model.c.ownerId == ownerId),
                                                (HotelTable.model.c.tableNum == tableNum))
        try:
            return connection.execute(query).fetchone()
        except Exception as e:
            return e


if __name__ == "__main__":

    # Admin class test
    # print(Admin.getAdmin('admin'))

    # Owner class test
    # print(Owner.getOwner('tinsaeShemalise14@gmail.com'))
    # print(Owner.createOwner(email='email@gmail.com' , firstName='tinsae' , lastName='shemalise' , hotelName='t-hotel' , birthDate='2001-06-27' , password='1234' , phoneNum='0911051392' , paymentClass=1))

    # Waiter class test

    # Order class test

    # Menu class test

    # Item class test

    # PaymentTypes class test

    # HotelTables class test
    # print(HotelTable.getTableNum(ownerId=2 , tableNum=1))

    # print(hash('12345'))
    pass
