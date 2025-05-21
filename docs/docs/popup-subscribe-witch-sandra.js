 // Показывать всплывающее окно через 20 секунд
add_action('wp_footer', function () {
    ?>
    <style>
    #jetpack-subscribe-overlay {
        display: none;
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(0,0,0,0.4);
        z-index: 9998;
    }
    #jetpack-subscribe-popup {
        display: none;
        position: fixed;
        z-index: 9999;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
        background: #fff;
        padding: 25px 20px;
        border-radius: 12px;
        box-shadow: 0 0 20px rgba(0,0,0,0.3);
        max-width: 400px;
        width: 90%;
        box-sizing: border-box;
    }
    .jetpack-subscribe-close {
        position: absolute;
        top: 8px;
        right: 12px;
        cursor: pointer;
        font-size: 22px;
        color: #999;
    }
    @media (max-width: 480px) {
        #jetpack-subscribe-popup {
            padding: 20px 15px;
        }
        .jetpack-subscribe-close {
            top: 5px;
            right: 10px;
            font-size: 20px;
        }
    }
    </style>

    <div id="jetpack-subscribe-overlay"></div>
    <div id="jetpack-subscribe-popup">
        <div class="jetpack-subscribe-close" onclick="closeSubscribe()">×</div>
        <p style="font-size:18px; margin-bottom:10px; color:#7A7A7A;">✨ Подпишитесь на новости ✨</p>
        <?php echo do_shortcode('[jetpack_subscription_form title="" subscribe_text="Введите ваш e-mail, чтобы получать обновления от Ведьмы Сандры." subscribe_button="Подписаться"]'); ?>
    </div>

    <script>
    function closeSubscribe() {
        document.getElementById('jetpack-subscribe-popup').style.display = 'none';
        document.getElementById('jetpack-subscribe-overlay').style.display = 'none';
    }

    function showSubscribePopup() {
        document.getElementById('jetpack-subscribe-popup').style.display = 'block';
        document.getElementById('jetpack-subscribe-overlay').style.display = 'block';

        // Сохраняем время показа в localStorage
        const now = new Date();
        localStorage.setItem("jetpackSubscribedTime", now.getTime());
    }

    window.addEventListener("load", function () {
        const lastTime = localStorage.getItem("jetpackSubscribedTime");
        const now = new Date().getTime();
        const delay = 20 * 1000; // 20 секунд
        const interval = 24 * 60 * 60 * 1000; // 24 часа

        if (!lastTime || (now - lastTime) > interval) {
            setTimeout(showSubscribePopup, delay);
        }
    });
    </script>
    <?php
});
