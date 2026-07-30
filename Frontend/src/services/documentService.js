import api from "../api/api";

const documentService = {

    async getDocuments() {

        const response = await api.get("/documents");

        return response.data;

    },

    async getDocument(id) {

        const response = await api.get(`/documents/${id}`);

        return response.data;

    },

    async deleteDocument(id) {

        const response = await api.delete(`/documents/${id}`);

        return response.data;

    }

};

export default documentService;