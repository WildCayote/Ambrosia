//function for seeing the currentprice
async function getServices(){
        var requestOptions = {
            method: 'GET',
            redirect: 'follow'
          };
          
         let res = await fetch("http://127.0.0.1:8000/services", requestOptions)
            .then(response => response.json())
            .then(data => {
                if (data.success){
                    const oldPrice = document.getElementById("current-price")
                    const newPrice = document.getElementById("new-price")
                    oldPrice.setAttribute("value" , data.services[1].price + " ETB") 
                    newPrice.setAttribute("placeholder" , data.services[1].price + " ETB" )
                }else{
                    alert(data.message)
                }
                
            })
            .catch(error => console.log('error', error));
}



function changePrice(){
    const newPrice = document.getElementById("new-price").value
    //here we will get the token from local storage
    const token = sessionStorage["token"]
    console.log(Number(newPrice))
    sendChangePrice(token , newPrice)
}


function sendChangePrice(token , price ){
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    var raw = JSON.stringify({
      "token": token,
      "id": 2,
      "price": price
    });

    var requestOptions = {
      method: 'POST',
      headers: myHeaders,
      body: raw,
      redirect: 'follow'
    };

    fetch("http://127.0.0.1:8000/services/update/price", requestOptions)
      .then(response => response.json())
      .then(data => {
            if(data.success){
                alert(data.message)
            }
            else{
                alert(data.message)
            }
      })
      .catch(error => console.log('error', error));
}

