document.addEventListener("DOMContentLoaded", function () {
  // 지도를 초기화하고 데이터를 가져오는 함수
  function initializeMap() {
    // API 호출
    axios.get("/api/maps/api/maps/")
      .then(function (response) {
        const places = response.data.places;
        if (places && places.length > 0) {
          // 지도를 초기화하고 첫 번째 장소를 표시
          const mapContainer = document.getElementById("map");
          const mapOptions = {
            center: new kakao.maps.LatLng(places[0].y, places[0].x), // 첫 번째 장소 좌표
            level: 3, // 지도 줌 레벨
          };
          const map = new kakao.maps.Map(mapContainer, mapOptions);

          // 모든 장소에 마커 추가
          places.forEach((place) => {
            const markerPosition = new kakao.maps.LatLng(place.y, place.x);
            const marker = new kakao.maps.Marker({
              position: markerPosition,
              map: map,
            });

            // 마커 클릭 시 장소 이름을 표시
            kakao.maps.event.addListener(marker, "click", function () {
              alert(place.place_name);
            });
          });
        } else {
          alert("지도 데이터를 불러올 수 없습니다.");
        }
      })
      .catch(function (error) {
        console.error("지도를 불러오는 중 오류 발생:", error);
        alert("지도를 불러오는 중 오류가 발생했습니다.");
      });
  }

  initializeMap(); // 페이지 로드 시 지도 초기화
});
