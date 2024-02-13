const baseURL = "http://127.0.0.1:8000"

function insertService(service){
    const elem = document.getElementById(service.id)
    elem.innerHTML(elem.innerHTML + " " + service.price + "ETB")
}

async function getServices(){
    var requestOptions = {
        method: 'GET',
        redirect: 'follow'
      };
      
     let res = await fetch(baseURL + "/services", requestOptions)
        .then(response => response.json())
        .then(data => {
            if (data.success){
                for (let service of data.services){
                    insertService(service)
                }

            }else{
                insertService(false) 
            }
            
        })
        .catch(error => console.log('error', error));
    

}
