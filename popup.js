// popup.js

document.addEventListener("DOMContentLoaded", function () {
  const getPasswordsButton = document.getElementById("getPasswords");
  const passwordList = document.getElementById("passwordList");
  const openPasswordsPageButton = document.getElementById('openPasswordsPage'); // Add this line

  getPasswordsButton.addEventListener("click", function () {
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
      const activeTab = tabs[0];
      chrome.scripting.executeScript(
        {
          target: { tabId: activeTab.id },
          function: extractPasswordsFromTable
        },
        function (results) {
          const passwords = results[0].result;
          passwordList.innerHTML = "";

          passwords.forEach(password => {
            const listItem = document.createElement("li");
            listItem.textContent = `Website: ${password.website}, Username: ${password.username}, Password: ${password.password}`;
            passwordList.appendChild(listItem);
          });
        }
      );
    });
  });
  openPasswordsPageButton.addEventListener('click', function () {
    // Open a new tab with the passwords page URL
    chrome.tabs.create({ url: 'http://localhost:5000/passwords' });
  });
});
