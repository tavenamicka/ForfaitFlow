import { defineStore } from "pinia";
import http from "../api/http";

export const useInterventionsStore = defineStore("interventions", {
  state: () => ({
    interventions: [],
  }),

  actions: {
    async fetchInterventions(params = {}) {
      const { data } = await http.get("/interventions", { params });
      this.interventions = data;
    },

    async createIntervention(payload) {
      await http.post("/interventions", payload);
    },

    async updateIntervention(id, payload) {
      await http.patch(`/interventions/${id}`, payload);
    },

    async deleteIntervention(id) {
      await http.delete(`/interventions/${id}`);
    },
  },
});
