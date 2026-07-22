<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";

const email = ref("");
const password = ref("");
const error = ref("");
const loading = ref(false);

const auth = useAuthStore();
const router = useRouter();

async function onSubmit() {
  error.value = "";
  loading.value = true;
  try {
    await auth.login(email.value, password.value);
    router.push("/");
  } catch {
    error.value = "Email ou mot de passe incorrect.";
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-forfait-50">
    <form
      @submit.prevent="onSubmit"
      class="bg-white p-8 rounded-lg shadow-md w-full max-w-sm space-y-4"
    >
      <h1 class="text-2xl font-bold text-forfait-800 text-center">ForfaitFlow</h1>

      <div>
        <label class="block text-sm font-medium text-gray-700">Email</label>
        <input
          v-model="email"
          type="email"
          required
          class="mt-1 w-full rounded border border-gray-300 px-3 py-2 shadow-sm focus:border-forfait-600 focus:ring-forfait-600"
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700">Mot de passe</label>
        <input
          v-model="password"
          type="password"
          required
          class="mt-1 w-full rounded border border-gray-300 px-3 py-2 shadow-sm focus:border-forfait-600 focus:ring-forfait-600"
        />
      </div>

      <p v-if="error" class="text-sm text-red-600">{{ error }}</p>

      <button
        type="submit"
        :disabled="loading"
        class="w-full bg-forfait-600 text-white rounded py-2 font-medium hover:bg-forfait-800 disabled:opacity-50"
      >
        {{ loading ? "Connexion..." : "Se connecter" }}
      </button>
    </form>
  </div>
</template>
