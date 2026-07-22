import { defineStore } from "pinia";
import http from "../api/http";

export const useAlertesStore = defineStore("alertes", {
  state: () => ({
    alertes: [],
  }),

  actions: {
    async fetchAlertes() {
      const { data } = await http.get("/alertes");
      this.alertes = data;
    },
  },
});
