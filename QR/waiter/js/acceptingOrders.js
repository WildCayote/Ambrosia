function removeItem(elem){
    id = elem.getAttribute("cs")
    token = sessionStorage["token"]
    acceptOrder(token , id)
}


function acceptOrder(token, order_id){
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    var raw = JSON.stringify({
      "token": token,
      "menuId": 2
    });

    var requestOptions = {
      method: 'POST',
      headers: myHeaders,
      body: raw,
      redirect: 'follow'
    };

    fetch(`http://127.0.0.1:8000/waiter/order/${order_id}`, requestOptions)
      .then(response => response.json())
      .then(data => {
        if (data.success){
            rw = document.getElementById(order_id)
            rw.style.display = "none"
        }
        else{
            alert(data.message)
        }
      })
      .catch(error => console.log('error', error));
}



