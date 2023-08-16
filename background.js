// background.js

chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
  if (message.action === 'getPasswords') {
    fetchPasswords(sendResponse);
    return true; // This tells Chrome to keep the message channel open for sendResponse
  }
});

function fetchPasswords(sendResponse) {
  fetch('http://localhost:5000/passwords', {
    method: 'GET',
    credentials: 'include' // Include cookies in the request for authentication
  })
    .then(response => response.json())
    .then(data => {
      sendResponse({ action: 'showPasswords', passwords: data.passwords });
    })
    .catch(error => console.error(error));
}
