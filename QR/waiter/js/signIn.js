function signIn() {
  const form = document.getElementById("sign-in-form").elements;
  const email = form[0].value;
  const password = form[1].value;
  alert(email + ":" + password);
  sendLogInInfo(email, password);
}

async function sendLogInInfo(email, password) {
  var myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");

  var raw = JSON.stringify({
    userName: email,
    password: password,
  });

  var requestOptions = {
    method: "POST",
    headers: myHeaders,
    body: raw,
    redirect: "follow",
  };

  await fetch("http://127.0.0.1:8000/waiter/login", requestOptions)
    .then((response) => response.json())
    .then((data) => {
      //if login is successfull store the token and go to admin.html
      if (data.success) {
        // alert(data.token)
        sessionStorage["token"] = data.token;
        alert("login successful");
        aftersignin();
      }
      //else alert the error
      else {
        alert(data.message);
        alert("Log in failed");
      }
    })
    .catch((error) => console.log("error", error));
}

async function aftersignin() {
  await window.location.replace("./waiter.html");
}
