document.getElementById('manual-scan').addEventListener('click', () => {
  document.getElementById("status").innerText = "⏳ Scanning...";

  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    chrome.scripting.executeScript({
      target: { tabId: tabs[0].id },
      func: () => {
        console.log("🧪 Manual scan triggered from popup.");
        getEmailData();  // must be defined in content.js
      }
    }, () => {
      if (chrome.runtime.lastError) {
        document.getElementById("status").innerText = "❌ Failed to scan. Check if Gmail is open.";
        console.error("Extension error:", chrome.runtime.lastError);
      } else {
        document.getElementById("status").innerText = "✅ Scan initiated.";
      }
    });
  });
});
