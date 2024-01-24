// Google Maps JavaScript API の初期化とマップ設定
var map;
var marker; // マーカーをグローバルに定義

function initMap() {
  // 緯度と経度の取得
  var latitude = parseFloat(document.getElementById('latitude').value);
  var longitude = parseFloat(document.getElementById('longitude').value);
  var userLocation = { lat: latitude, lng: longitude };

  // Google Mapsの初期化
  map = new google.maps.Map(document.getElementById('map'), {
    center: userLocation,
    zoom: 16
  });

  // サーバーからユーザーステータスを取得してマーカーを設定
  fetchUserStatusAndSetMarker(userLocation);

  fetchGroupUsersAndSetMarkers();
}

function fetchUserStatusAndSetMarker(userLocation) {
  fetch('/api/get-user-status')
    .then(response => response.json())
    .then(data => {
      if (data.user_status) {
        // 仮に現在のユーザーIDを 'currentUserId' と仮定
        var iconUrl = getIcon(currentUserId, data.user_status);

        // マーカーの設定
        marker = new google.maps.Marker({
          position: userLocation,
          map: map,
          icon: iconUrl
        });
      }
    })
    .catch(error => {
      console.error('Error fetching user status:', error);
      var iconUrl = getIcon('通常');
      marker = new google.maps.Marker({
        position: userLocation,
        map: map,
        icon: iconUrl
      });
    });
}


function getIcon(userId, userStatus) {
  var iconUrl = getIconUrl(userId, userStatus); // アイコンのURLを取得

  // アイコンサイズを設定
  var iconSize = new google.maps.Size(50, 50);
  return {
    url: iconUrl,
    scaledSize: iconSize // アイコンの表示サイズを設定
  };
}

function getIconUrl(userId, userStatus) {
  var iconBasePath = '/static/map/';
  var iconType = (userId == currentUserId) ? 'user' : 'member';
  // console.log("userId + ",userId," == ",currentUserId,"currentUserId")
  var iconFileName = iconType + '_' + userStatus + '.png';
  var fullPath = iconBasePath + iconFileName;
  console.log("Icon URL:", fullPath); // デバッグ情報
  return fullPath;
}

function updateMarkerPosition(latitude, longitude) {
  var newLatLng = new google.maps.LatLng(latitude, longitude);
  if (marker) {
    marker.setPosition(newLatLng);
    map.setCenter(newLatLng);
  }
}

function updateMarkerIcon(userId, userStatus) {
  if (marker) {
    var iconUrl = getIconUrl(userId, userStatus);
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
        // console.log('Location update successful:', data);
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
    updateUserStatus(currentUserId,selectedStatus);
  });

});

function updateUserStatus(user_id,status) {
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
    updateMarkerIcon(user_id,status);
  })
  .catch(error => {
    console.error('Error updating status:', error);
  });
}


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

//新しく追加した機能
function fetchGroupUsersAndSetMarkers() {
  fetch('/api/get-group-users')
      .then(response => response.json())
      .then(data => {
          console.log("API response:", data); // APIからの応答をログに出力
          data.group_users.forEach(user => {
              var userLocation = {
                  lat: user[2], // 緯度
                  lng: user[3]  // 経度
              };
              var iconUrl = getIcon(user[0], user[4]); // ユーザーIDとステータス

              var marker = new google.maps.Marker({
                  position: userLocation,
                  map: map,
                  icon: iconUrl,
                  title: user[1] // ユーザーの名前
              });
              console.log("Marker for user:", user[1], userLocation); // マーカー設定のログ
          });
      })
      .catch(error => {
          console.error('Error fetching group users:', error);
      });
}




// 位置情報を更新するためのインターバル設定
setInterval(getLocationAndUpdate, 10000); // 10秒ごとに更新
