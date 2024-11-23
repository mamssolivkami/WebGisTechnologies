import { initMap } from './components/map.js';
import { initChildForms } from './services/childForms.js';

document.addEventListener('DOMContentLoaded', () => {
    if (window.location.pathname === '/map/') {
        initMap();
    }

    if (window.location.pathname === '/create_marker/') {
        initChildForms();    
    }
});
