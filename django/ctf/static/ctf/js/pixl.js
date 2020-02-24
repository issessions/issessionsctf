window.addEventListener("DOMContentLoaded", (e) =>{

    $navImg = $('nav').find('img');

    //Better Query Selectors
    //dynamicly highlight button on selected page
    if (document.location.toString().indexOf("sponsors") >= 0){
        $navImg.eq(3).attr("src","../../static/ctf/img/btn_sponsors.png");
    }else if (document.location.toString().indexOf("challenges") >= 0){
        $navImg.eq(2).attr("src","../../static/ctf/img/btn_challenges.png");
    }else if (document.location.toString().indexOf("scoreboard") >= 0){
        $navImg.eq(1).attr("src","../../static/ctf/img/btn_scoreboard.png");
    }else{
        $navImg.eq(0).attr("src","../../static/ctf/img/btn_home.png");
    }

    //Do event delegation for perf++
    // pressed action change image to pressed
    $navImg.eq(0).mousedown(function(){
        $(this).attr("src", "../../static/ctf/img/btn_home_pressed.png");
    });
    $navImg.eq(1).mousedown(function(){
        $(this).attr("src", "../../static/ctf/img/btn_scrbrd_pressed.png");
    });
    $navImg.eq(2).mousedown(function(){
        $(this).attr("src", "../../static/ctf/img/btn_challenges_pressed.png");
    });
    $navImg.eq(3).mousedown(function(){
        $(this).attr("src", "../../static/ctf/img/btn_sponsors_pressed.png");
    });



    var navGrid = document.getElementsByClassName("pixl-grid-wrapper");
    

   // navGrid[0].addEventListener("click", function(){
     //   console.dir(this);
    //});

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