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

        var new_password = document.querySelector(".password");
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

    function hideInfo(){
        is_submited=document.getElementById("hidden_element").value
        if (is_submited==="submitted"){
            document.getElementById("my-form").style.display="none"
        }
        else{
            document.getElementById("details-div").style.display="none"
        }
    }

    function hideInfoTable(){
        is_submited=document.getElementById("hidden_element").value
        if (is_submited!="submitted"){
            document.getElementById("details-div").style.display="none"
        }
        
    }