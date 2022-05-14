const firstNameInput = document.getElementById("firstName");
const lastNameInput = document.getElementById("lastName");
const usernameInput = document.getElementById("username");
const passwordInput = document.getElementById("password");
const emailInput = document.getElementById("email");
document.getElementById("dataForm").onsubmit = function (event) {
    event.preventDefault();
    const firstName = firstNameInput.value;
    const lastName = lastNameInput.value;
    const username = usernameInput.value;
    const password = passwordInput.value;
    const email = emailInput.value;
    fetch("/register/newUser", {
        method: "POST",
        body: JSON.stringify({
            "firstName": firstName,
            "lastName": lastName,
            "username": username,
            "password": password,
            "email": email,
        }),
        headers: {
            "Content-Type": "application/json"
        }
    })
}