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

function mobileValidation() {
    var mobile_number = document.querySelector("#mobile_number").value;
    if (mobile_number.length !== 10 || isNaN(mobile_number)) {
        alert("Mobile number should be exactly 10 digits.");
        return false;
    }
    return true;
}


    
function hideInfoTable(){
    is_submited=document.getElementById("hidden_element").value
    if (is_submited!="submitted"){
        document.getElementById("details-div").style.display="none"
    }
    
    }

        function checkFileType(input) {
            const file = input.files[0];
            if (!file) return;

            const allowedExtensions = ["pdf", "png", "jpg", "jpeg", "doc", "docx"];
            const allowedTypes = [
                "application/pdf",
                "image/png",
                "image/jpeg",
                "application/msword",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            ];
            const maxSize = 5 * 1024 * 1024; // 5MB

            const fileName = file.name.toLowerCase();
            const fileExt = fileName.split('.').pop();

            // Extension check
            if (!allowedExtensions.includes(fileExt)) {
                alert("Only PDF, PNG, JPG, DOC, DOCX files are allowed.");
                input.value = "";
                return;
            }

            // MIME check
            if (!allowedTypes.includes(file.type)) {
                alert("Invalid file type.");
                input.value = "";
                return;
            }

            // Size check
            if (file.size > maxSize) {
                alert("File size must be less than 5MB.");
                input.value = "";
                return;
            }
        }