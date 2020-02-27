window.addEventListener("DOMContentLoaded", (e) =>{

    var loginForm = document.getElementById("chunk-login-form");

    checkSize(loginForm);

    window.addEventListener("resize", function(){
        console.log(this.innerWidth);
        
        checkSize(loginForm);
    });
});

function checkSize(elem){
    if(this.innerWidth > 1095){
        elem.classList.remove("chunk-login-form-narrow");
        elem.classList.add("chunk-login-form-wide")
    } else {
        elem.classList.remove("chunk-login-form-wide")
        elem.classList.add("chunk-login-form-narrow");
    }
}