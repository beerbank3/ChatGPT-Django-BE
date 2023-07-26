function openRegister() {
    document.getElementById("Register").style.display = "block";
}

function openLogin() {
    document.getElementById("Login").style.display = "block";
}

// Close the modal
function closeModal() {
    document.getElementById("Register").style.display = "none";
    document.getElementById("Login").style.display = "none";
}

document.getElementById("registerForm").onsubmit = function(event) {
    event.preventDefault(); // Prevent default form submission behavior

    const formData = new FormData(document.getElementById("registerForm"));

    fetch('user/register/', {
        method: "POST",
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if ('message' in data) {
            alert(data.message); // 성공 메시지 띄우기
            closeModal();
        } else if ('error' in data) {
            const errorDiv = document.getElementById("registerErrorDiv");
            errorDiv.innerHTML = `<p style="color: red">${data.error}</p>`; // 에러 메시지 띄우기
        }
    })
    .catch(error => console.error("Error:", error));
};

document.getElementById("loginForm").onsubmit = function(event) {
    event.preventDefault(); // Prevent default form submission behavior

    const formData = new FormData(document.getElementById("loginForm"));

    fetch('user/login/', {
        method: "POST",
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if ('message' in data) {
            alert(data.message); // 성공 메시지 띄우기
            closeModal();
        } else if ('error' in data) {
            const errorDiv = document.getElementById("loginErrorDiv");
            errorDiv.innerHTML = `<p style="color: red">${data.error}</p>`; // 에러 메시지 띄우기
        }
    })
    .catch(error => console.error("Error:", error));
};