function showConfirmation() {
    var isLogout = window.confirm("ログアウトしますか？");
    confirmLogout(isLogout);
}

function cancelLogout() {
    alert("ログアウトしませんでした。");
    window.location.href = "/index";
}

function confirmLogout(isLogout) {
    if (isLogout) {
        fetch("/logout", { method: "POST" })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert("ログアウトしました。");
                    window.location.href = "/index";
                } else {
                    alert("ログアウトに失敗しました。");
                }
            });
    } else {
        // キャンセルされた場合、何もしない
    }
}

document.querySelector('.hamburger-menu').addEventListener('click', function () {
    document.querySelector('.menu').classList.toggle('active');
});
