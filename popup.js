// 🔁 When popup opens, request last scan data from background
document.addEventListener("DOMContentLoaded", () => {
  chrome.runtime.sendMessage({ type: "GET_SCAN_RESULT" }, (response) => {
    const result = response?.data;
    if (!result) {
      document.getElementById("scan-result").innerText = "⚠️ No recent scan data found.";
      return;
    }

    displaySecurityScore(result.score);
    displayReport(result.subject, result.sender, result.vtResults || []);
  });
});

// 🧠 Display total security score + risk level
function displaySecurityScore(score) {
  const div = document.getElementById("security-score");
  if (!score) return;

  const color = score.risk_level === "High" ? "#e53935"
             : score.risk_level === "Moderate" ? "#fb8c00"
             : "#43a047";

  div.innerHTML = `
    <div style="padding: 10px; border-radius: 8px; background: ${color}; color: white;">
       Risk Level: <strong>${score.risk_level}</strong><br/>
       Total Score: <strong>${score.total_score}</strong>/100
    </div>
  `;
}

// 🧾 Display scan results (links + attachments)
function displayReport(subject, sender, vtResults) {
  const reportDiv = document.getElementById("scan-result");

  reportDiv.innerHTML = `
    <h3> Email Security Report</h3>
    <strong>Subject:</strong> ${subject}<br/>
    <strong>Sender:</strong> ${sender}<br/><br/>

    <h4> Links & Attachments:</h4>
    <ul style="font-size: 13px; padding-left: 20px;">
      ${vtResults.map(result => {
        const stats = result?.data?.attributes?.stats || {};
        const label = determineRiskLabel(stats);
        return `<li><code>${result.link || result.name || "Attachment"}</code><br/>→ ${label}</li>`;
      }).join("")}
    </ul>
  `;
}

// 🟢 Determine risk label from VirusTotal stats
function determineRiskLabel(stats) {
  if (!stats) return "⚠️ Unknown";
  const { malicious = 0, suspicious = 0 } = stats;
  if (malicious > 0) return " Malicious";
  if (suspicious > 0) return " Suspicious";
  return "✅ Safe";
}
