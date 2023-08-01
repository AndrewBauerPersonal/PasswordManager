chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.type === 'credentials') {
      // Here, you can handle the received credentials and send them to your server-side API
      // Implement the logic to securely transmit the credentials to your server-side component
      // Example: Send a POST request to your server-side API
      fetch('http://127.0.0.1:5000/api/saveCredentials', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(message.credentials),
      })
        .then(response => response.json())
        .then(data => {
          // Handle the response from your server-side API
          console.log(data);
        })
        .catch(error => {
          // Handle any errors that occur during the request
          console.error(error);
        });
    }
  });