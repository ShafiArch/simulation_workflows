/* Simulation Workflows: theme switch, sequence players, lightbox, the current section in the top bar. */
(function () {
  var root = document.documentElement;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* themes: Trace, Night, Clay; remembered with the works site's key */
  var btns = [].slice.call(document.querySelectorAll(".themes button"));
  function mark() { btns.forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.theme === root.dataset.theme ? "true" : "false"); }); }
  btns.forEach(function (b) {
    b.addEventListener("click", function () {
      root.dataset.theme = b.dataset.theme; mark();
      try { localStorage.setItem("site-theme", b.dataset.theme); } catch (e) {}
    });
  });
  mark();

  /* sequence players. <div class="seq" id="x" data-labels="A|B|C" data-ms="1400">: every .stack inside
     holds one child per frame. Anything on the page with data-seq="x" data-frame="i" lights up with
     the current frame and jumps the player to its frame when clicked. Plays while on screen. */
  [].slice.call(document.querySelectorAll(".seq")).forEach(function (seq) {
    var labels = (seq.dataset.labels || "").split("|");
    var n = labels.length, i = 0, timer = null, playing = !reduce, visible = false;
    var ms = +seq.dataset.ms || 1400;
    var stacks = [].slice.call(seq.querySelectorAll(".stack"));
    var linked = [].slice.call(document.querySelectorAll('[data-seq="' + seq.id + '"]'));
    var bar = document.createElement("div"); bar.className = "bar";
    var play = document.createElement("button"); play.type = "button"; play.className = "play";
    var steps = document.createElement("div"); steps.className = "steps";
    var now = document.createElement("span"); now.className = "now";
    labels.forEach(function (l, k) {
      var s = document.createElement("button"); s.type = "button"; s.textContent = seq.dataset.short ? seq.dataset.short.split("|")[k] : k + 1;
      s.setAttribute("aria-label", l); s.addEventListener("click", function () { stop(); show(k); });
      steps.appendChild(s);
    });
    bar.appendChild(play); bar.appendChild(steps); bar.appendChild(now); seq.appendChild(bar);
    function show(k) {
      i = (k + n) % n;
      stacks.forEach(function (st) { [].forEach.call(st.children, function (c, j) { c.classList.toggle("on", j === i); }); });
      [].forEach.call(steps.children, function (c, j) { c.classList.toggle("on", j === i); });
      linked.forEach(function (el) { el.classList.toggle("on", +el.dataset.frame === i); });
      now.textContent = labels[i];
    }
    function tick() { show(i + 1); }
    function run() { clearInterval(timer); timer = null; if (playing && visible) timer = setInterval(tick, ms); }
    function setPlay(p) { playing = p; play.textContent = p ? "❚❚" : "▶"; play.setAttribute("aria-label", p ? "Pause" : "Play"); run(); }
    function stop() { setPlay(false); }
    play.addEventListener("click", function () { setPlay(!playing); });
    linked.forEach(function (el) { el.addEventListener("click", function (e) { e.preventDefault(); e.stopPropagation(); stop(); show(+el.dataset.frame); }); });
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (es) { visible = es[0].isIntersecting; run(); }, { threshold: 0.25 }).observe(seq);
    } else { visible = true; }
    show(0); setPlay(playing);
  });

  /* lightbox: opens the large copy (data-l) when there is one */
  var lb = document.createElement("div"); lb.className = "lb"; lb.innerHTML = '<div><img alt=""><p></p></div>';
  document.body.appendChild(lb);
  var lbImg = lb.querySelector("img"), lbCap = lb.querySelector("p");
  document.addEventListener("click", function (e) {
    var img = e.target.closest && e.target.closest("figure img");
    if (!img || img.closest("[data-seq]")) return;
    var fig = img.closest("figure"), cap = fig.querySelector("figcaption");
    lbImg.src = img.dataset.l || img.currentSrc || img.src; lbImg.alt = img.alt;
    lbImg.className = img.classList.contains("sheet") || img.closest(".sheet") ? "sheet" : "";
    lbCap.textContent = cap ? cap.textContent : img.alt;
    lb.classList.toggle("scroll", fig.classList.contains("readable"));
    lb.classList.add("open"); lb.scrollTop = 0;
  });
  lb.addEventListener("click", function () { lb.classList.remove("open"); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") lb.classList.remove("open"); });

  /* the section in view, marked in the top bar */
  var links = [].slice.call(document.querySelectorAll(".toc a"));
  if ("IntersectionObserver" in window && links.length) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) { if (en.isIntersecting) links.forEach(function (a) { a.classList.toggle("on", a.getAttribute("href") === "#" + en.target.id); }); });
    }, { rootMargin: "-45% 0px -50% 0px" });
    links.forEach(function (a) { var s = document.querySelector(a.getAttribute("href")); if (s) io.observe(s); });
  }
})();
