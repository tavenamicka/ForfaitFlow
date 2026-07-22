<script setup>
import { onMounted } from "vue";
import { useAlertesStore } from "../stores/alertes";
import AppHeader from "../components/AppHeader.vue";

const alertesStore = useAlertesStore();

const niveauBadge = {
  N1: "bg-blue-100 text-blue-800",
  N2: "bg-teal-100 text-teal-800",
};

onMounted(() => alertesStore.fetchAlertes());
</script>

<template>
  <div class="min-h-screen bg-forfait-50">
    <AppHeader />

    <div class="p-6 max-w-3xl mx-auto space-y-6">
      <h1 class="text-2xl font-bold text-forfait-800">Alertes actives</h1>
      <p class="text-sm text-gray-500">
        Clients ayant atteint au moins 80% de leur forfait N1 ou N2 sur la période courante.
      </p>

      <div class="bg-white rounded-lg shadow-sm overflow-x-auto">
        <table class="min-w-full text-sm">
          <thead class="bg-gray-50 text-left text-gray-500">
            <tr>
              <th class="px-4 py-3">Client</th>
              <th class="px-4 py-3">Niveau</th>
              <th class="px-4 py-3">Consommation</th>
              <th class="px-4 py-3"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="a in alertesStore.alertes" :key="`${a.client_id}-${a.niveau}`" class="border-t">
              <td class="px-4 py-3 font-medium">{{ a.client_nom }}</td>
              <td class="px-4 py-3">
                <span class="px-2 py-1 rounded text-xs font-medium" :class="niveauBadge[a.niveau]">
                  {{ a.niveau }}
                </span>
              </td>
              <td class="px-4 py-3">
                <span :class="a.pourcentage > 100 ? 'text-red-700 font-semibold' : 'text-orange-600 font-semibold'">
                  {{ a.pourcentage }}%
                </span>
              </td>
              <td class="px-4 py-3 text-right">
                <router-link
                  :to="`/clients/${a.client_id}`"
                  class="text-forfait-600 hover:text-forfait-800"
                >
                  Voir la fiche
                </router-link>
              </td>
            </tr>
            <tr v-if="!alertesStore.alertes.length">
              <td colspan="4" class="px-4 py-6 text-center text-gray-500">
                Aucune alerte active — tous les clients sont sous le seuil de 80%.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
