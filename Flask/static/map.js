// map.js
// Google Maps JavaScript API の初期化とマップ設定
var map;

function initMap() {
  // HTMLのhidden inputから緯度と経度を取得
  var latitude = parseFloat(document.getElementById('latitude').value);
  var longitude = parseFloat(document.getElementById('longitude').value);

  // 取得した緯度と経度からマップの中心地点を定義
  var userLocation = {lat: latitude, lng: longitude};

  // マップオブジェクトの作成とDOMへの紐付け
  map = new google.maps.Map(document.getElementById('map'), {
    center: userLocation,
    zoom: 8 // マップのズームレベル
  });

  // マップ上にマーカーを設置
  new google.maps.Marker({
    position: userLocation,
    map: map
  });
}

// 位置情報の取得とサーバーへの送信
function getLocationAndUpdate() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      // 位置情報が取得できた場合、その情報をサーバーへPOSTリクエストで送信
      fetch('/api/update-location', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
          // その他必要な情報があればここに追加
        }),
      })
      .then(response => response.json())
      .then(data => {
        console.log('Location update successful:', data);
      })
      .catch((error) => {
        console.error('Error updating location:', error);
      });
    }, function(error) {
      // 位置情報の取得に失敗した場合のエラーハンドリング
      console.error('Error getting location', error);
    });
  } else {
    // Geolocation APIがサポートされていない場合
    console.error("Geolocation is not supported by this browser.");
  }
}

// 5分ごとに位置情報を更新するためのインターバル設定
setInterval(getLocationAndUpdate, 300000); // 300000ミリ秒 = 5分
