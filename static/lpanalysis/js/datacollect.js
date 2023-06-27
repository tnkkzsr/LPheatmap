const csrftoken = "{{ csrf_token }}";

let jsonString = localStorage.getItem('clickData');
let clickData = jsonString ? JSON.parse(jsonString) : {};

let attentionInterval = 1000; // 1秒ごとにチェック
let rangeSize = 1; // ピクセルごとに区切る

// ページロード時に既存のデータをローカルストレージから読み込む
jsonString = localStorage.getItem('attentionData');
let attentionData = jsonString ? JSON.parse(jsonString) : {};
let intervalID = null;

jsonString = localStorage.getItem('scrollData');
let scrollData = jsonString ? JSON.parse(jsonString) : {};
let maxScrollPosition = 0;

// スクロールイベントのリスニング
window.addEventListener('scroll', function() {
    let scrollPosition = window.scrollY;
    if(scrollPosition > maxScrollPosition) {
        maxScrollPosition = scrollPosition;
        if(scrollData[scrollPosition]) {
            scrollData[scrollPosition] += 1;
        } else {
            scrollData[scrollPosition] = 1;
        }
    }
});

// クリックイベントのリスニング
window.addEventListener('click', function(event) {
    // クリック位置を文字列で表現
    let clickPosition = `${event.clientX},${event.clientY}`;

    // クリック位置のデータを追加
    if(clickData[clickPosition]) {
        clickData[clickPosition] += 1;
    } else {
        clickData[clickPosition] = 1;
    }
});

function increaseStayTime() {
    if (document.hasFocus()) {  // <- 追加：ウェブページがフォーカスされている時だけ滞在時間を増やす
        let scrollPosition = Math.floor(window.scrollY / rangeSize) * rangeSize;
        if(attentionData[scrollPosition]) {
            attentionData[scrollPosition] += attentionInterval / 1000;
        } else {
            attentionData[scrollPosition] = attentionInterval / 1000;
        }
    }
}

function handleVisibilityChange() {
    if (document.hidden) {
        // ページが非表示状態になったとき、setIntervalをクリアする
        clearInterval(intervalID);
        intervalID = null;
    } else {
        // ページが表示状態になったとき、setIntervalを開始する
        intervalID = setInterval(increaseStayTime, attentionInterval);
    }
}

document.addEventListener('visibilitychange', handleVisibilityChange);

intervalID = setInterval(increaseStayTime, attentionInterval);

window.addEventListener('beforeunload', function() {
    // データをローカルストレージに保存
    localStorage.setItem('clickData', JSON.stringify(clickData));
    localStorage.setItem('attentionData', JSON.stringify(attentionData));
    localStorage.setItem('scrollData', JSON.stringify(scrollData));

    sendDataToServer('/receive-click-data', clickData);
    sendDataToServer('/receive-attention-data', attentionData);
    sendDataToServer('/receive-scroll-data', scrollData);
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function sendDataToServer(url, data) {
    let csrfToken = getCookie('csrftoken'); // CSRFトークンの取得
    let jsonString = JSON.stringify(data);
    let xhr = new XMLHttpRequest();
    xhr.open("POST", url); 
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.setRequestHeader("X-CSRFToken", csrfToken); // リクエストヘッダーにCSRFトークンを設定
    xhr.send(jsonString);
}
