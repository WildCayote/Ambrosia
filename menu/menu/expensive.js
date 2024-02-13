var cartItems = [] 
const cartList = document.getElementById("cart_items")
var menuId = Number(document.getElementsByTagName("body")[0].getAttribute("menuId"))
var tableId = Number(document.getElementsByTagName("body")[0].getAttribute("tableId"))

function addCartItem(elem){
    amountForm = document.getElementById("form"+elem.getAttribute("item"))
    var amount = Number(amountForm.elements[0].value)
    if (amount){
        // add to the cart
        cartItems.push({
            "itemId" : Number(elem.getAttribute("item")),
            "amount" : amount
        })

        var nameOfItem = document.getElementById("name"+ elem.getAttribute("item")).innerHTML


        cartList.innerHTML = `<a class="dropdown-item" href="#">${nameOfItem}  x${amount}</a>` + cartList.innerHTML


        console.log(cartItems)
    }
    
}

function orderCart(){
    if (cartItems.length){
        sendOrderRequest()   
        //cleaning out the cart
        cartItems = []
        cartList.innerHTML = `<a class="dropdown-item" href="#" onclick="orderCart()">Place Order</a>`                 
    }
}

function sendOrderRequest(){
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    
    var raw = JSON.stringify({
      "menuId": menuId,
      "tableNum": tableId,
      "items": cartItems
    });
    
    var requestOptions = {
      method: 'POST',
      headers: myHeaders,
      body: raw,
      redirect: 'follow'
    };
    
    fetch("http://127.0.0.1:8000/menu/order", requestOptions)
      .then(response => response.json())
      .then(data => {
                alert(data.message)
      })
      .catch(error => console.log('error', error));
}