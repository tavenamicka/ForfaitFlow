<script setup>
import { ref } from "vue";
import ModalDescription from "./ModalDescription.vue";

defineProps({
  rapport: { type: Object, required: true },
});
const emit = defineEmits(["save-intervention"]);

const niveauBadge = {
  N1: "bg-blue-100 text-blue-800",
  N2: "bg-teal-100 text-teal-800",
  N3: "bg-purple-100 text-purple-800",
};

const selected = ref(null);

function formatDuree(minutes) {
  const h = Math.floor(minutes / 60);
  const m = minutes % 60;
  return `${h}:${String(m).padStart(2, "0")}`;
}

function onSave(event) {
  emit("save-intervention", event);
  selected.value = null;
}
</script>

<template>
  <div class="space-y-6">
    <p class="text-sm text-gray-500">
      Période du {{ rapport.periode_debut }} au {{ rapport.periode_fin }}
    </p>

    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div class="bg-white rounded-lg shadow-sm p-4">
        <p class="text-xs text-gray-500">N1 — Assistance</p>
        <p class="text-xl font-bold text-blue-800">
          {{ (rapport.n1.consomme_minutes / 60).toFixed(1) }}h
          <span class="text-sm font-normal text-gray-400">/ {{ rapport.n1.forfait_h }}h</span>
        </p>
      </div>
      <div class="bg-white rounded-lg shadow-sm p-4">
        <p class="text-xs text-gray-500">N2 — Optimisation</p>
        <p class="text-xl font-bold text-teal-800">
          {{ (rapport.n2.consomme_minutes / 60).toFixed(1) }}h
          <span class="text-sm font-normal text-gray-400">/ {{ rapport.n2.forfait_h }}h</span>
        </p>
      </div>
      <div class="bg-white rounded-lg shadow-sm p-4">
        <p class="text-xs text-gray-500">N3 — Conseil (hors forfait)</p>
        <p class="text-xl font-bold text-purple-800">
          {{ (rapport.n3.consomme_minutes / 60).toFixed(1) }}h
        </p>
      </div>
      <div class="bg-white rounded-lg shadow-sm p-4">
        <p class="text-xs text-gray-500">Heures supp.</p>
        <p class="text-xl font-bold text-red-700">{{ (rapport.heures_supp_minutes / 60).toFixed(1) }}h</p>
      </div>
    </div>

    <div class="bg-white rounded-lg shadow-sm overflow-x-auto">
      <table class="min-w-full text-sm">
        <thead class="bg-gray-50 text-left text-gray-500">
          <tr>
            <th class="px-4 py-3">Date</th>
            <th class="px-4 py-3">Niveau</th>
            <th class="px-4 py-3">Durée</th>
            <th class="px-4 py-3">Description</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="i in rapport.interventions"
            :key="i.id"
            class="border-t cursor-pointer hover:bg-gray-50"
            @click="selected = i"
          >
            <td class="px-4 py-3">{{ i.date_intervention }}</td>
            <td class="px-4 py-3">
              <span class="px-2 py-1 rounded text-xs font-medium" :class="niveauBadge[i.niveau]">
                {{ i.niveau }}
              </span>
            </td>
            <td class="px-4 py-3">{{ formatDuree(i.duree_minutes) }}</td>
            <td class="px-4 py-3 max-w-md truncate">{{ i.description }}</td>
          </tr>
          <tr v-if="!rapport.interventions.length">
            <td colspan="4" class="px-4 py-6 text-center text-gray-400">
              Aucune intervention sur cette période.
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <ModalDescription
      v-if="selected"
      :intervention="selected"
      @close="selected = null"
      @save="onSave"
    />
  </div>
</template>
