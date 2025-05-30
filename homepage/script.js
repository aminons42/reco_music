const form = document.querySelector("#loginForm");
form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const user=document.querySelector("#username").value;
    const pass=document.querySelector("#password").value;
    const data = {
        username: user,
        password: pass
    }
    const request = await fetch("http://localhost:8000/login",{
        method:"Post",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify(data)
        })
    const resp= await request.json();
    if (resp.ok) {
        alert("Login successful");
        window.location.href = "http://localhost:8000/dashboard.html";
    } else {
        alert("Login failed");
    }    

        







})
