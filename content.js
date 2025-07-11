function getEmailData() {
  const subject = document.querySelector("h2.hP")?.innerText || "";
  const senderEl = document.querySelector("span.gD");
  const senderName = senderEl?.innerText || "";
  const senderEmail = senderEl?.getAttribute("email") || "";

  const bodyEl = document.querySelector("div.a3s.aXjCH") || document.querySelector("div.a3s");
  const bodyText = bodyEl?.innerText || "";
  const bodyHTML = bodyEl?.innerHTML || "";

  const tempDiv = document.createElement("div");
  tempDiv.innerHTML = bodyHTML;

  const links = Array.from(tempDiv.querySelectorAll("a"))
    .map(a => a.href)
    .filter(href => href && href.startsWith("http"));

  const images = Array.from(tempDiv.querySelectorAll("img"))
    .map(img => img.src)
    .filter(src => src && src.startsWith("http"));

  const attachmentSpans = document.querySelectorAll('div.hq.gt div.aQH span.aZo[download_url]');
  const attachments = [];

  attachmentSpans.forEach(span => {
    const downloadAttr = span.getAttribute('download_url');
    if (downloadAttr) {
      const parts = downloadAttr.split(':');
      if (parts.length >= 3) {
        const type = parts[0];
        const name = parts[1];
        const url = parts.slice(2).join(':');
        attachments.push({ name, type, url });
      }
    }
  });

  const emailData = {
    subject,
    body: bodyText,
    senderName,
    senderEmail,
    links,
    images,
    attachments
  };

  // console.log("📧 RetailerShield Email Extracted:", emailData);
  
  // 🚀 Send data to FastAPI backend
  try {
  fetch("http://127.0.0.1:8000/api/process_email", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(emailData)
  })
    .then(res => res.json())
    .then(data => {
      console.log("✅ Backend response:", data);
      alert(`RetailerShield Scan Complete\nSubject: ${data.subject}`);
    })
    .catch(err => {
      console.error("❌ Fetch error:", err);
    });
  } catch (error) {
  console.error("❌ Unexpected error:", error);
  // alert(`RetailerShield Scan ✅\n\nFrom: ${senderName} <${senderEmail}>\nSubject: ${subject}\n\nLinks:\n${links.join("\n")}\n\nAttachments:\n${attachments.map(a => a.name).join("\n")}`);
  }
}

// 🔁 Watch the body for dynamic email changes
let lastEmailId = "";

const observer = new MutationObserver(() => {
  const subject = document.querySelector("h2.hP")?.innerText || "";
  const body = document.querySelector("div.a3s.aXjCH")?.innerText || "";

  const emailId = subject + body?.slice(0, 30);

  if (emailId && emailId !== lastEmailId) {
    lastEmailId = emailId;
    console.log("📩 RetailerShield: New email detected, scanning...");
    setTimeout(getEmailData, 3500); // Gmail sometimes loads content late
  }
});

// 👁️ Watch Gmail’s dynamic region
observer.observe(document.body, {
  childList: true,
  subtree: true
});

console.log("👀 RetailerShield: MutationObserver watching for emails...");
