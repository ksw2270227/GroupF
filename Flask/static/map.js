// Google Maps JavaScript API の初期化とマップ設定
var map;
var marker; // マーカーをグローバルに定義
var userLocation; // グローバル変数として定義
var selectedMemberLocation; // 選択されたメンバーの位置情報

function initMap() {
  // 緯度と経度の取得
  var latitude = parseFloat(document.getElementById('latitude').value);
  var longitude = parseFloat(document.getElementById('longitude').value);
  userLocation = new google.maps.LatLng(latitude, longitude);

  // Google Mapsの初期化
  map = new google.maps.Map(document.getElementById('map'), {
    center: userLocation,
    zoom: 16
  });

  fetchUserStatusAndSetMarker(userLocation);
  fetchGroupUsersAndSetMarkers();
}

document.addEventListener('DOMContentLoaded', function() {
  var createButton = document.querySelector('.create-button');
  if (createButton) {
    createButton.addEventListener('click', function() {
      if (selectedMemberLocation) {
        calculateRoute(userLocation, selectedMemberLocation);
      } else {
        alert('メンバーが選択されていません！');
      }
    });
  }
});

function fetchGroupUsersAndSetMarkers() {
  fetch('/api/get-group-users')
    .then(response => response.json())
    .then(data => {
        data.group_users.forEach(user => {
            var userLocation = new google.maps.LatLng(user[2], user[3]);
            var iconUrl = getIcon(user[0], user[4]);

            var memberMarker = new google.maps.Marker({
                position: userLocation,
                map: map,
                icon: iconUrl
            });

            memberMarker.addListener('click', function() {
              selectedMemberLocation = userLocation;
            });

            var infowindow = new google.maps.InfoWindow({
              content: user[1]
            });

            memberMarker.addListener('click', function() {
              infowindow.open(map, memberMarker);
            });
        });
    })
    .catch(error => {
        console.error('Error fetching group users:', error);
    });
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
    // map.setCenter(newLatLng);
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

function fetchGroupUsersAndSetMarkers() {
  fetch('/api/get-group-users')
    .then(response => response.json())
    .then(data => {
        data.group_users.forEach(user => {
            var userLocation = { lat: user[2], lng: user[3] };
            var iconUrl = getIcon(user[0], user[4]);

            var memberMarker = new google.maps.Marker({
                position: userLocation,
                map: map,
                icon: iconUrl
            });

            memberMarker.addListener('click', function() {
              selectedMemberLocation = userLocation;
              // 必要なUIの更新
            });

            var infowindow = new google.maps.InfoWindow({
              content: user[1]
            });

            memberMarker.addListener('click', function() {
              infowindow.open(map, memberMarker);
            });
        });
    })
    .catch(error => {
        console.error('Error fetching group users:', error);
    });
}

function onMemberPinClick(memberLocation) {
  selectedMemberLocation = memberLocation;
  // 必要に応じてUIの更新など
}

function calculateRoute(from, to) {
  var directionsService = new google.maps.DirectionsService();
  var directionsRenderer = new google.maps.DirectionsRenderer();
  directionsRenderer.setMap(map);

  var request = {
    origin: from,
    destination: to,
    travelMode: 'DRIVING'
  };

  directionsService.route(request, function(result, status) {
    if (status == 'OK') {
      directionsRenderer.setDirections(result);
    } else {
      console.error('Directions request failed due to ' + status);
    }
  });
}

// イベントリスナー内
createButton.addEventListener('click', function() {
  if (selectedMemberLocation && userLocation) {
    calculateRoute(userLocation, selectedMemberLocation);
  } else {
    console.error('Location not defined');
  }
});




// 位置情報を更新するためのインターバル設定
setInterval(getLocationAndUpdate, 10000); // 10秒ごとに更新

