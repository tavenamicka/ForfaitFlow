<script setup>
import { computed, onMounted } from "vue";
import { useClientsStore } from "../stores/clients";
import AppHeader from "../components/AppHeader.vue";
import CarteClient from "../components/CarteClient.vue";

const clientsStore = useClientsStore();

const clientsActifs = computed(() => clientsStore.clients.filter((c) => c.actif));

const dashboardsCharges = computed(() =>
  clientsActifs.value.map((c) => clientsStore.dashboards[c.id]).filter(Boolean)
);

onMounted(async () => {
  await clientsStore.fetchClients();
  await clientsStore.fetchDashboards(clientsActifs.value.map((c) => c.id));
});
</script>

<template>
  <div class="min-h-screen bg-forfait-50">
    <AppHeader />
    <main class="p-6">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <CarteClient v-for="dashboard in dashboardsCharges" :key="dashboard.client_id" :dashboard="dashboard" />
      </div>
      <p v-if="!clientsActifs.length" class="text-gray-500 text-center py-12">
        Aucun client actif. Ajoutez-en un depuis la page Clients.
      </p>
    </main>
  </div>
</template>
