function signIn() {
  const form = document.getElementById("sign-in-form").elements;
  const email = form[0].value;
  const password = form[1].value;

  sendLogInInfo(email, password);
}

async function sendLogInInfo(email, password) {
  var myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");

  var raw = JSON.stringify({
    email: email,
    password: password,
  });

  var requestOptions = {
    method: "POST",
    headers: myHeaders,
    body: raw,
    redirect: "follow",
  };

  await fetch("http://127.0.0.1:8000/login", requestOptions)
    .then((response) => response.json())
    .then((data) => {
      // alert("HUH")
      //if login is successfull store the token and go to userpage , the one u have I guess
      if (data.success) {
        // alert(data.token)
        sessionStorage.setItem("token", data.token);
        window.location.href = "./owner/owner.html";

        console.log(sessionStorage["token"]);
      }
      //else alert the error
      else {
        alert(data.message);
      }
    })
    .catch((error) => console.log("error", error));
}

//function to call on successful login
function afterLogin() {}
