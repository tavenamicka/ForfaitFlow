<script setup>
import { ref, reactive, onMounted } from "vue";
import { useClientsStore } from "../stores/clients";

const store = useClientsStore();
const showForm = ref(false);
const editingId = ref(null);
const error = ref("");

const emptyForm = () => ({
  nom: "",
  email: "",
  telephone: "",
  date_debut_contrat: "",
  forfait_n1_h: 4,
  forfait_n2_h: 3,
  notes: "",
});

const form = reactive(emptyForm());

onMounted(() => store.fetchClients());

function openCreate() {
  editingId.value = null;
  Object.assign(form, emptyForm());
  error.value = "";
  showForm.value = true;
}

function openEdit(client) {
  editingId.value = client.id;
  Object.assign(form, {
    nom: client.nom,
    email: client.email || "",
    telephone: client.telephone || "",
    date_debut_contrat: client.date_debut_contrat,
    forfait_n1_h: client.forfait_n1_h,
    forfait_n2_h: client.forfait_n2_h,
    notes: client.notes || "",
  });
  error.value = "";
  showForm.value = true;
}

async function onSubmit() {
  error.value = "";
  try {
    if (editingId.value) {
      await store.updateClient(editingId.value, form);
    } else {
      await store.createClient(form);
    }
    showForm.value = false;
  } catch {
    error.value = "Erreur lors de l'enregistrement du client.";
  }
}

async function onArchive(client) {
  if (confirm(`Archiver ${client.nom} ?`)) {
    await store.archiveClient(client.id);
  }
}
</script>

<template>
  <div class="min-h-screen bg-forfait-50">
    <header class="bg-white shadow-sm flex items-center gap-6 px-6 py-4">
      <router-link to="/" class="text-xl font-bold text-forfait-800">ForfaitFlow</router-link>
      <router-link to="/clients" class="text-sm text-forfait-800 font-medium">Clients</router-link>
      <router-link to="/interventions/nouvelle" class="text-sm text-gray-600 hover:text-forfait-800">
        Nouvelle intervention
      </router-link>
      <router-link to="/alertes" class="text-sm text-gray-600 hover:text-forfait-800">Alertes</router-link>
    </header>
    <div class="p-6">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-forfait-800">Gestion des clients</h1>
      <button
        @click="openCreate"
        class="bg-forfait-600 text-white px-4 py-2 rounded font-medium hover:bg-forfait-800"
      >
        + Nouveau client
      </button>
    </div>

    <div class="bg-white rounded-lg shadow-sm overflow-x-auto">
      <table class="min-w-full text-sm">
        <thead class="bg-gray-50 text-left text-gray-500">
          <tr>
            <th class="px-4 py-3">Nom</th>
            <th class="px-4 py-3">Contact</th>
            <th class="px-4 py-3">Début contrat</th>
            <th class="px-4 py-3">Forfait N1/N2</th>
            <th class="px-4 py-3">Statut</th>
            <th class="px-4 py-3"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="client in store.clients" :key="client.id" class="border-t">
            <td class="px-4 py-3 font-medium">
              <router-link :to="`/clients/${client.id}`" class="text-forfait-600 hover:text-forfait-800">
                {{ client.nom }}
              </router-link>
            </td>
            <td class="px-4 py-3 text-gray-500">
              <div>{{ client.email }}</div>
              <div>{{ client.telephone }}</div>
            </td>
            <td class="px-4 py-3">{{ client.date_debut_contrat }}</td>
            <td class="px-4 py-3">{{ client.forfait_n1_h }}h / {{ client.forfait_n2_h }}h</td>
            <td class="px-4 py-3">
              <span
                class="px-2 py-1 rounded text-xs font-medium"
                :class="client.actif ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-600'"
              >
                {{ client.actif ? "Actif" : "Archivé" }}
              </span>
            </td>
            <td class="px-4 py-3 text-right space-x-3">
              <button @click="openEdit(client)" class="text-forfait-600 hover:text-forfait-800">
                Éditer
              </button>
              <button
                v-if="client.actif"
                @click="onArchive(client)"
                class="text-red-600 hover:text-red-800"
              >
                Archiver
              </button>
            </td>
          </tr>
          <tr v-if="!store.clients.length">
            <td colspan="6" class="px-4 py-6 text-center text-gray-400">Aucun client.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div
      v-if="showForm"
      class="fixed inset-0 bg-black/40 flex items-center justify-center p-4"
      @click.self="showForm = false"
    >
      <form
        @submit.prevent="onSubmit"
        class="bg-white rounded-lg shadow-md w-full max-w-md p-6 space-y-4"
      >
        <h2 class="text-lg font-bold text-forfait-800">
          {{ editingId ? "Éditer le client" : "Nouveau client" }}
        </h2>

        <div>
          <label class="block text-sm font-medium text-gray-700">Nom</label>
          <input v-model="form.nom" required class="mt-1 w-full rounded border-gray-300" />
        </div>

        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-sm font-medium text-gray-700">Email</label>
            <input v-model="form.email" type="email" class="mt-1 w-full rounded border-gray-300" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Téléphone</label>
            <input v-model="form.telephone" class="mt-1 w-full rounded border-gray-300" />
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700">Date début contrat</label>
          <input
            v-model="form.date_debut_contrat"
            type="date"
            required
            class="mt-1 w-full rounded border-gray-300"
          />
        </div>

        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-sm font-medium text-gray-700">Forfait N1 (h/mois)</label>
            <input
              v-model.number="form.forfait_n1_h"
              type="number"
              min="0"
              class="mt-1 w-full rounded border-gray-300"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Forfait N2 (h/mois)</label>
            <input
              v-model.number="form.forfait_n2_h"
              type="number"
              min="0"
              class="mt-1 w-full rounded border-gray-300"
            />
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700">Notes</label>
          <textarea v-model="form.notes" rows="2" class="mt-1 w-full rounded border-gray-300" />
        </div>

        <p v-if="error" class="text-sm text-red-600">{{ error }}</p>

        <div class="flex justify-end gap-3">
          <button type="button" @click="showForm = false" class="px-4 py-2 text-gray-600">
            Annuler
          </button>
          <button
            type="submit"
            class="bg-forfait-600 text-white px-4 py-2 rounded font-medium hover:bg-forfait-800"
          >
            Enregistrer
          </button>
        </div>
      </form>
    </div>
    </div>
  </div>
</template>
