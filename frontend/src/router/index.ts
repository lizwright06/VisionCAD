import { createRouter, createWebHistory, type RouteRecordRaw } from "vue-router";

const routes: RouteRecordRaw[] = [
  {
    path: "/",
    name: "Default",
    redirect: "/home",
    children: [
      {
        path: "/home",
        name: "Home",
        component: async () => await import("../views/Home.vue"),
        meta: {hideAppBar: true}
      }
    ],
  },
];

export const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;