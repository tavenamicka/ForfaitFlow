import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "../stores/auth";
import Login from "../views/Login.vue";
import Dashboard from "../views/Dashboard.vue";
import GestionClients from "../views/GestionClients.vue";
import NouvelleIntervention from "../views/NouvelleIntervention.vue";
import FicheClient from "../views/FicheClient.vue";
import Historique from "../views/Historique.vue";
import Alertes from "../views/Alertes.vue";

const routes = [
  { path: "/login", name: "login", component: Login },
  { path: "/", name: "dashboard", component: Dashboard, meta: { requiresAuth: true } },
  { path: "/clients", name: "clients", component: GestionClients, meta: { requiresAuth: true } },
  {
    path: "/interventions/nouvelle",
    name: "nouvelle-intervention",
    component: NouvelleIntervention,
    meta: { requiresAuth: true },
  },
  {
    path: "/clients/:id",
    name: "fiche-client",
    component: FicheClient,
    meta: { requiresAuth: true },
  },
  {
    path: "/clients/:id/historique",
    name: "historique",
    component: Historique,
    meta: { requiresAuth: true },
  },
  { path: "/alertes", name: "alertes", component: Alertes, meta: { requiresAuth: true } },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to) => {
  const auth = useAuthStore();
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return { name: "login" };
  }
  if (to.name === "login" && auth.isAuthenticated) {
    return { name: "dashboard" };
  }
});

export default router;
