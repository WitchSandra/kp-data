 // Показывать всплывающее окно через 20 секунд
function closeSubscribe() {
    document.getElementById('jetpack-subscribe-popup').style.display = 'none';
    document.getElementById('jetpack-subscribe-overlay').style.display = 'none';
}

function showSubscribePopup() {
    const popup = document.getElementById('jetpack-subscribe-popup');
    const overlay = document.getElementById('jetpack-subscribe-overlay');
    if (popup && overlay) {
        popup.style.display = 'block';
        overlay.style.display = 'block';
    }
    const now = new Date().getTime();
    localStorage.setItem("jetpackSubscribedTime", now);
}

window.addEventListener("load", function () {
    const lastTime = localStorage.getItem("jetpackSubscribedTime");
    const now = new Date().getTime();
    const delay = 20 * 1000;
    const interval = 24 * 60 * 60 * 1000;

    if (!lastTime || (now - lastTime) > interval) {
        setTimeout(showSubscribePopup, delay);
    }
});
