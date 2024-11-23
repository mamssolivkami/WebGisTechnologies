import { initMap } from './components/map.js';
import { initChildForms } from './services/childForms.js';
import { getCookie } from './components/cookie.js';

document.addEventListener('DOMContentLoaded', () => {
    if (window.location.pathname === '/map/') {
        getCookie('csrftoken');
        initMap();
    }

    if (window.location.pathname === '/create_marker/') {
        initChildForms();    
    }
});
