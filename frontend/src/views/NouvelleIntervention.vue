<script setup>
import { reactive, ref, onMounted, computed } from "vue";
import { useClientsStore } from "../stores/clients";
import { useInterventionsStore } from "../stores/interventions";
import BlocNiveau from "../components/BlocNiveau.vue";

const clientsStore = useClientsStore();
const interventionsStore = useInterventionsStore();

const error = ref("");

function emptyBloc() {
  return { niveau: "N1", duree_minutes: 30, description: "" };
}

const form = reactive({
  client_id: "",
  date_intervention: new Date().toISOString().slice(0, 10),
  blocs: [emptyBloc()],
});

const niveauBadge = {
  N1: "bg-blue-100 text-blue-800",
  N2: "bg-teal-100 text-teal-800",
  N3: "bg-purple-100 text-purple-800",
};

const clientsActifs = computed(() => clientsStore.clients.filter((c) => c.actif));

function nomClient(clientId) {
  return clientsStore.clients.find((c) => c.id === clientId)?.nom || `#${clientId}`;
}

function formatDuree(minutes) {
  const h = Math.floor(minutes / 60);
  const m = minutes % 60;
  return `${h}:${String(m).padStart(2, "0")}`;
}

function addBloc() {
  form.blocs.push(emptyBloc());
}

function removeBloc(index) {
  form.blocs.splice(index, 1);
}

onMounted(async () => {
  await clientsStore.fetchClients();
  await interventionsStore.fetchInterventions();
});

async function onSubmit() {
  error.value = "";
  try {
    await interventionsStore.createIntervention({
      client_id: Number(form.client_id),
      date_intervention: form.date_intervention,
      blocs: form.blocs,
    });
    await interventionsStore.fetchInterventions();
    form.blocs = [emptyBloc()];
  } catch {
    error.value = "Erreur lors de l'enregistrement de l'intervention.";
  }
}

async function onDelete(id) {
  if (confirm("Supprimer cette intervention ?")) {
    await interventionsStore.deleteIntervention(id);
    await interventionsStore.fetchInterventions();
  }
}
</script>

<template>
  <div class="min-h-screen bg-forfait-50">
    <header class="bg-white shadow-sm flex items-center gap-6 px-6 py-4">
      <router-link to="/" class="text-xl font-bold text-forfait-800">ForfaitFlow</router-link>
      <router-link to="/clients" class="text-sm text-gray-600 hover:text-forfait-800">Clients</router-link>
      <router-link to="/interventions/nouvelle" class="text-sm text-forfait-800 font-medium">
        Nouvelle intervention
      </router-link>
      <router-link to="/alertes" class="text-sm text-gray-600 hover:text-forfait-800">Alertes</router-link>
    </header>

    <div class="p-6 max-w-3xl mx-auto space-y-6">
      <form @submit.prevent="onSubmit" class="bg-white rounded-lg shadow-sm p-6 space-y-4">
        <h1 class="text-xl font-bold text-forfait-800">Nouvelle intervention</h1>

        <div>
          <label class="block text-sm font-medium text-gray-700">Client</label>
          <select v-model="form.client_id" required class="mt-1 w-full rounded border-gray-300">
            <option value="" disabled>Sélectionner un client</option>
            <option v-for="c in clientsActifs" :key="c.id" :value="c.id">{{ c.nom }}</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700">Date</label>
          <input
            v-model="form.date_intervention"
            type="date"
            required
            class="mt-1 w-full rounded border-gray-300"
          />
        </div>

        <BlocNiveau
          v-for="(bloc, index) in form.blocs"
          :key="index"
          v-model="form.blocs[index]"
          :index="index"
          :removable="form.blocs.length > 1"
          @remove="removeBloc(index)"
        />

        <button
          type="button"
          @click="addBloc"
          class="text-sm text-forfait-600 hover:text-forfait-800 font-medium"
        >
          + Ajouter un bloc (split)
        </button>

        <p v-if="error" class="text-sm text-red-600">{{ error }}</p>

        <div>
          <button
            type="submit"
            class="bg-forfait-600 text-white px-4 py-2 rounded font-medium hover:bg-forfait-800"
          >
            Enregistrer
          </button>
        </div>
      </form>

      <div class="bg-white rounded-lg shadow-sm overflow-x-auto">
        <table class="min-w-full text-sm">
          <thead class="bg-gray-50 text-left text-gray-500">
            <tr>
              <th class="px-4 py-3">Date</th>
              <th class="px-4 py-3">Client</th>
              <th class="px-4 py-3">Niveau</th>
              <th class="px-4 py-3">Durée</th>
              <th class="px-4 py-3">Description</th>
              <th class="px-4 py-3"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="i in interventionsStore.interventions" :key="i.id" class="border-t">
              <td class="px-4 py-3">{{ i.date_intervention }}</td>
              <td class="px-4 py-3">{{ nomClient(i.client_id) }}</td>
              <td class="px-4 py-3">
                <span class="px-2 py-1 rounded text-xs font-medium" :class="niveauBadge[i.niveau]">
                  {{ i.niveau }}
                </span>
                <span
                  v-if="i.groupe_id"
                  title="Fait partie d'une intervention splittée sur plusieurs niveaux"
                  class="ml-1 text-xs text-gray-400"
                >
                  🔗
                </span>
              </td>
              <td class="px-4 py-3">{{ formatDuree(i.duree_minutes) }}</td>
              <td class="px-4 py-3 max-w-xs truncate" :title="i.description">{{ i.description }}</td>
              <td class="px-4 py-3 text-right">
                <button @click="onDelete(i.id)" class="text-red-600 hover:text-red-800">
                  Supprimer
                </button>
              </td>
            </tr>
            <tr v-if="!interventionsStore.interventions.length">
              <td colspan="6" class="px-4 py-6 text-center text-gray-400">Aucune intervention.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
