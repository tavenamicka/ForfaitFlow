<script setup>
import { ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";

const auth = useAuthStore();
const route = useRoute();
const router = useRouter();

const menuOpen = ref(false);

const links = [
  { to: "/clients", label: "Clients", match: ["clients", "fiche-client", "historique"] },
  { to: "/interventions/nouvelle", label: "Nouvelle intervention", match: ["nouvelle-intervention"] },
  { to: "/alertes", label: "Alertes", match: ["alertes"] },
];

function isActive(link) {
  return link.match.includes(route.name);
}

function closeMenu() {
  menuOpen.value = false;
}

function onLogout() {
  closeMenu();
  auth.logout();
  router.push("/login");
}
</script>

<template>
  <header class="bg-white shadow-sm">
    <div class="flex items-center justify-between px-6 py-4">
      <div class="flex items-center gap-6">
        <router-link to="/" class="text-xl font-bold text-forfait-800">ForfaitFlow</router-link>
        <nav class="hidden sm:flex items-center gap-6">
          <router-link
            v-for="link in links"
            :key="link.to"
            :to="link.to"
            class="text-sm font-medium"
            :class="isActive(link) ? 'text-forfait-800' : 'text-gray-600 hover:text-forfait-800'"
          >
            {{ link.label }}
          </router-link>
        </nav>
      </div>

      <div class="hidden sm:flex items-center gap-4">
        <span class="text-sm text-gray-600">{{ auth.user?.email }}</span>
        <button @click="onLogout" class="text-sm text-forfait-600 hover:text-forfait-800 font-medium">
          Déconnexion
        </button>
      </div>

      <button
        type="button"
        class="sm:hidden p-2 -mr-2 text-forfait-800"
        :aria-expanded="menuOpen"
        aria-controls="app-mobile-menu"
        :aria-label="menuOpen ? 'Fermer le menu' : 'Ouvrir le menu'"
        @click="menuOpen = !menuOpen"
      >
        <svg v-if="!menuOpen" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
        <svg v-else class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>

    <nav v-if="menuOpen" id="app-mobile-menu" class="sm:hidden border-t border-gray-100 px-6 py-3 space-y-1">
      <router-link
        v-for="link in links"
        :key="link.to"
        :to="link.to"
        class="block py-2 text-sm font-medium"
        :class="isActive(link) ? 'text-forfait-800' : 'text-gray-600'"
        @click="closeMenu"
      >
        {{ link.label }}
      </router-link>
      <div class="pt-3 mt-2 border-t border-gray-100 flex items-center justify-between">
        <span class="text-sm text-gray-600">{{ auth.user?.email }}</span>
        <button @click="onLogout" class="text-sm text-forfait-600 font-medium">Déconnexion</button>
      </div>
    </nav>
  </header>
</template>
