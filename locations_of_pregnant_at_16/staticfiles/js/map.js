let map = L.map('map').setView([55.751244, 37.618423], 5);

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

    let markerPopup = L.marker([marker.latitude, marker.longitude]).addTo(map)
        .bindPopup("<b>Сезон " + marker.season_number + ", Выпуск " + marker.episode_number + "</b><br>" +
            (marker.heroine_photo ? "<img src='" + marker.heroine_photo + "' alt='Фото героини' style='width: 100px; height: auto;'>" : "Нет фото") +
            "<br>" +
            "Мама: " + marker.heroine_name + " " + marker.heroine_age + " лет<br>" +
            childrenInfo + "<br>" +
            fatherInfo + "<br>" +
            "Дата создания метки: " + marker.date_of_creation + "<br>" +
            "Координаты: " + marker.latitude + ", " + marker.longitude + "<br>" +
            "<button onclick='deleteMarker(" + marker.id_marker + ")'>Удалить метку</button>" +
            "<button onclick='editMarker(" + marker.id_marker + ", " + marker.latitude + ", " + marker.longitude + ")'>Редактировать метку</button>");
});

function deleteMarker(markerId) {
    if (confirm("Вы уверены, что хотите удалить эту метку?")) {
        fetch(`/map/delete_marker/${markerId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 'marker_id': markerId })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Метка удалена успешно.');
                    location.reload();
                } else {
                    alert(data.error || 'Ошибка удаления метки');
                }
            });
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();

            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function editMarker(markerId, latitude, longitude) {
    fetch(`/map/edit_marker/${markerId}/`)
        .then(response => response.text())
        .then(data => {
            let popupContent = L.popup()
                .setLatLng([latitude, longitude]) 
                .setContent(data)
                .openOn(map);
        })
        .catch(error => console.error('Ошибка при получении данных для редактирования:', error));
}

document.addEventListener('DOMContentLoaded', function() {
    let addChildButton = document.getElementById('add-child');
    let totalForms = document.getElementById('id_child_set-TOTAL_FORMS');
    let childrenContainer = document.getElementById('children-container');
    let emptyFormTemplate = document.getElementById('empty-form-template').innerHTML;

    addChildButton.addEventListener('click', function() {
        let formIndex = parseInt(totalForms.value); 

        let newForm = document.createElement('div');
        newForm.innerHTML = emptyFormTemplate.replace(/__prefix__/g, formIndex); 

        let removeButton = newForm.querySelector('.remove-child');
        removeButton.addEventListener('click', function() {
            childrenContainer.removeChild(newForm);
            totalForms.value = parseInt(totalForms.value) - 1;
            updateFormIndexes(); 
        });

        childrenContainer.appendChild(newForm);
        totalForms.value = formIndex + 1;
    });

    function updateFormIndexes() {
        let forms = document.querySelectorAll('.child-form');
        forms.forEach((form, index) => {
            form.querySelectorAll('input, select, textarea').forEach(function(input) {
                let name = input.name.replace(/child_set-\d+/, `child_set-${index}`);
                let id = input.id.replace(/id_child_set-\d+/, `id_child_set-${index}`);
                input.name = name;
                input.id = id;
            });
        });
    }
});
