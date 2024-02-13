function addOrdersToTable(id, table_id , name , amount){
    tb = document.getElementById("table-body")
    
    if(!document.getElementById(id)){
        rw = `<tr id="${id}">
        <th scope='row'>${id}</th>
        <td>${table_id}</td>
        <td>
          <ul class='list-unstyled'>
            <li>${name} x${amount}</li>
          </ul>
        </td>
        <td>
        <button onclick="removeItem(this)" cs="${id}"> Place Order</button>
        </td>
        </tr>`
    
        tb.innerHTML += rw
    }

     
 

}

function getOrders(){
    token = sessionStorage["token"]
    var myHeaders = new Headers();
    myHeaders.append("token", `${token}`);

    var requestOptions = {
      method: 'GET',
      headers: myHeaders,
      redirect: 'follow'
    };

    fetch("http://127.0.0.1:8000/waiter/order", requestOptions)
      .then(response => response.json())
      .then(data => {
            if(data.success){
                for(let item in data.items){
                    addOrdersToTable(data.items[item].order_id , data.items[item].table_id ,data.items[item].item_name , data.items[item].amount)
                }
            }
            else{
                alert(data.message)
            }
      })
      .catch(error => console.log('error', error));
}


function getOrdersAndRefresh(){
    getOrders()
    setInterval(getOrders , 1000)
}