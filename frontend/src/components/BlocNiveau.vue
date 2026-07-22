<script setup>
defineProps({
  index: { type: Number, required: true },
  removable: { type: Boolean, default: false },
});
defineEmits(["remove"]);
const bloc = defineModel({ required: true });
</script>

<template>
  <div class="border border-gray-200 rounded p-4 space-y-3">
    <div class="flex items-center justify-between">
      <span class="text-sm font-medium text-gray-500">Bloc {{ index + 1 }}</span>
      <button
        v-if="removable"
        type="button"
        @click="$emit('remove')"
        class="text-sm text-red-600 hover:text-red-800"
      >
        Retirer
      </button>
    </div>

    <div class="grid grid-cols-2 gap-3">
      <div>
        <label class="block text-sm font-medium text-gray-700">Niveau</label>
        <select v-model="bloc.niveau" class="mt-1 w-full rounded border-gray-300">
          <option value="N1">N1</option>
          <option value="N2">N2</option>
          <option value="N3">N3</option>
        </select>
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700">Durée (minutes)</label>
        <input
          v-model.number="bloc.duree_minutes"
          type="number"
          min="1"
          required
          class="mt-1 w-full rounded border-gray-300"
        />
      </div>
    </div>

    <div>
      <label class="block text-sm font-medium text-gray-700">Description</label>
      <textarea v-model="bloc.description" rows="2" required class="mt-1 w-full rounded border-gray-300" />
    </div>
  </div>
</template>
