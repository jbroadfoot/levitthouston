/* Levitt Pavilion Houston | site.js
   Mobile menu, logo fallback, email signup. No dependencies. */

(function () {
  // Paste the email provider's form endpoint here once chosen (Mailchimp or MailerLite).
  // While empty, signups open a pre-addressed email to info@levitthouston.org.
  var SIGNUP_ENDPOINT = "";
  var CONTACT = "info@levitthouston.org";

  // Mobile menu
  var toggle = document.querySelector(".menu-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("open")) {
        nav.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
        toggle.focus();
      }
    });
  }

  // Logo fallback: if a logo file is missing, show the name as text
  document.querySelectorAll("img[data-logo]").forEach(function (img) {
    function swap() {
      var span = document.createElement("span");
      span.className = "brand-text";
      span.textContent = "Levitt Pavilion Houston";
      img.replaceWith(span);
    }
    if (img.complete && img.naturalWidth === 0) swap();
    else img.addEventListener("error", swap);
  });

  // Email signup
  document.querySelectorAll(".signup-form").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var input = form.querySelector("input[type=email]");
      var status = form.querySelector(".signup-status");
      if (!input.checkValidity()) {
        status.textContent = "Enter a valid email address.";
        input.focus();
        return;
      }
      var email = input.value.trim();
      var source = form.getAttribute("data-source") || location.pathname;
      if (!SIGNUP_ENDPOINT) {
        var body = "Please add " + email + " to Levitt Houston concert updates.\n\nSource: " + source;
        location.href = "mailto:" + CONTACT + "?subject=" + encodeURIComponent("Concert updates") + "&body=" + encodeURIComponent(body);
        status.textContent = "Your email app is opening. Send the message to join the list.";
        return;
      }
      var data = new FormData();
      data.append("email", email);
      data.append("source", source);
      fetch(SIGNUP_ENDPOINT, { method: "POST", body: data, mode: "no-cors" })
        .then(function () { status.textContent = "You're on the list. Watch your inbox for who's playing."; form.reset(); })
        .catch(function () { status.textContent = "Signup didn't go through. Email " + CONTACT + " and we'll add you."; });
    });
  });
})();
