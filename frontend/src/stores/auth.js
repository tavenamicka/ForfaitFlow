import { defineStore } from "pinia";
import http from "../api/http";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: localStorage.getItem("forfaitflow_token") || null,
    user: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
  },

  actions: {
    async login(email, password) {
      const { data } = await http.post("/auth/login", { email, password });
      this.token = data.access_token;
      localStorage.setItem("forfaitflow_token", this.token);
      await this.fetchMe();
    },

    async fetchMe() {
      const { data } = await http.get("/auth/me");
      this.user = data;
    },

    logout() {
      this.token = null;
      this.user = null;
      localStorage.removeItem("forfaitflow_token");
    },
  },
});
