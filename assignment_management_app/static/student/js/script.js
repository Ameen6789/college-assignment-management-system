



var submenuToggle = document.querySelector('[data-bs-toggle="collapse"]');
    var chevronIcon = submenuToggle.querySelector('.fa-chevron-down');

    submenuToggle.addEventListener('click', function() {
        chevronIcon.classList.toggle('rotate');
    });


document.getElementById("nav-button").addEventListener("click",function(){
    if (document.getElementById("sidebar").style.display==="none"){
        document.getElementById("sidebar").style.display="block"
    }
    else{
        document.getElementById("sidebar").style.display="none"
    }
    
})

    function updatePassword() {

        var new_password = document.querySelector(".new_password");
        var confirm_password = document.querySelector(".confirm_password");
        isvalid=true
        if (new_password.value !== confirm_password.value) {
    
            new_password.style.border = "2px solid red";
            confirm_password.style.border = "2px solid red";
            alert("Passwords must be the same");
            new_password.addEventListener("focus", function() {
                password.style.border = "";
            });
            confirm_password.addEventListener("focus", function() {
                confirm_password.style.border = "";
            });
            isvalid=false;
            
        }
        
        
        
        return isvalid
        
    }


function validatePasswordandMobile() {

    var password = document.querySelector(".password");
    var confirm_password = document.querySelector(".confirm_password");
    result=true
    if (password.value !== confirm_password.value) {

        password.style.border = "2px solid red";
        confirm_password.style.border = "2px solid red";
        alert("Passwords must be the same");
        password.addEventListener("focus", function() {
            password.style.border = "";
        });
        confirm_password.addEventListener("focus", function() {
            confirm_password.style.border = "";
        });
        result=false;
        
    }
    var mobile_number = document.querySelector(".mobile_number");


    if (String(mobile_number.value).length < 10 || String(mobile_number.value).length > 10) {
        alert("Mobile number should be exactly 10 digits");

        mobile_number.style.border = "2px solid red";

        mobile_number.addEventListener("focus", function() {
            mobile_number.style.border = "";
        });

        result=false; 
    }    
    return result
    
}
function validateMobile(){
    var mobile_number = document.querySelector(".mobile_number");


    if (String(mobile_number.value).length < 10 || String(mobile_number.value).length > 10) {
        alert("Mobile number should be exactly 10 digits");

        mobile_number.style.border = "2px solid red";

        mobile_number.addEventListener("focus", function() {
            mobile_number.style.border = "";
        });

        return false
    }    
    return true
}
