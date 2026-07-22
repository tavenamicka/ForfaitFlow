<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import { useClientsStore } from "../stores/clients";
import { useInterventionsStore } from "../stores/interventions";
import RapportPeriode from "../components/RapportPeriode.vue";

const route = useRoute();
const clientId = Number(route.params.id);

const clientsStore = useClientsStore();
const interventionsStore = useInterventionsStore();

const client = ref(null);
const periodes = ref([]);
const selectedPeriodeId = ref(null);
const rapport = ref(null);

const moisNoms = [
  "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
  "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre",
];

function labelPeriode(periodeId) {
  const [annee, mois] = periodeId.split("-").map(Number);
  return `${moisNoms[mois - 1]} ${annee}`;
}

async function loadPeriode() {
  rapport.value = await clientsStore.fetchRapport(clientId, selectedPeriodeId.value);
}

async function load() {
  client.value = await clientsStore.fetchClient(clientId);
  periodes.value = await clientsStore.fetchPeriodes(clientId);
  if (periodes.value.length) {
    selectedPeriodeId.value = periodes.value[0].periode_id;
    await loadPeriode();
  }
}

onMounted(load);

async function onSaveIntervention({ id, payload }) {
  await interventionsStore.updateIntervention(id, payload);
  await loadPeriode();
}
</script>

<template>
  <div class="min-h-screen bg-forfait-50">
    <header class="bg-white shadow-sm flex items-center gap-6 px-6 py-4">
      <router-link to="/" class="text-xl font-bold text-forfait-800">ForfaitFlow</router-link>
      <router-link to="/clients" class="text-sm text-gray-600 hover:text-forfait-800">Clients</router-link>
      <router-link to="/interventions/nouvelle" class="text-sm text-gray-600 hover:text-forfait-800">
        Nouvelle intervention
      </router-link>
      <router-link to="/alertes" class="text-sm text-gray-600 hover:text-forfait-800">Alertes</router-link>
    </header>

    <div v-if="client" class="p-6 max-w-5xl mx-auto space-y-6">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-forfait-800">Historique — {{ client.nom }}</h1>
          <router-link :to="`/clients/${clientId}`" class="text-sm text-forfait-600 hover:text-forfait-800">
            Retour à la fiche client
          </router-link>
        </div>
        <select
          v-if="periodes.length"
          v-model="selectedPeriodeId"
          @change="loadPeriode"
          class="rounded border-gray-300"
        >
          <option v-for="p in periodes" :key="p.periode_id" :value="p.periode_id">
            {{ labelPeriode(p.periode_id) }}
          </option>
        </select>
      </div>

      <p v-if="!periodes.length" class="text-gray-400 text-center py-12">
        Aucune période passée pour ce client — l'historique apparaîtra après le premier renouvellement mensuel.
      </p>

      <RapportPeriode v-else-if="rapport" :rapport="rapport" @save-intervention="onSaveIntervention" />
    </div>
  </div>
</template>
