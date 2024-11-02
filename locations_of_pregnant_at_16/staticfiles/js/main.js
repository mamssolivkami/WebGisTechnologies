import ChildFormManager from './ChildFormManager.js';
import MapManager from './MapManager.js';
import markerService from './MarkerService.js';

// Данные меток (например, из шаблона)
const markersData = JSON.parse(document.getElementById('markers-data').textContent);

// Инициализация
document.addEventListener('DOMContentLoaded', () => {
    new ChildFormManager();
    new MapManager(markersData);
});
