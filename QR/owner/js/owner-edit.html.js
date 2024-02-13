function updateItem(itemId) {
    let name = document.getElementById('edit-name').value;
    let description = document.getElementById('edit-description').value;

    itemId = Number(itemId)
    // itemId = getparam();
    let price = Number(document.getElementById('edit-price').value);
    let token = sessionStorage["token"]


    console.log(name);
    console.log(description);
    console.log(itemId);


    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    var raw = JSON.stringify({
        "itemId": itemId,
        "description": description,
        "price": price,
        "token": token
    });

    var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: raw,
        redirect: 'follow'
    };

    fetch("http://127.0.0.1:8000/menus/items/update", requestOptions)
        .then(response => response.text())
        .then(result => console.log(result))
        .catch(error => console.log('error', error));

}

function addItem() {

    const urlParams = new URL(window.location.toLocaleString()).searchParams;
    // let menuId = urlParams.get('id');
    // let menuId = getparam()
    let menuId = sessionStorage["menuId"]
    alert("here")
    let name = document.getElementById("new-item-name-1").value;
    let description = document.getElementById("new-description-1").value;

    let price = document.getElementById('item-price').value;

    let token = sessionStorage["token"]

    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    var raw = JSON.stringify({
        "menuId": menuId,
        "name": name,
        "price": price,
        "description": description,
        "token": token
    });

    var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: raw,
        redirect: 'follow'
    };

    fetch("http://127.0.0.1:8000/menus/items", requestOptions)
        .then(response => response.text())
        .then(result => console.log(result))
        .catch(error => console.log('error', error));
}

function getItems() {
    let token = sessionStorage["token"]
    var myHeaders = new Headers();
    myHeaders.append("token", token);

    var requestOptions = {
        method: 'GET',
        headers: myHeaders,
        redirect: 'follow'
    };

    fetch("http://127.0.0.1:8000/menus/items", requestOptions)
        .then(response => response.json())
        .then(result => {
            const itemsContainer = document.getElementById("category-1")
            // alert(result)
            for (let item in result) {
                let newItem = `                <div class="d-flex flex-column my-3 ms-5 p-2 shadow-lg p-3 bg-white rounded">
                <div class="item d-flex flex-column" id=${result[item].itemId}>
                    <img style="width: 8px;" src="../imgs/Ellipse 11.png" alt="">
                    <div class="edit-form form-floating">
                        <div class="mb-3">
                        <p>ItemID ${result[item].itemId}</p>
                          <label for="edit-name">Name</label>
                          <input type="text" class="form-control" id="edit-name" placeholder=${result[item].name}>
                        </div>
                        
                        <div class="mb-3">
                          <label for="edit-description">Description</label>
                          <input type="text" class="form-control" id="edit-description" placeholder="${result[item].description}">
                        </div>
                        
                        <div class="mb-3">
                          <label for="edit-price">Price</label>
                          <input type="text" class="form-control" id="edit-price" placeholder="${result[item].price}">
                        </div>
                        
                        <button class="save-button btn btn-outline-success" id="save-item" onclick="updateItem(${result[item].itemId})" itemId =  >Save</button>
                        <button class="btn btn-danger fw-bold" id="delete-item" onclick="deleteItem(${result[item].itemId})" itemId =  >DELETE</button>
                      </div>
                      
                </div>
            </div>`

                itemsContainer.innerHTML += newItem

            }

        })
        .catch(error => console.log('error', error));
}


function deleteItem(id) {
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    token = sessionStorage["token"]

    var raw = JSON.stringify({
        "token": token,
        "itemId": id
    });

    var requestOptions = {
        method: 'DELETE',
        headers: myHeaders,
        body: raw,
        redirect: 'follow'
    };

    fetch("http://127.0.0.1:8000/menus/items", requestOptions)
        .then(response => response.text())
        .then(result => console.log(result))
        .catch(error => console.log('error', error));
}



function getparam() {
    const urlParams = new URL(window.location.toLocaleString()).searchParams;
    return (urlParams.get('id'))
}



