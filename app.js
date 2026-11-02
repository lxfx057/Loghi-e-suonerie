const tones = [
  ["Crazy Frog", "crazy-frog.mp3"],
  ["Topolona", "topolona.mp3"],
  ["Dragostea din tei", "dragostea-din-tei.mp3"],
  ["Ketchup Song", "ketchup-song.mp3"],
  ["Super Mario Theme", "super-mario-theme.mp3"],
  ["Nokia 3310", "nokia-3310.mp3"],
  ["Motorola Hello Moto", "motorola-hello-moto.mp3"]
];

let selected = null;
const list = document.querySelector("#tones");
const preview = document.querySelector("#preview");
const status = document.querySelector("#status");
const downloadButton = document.querySelector("#downloadTone");
const shareButton = document.querySelector("#shareTone");

function selectedUrl() {
  return selected ? new URL(`audio/${selected[1]}`, location.href).href : null;
}

function setStatus(message) {
  status.textContent = message;
}

tones.forEach((tone, index) => {
  const button = document.createElement("button");
  button.className = "tone";
  button.type = "button";
  button.innerHTML = `${index + 1}. ${tone[0]}<small>CLICK TO SELECT / PREVIEW</small>`;
  button.addEventListener("click", () => {
    selected = tone;
    preview.pause();
    preview.currentTime = 0;
    preview.src = selectedUrl();
    preview.load();
    downloadButton.disabled = false;
    shareButton.disabled = false;
    document.querySelectorAll(".tone").forEach(item => item.classList.remove("selected"));
    button.classList.add("selected");
    setStatus(`Selected: ${tone[0]}`);
  });
  list.appendChild(button);
});

downloadButton.addEventListener("click", () => {
  if (!selected) return setStatus("Please select a tone first.");
  const link = document.createElement("a");
  link.href = selectedUrl();
  link.download = selected[1];
  document.body.appendChild(link);
  link.click();
  link.remove();
  setStatus(`Downloading ${selected[0]}…`);
});

shareButton.addEventListener("click", async () => {
  if (!selected) return setStatus("Please select a tone first.");
  const url = selectedUrl();
  try {
    if (navigator.share) {
      await navigator.share({ title: selected[0] + " ringtone", text: "Listen to this ringtone", url });
      setStatus("Share sheet opened.");
    } else if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(url);
      setStatus("Ringtone link copied.");
    } else {
      setStatus(url);
    }
  } catch (error) {
    if (error.name !== "AbortError") setStatus("Could not share the link.");
  }
});

document.querySelector("#send").addEventListener("click", () => {
  const phone = document.querySelector("#phone").value.trim();
  if (!selected) return setStatus("Please select a tone first.");
  if (!phone) return setStatus("Please enter a phone number.");
  const message = `Hey! I found this awesome ringtone for you:\n${selectedUrl()}`;
  const smsUrl = /iPad|iPhone|iPod/.test(navigator.userAgent)
    ? `sms:${encodeURIComponent(phone)}&body=${encodeURIComponent(message)}`
    : `sms:${encodeURIComponent(phone)}?body=${encodeURIComponent(message)}`;
  location.href = smsUrl;
});
