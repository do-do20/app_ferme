function login(){
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    if(!email || !password){
        document.getElementById("error").innerText = "3ammar ga3 les champs";
        return;
    }

    fetch("/login",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({email, password})
    })
    .then(res=>{
        if(!res.ok) throw new Error("login failed");
        return res.json();
    })
    .then(data=>{
        // ✅ هنا التصحيح
        localStorage.setItem("user_id", data.id_user);

        window.location.href = "/dashboard";
    })
    .catch(()=>{
        document.getElementById("error").innerText = "Email ou password ghalat";
    });
}