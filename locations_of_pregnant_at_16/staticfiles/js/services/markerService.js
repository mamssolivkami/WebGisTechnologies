class MarkerService {
    constructor(url) {
        this.url = url;
    }

    async getAll() {
        const response = await fetch(this.url);
        return response.json();
    }

    async getById(id) {
        const response = await fetch(`${this.url}/${id}/`);
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
        const response = await fetch(`${this.url}/${id}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
        });
        return response.json();
    }

    async put(object) {
        const response = await fetch(`${this.url}/${object.id}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify(object),
        });
        return response.json();
    }
}

export default new MarkerService('YOUR_API_URL'); // Замените 'YOUR_API_URL' на фактический URL вашего API
