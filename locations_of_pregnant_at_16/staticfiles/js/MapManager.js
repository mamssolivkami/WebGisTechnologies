import L from 'leaflet';


export default class MapManager {
    constructor(mapData) {
        this.map = L.map('map').setView([55.751244, 37.618423], 5);
        this.initMap();
        this.loadMarkers(mapData);
    }

    initMap() {
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap contributors'
        }).addTo(this.map);
    }

    loadMarkers(markers) {
        markers.forEach(marker => this.createMarker(marker));
    }

    createMarker(marker) {
        const popupContent = `<b>Сезон ${marker.season_number}, Выпуск ${marker.episode_number}</b><br>` +
            `Мама: ${marker.heroine_name} ${marker.heroine_age} лет<br>` +
            `<button onclick='MarkerService.deleteMarker(${marker.id_marker})'>Удалить метку</button>` +
            `<button onclick='MarkerService.editMarker(${marker.id_marker})'>Редактировать метку</button>`;

        L.marker([marker.latitude, marker.longitude]).addTo(this.map)
            .bindPopup(popupContent);
    }
}
