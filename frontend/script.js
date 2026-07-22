// Landing page typing animation
const titleEl = document.getElementById("title");
const cursor = document.getElementById("cursor");
const subtitle = document.getElementById("subtitle");
const root = document.getElementById("root");
const video = document.getElementById("landingVideo");
const btnStart = document.getElementById("btn-getstarted");

if (titleEl) {
  const text = "Your Personal AI Stylist";
  let i = 0;
  function type() {
    if (i < text.length) {
      titleEl.textContent += text[i++];
      setTimeout(type, 45);
    } else {
      cursor.style.display = "none";
      subtitle.classList.add("show");
    }
  }
  setTimeout(type, 200);
}

// Fade out landing + show React chatbot
btnStart?.addEventListener("click", () => {
  document.body.classList.add("fade-out");
  setTimeout(() => {
    document.querySelector(".center-wrap").style.display = "none";
    root.style.display = "block";
    document.body.classList.remove("fade-out");
  }, 600);
});
