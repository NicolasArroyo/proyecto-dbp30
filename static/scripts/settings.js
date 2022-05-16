// Update password

const usernameInput = document.getElementById("username");
const passwordInput = document.getElementById("passwordToChange");
const newPasswordInput = document.getElementById("new-password");


document.getElementById("newpassword-form").onsubmit = function(e) {
    e.preventDefault();
    const newPassword = newPasswordInput.value
    const username = usernameInput.value
    const password = passwordInput.value
    fetch("/settings/newPassword", {
        method: 'POST',
        body: JSON.stringify({
            "username": username,
            "password": password,
            'newPassword': newPassword
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(response) {
        return response.json();
    }).then(function(jsonResponse) {
        correctUsernamePassword = jsonResponse["correctUsernamePassword"];
        document.getElementById("server-error").className = "hidden";
        if (correctUsernamePassword) {
            document.getElementById("username-password-error").className = "hidden";
            window.location.href = "/home";
        }
        else {
            document.getElementById("username-password-error").className = "";
        }
    })
    .catch(function() {
        document.getElementById("server-error").className = "";
    });
}

// Delete account
const usernameToDeleteInput = document.getElementById("usernameToDelete")
const passwordToDeleteInput = document.getElementById("passwordToDelete")

document.getElementById("delete-form").onsubmit = function (e) {
    e.preventDefault();
    const username = usernameToDeleteInput.value;
    const password = passwordToDeleteInput.value;
    fetch("/settings/deleteUser", {
        method: 'POST',
        body: JSON.stringify({
            'username': username,
            'password': password
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(response) {
        return response.json();
    }).then(function(jsonResponse) {
        correctUsernamePassword = jsonResponse["correctUsernamePassword"];
        console.log(correctUsernamePassword)
        document.getElementById("server-error").className = "hidden";
        if (correctUsernamePassword) {
            document.getElementById("username-password-error-delete").className = "hidden";
            window.location.href = "/home";
        }
        else {
            document.getElementById("username-password-error-delete").className = "";
        }
    })
    .catch(function() {
        document.getElementById("server-error").className = "";
    });
}
