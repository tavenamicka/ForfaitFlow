<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import { useClientsStore } from "../stores/clients";
import { useInterventionsStore } from "../stores/interventions";
import RapportPeriode from "../components/RapportPeriode.vue";
import AppHeader from "../components/AppHeader.vue";
import http from "../api/http";

const route = useRoute();
const clientId = Number(route.params.id);

const clientsStore = useClientsStore();
const interventionsStore = useInterventionsStore();

const client = ref(null);
const rapport = ref(null);

async function load() {
  client.value = await clientsStore.fetchClient(clientId);
  rapport.value = await clientsStore.fetchRapport(clientId, "courante");
}

onMounted(load);

async function onSaveIntervention({ id, payload }) {
  await interventionsStore.updateIntervention(id, payload);
  await load();
}

const downloading = ref(null);

async function downloadRapport(format) {
  downloading.value = format;
  try {
    const response = await http.get(`/rapports/${clientId}/${format}`, {
      params: { periode: "courante" },
      responseType: "blob",
    });
    const url = URL.createObjectURL(response.data);
    const a = document.createElement("a");
    a.href = url;
    a.download = `rapport_${client.value.nom}_${rapport.value.periode_debut}.${format}`;
    a.click();
    URL.revokeObjectURL(url);
  } finally {
    downloading.value = null;
  }
}
</script>

<template>
  <div class="min-h-screen bg-forfait-50">
    <AppHeader />

    <div v-if="client && rapport" class="p-6 max-w-5xl mx-auto space-y-6">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-forfait-800">{{ client.nom }}</h1>
          <router-link
            :to="`/clients/${clientId}/historique`"
            class="text-sm text-forfait-600 hover:text-forfait-800"
          >
            Voir l'historique des périodes
          </router-link>
        </div>
        <div class="space-x-2">
          <button
            :disabled="downloading !== null"
            @click="downloadRapport('pdf')"
            class="px-4 py-2 rounded border border-forfait-600 text-forfait-600 hover:bg-forfait-50 disabled:opacity-50"
          >
            {{ downloading === "pdf" ? "Génération..." : "Export PDF" }}
          </button>
          <button
            :disabled="downloading !== null"
            @click="downloadRapport('xlsx')"
            class="px-4 py-2 rounded border border-forfait-600 text-forfait-600 hover:bg-forfait-50 disabled:opacity-50"
          >
            {{ downloading === "xlsx" ? "Génération..." : "Export Excel" }}
          </button>
        </div>
      </div>

      <RapportPeriode :rapport="rapport" @save-intervention="onSaveIntervention" />
    </div>
  </div>
</template>
