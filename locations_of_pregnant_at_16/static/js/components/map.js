import markerService from '../services/markerService.js';

export function initMap() {
    const map = L.map('map').setView([55.751244, 37.618423], 5);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    
    loadMarkers(map);
}

async function loadMarkers(map) {

   
    let markersData = await markerService.getAll();
    markersData.forEach(marker => {
        const childrenCount = marker.children_names.length;
        const childrenLabel = childrenCount === 1 ? "Ребенок: " : "Дети: ";
        const childrenInfo = childrenCount > 0 ? childrenLabel + marker.children_names.join(', ') : "Нет детей";

        const fatherInfo = marker.father_name ?
            `Отец: ${marker.father_name} ${marker.father_age} лет<br>` +
            (marker.father_photo ? `<img src='${marker.father_photo}' alt='Фото отца' style='width: 100px; height: auto;'>` : "Нет фото") :
            "Нет информации об отце";

        const markerPopup = L.marker([marker.latitude, marker.longitude]).addTo(map)
            .bindPopup("<b>Сезон " + marker.season_number + ", Выпуск " + marker.episode_number + "</b><br>" +
                (marker.heroine_photo ? `<img src='${marker.heroine_photo}' alt='Фото героини' style='width: 100px; height: auto;'>` : "Нет фото") +
                "<br>" +
                "Мама: " + marker.heroine_name + " " + marker.heroine_age + " лет<br>" +
                childrenInfo + "<br>" +
                fatherInfo + "<br>" +
                "Дата создания метки: " + marker.date_of_creation + "<br>" +
                "Координаты: " + marker.latitude + ", " + marker.longitude + "<br>" +
                `<button onclick='deleteMarker(${marker.id_marker})'>Удалить метку</button>` +
                `<button onclick='editMarker(${marker.id_marker}, ${marker.latitude}, ${marker.longitude})'>Редактировать метку</button>`);
    });
}