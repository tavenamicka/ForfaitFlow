<script setup>
import { computed } from "vue";

const props = defineProps({
  label: { type: String, required: true },
  pourcentage: { type: Number, required: true },
  consommeMinutes: { type: Number, required: true },
  forfaitH: { type: Number, required: true },
});

const largeur = computed(() => `${Math.min(props.pourcentage, 100)}%`);

const couleur = computed(() => {
  if (props.pourcentage > 100) return "bg-red-500";
  if (props.pourcentage >= 80) return "bg-orange-500";
  return "bg-green-500";
});

const consommeH = computed(() => (props.consommeMinutes / 60).toFixed(1));
</script>

<template>
  <div>
    <div class="flex justify-between text-xs text-gray-500 mb-1">
      <span class="font-medium">{{ label }}</span>
      <span>{{ consommeH }}h / {{ forfaitH }}h ({{ pourcentage.toFixed(0) }}%)</span>
    </div>
    <div class="w-full h-2 rounded bg-gray-200 overflow-hidden">
      <div class="h-full rounded transition-all" :class="couleur" :style="{ width: largeur }"></div>
    </div>
  </div>
</template>
