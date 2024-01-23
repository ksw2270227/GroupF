// map.js
// Google Maps JavaScript API の初期化とマップ設定
var map;
var marker;

function initMap() {
  var latitude = parseFloat(document.getElementById('latitude').value);
  var longitude = parseFloat(document.getElementById('longitude').value);

  var userLocation = {lat: latitude, lng: longitude};

  map = new google.maps.Map(document.getElementById('map'), {
    center: userLocation,
    zoom: 16
  });

  // マーカーをグローバル変数に割り当てる
  marker = new google.maps.Marker({
    position: userLocation,
    map: map
  });
}



function updateMarkerPosition(latitude, longitude) {
  var newLatLng = new google.maps.LatLng(latitude, longitude);
  marker.setPosition(newLatLng);
  map.setCenter(newLatLng);
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
              // マーカーの位置を更新
              updateMarkerPosition(position.coords.latitude, position.coords.longitude);
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


// 5分ごとに位置情報を更新するためのインターバル設定
setInterval(getLocationAndUpdate, 10000); // 300000ミリ秒 = 5分
