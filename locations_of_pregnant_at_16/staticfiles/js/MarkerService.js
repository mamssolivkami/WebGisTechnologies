import Service from './Service.js';

class MarkerService extends Service {
    constructor() {
        super('/map'); // URL для работы с метками
    }

    async deleteMarker(markerId) {
        return await this.Remove(`delete_marker/${markerId}`);
    }

    async editMarker(markerId) {
        return await this.GetById(`edit_marker/${markerId}`);
    }
}

export default new MarkerService();
