// для многих всплывающих окон 
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

// Вызов всплывающего окна Jetpack подписки через 20 секунд, повтор через 24 часа
window.addEventListener("load", function () {
    showPopupWithDelay(
        "jetpack-subscribe-popup",     // ID всплывающего окна
        "jetpack-subscribe-overlay",   // ID фона-затемнения
        20,                             // Задержка: 20 секунд
        "jetpackSubscribedTime",        // Ключ localStorage
        24                              // Интервал показа: 24 часа
    );
});
