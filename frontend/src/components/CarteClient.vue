<script setup>
import JaugeConso from "./JaugeConso.vue";

defineProps({
  dashboard: { type: Object, required: true },
});
</script>

<template>
  <div class="bg-white rounded-lg shadow-sm p-5 space-y-4">
    <div class="flex items-start justify-between">
      <div>
        <router-link :to="`/clients/${dashboard.client_id}`" class="font-bold text-forfait-800 hover:underline">
          {{ dashboard.client_nom }}
        </router-link>
        <p class="text-xs text-gray-500">
          Période du {{ dashboard.periode_debut }} au {{ dashboard.periode_fin }}
        </p>
      </div>
      <span
        v-if="dashboard.alerte"
        class="px-2 py-1 rounded text-xs font-medium bg-red-100 text-red-800"
      >
        ⚠ Seuil atteint
      </span>
    </div>

    <JaugeConso
      label="N1 — Assistance"
      :pourcentage="dashboard.n1.pourcentage"
      :consomme-minutes="dashboard.n1.consomme_minutes"
      :forfait-h="dashboard.n1.forfait_h"
    />
    <JaugeConso
      label="N2 — Optimisation"
      :pourcentage="dashboard.n2.pourcentage"
      :consomme-minutes="dashboard.n2.consomme_minutes"
      :forfait-h="dashboard.n2.forfait_h"
    />

    <div class="text-xs text-gray-500 pt-2 border-t">
      N3 — Conseil stratégique (hors forfait) :
      <span class="font-medium">{{ (dashboard.n3.consomme_minutes / 60).toFixed(1) }}h</span>
    </div>
  </div>
</template>
