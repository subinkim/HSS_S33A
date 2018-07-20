document.addEventListener('DOMContentLoaded', () => {
    if (!localStorage.getItem("username"))
        var username = prompt("Please enter your username: ");
        document.write(username);
        localStorage.setItem("username", username);
});