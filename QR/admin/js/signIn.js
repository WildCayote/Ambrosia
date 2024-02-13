function signIn(){
    const form = document.getElementById("sign-in-form").elements
    const email = form[0].value
    const password = form[1].value
    console.log(email + ":" + password)
    sendLogInInfo(email , password)
}


async function sendLogInInfo(email , password){
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    
    var raw = JSON.stringify({
      "adminName": email,
      "password": password
    });
    
    var requestOptions = {
      method: 'POST',
      headers: myHeaders,
      body: raw,
      redirect: 'follow'
    };
    
    await fetch("http://127.0.0.1:8000/admin/login", requestOptions)
      .then(response => response.json())
      .then(data => {
        //if the login is successfull go to admin.html and save the token
        if (data.success){
            // alert(data.token)
            sessionStorage["token"] = data.token
            afterLogin()

        }
        else{
            alert(data.message)
        }
      })
      .catch(error => console.log('error', error));
}


//function to call on successful login
async function afterLogin(){
  await (window.location.replace("./admin.html"));
}