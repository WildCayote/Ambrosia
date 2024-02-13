const baseURL = "http://127.0.0.1:8000"

// code for updating the price of the services we give
// nothing to touch in here
async function getServices(){
    var requestOptions = {
        method: 'GET',
        redirect: 'follow'
      };
      
     let res = await fetch(baseURL + "/services", requestOptions)
        .then(response => response.json())
        .then(data => {
            if (data.success){
                const elem = document.getElementById(data.services[1].id)
                elem.innerHTML = elem.innerHTML + " " + data.services[1].price + "ETB"

            }else{
                alert(data.message)
            }
            
        })
        .catch(error => console.log('error', error));
    

}


// code for sign up
function signUp(){
    const form = document.getElementById("sign-up-form")
    const email = form.elements[0].value
    const password = form.elements[1].value
    const confirmPassword = form.elements[2].value
    const checkBox = form.elements[3].checked 

    if (checkBox){
        var paymentClass = 2
    }else{
        var paymentClass = 1
    }
    
    //basic form validation will go here
    //like if the password and confirm password are the dame
    
    //sending the cheked input
    //you will send this if the form validation is correct
    sendSignUpInfo(email , password , paymentClass )
 }

function sendSignUpInfo(email="t" , password="t" , paymentClass){
        var myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json");

        var raw = JSON.stringify({
            "email": email,
            "firstName": "tinsae",
            "lastName": "shemalise",
            "password": password,
            "birthDate": "2001-06-27",
            "phoneNum": "0911051392",
            "hotelName": "Bruh what ever",
            "paymentClass": paymentClass
        });

        var requestOptions = {
          method: 'POST',
          headers: myHeaders,
          body: raw,
          redirect: 'follow'
        };

        fetch("http://127.0.0.1:8000/createAccount", requestOptions)
          .then(response => response.json())
          .then(data => {
                //code to be executed when login is successfull
                //go to the login page
                if (data.success){
                    // alert(data.message)
                    afterSignUp()
                }
                //code to be executed when login is unsuccessful
                else{
                    alert(data.message)
                }
          })
          .catch(error => console.log('error', error));
        //   alert("here")
          
 }

async function afterSignUp(){
    await document.location.replace("./Sign-in.html");
    // alert("passed")
} 