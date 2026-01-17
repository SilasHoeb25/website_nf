(function () {
    // Prevent double-init (useful if scripts get loaded twice)
    if (window.__heroGalleryInit) return;
    window.__heroGalleryInit = true;
  
    const gallery = document.getElementById("hero-gallery");
    const slides = Array.from(document.querySelectorAll(".gallery-slide"));
    const prevBtn = document.getElementById("gallery-prev");
    const nextBtn = document.getElementById("gallery-next");
  
    if (!gallery || slides.length <= 1) return;
  
    const INTERVAL_MS = 7000;
    const SWIPE_THRESHOLD_PX = 40;
  
    let index = 0;
    let timer = null;
    let isPaused = false;
  
    let touchStartX = null;
    let touchStartY = null;
  
    function setTransitionEnabled(enabled) {
      slides.forEach((img) => {
        if (enabled) img.classList.add("transition-opacity");
        else img.classList.remove("transition-opacity");
      });
    }
  
    function show(nextIndex, { animated = true } = {}) {
      setTransitionEnabled(animated);
  
      slides[index].classList.remove("opacity-100");
      slides[index].classList.add("opacity-0");
  
      index = (nextIndex + slides.length) % slides.length;
      slides[index].classList.remove("opacity-0");
      slides[index].classList.add("opacity-100");
  
      if (!animated) requestAnimationFrame(() => setTransitionEnabled(true));
    }
  
    function next(animated = true) { show(index + 1, { animated }); }
    function prev(animated = true) { show(index - 1, { animated }); }
  
    function start() {
      stop();
      timer = setInterval(() => {
        if (!isPaused) next(true); // auto uses fade
      }, INTERVAL_MS);
    }
  
    function stop() {
      if (timer) clearInterval(timer);
      timer = null;
    }
  
    function resetTimer() { start(); }
  
    // Buttons (instant)
    if (prevBtn) prevBtn.addEventListener("click", () => { prev(false); resetTimer(); });
    if (nextBtn) nextBtn.addEventListener("click", () => { next(false); resetTimer(); });
  
    // Pause on hover / focus
    gallery.addEventListener("mouseenter", () => { isPaused = true; });
    gallery.addEventListener("mouseleave", () => { isPaused = false; });
    gallery.addEventListener("focusin", () => { isPaused = true; });
    gallery.addEventListener("focusout", () => { isPaused = false; });
  
    // Swipe (instant)
    gallery.addEventListener("touchstart", (e) => {
      if (!e.touches || e.touches.length !== 1) return;
      touchStartX = e.touches[0].clientX;
      touchStartY = e.touches[0].clientY;
      isPaused = true;
    }, { passive: true });
  
    gallery.addEventListener("touchend", (e) => {
      if (touchStartX === null || touchStartY === null) {
        isPaused = false;
        return;
      }
  
      const touch = (e.changedTouches && e.changedTouches[0]) ? e.changedTouches[0] : null;
      if (!touch) {
        touchStartX = touchStartY = null;
        isPaused = false;
        return;
      }
  
      const dx = touch.clientX - touchStartX;
      const dy = touch.clientY - touchStartY;
  
      if (Math.abs(dx) > Math.abs(dy) && Math.abs(dx) >= SWIPE_THRESHOLD_PX) {
        if (dx < 0) next(false);
        else prev(false);
        resetTimer();
      }
  
      touchStartX = touchStartY = null;
      isPaused = false;
    }, { passive: true });
  
    // Init
    slides.forEach((img, i) => {
      if (i === 0) {
        img.classList.add("opacity-100");
        img.classList.remove("opacity-0");
      } else {
        img.classList.add("opacity-0");
        img.classList.remove("opacity-100");
      }
    });
  
    start();
  })();
  