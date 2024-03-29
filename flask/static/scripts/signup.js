const myButton = document.getElementById('submit_button');
function checkCondition() {
  const password = document.getElementById('password').value;
  const confirmPassword = document.getElementById('confirm-password').value;
  return password === confirmPassword && password != '';
}

  // Function to enable or disable the button based on the condition
function updateButtonState() {
  const conditionMet = !checkCondition();
  myButton.disabled = conditionMet;
  if (conditionMet){
    myButton.style.backgroundColor = 'grey'
  }
  else {
    myButton.style.backgroundColor = 'green'
  }
}

// Call the updateButtonState function initially
updateButtonState();
