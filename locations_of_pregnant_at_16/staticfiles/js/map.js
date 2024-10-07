let map = L.map('map').setView([55.751244, 37.618423], 5);  // Центр карты

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

let markers = JSON.parse(markersData); 

markers.forEach(function (marker) {
    let childrenCount = marker.children_names.length;
    let childrenLabel = childrenCount === 1 ? "Ребенок: " : "Дети: ";
    let childrenInfo = childrenCount > 0 ? childrenLabel + marker.children_names.join(', ') : "Нет детей";

    let fatherInfo = marker.father_name ?
        "Отец: " + marker.father_name + " " + marker.father_age + " лет<br>" +
        (marker.father_photo ? "<img src='" + marker.father_photo + "' alt='Фото отца' style='width: 100px; height: auto;'>" : "Нет фото") :
        "Нет информации об отце";

    L.marker([marker.latitude, marker.longitude]).addTo(map)
        .bindPopup("<b>Сезон " + marker.season_number + ", Выпуск " + marker.episode_number + "</b><br>" +
            (marker.heroine_photo ? "<img src='" + marker.heroine_photo + "' alt='Фото героини' style='width: 100px; height: auto;'>" : "Нет фото") + // Добавление фото героини
            "<br>" +
            "Мама: " + marker.heroine_name + " " + marker.heroine_age + " лет<br>" +
            childrenInfo + "<br>" +
            fatherInfo + "<br>" +
            "Дата создания метки: " + marker.date_of_creation + "<br>");
});
