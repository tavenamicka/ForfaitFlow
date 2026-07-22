<script setup>
import { computed, onMounted } from "vue";
import { useAuthStore } from "../stores/auth";
import { useClientsStore } from "../stores/clients";
import { useRouter } from "vue-router";
import CarteClient from "../components/CarteClient.vue";

const auth = useAuthStore();
const clientsStore = useClientsStore();
const router = useRouter();

const clientsActifs = computed(() => clientsStore.clients.filter((c) => c.actif));

const dashboardsCharges = computed(() =>
  clientsActifs.value.map((c) => clientsStore.dashboards[c.id]).filter(Boolean)
);

onMounted(async () => {
  await clientsStore.fetchClients();
  await clientsStore.fetchDashboards(clientsActifs.value.map((c) => c.id));
});

function onLogout() {
  auth.logout();
  router.push("/login");
}
</script>

<template>
  <div class="min-h-screen bg-forfait-50">
    <header class="bg-white shadow-sm flex items-center justify-between px-6 py-4">
      <div class="flex items-center gap-6">
        <h1 class="text-xl font-bold text-forfait-800">ForfaitFlow</h1>
        <router-link to="/clients" class="text-sm text-forfait-600 hover:text-forfait-800 font-medium">
          Clients
        </router-link>
        <router-link
          to="/interventions/nouvelle"
          class="text-sm text-forfait-600 hover:text-forfait-800 font-medium"
        >
          Nouvelle intervention
        </router-link>
        <router-link to="/alertes" class="text-sm text-forfait-600 hover:text-forfait-800 font-medium">
          Alertes
        </router-link>
      </div>
      <div class="flex items-center gap-4">
        <span class="text-sm text-gray-600">{{ auth.user?.email }}</span>
        <button
          @click="onLogout"
          class="text-sm text-forfait-600 hover:text-forfait-800 font-medium"
        >
          Déconnexion
        </button>
      </div>
    </header>
    <main class="p-6">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <CarteClient v-for="dashboard in dashboardsCharges" :key="dashboard.client_id" :dashboard="dashboard" />
      </div>
      <p v-if="!clientsActifs.length" class="text-gray-400 text-center py-12">
        Aucun client actif. Ajoutez-en un depuis la page Clients.
      </p>
    </main>
  </div>
</template>
