const bts = document.querySelector(".bts");
bts.addEventListener("submit", (e) => {
    e.preventDefault();
    const user=document.querySelector("#username").value;
    const pass=document.querySelector("#password").value;
    const data = {
        username: user,
        password: pass
    }
    const request = await fetch()







})
