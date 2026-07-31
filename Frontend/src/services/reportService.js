import api from "../api/api";

const reportService = {
    async getReport(id) {
        const response = await api.get(`/reports/${id}`);
        return response.data;
    },
};

export default reportService;
