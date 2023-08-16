// contentScript.js

function extractPasswordsFromTable() {
  const passwords = [];
  const rows = document.querySelectorAll("#passwords-table tbody tr");

  rows.forEach(row => {
    const websiteCell = row.querySelector("td:nth-child(1)");
    const usernameCell = row.querySelector("td:nth-child(2)");
    const passwordCell = row.querySelector(".actual-password");

    const website = websiteCell.textContent.trim();
    const username = usernameCell.textContent.trim();
    const password = passwordCell.textContent.trim();

    passwords.push({ website, username, password });
  });

  return passwords;
}

chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
  if (message.action === "getPasswords") {
    const passwords = extractPasswordsFromTable();
    sendResponse({ passwords });
  }
});