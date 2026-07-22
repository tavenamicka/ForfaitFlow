<script setup>
import { reactive, ref } from "vue";

const props = defineProps({
  intervention: { type: Object, required: true },
});
const emit = defineEmits(["close", "save"]);

const editing = ref(false);

const form = reactive({
  niveau: props.intervention.niveau,
  duree_minutes: props.intervention.duree_minutes,
  description: props.intervention.description,
});

function onSave() {
  emit("save", { id: props.intervention.id, payload: { ...form } });
}
</script>

<template>
  <div class="fixed inset-0 bg-black/40 flex items-center justify-center p-4" @click.self="$emit('close')">
    <div class="bg-white rounded-lg shadow-md w-full max-w-md p-6 space-y-4">
      <div class="flex items-center justify-between">
        <h2 class="text-lg font-bold text-forfait-800">
          Intervention du {{ intervention.date_intervention }}
        </h2>
        <button @click="$emit('close')" aria-label="Fermer" class="text-gray-500 hover:text-gray-700">✕</button>
      </div>

      <template v-if="!editing">
        <p class="text-sm"><span class="font-medium">Niveau :</span> {{ intervention.niveau }}</p>
        <p class="text-sm">
          <span class="font-medium">Durée :</span> {{ intervention.duree_minutes }} min
        </p>
        <p class="text-sm whitespace-pre-wrap text-gray-700">{{ intervention.description }}</p>
        <div class="flex justify-end gap-3">
          <button @click="$emit('close')" class="px-4 py-2 text-gray-600">Fermer</button>
          <button
            @click="editing = true"
            class="bg-forfait-600 text-white px-4 py-2 rounded font-medium hover:bg-forfait-800"
          >
            Éditer
          </button>
        </div>
      </template>

      <template v-else>
        <div>
          <label class="block text-sm font-medium text-gray-700">Niveau</label>
          <select v-model="form.niveau" class="mt-1 w-full rounded border border-gray-300 px-3 py-2">
            <option value="N1">N1</option>
            <option value="N2">N2</option>
            <option value="N3">N3</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700">Durée (minutes)</label>
          <input
            v-model.number="form.duree_minutes"
            type="number"
            min="1"
            class="mt-1 w-full rounded border border-gray-300 px-3 py-2"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700">Description</label>
          <textarea v-model="form.description" rows="3" class="mt-1 w-full rounded border border-gray-300 px-3 py-2" />
        </div>
        <div class="flex justify-end gap-3">
          <button type="button" @click="editing = false" class="px-4 py-2 text-gray-600">
            Annuler
          </button>
          <button
            @click="onSave"
            class="bg-forfait-600 text-white px-4 py-2 rounded font-medium hover:bg-forfait-800"
          >
            Enregistrer
          </button>
        </div>
      </template>
    </div>
  </div>
</template>
