const csrftoken = "{{ csrf_token }}";
let checkInterval = 1000; // 1秒ごとにチェック
let rangeSize = 1; // ピクセルごとに区切る
    

// ページロード時に既存のデータをローカルストレージから読み込む
let jsonString = localStorage.getItem('attentionData');
let attentionData = jsonString ? JSON.parse(jsonString) : {};
let intervalID = null;

// ウェブページが表示状態にあるときだけ滞在時間を増やす関数
function increaseStayTime() {
    if (document.hasFocus()) {  // <- 追加：ウェブページがフォーカスされている時だけ滞在時間を増やす
        let scrollPosition = Math.floor(window.scrollY / rangeSize) * rangeSize;
        if(attentionData[scrollPosition]) {
            attentionData[scrollPosition] += checkInterval / 1000;
        } else {
            attentionData[scrollPosition] = checkInterval / 1000;
        }
    }
}

// ページの表示状態が変わったときに呼び出される関数
function handleVisibilityChange() {
    if (document.hidden) {
        // ページが非表示状態になったとき、setIntervalをクリアする
        clearInterval(intervalID);
        intervalID = null;
    } else {
        // ページが表示状態になったとき、setIntervalを開始する
        intervalID = setInterval(increaseStayTime, checkInterval);
    }
}

// visibilitychangeイベントのハンドラを設定する
document.addEventListener('visibilitychange', handleVisibilityChange);

// 初回のsetIntervalを開始する
intervalID = setInterval(increaseStayTime, checkInterval);

// ページ離脱時にデータをJSON形式で保存
window.addEventListener('beforeunload', function() {
    let jsonString = JSON.stringify(attentionData);
    localStorage.setItem('attentionData', jsonString);
    sendDataToServer();  
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


function sendDataToServer() {
    let csrfToken = getCookie('csrftoken'); // CSRFトークンの取得
    let jsonString = JSON.stringify(attentionData);
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/receive-attention-data"); 
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.setRequestHeader("X-CSRFToken", csrfToken); // リクエストヘッダーにCSRFトークンを設定
    xhr.send(jsonString);
}