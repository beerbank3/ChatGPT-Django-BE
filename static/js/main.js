function openModal() {
    document.getElementById("myModal").style.display = "block";
}

// Close the modal
function closeModal() {
    document.getElementById("myModal").style.display = "none";
}

document.getElementById("loginForm").onsubmit = function(event) {
    event.preventDefault(); // Prevent default form submission behavior

    const formData = new FormData(document.getElementById("loginForm"));

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
            const errorDiv = document.getElementById("errorDiv");
            errorDiv.innerHTML = `<p style="color: red">${data.error}</p>`; // 에러 메시지 띄우기
        }
    })
    .catch(error => console.error("Error:", error));
};