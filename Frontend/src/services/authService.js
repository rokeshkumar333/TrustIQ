import api from "../api/api";
import { saveToken } from "../utils/auth";

const authService = {

    async login(data) {

        const response = await api.post("/login", data);

        if (response.data.token) {
            saveToken(response.data.token);
        }

        return response.data;
    },

    async register(data) {

        const response = await api.post("/register", data);

        return response.data;
    },

    logout() {

    localStorage.removeItem("token");

}

};

export default authService;