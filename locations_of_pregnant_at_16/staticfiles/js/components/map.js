import markerService from '../services/markerService.js';
import { getCookie } from '../components/cookie.js';

let map;

export function initMap() {
    map = L.map('map').setView([56.015, 92.87], 12);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    loadMarkers(map);
}

async function loadMarkers() {

    console.log('я инициализировался1')
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
                `<button onclick='editMarker(${marker.id_marker})'>Редактировать метку</button>`);
    });
}

export function deleteMarker(id) {
    markerService.remove(id).then(() => {
        map.eachLayer(layer => {
            if (layer.options.id === id) {
                map.removeLayer(layer);
            }
        });
        window.location.reload();
    });
}

window.deleteMarker = deleteMarker;

export async function editMarker(markerId) {
    const markerData = await markerService.getById(markerId);
    console.log("ID маркера:", markerId);

    let childrenFields = '';
    if (markerData.children.data.length > 0) {
        markerData.children.data.forEach((child, index) => {
            childrenFields += `
                <label>${markerData.children.label} ${index + 1}:</label>
                <input type="text" name="child_name_${index}" value="${child.child_name}"><br>
            `;
        });
    } else {
        childrenFields = `<p>Нет детей</p>`;
    }

    const formHtml = `
        <form id="edit-marker-form">
            <label>Сезон:</label><input type="number" name="season_number" value="${markerData.marker.season_number}"><br>
            <label>Выпуск:</label><input type="number" name="episode_number" value="${markerData.marker.episode_number}"><br>
            <label>Город:</label><input type="text" name="city" value="${markerData.marker.city}"><br>
            <label>Широта:</label><input type="text" name="latitude" value="${markerData.marker.latitude}"><br>
            <label>Долгота:</label><input type="text" name="longitude" value="${markerData.marker.longitude}"><br>
            <label>Имя героини:</label><input type="text" name="heroine_name" value="${markerData.heroine.heroine_name}"><br>
            <label>Возраст героини:</label><input type="number" name="heroine_age" value="${markerData.heroine.heroine_age}"><br>
            <label>Имя отца:</label><input type="text" name="father_name" value="${markerData.father?.father_name || ''}"><br>
            <label>Возраст отца:</label><input type="number" name="father_age" value="${markerData.father?.father_age || ''}"><br>
            ${childrenFields}
            <button type="submit">Сохранить</button>
        </form>
    `;

    const popup = L.popup()
        .setLatLng([markerData.marker.latitude, markerData.marker.longitude])
        .setContent(formHtml)
        .openOn(map);

    const form = document.getElementById("edit-marker-form");
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
    
        const formData = new FormData(form);
        const object = {};
    
        // Собираем данные для основной части формы
        object.season_number = formData.get("season_number");
        object.episode_number = formData.get("episode_number");
        object.city = formData.get("city");
        object.latitude = formData.get("latitude");
        object.longitude = formData.get("longitude");
    
        // Данные героини
        object.heroine = {
            heroine_name: formData.get("heroine_name"),
            heroine_age: parseInt(formData.get("heroine_age"), 10),
        };
    
        // Данные отца
        object.father = {
            father_name: formData.get("father_name") || null,
            father_age: formData.get("father_age") ? parseInt(formData.get("father_age"), 10) : null,
        };
    
        // Данные детей
        object.children = [];
        markerData.children.data.forEach((child, index) => {
            const childName = formData.get(`child_name_${index}`);
            if (childName) {
                object.children.push({
                    id: child.id || null,
                    child_name: childName,
                });
            }
        });
    
        // Отправка данных через метод `put` сервиса
        try {
            const response = await markerService.put(object);
            console.log(object);
            if (response.message) {
                alert(response.message);
                map.closePopup();
                loadMarkers();
            } else {
                console.error(response.errors);
                alert("Ошибка при обновлении маркера!");
            }
        } catch (error) {
            console.error("Ошибка:", error);
            alert("Не удалось сохранить изменения.");
        }
    });    
}

window.editMarker = editMarker;
