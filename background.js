let lastScanData = null;

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "SAVE_SCAN_RESULT") {
    lastScanData = message.payload;
    sendResponse({ status: "saved" });

    // Open a small popup window with the scan report
    chrome.windows.create({
      url: chrome.runtime.getURL("popup.html"),
      type: "popup",
      width: 420,
      height: 600
    });
  }

  if (message.type === "GET_SCAN_RESULT") {
    sendResponse({ data: lastScanData });
  }
});

