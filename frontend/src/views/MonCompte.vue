<script setup>
import { reactive, ref } from "vue";
import { useAuthStore } from "../stores/auth";
import AppHeader from "../components/AppHeader.vue";

const auth = useAuthStore();

const form = reactive({
  ancien: "",
  nouveau: "",
  confirmation: "",
});

const error = ref("");
const success = ref(false);
const loading = ref(false);

async function onSubmit() {
  error.value = "";
  success.value = false;

  if (form.nouveau !== form.confirmation) {
    error.value = "Les deux mots de passe ne correspondent pas.";
    return;
  }
  if (form.nouveau.length < 8) {
    error.value = "Le nouveau mot de passe doit faire au moins 8 caractères.";
    return;
  }

  loading.value = true;
  try {
    await auth.changePassword(form.ancien, form.nouveau);
    success.value = true;
    form.ancien = "";
    form.nouveau = "";
    form.confirmation = "";
  } catch (e) {
    error.value =
      e.response?.status === 400
        ? "Mot de passe actuel incorrect."
        : "Erreur lors de la mise à jour du mot de passe.";
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="min-h-screen bg-forfait-50">
    <AppHeader />

    <div class="p-6 max-w-md mx-auto space-y-6">
      <h1 class="text-2xl font-bold text-forfait-800">Mon compte</h1>
      <p class="text-sm text-gray-500">{{ auth.user?.email }}</p>

      <form @submit.prevent="onSubmit" class="bg-white rounded-lg shadow-sm p-6 space-y-4">
        <h2 class="text-lg font-bold text-forfait-800">Changer le mot de passe</h2>

        <div>
          <label for="ancien-mdp" class="block text-sm font-medium text-gray-700">
            Mot de passe actuel
          </label>
          <input
            id="ancien-mdp"
            v-model="form.ancien"
            type="password"
            required
            class="mt-1 w-full rounded border border-gray-300 px-3 py-2"
          />
        </div>

        <div>
          <label for="nouveau-mdp" class="block text-sm font-medium text-gray-700">
            Nouveau mot de passe
          </label>
          <input
            id="nouveau-mdp"
            v-model="form.nouveau"
            type="password"
            required
            minlength="8"
            class="mt-1 w-full rounded border border-gray-300 px-3 py-2"
          />
        </div>

        <div>
          <label for="confirmation-mdp" class="block text-sm font-medium text-gray-700">
            Confirmer le nouveau mot de passe
          </label>
          <input
            id="confirmation-mdp"
            v-model="form.confirmation"
            type="password"
            required
            minlength="8"
            class="mt-1 w-full rounded border border-gray-300 px-3 py-2"
          />
        </div>

        <p v-if="error" role="alert" class="text-sm text-red-600">{{ error }}</p>
        <p v-if="success" role="status" class="text-sm text-forfait-600">
          Mot de passe mis à jour avec succès.
        </p>

        <button
          type="submit"
          :disabled="loading"
          class="w-full bg-forfait-600 text-white rounded py-2 font-medium hover:bg-forfait-800 disabled:opacity-50"
        >
          {{ loading ? "Enregistrement..." : "Enregistrer" }}
        </button>
      </form>
    </div>
  </div>
</template>
