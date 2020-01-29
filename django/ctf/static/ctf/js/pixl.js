window.addEventListener("DOMContentLoaded", (e) =>{

    var loginForm = document.getElementById("pixl-login-form");

    checkSize(loginForm);

    window.addEventListener("resize", function(){
        console.log(this.innerWidth);
        
        checkSize(loginForm);
    });
});

function checkSize(elem){
    if(this.innerWidth > 1135){
        elem.classList.remove("pixl-login-form-narrow");
        elem.classList.add("pixl-login-form-wide")
    } else {
        elem.classList.remove("pixl-login-form-wide")
        elem.classList.add("pixl-login-form-narrow");
    }
}