//クリックヒートマップのためのデータ収集部分
const csrftoken = "{{ csrf_token }}";
let jsonString = localStorage.getItem('clickData');
let clickData = jsonString ? JSON.parse(jsonString) : {};


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

// ページ離脱時にデータをJSON形式で保存
window.addEventListener('beforeunload', function() {
    // データをJSON形式に変換
    let jsonString = JSON.stringify(clickData);
    
    // データをローカルストレージに保存
    localStorage.setItem('clickData', jsonString);
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
    let JsonString = JSON.stringify(clickData);
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/receive-click-data"); 
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.setRequestHeader("X-CSRFToken", csrfToken); // リクエストヘッダーにCSRFトークンを設定
    xhr.send(JsonString);
}


