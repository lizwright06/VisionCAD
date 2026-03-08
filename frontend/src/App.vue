<script setup lang="ts">
  import { useRouter, useRoute } from 'vue-router'

  const router = useRouter();
  const route = useRoute();

  const links = [{
      name: 'Home',
      url: '/home'
    },
    {
      name: 'Devpost',
      url: '/devpost'
    },
    {
      name: 'Github',
      url: '/github'
    }
  ]

  function navTo(url: string) {
    if(url==='/github') {
      url = route.path;
      window.open('https://github.com/lizwright06/VisionCAD', '_blank')?.focus();
    }
    if(url==='/devpost') {
      url = route.path;
       window.open('https://devpost.com/software/visioncad', '_blank')?.focus();
     }
    router.push(url);
  }
</script>

<template>
  <v-app>
    <v-locale-provider>
      <v-app-bar scroll-behavior="hide" app>
        <v-row class="align-center ma-2">
          <v-col @click="navTo('home')" class="text-display-large font-weight-black cursor-pointer">
            VisionCAD
          </v-col>
          <v-row class="justify-end">
            <v-col 
              v-for="link in links" 
              cols="auto" 
              class="my-2 mx-1 align-center justify-end cursor-pointer"
              @click="navTo(link.url)"
            >
              {{link.name}}
            </v-col>
          </v-row>
        </v-row>
      </v-app-bar>
      <v-main id="main">
        <router-view />
      </v-main>
      <v-footer class="d-flex align-center justify-center ga-2 flex-wrap flex-grow-1 py-3">
        <v-btn
          v-for="link in links"
          :key="link.name"
          :text="link.name"
          rounded
          @click="navTo(link.url)"
        ></v-btn>

        <div class="flex-1-0-100 text-center mt-2">
          2026 — <strong>VisionCAD</strong>
        </div>
      </v-footer>
    </v-locale-provider>
  </v-app>
</template>

<style scoped></style>
