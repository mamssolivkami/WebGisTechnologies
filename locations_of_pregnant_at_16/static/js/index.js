import { initChildForms } from './services/childForms.js';
import { initMap } from './components/map.js';

// Инициализация компонентов
document.addEventListener('DOMContentLoaded', () => {
    initChildForms();
    initMap();
    console.log('я инициализировался')
});
