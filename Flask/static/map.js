// Google Maps JavaScript API の初期化とマップ設定
var map;
var marker; // マーカーをグローバルに定義

function initMap() {
  var latitude = parseFloat(document.getElementById('latitude').value);
  var longitude = parseFloat(document.getElementById('longitude').value);

  var userLocation = { lat: latitude, lng: longitude };

  map = new google.maps.Map(document.getElementById('map'), {
    center: userLocation,
    zoom: 16
  });

  var userStatus = '緊急'; // 仮のユーザーステータス
  var iconUrl = getIcon(userStatus);

  // マーカーの初期化と設定
  marker = new google.maps.Marker({
    position: userLocation,
    map: map,
    icon: iconUrl
  });
}

function getIcon(userStatus) {
  var iconUrl = getIconUrl(userStatus); // アイコンのURLを取得

  // アイコンサイズを設定
  var iconSize = new google.maps.Size(50, 50);
  return {
    url: iconUrl,
    scaledSize: iconSize // アイコンの表示サイズを設定
  };
}

function getIconUrl(userStatus) {
  switch (userStatus) {
    case '待機':
      return '/static/map/user_待機.png';
    case '緊急':
      return '/static/map/user_緊急.png';
    case '迷子':
      return '/static/map/user_迷子.png';
    case '通常':
    default:
      return '/static/map/user_通常.png';
  }
}

function updateMarkerPosition(latitude, longitude) {
  var newLatLng = new google.maps.LatLng(latitude, longitude);
  if (marker) {
    marker.setPosition(newLatLng);
    map.setCenter(newLatLng);
  }
}

function updateMarkerIcon(userStatus) {
  if (marker) {
    var iconUrl = getIconUrl(userStatus);
    var icon = {
      url: iconUrl,
      scaledSize: new google.maps.Size(50, 50) // ここでアイコンのサイズを指定
    };
    marker.setIcon(icon);
  }
}


function getLocationAndUpdate() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      fetch('/api/update-location', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          latitude: position.coords.latitude,
          longitude: position.coords.longitude
        }),
      })
      .then(response => response.json())
      .then(data => {
        console.log('Location update successful:', data);
        updateMarkerPosition(position.coords.latitude, position.coords.longitude, '緊急'); // ステータスは例として「緊急」
      })
      .catch((error) => {
        console.error('Error updating location:', error);
      });
    }, function(error) {
      console.error('Error getting location', error);
    });
  } else {
    console.error("Geolocation is not supported by this browser.");
  }
}

// ユーザー状況を取得する関数
function getUserStatus() {
  fetch('/api/get-user-status')
    .then(response => response.json())
    .then(data => {
      if (data.user_status) {
        document.querySelector('.sub1').value = data.user_status;
      }
    })
    .catch(error => {
      console.error('Error fetching user status:', error);
    });
}

// ページ読み込み時にユーザー状況を取得
document.addEventListener('DOMContentLoaded', function() {
  getUserStatus();
  fetchUserStatus();
  var statusSelect = document.querySelector('.sub1');

  statusSelect.addEventListener('change', function() {
    var selectedStatus = this.value;
    updateUserStatus(selectedStatus);
  });

});

function updateUserStatus(status) {
  fetch('/api/update-user-status', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ status: status })
  })
  .then(response => response.json())
  .then(data => {
    console.log('Status update successful:', data);
    // アイコンを更新
    updateMarkerIcon(status);
  })
  .catch(error => {
    console.error('Error updating status:', error);
  });
}

document.querySelector('.sub1').addEventListener('change', function() {
  var selectedStatus = this.value;
  updateUserStatus(selectedStatus);
});

function fetchUserStatus() {
  fetch('/api/get-user-status')
    .then(response => response.json())
    .then(data => {
      if (data.user_status) {
        const statusSelect = document.querySelector('.sub1');
        statusSelect.value = data.user_status;

        // 「自分の状況」オプションを無効化
        const defaultOption = statusSelect.querySelector('option[value=""]');
        if (defaultOption) {
          defaultOption.disabled = true;
        }
      }
    })
    .catch(error => {
      console.error('Error fetching user status:', error);
    });
}

// 位置情報を更新するためのインターバル設定
setInterval(getLocationAndUpdate, 10000); // 10秒ごとに更新
