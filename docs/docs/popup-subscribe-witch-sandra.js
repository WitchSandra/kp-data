// 📦 Универсальные функции для многих окон
function openPopup(popupId, overlayId) {
    const popup = document.getElementById(popupId);
    const overlay = document.getElementById(overlayId);
    if (popup && overlay) {
        popup.style.display = 'block';
        overlay.style.display = 'block';
    }
}

function closePopup(popupId, overlayId) {
    const popup = document.getElementById(popupId);
    const overlay = document.getElementById(overlayId);
    if (popup && overlay) {
        popup.style.display = 'none';
        overlay.style.display = 'none';
    }
}

function showPopupWithDelay(popupId, overlayId, delaySeconds, storageKey, intervalHours) {
    const lastTime = localStorage.getItem(storageKey);
    const now = new Date().getTime();
    const delay = delaySeconds * 1000;
    const interval = intervalHours * 60 * 60 * 1000;

    if (!lastTime || (now - lastTime) > interval) {
        setTimeout(() => {
            openPopup(popupId, overlayId);
            localStorage.setItem(storageKey, now);
        }, delay);
    }
}

// 📜 Вместо window.load — срабатывание при прокрутке 50% вниз
window.addEventListener("scroll", function onScroll() {
    const scrollY = window.scrollY || window.pageYOffset;
    const pageHeight = document.body.scrollHeight - window.innerHeight;
    const scrolledPercent = (scrollY / pageHeight) * 100;

    if (scrolledPercent > 50) {
        window.removeEventListener("scroll", onScroll);

        showPopupWithDelay(
            "jetpack-subscribe-popup",     // ID всплывающего окна
            "jetpack-subscribe-overlay",   // ID затемнения
            0,                              // без задержки (сразу после условия)
            "jetpackSubscribedTime",        // ключ localStorage
            24                              // интервал повторного показа (в часах)
        );
    }
});
