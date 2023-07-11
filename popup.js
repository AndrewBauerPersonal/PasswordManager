// Popup script code
document.addEventListener('DOMContentLoaded', function() {
    const credentialsList = document.getElementById('credentials-list');
  
    // Send a message to the background script to retrieve the captured credentials
    chrome.runtime.sendMessage({ type: 'getCredentials' }, function(response) {
      const credentialsData = response.credentials;
  
      // Populate the credentials list
      credentialsData.forEach(function(credentials) {
        const listItem = document.createElement('li');
        listItem.innerHTML = `
          <span class="website">${credentials.website}</span><br>
          <span class="username">${credentials.username}</span><br>
          <span class="password">${credentials.password}</span>
        `;
        credentialsList.appendChild(listItem);
      });
    });
  });