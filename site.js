/* Levitt Pavilion Houston | site.js
   Mobile menu, logo fallback, email signup and contact forms. No dependencies. */
(function () {
  // ONE setting turns on every form on the site.
  // Create a free Formspree form that delivers to info@levitthouston.org and paste its URL here,
  // for example "https://formspree.io/f/abcdwxyz". Contact, Get Involved and signup forms all post to it.
  // Netlify Forms: posts to the site itself. Submissions appear in Netlify under Forms.
  var FORM_ENDPOINT = "/";
  // Optional: once a mailing list (Mailchimp or MailerLite) is set up, paste its endpoint here.
  // Until then, signups go to FORM_ENDPOINT and arrive at info@ as emails.
  var SIGNUP_ENDPOINT = "";
  var CONTACT = "info@levitthouston.org";

  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("open")) {
        nav.classList.remove("open"); toggle.setAttribute("aria-expanded", "false"); toggle.focus();
      }
    });
  }

  document.querySelectorAll("img[data-logo]").forEach(function (img) {
    function swap() { var s = document.createElement("span"); s.className = "brand-text"; s.textContent = "Levitt Pavilion Houston"; img.replaceWith(s); }
    if (img.complete && img.naturalWidth === 0) swap(); else img.addEventListener("error", swap);
  });

  // Preselect interest from ?interest=volunteer etc.
  var params = new URLSearchParams(location.search);
  var interest = params.get("interest");
  if (interest) {
    document.querySelectorAll("select[name=interest]").forEach(function (sel) {
      for (var i = 0; i < sel.options.length; i++) if (sel.options[i].value === interest) sel.selectedIndex = i;
    });
  }

  // Next concert bar rolls forward after each date.
  var bar = document.querySelector(".nextbar[data-events]");
  if (bar) {
    try {
      var events = JSON.parse(bar.getAttribute("data-events"));
      var today = new Date(); today.setHours(0, 0, 0, 0);
      var next = events.filter(function (ev) { return new Date(ev.date + "T23:59:59") >= today; })[0];
      var p = bar.querySelector("p");
      if (next) p.innerHTML = "Next concert: " + next.label + " at Willow Waterhole. Free. <a href=\"" + next.href + "\">Details</a>";
      else bar.remove();
    } catch (e) {}
  }

  // UTM tags from QR codes and links, kept for the visit.
  var utm = {};
  ["utm_source", "utm_medium", "utm_campaign"].forEach(function (k) {
    var v = params.get(k);
    try { if (v) sessionStorage.setItem(k, v); v = v || sessionStorage.getItem(k); } catch (e) {}
    if (v) utm[k] = v;
  });

  function send(form, fields, status, okMsg, subject, endpoint) {
    var hp = form.querySelector("[name=_gotcha]");
    if (hp && hp.value) { status.textContent = okMsg; form.reset(); return; }
    if (!endpoint) {
      status.innerHTML = "Our online form isn&rsquo;t connected yet. Please email <a href=\"mailto:" + CONTACT + "\">" + CONTACT + "</a>.";
      return;
    }
    fields.subject = subject;
    fields.page = location.pathname;
    Object.keys(utm).forEach(function (k) { fields[k] = utm[k]; });
    var nameField = form.querySelector("[name=form-name]");
    if (nameField) fields["form-name"] = nameField.value;
    var btn = form.querySelector("button[type=submit]");
    if (btn) btn.disabled = true;
    status.textContent = "Sending...";
    var netlify = form.hasAttribute("data-netlify");
    fetch(endpoint, netlify
      ? { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" }, body: new URLSearchParams(fields).toString() }
      : { method: "POST", headers: { "Accept": "application/json", "Content-Type": "application/json" }, body: JSON.stringify(fields) })
      .then(function (r) { if (!r.ok) throw new Error("code " + r.status); status.textContent = okMsg; form.reset(); })
      .catch(function (err) { status.innerHTML = "Something went wrong (" + (err && err.message ? err.message : "no response") + "). Please try again, or email <a href=\"mailto:" + CONTACT + "\">" + CONTACT + "</a>."; })
      .then(function () { if (btn) btn.disabled = false; });
  }

  document.querySelectorAll(".signup-form").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var input = form.querySelector("input[type=email]"), status = form.querySelector(".signup-status");
      if (!input.checkValidity()) { status.textContent = "Enter a valid email address."; input.focus(); return; }
      send(form, { email: input.value.trim(), source: form.getAttribute("data-source") || location.pathname },
        status, "You&rsquo;re on the list. Watch your inbox for who&rsquo;s playing.".replace(/&rsquo;/g, "\u2019"),
        "Concert updates signup", SIGNUP_ENDPOINT || FORM_ENDPOINT);
    });
  });

  document.querySelectorAll(".lh-form").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var status = form.querySelector(".form-status");
      if (!form.checkValidity()) { status.textContent = "Please add your name and a valid email."; form.reportValidity(); return; }
      var d = new FormData(form), fields = {};
      d.forEach(function (v, k) { fields[k] = String(v).trim(); });
      fields.source = form.getAttribute("data-source") || location.pathname;
      var sel = form.querySelector("select[name=interest]");
      var label = sel ? sel.options[sel.selectedIndex].text : "General question";
      send(form, fields, status, "Thanks. Your message was sent and someone from Levitt Houston will follow up.",
        "Website inquiry: " + label, FORM_ENDPOINT);
    });
  });
})();
