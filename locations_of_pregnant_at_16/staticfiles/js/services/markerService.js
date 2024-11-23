import { getCookie } from '../components/cookie.js';

class MarkerService {
    constructor(url) {
        this.url = url;
    }

    async getAll() {
        const response = await fetch(this.url);
        const markersData = await response.json();
        return markersData;
    }

    async getById(id) {
        const response = await fetch(`${this.url}${id}/`);
        return response.json();
    }

    async post(object) {
        const response = await fetch(this.url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify(object),
        });
        return response.json();
    }

    async remove(id) {
        const response = await fetch(`${this.url}delete_marker/${id}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
        });
        return response.json();
    }

    async put(object) {
        const response = await fetch(`${this.url}edit_marker/${object.id}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify(object),
        });
        return response.json();
    }
}

export default new MarkerService('http://127.0.0.1:8000/map/markers/'); 
