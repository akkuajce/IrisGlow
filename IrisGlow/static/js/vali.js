document.addEventListener("DOMContentLoaded", function () {
    const first_nameInput = document.getElementById("first_name");
    const last_nameInput = document.getElementById("last_name");
    const emailInput = document.getElementById("email");
    const phoneInput = document.getElementById("phone");
    const passwordInput = document.getElementById("password");
    const confirmPasswordInput = document.getElementById("confirm_password");
    const addressInput = document.getElementById("address");
    const addressInput2 = document.getElementById("address1");
    const addressInput3 = document.getElementById("address2");
    const cityInput = document.getElementById("city");
  
    
    console.log("Address input:", addressInput);
  
    first_nameInput.addEventListener("blur", validateName);
    last_nameInput.addEventListener("blur", validateName);
    emailInput.addEventListener("blur", validateEmail);
    if (passwordInput) {
      // Check if the addressInput element exists
      passwordInput.addEventListener("keyup", validatePassword);
    }
    if (confirmPasswordInput) {
      // Check if the addressInput element exists
      confirmPasswordInput.addEventListener("keyup", validateConfirmPassword);
    }
  
    phoneInput.addEventListener("blur", validatePhoneNumber);
    phoneInput.addEventListener("blur", function (event) {
      formatPhoneNumber();
    });
    //  addressInput.addEventListener('blur', validateAddress);
    addressInput.addEventListener("blur", validateAddress);
    if (addressInput) {
      // Check if the addressInput element exists
   
      addressInput.addEventListener("onchange", validateAddress);
    }
    addressInput2.addEventListener("blur", validateAddress1);
    if (addressInput2) {
  
      addressInput2.addEventListener("onchange", validateAddress1);
    }
    addressInput3.addEventListener("blur", validateAddress2);
    if (addressInput3) {
      // Check if the addressInput element exists
  
      addressInput3.addEventListener("onchange", validateAddress2);
    }
  
    function validateName() {
      console.log("validateName function called");
      const namePattern = /^[A-Za-z ]+$/;
      const nameValidation = document.getElementById("nameValidation");
  
      if (!namePattern.test(nameInput.value)) {
        nameInput.classList.add("is-invalid");
        nameInput.classList.remove("is-valid");
        nameValidation.style.display = "block";
        // If you have a 'nameValid' element, you can also hide it here
      } else {
        nameInput.classList.remove("is-invalid");
        nameInput.classList.add("is-valid");
        nameValidation.style.display = "none";
        // If you have a 'nameValid' element, you can also display it here
      }
    }
  
    function validateEmail() {
      const emailPattern =
        /^[a-zA-Z0-9._%+-]+@(gmail\.com|[a-zA-Z0-9.-]+\.(com|in))$/;
      if (!emailPattern.test(emailInput.value)) {
        emailInput.classList.add("is-invalid");
        emailInput.classList.remove("is-valid");
        return false;
      } else {
        emailInput.classList.remove("is-invalid");
        emailInput.classList.add("is-valid");
        return true;
      }
    }
  
    function formatPhoneNumber() {
      const phoneInput = document.getElementById("phone");
      const phoneNumber = phoneInput.value.replace(/\s/g, ""); // Remove any white spaces
  
      if (phoneNumber.length > 5 && phoneNumber.substring(0, 5) !== "00000") {
        phoneInput.value = phoneNumber.replace(
          /(\d{5})(\d{0,5})(\d{0,4})(\d{0,4})/,
          "$1 $2 $3 $4"
        );
      } else {
        phoneInput.value = phoneNumber;
      }
    }
  
    // function validatePhoneNumber() {
    //   const phonePattern = /^(?!0)(?!.*0{5})[0-9 ]{10,}$/; // Phone number must not start with 0, and no sequence of 5 consecutive 0s
    //   const phoneInput = document.getElementById("validatePhoneNumber");
  
    //   if (!phonePattern.test(phoneInput.value.replace(/\s/g, ""))) {
    //     phoneInput.classList.add("is-invalid"); // Adding invalid class to show input in red
    //     phoneInput.classList.remove("is-valid"); // Removing valid class
    //     phoneInput.nextElementSibling.textContent = "Enter a valid phone number"; // Display error message
    //     return false;
    //   } else {
    //     phoneInput.classList.remove("is-invalid"); // Removing invalid class
    //     phoneInput.classList.add("is-valid"); // Adding valid class
    //     phoneInput.nextElementSibling.textContent = ""; // Clear error message
    //     return true;
    //   }
    // }

    function validatePhoneNumber() {
      const phonePattern = /^[0-9 ]*$/; // Only allow numeric digits and spaces
      const phoneInput = document.getElementById("phone");
  
      if (!phonePattern.test(phoneInput.value)) {
          phoneInput.classList.add("is-invalid");
          phoneInput.classList.remove("is-valid");
          document.getElementById("phoneValidation").textContent = "Enter a valid phone number containing only numbers and spaces";
          return false;
      } else {
          phoneInput.classList.remove("is-invalid");
          phoneInput.classList.add("is-valid");
          document.getElementById("phoneValidation").textContent = "";
          return true;
      }
  }
  
  // Add an event listener to trigger the validation function when the input field changes
  document.getElementById("phone").addEventListener("input", validatePhoneNumber);
  
  
  
  
  
    function validatePassword() {
      const passwordPattern =
        /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()_+[\]{}|;:'",.<>?/~`]).{8,}$/;
      const passValidation = document.getElementById("passValidation");
      const passValid = document.getElementById("passValid");
  
      if (!passwordPattern.test(passwordInput.value)) {
        passwordInput.classList.add("is-invalid");
        passwordInput.classList.remove("is-valid");
        passValidation.style.display = "block";
        passValid.style.display = "none";
      } else {
        passwordInput.classList.remove("is-invalid");
        passwordInput.classList.add("is-valid");
        passValidation.style.display = "none";
        passValid.style.display = "block";
      }
    }
  
    function validateConfirmPassword() {
      const confirmPasswordValidation =
        document.getElementById("cpassValidation");
      const confirmPasswordValid = document.getElementById("cpassValid");
  
      if (passwordInput.value !== confirmPasswordInput.value) {
        confirmPasswordInput.classList.add("is-invalid");
        confirmPasswordInput.classList.remove("is-valid");
        confirmPasswordValidation.style.display = "block";
        confirmPasswordValid.style.display = "none";
      } else {
        confirmPasswordInput.classList.remove("is-invalid");
        confirmPasswordInput.classList.add("is-valid");
        confirmPasswordValidation.style.display = "none";
        confirmPasswordValid.style.display = "block";
      }
    }
  
    // try {
    // Your validation code here
    if (cityInput) {
      // Check if the addressInput element exists
  
      cityInput.addEventListener("onchange", validateCity);
    }
  //   
      addressInput.addEventListener("keyup", validateAddress);
      addressInput2.addEventListener("keyup", validateAddress1);
      addressInput3.addEventListener("keyup", validateAddress2);
      cityInput.addEventListener("keyup", validateCity);
  
  
      function validateCity() {
        console.log("validateCity function called");
        const cityPattern = /^[A-Za-z ]+$/;
        const cityValidation = document.getElementById("cityValidation");
        const cityValid = document.getElementById("cityValid");
        const inputValue = cityInput.value.trim();
  
        if (!cityPattern.test(inputValue)) {
          cityInput.classList.add("is-invalid");
          cityInput.classList.remove("is-valid");
          cityValidation.style.display = "block";
          cityValid.style.display = "none";
        } else {
          cityInput.classList.remove("is-invalid");
          cityInput.classList.add("is-valid");
          cityValidation.style.display = "none";
          cityValid.style.display = "block";
        }
      }
  
      function validateAddress() {
          console.log("validateAddress function called");
          const addressPattern = /^(?=.*[A-Za-z])[A-Za-z0-9(),\- ]+$/;
          const addressValidation = document.getElementById("addressValidation");
          const addressValid = document.getElementById("addressValid");
          const inputValue = addressInput.value.trim();
    
          if (!addressPattern.test(inputValue)) {
            addressInput.classList.add("is-invalid");
            addressInput.classList.remove("is-valid");
            addressValidation.style.display = "block";
            addressValid.style.display = "none";
          } else {
            addressInput.classList.remove("is-invalid");
            addressInput.classList.add("is-valid");
            addressValidation.style.display = "none";
            addressValid.style.display = "block";
          }
        }
    
        function validateAddress1() {
          console.log("validateAddress1 function called");
          const addressPattern = /^(?=.*[A-Za-z])[A-Za-z0-9(),\- ]+$/;
          const addressValidation1 = document.getElementById("addressValidation1");
          const addressValid = document.getElementById("addressValid");
          const inputValue = addressInput2.value.trim();
    
          if (!addressPattern.test(inputValue)) {
            addressInput2.classList.add("is-invalid");
            addressInput2.classList.remove("is-valid");
            addressValidation1.style.display = "block";
            addressValid.style.display = "none";
          } else {
            addressInput2.classList.remove("is-invalid");
            addressInput2.classList.add("is-valid");
            addressValidation1.style.display = "none";
            addressValid.style.display = "block";
          }
        }
    
        function validateAddress2() {
          console.log("validateAddress2 function called");
          const addressPattern = /^(?=.*[A-Za-z])[A-Za-z0-9(),\- ]+$/;
          const addressValidation2 = document.getElementById("addressValidation2");
          const addressValid = document.getElementById("addressValid");
          const inputValue = addressInput3.value.trim();
    
          if (!addressPattern.test(inputValue)) {
            addressInput3.classList.add("is-invalid");
            addressInput3.classList.remove("is-valid");
            addressValidation2.style.display = "block";
            addressValid.style.display = "none";
          } else {
            addressInput3.classList.remove("is-invalid");
            addressInput3.classList.add("is-valid");
            addressValidation2.style.display = "none";
            addressValid.style.display = "block";
          }
        }
  
        const zipcodeInput = document.getElementById("zipcode");
        zipcodeInput.addEventListener("keyup", validateZipcode);
  
      function validateZipcode() {
        console.log("validateZipcode function called");
        const zipcodePattern = /^\d{6}$/;
        const zipcodeValidation = document.getElementById("zipcodeValidation");
        const zipcodeValid = document.getElementById("zipcodeValid");
        const inputValue = zipcodeInput.value.trim();
  
        if (!zipcodePattern.test(inputValue)) {
          zipcodeInput.classList.add("is-invalid");
          zipcodeInput.classList.remove("is-valid");
          zipcodeValidation.style.display = "block";
          zipcodeValid.style.display = "none";
        } else {
          zipcodeInput.classList.remove("is-invalid");
          zipcodeInput.classList.add("is-valid");
          zipcodeValidation.style.display = "none";
          zipcodeValid.style.display = "block";
        }
      }
  
  
      const dobInput = document.getElementById("dob");
  
      if (dobInput) {
        // Check if the addressInput element exists
     
        dobInput.addEventListener("keyup", validateDOB);
      }
      // dobInput.addEventListener("blur", validateDOB);
  
      function validateDOB() {
        console.log("validateDOB function called");
        const dobValidation = document.getElementById("dobValidation");
        const dobValid = document.getElementById("dobValid");
        const inputValue = dobInput.value;
  
        // Calculate the age based on the entered date of birth
        const currentDate = new Date();
        const selectedDate = new Date(inputValue);
        const age = currentDate.getFullYear() - selectedDate.getFullYear();
  
        if (age < 23 || age > 100) {
          dobInput.classList.add("is-invalid");
          dobInput.classList.remove("is-valid");
          dobValidation.style.display = "block";
          dobValid.style.display = "none";
        } else {
          dobInput.classList.remove("is-invalid");
          dobInput.classList.add("is-valid");
          dobValidation.style.display = "none";
          dobValid.style.display = "block";
        }
      }
  
      const dobclientInput = document.getElementById("dobclient");
      console.log(dobclientInput)
      if (dobclientInput) {
        // Check if the addressInput element exists
        dobclientInput.addEventListener("blur", validateDOBclient);
      }
      // dobclientInput.addEventListener("blur", validateDOBclient);
      
      function validateDOBclient() {
        console.log("validateDOB function called");
        const dobclientValidation = document.getElementById("dobclientValidation");
        const dobValid = document.getElementById("dobValid");
        const inputValue = dobclientInput.value;
      
        // Calculate the age based on the entered date of birth
        const currentDate = new Date();
        const selectedDate = new Date(inputValue);
        const ageInYears = currentDate.getFullYear() - selectedDate.getFullYear();
      
        // Check if the age is at least 5 years
        if (ageInYears < 8) {
          dobclientInput.classList.add("is-invalid");
          dobclientInput.classList.remove("is-valid");
          dobclientValidation.style.display = "block";
          dobValid.style.display = "none";
        } else {
          dobclientInput.classList.remove("is-invalid");
          dobclientInput.classList.add("is-valid");
          dobclientValidation.style.display = "none";
          dobValid.style.display = "block";
        }
      }
      
  
  
      const bioInput = document.getElementById("bio");
      if (bioInput) {
        // Check if the addressInput element exists
        bioInput.addEventListener("blur", validateBio);
      }
      
  
      function validateBio() {
        console.log("validateBio function called");
        const bioValidation = document.getElementById("bioValidation");
        const bioValid = document.getElementById("bioValid");
        const inputValue = bioInput.value;
  
        // Remove all non-alphanumeric characters except '()', '-', "'", '"', and '.'
        const cleanedInput = inputValue.replace(/[^A-Za-z0-9()\-'"\.]/g, ' ');
  
        // Split the cleaned input into words
        const words = cleanedInput.split(/\s+/);
  
        if (words.length < 100) {
          bioInput.classList.add("is-invalid");
          bioInput.classList.remove("is-valid");
          bioValidation.style.display = "block";
          bioValid.style.display = "none";
        } else {
          bioInput.classList.remove("is-invalid");
          bioInput.classList.add("is-valid");
          bioValidation.style.display = "none";
          bioValid.style.display = "block";
        }
      }
  
  
      const certificationNameInput = document.getElementById("certname");
      if (certificationNameInput) {
        // Check if the addressInput element exists
        certificationNameInput.addEventListener("blur", validateCertificationName);
      }
  
      function validateCertificationName() {
        console.log("validateCertificationName function called");
        const certificationNameValidation = document.getElementById("certificationNameValidation");
        const certificationNameValid = document.getElementById("certificationNameValid");
        const inputValue = certificationNameInput.value;
  
        const certificationNamePattern = /^[A-Za-z][A-Za-z\s]*[-_]?[A-Za-z\s]*$/;
  
  
        if (!certificationNamePattern.test(inputValue)) {
          certificationNameInput.classList.add("is-invalid");
          certificationNameInput.classList.remove("is-valid");
          certificationNameValidation.style.display = "block";
          certificationNameValid.style.display = "none";
        } else {
          certificationNameInput.classList.remove("is-invalid");
          certificationNameInput.classList.add("is-valid");
          certificationNameValidation.style.display = "none";
          certificationNameValid.style.display = "block";
        }
      }
  
  
  
      const certificationIdInput = document.getElementById("certificationId");
      if (certificationIdInput) {
        // Check if the addressInput element exists
        certificationIdInput.addEventListener("blur", validateCertificationId);
      }
  
      function validateCertificationId() {
        console.log("validateCertificationId function called");
        const certificationIdValidation = document.getElementById("certificationIdValidation");
        const certificationIdValid = document.getElementById("certificationIdValid");
        const inputValue = certificationIdInput.value.trim();
  
        // Regular expression to match certification ID criteria (letters and numbers only)
        const certificationIdPattern = /^[A-Za-z0-9]+$/;
  
        if (!certificationIdPattern.test(inputValue)) {
          certificationIdInput.classList.add("is-invalid");
          certificationIdInput.classList.remove("is-valid");
          certificationIdValidation.style.display = "block";
          certificationIdValid.style.display = "none";
        } else {
          certificationIdInput.classList.remove("is-invalid");
          certificationIdInput.classList.add("is-valid");
          certificationIdValidation.style.display = "none";
          certificationIdValid.style.display = "block";
        }
      }
        
  
  
      const experienceInput = document.getElementById("experience");
      if (experienceInput) {
        // Check if the addressInput element exists
        experienceInput.addEventListener("blur", validateExperience);
      }
  
      function validateExperience() {
        console.log("validateExperience function called");
        const experienceValidation = document.getElementById("experienceValidation");
        const experienceValid = document.getElementById("experienceValid");
        const inputValue = experienceInput.value.trim();
  
        // Regular expression to match valid numbers (positive integers)
        const numberPattern = /^\d+$/;
  
        if (!numberPattern.test(inputValue) || parseInt(inputValue) < 2) {
          experienceInput.classList.add("is-invalid");
          experienceInput.classList.remove("is-valid");
          experienceValidation.style.display = "block";
          experienceValid.style.display = "none";
        } else {
          experienceInput.classList.remove("is-invalid");
          experienceInput.classList.add("is-valid");
          experienceValidation.style.display = "none";
          experienceValid.style.display = "block";
        }
      }
  
      const pictureInput = document.getElementById("pictureInput");
      const pictureForm = document.getElementById("pictureForm");
      if (pictureInput) {
        // Check if the addressInput element exists
        pictureInput.addEventListener("change", validatePicture);
      }
  
      function validatePicture() {
        console.log("validatePicture function called");
        const pictureValidation = document.getElementById("pictureValidation");
        const pictureValid = document.getElementById("pictureValid");
  
        // Check if a file is selected
        if (!pictureInput.files || pictureInput.files.length === 0) {
          pictureForm.classList.add("was-validated");
          return;
        }
  
        const file = pictureInput.files[0];
        const validExtensions = ["jpg", "jpeg", "png", "gif"];
  
        const fileNameParts = file.name.split(".");
        const fileExtension = fileNameParts[fileNameParts.length - 1].toLowerCase();
  
        if (validExtensions.indexOf(fileExtension) === -1) {
          pictureForm.classList.add("was-validated");
          pictureValidation.style.display = "block";
          pictureValid.style.display = "none";
        } else {
          pictureForm.classList.add("was-validated");
          pictureValidation.style.display = "none";
          pictureValid.style.display = "block";
        }
      }
  
  
  
  
  
   });
  