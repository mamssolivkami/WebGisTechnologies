class Service {
    constructor(url) {
        this.url = url;
    }

    async Get() {
        try {
            const response = await fetch(this.url);
            return await response.json();
        } catch (error) {
            console.error('Ошибка получения данных:', error);
        }
    }

    async GetById(id) {
        try {
            const response = await fetch(`${this.url}/${id}`);
            return await response.json();
        } catch (error) {
            console.error(`Ошибка получения данных по id ${id}:`, error);
        }
    }

    async Post(object) {
        try {
            const response = await fetch(this.url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(object)
            });
            return await response.json();
        } catch (error) {
            console.error('Ошибка создания:', error);
        }
    }

    async Remove(id) {
        try {
            const response = await fetch(`${this.url}/${id}`, {
                method: 'DELETE'
            });
            return await response.json();
        } catch (error) {
            console.error(`Ошибка удаления объекта с id ${id}:`, error);
        }
    }

    async Put(id, object) {
        try {
            const response = await fetch(`${this.url}/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(object)
            });
            return await response.json();
        } catch (error) {
            console.error('Ошибка обновления:', error);
        }
    }
}

export default Service;
