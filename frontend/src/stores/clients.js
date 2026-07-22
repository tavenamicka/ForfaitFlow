import { defineStore } from "pinia";
import http from "../api/http";

export const useClientsStore = defineStore("clients", {
  state: () => ({
    clients: [],
    dashboards: {},
  }),

  actions: {
    async fetchClients() {
      const { data } = await http.get("/clients");
      this.clients = data;
    },

    async fetchClient(id) {
      const { data } = await http.get(`/clients/${id}`);
      return data;
    },

    async fetchDashboard(clientId) {
      const { data } = await http.get(`/clients/${clientId}/dashboard`);
      this.dashboards[clientId] = data;
    },

    async fetchDashboards(clientIds) {
      await Promise.all(clientIds.map((id) => this.fetchDashboard(id)));
    },

    async fetchRapport(clientId, periode = "courante") {
      const { data } = await http.get(`/rapports/${clientId}`, { params: { periode } });
      return data;
    },

    async fetchPeriodes(clientId) {
      const { data } = await http.get(`/clients/${clientId}/periodes`);
      return data;
    },

    async createClient(payload) {
      await http.post("/clients", payload);
      await this.fetchClients();
    },

    async updateClient(id, payload) {
      await http.patch(`/clients/${id}`, payload);
      await this.fetchClients();
    },

    async archiveClient(id) {
      await http.post(`/clients/${id}/archiver`);
      await this.fetchClients();
    },
  },
});
