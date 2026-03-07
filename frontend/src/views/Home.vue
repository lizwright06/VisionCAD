<script setup lang="ts">
  import { useTheme } from 'vuetify';
  
  const theme = useTheme();
</script>

<template>
  <v-card><h1>You did it!</h1>
  <p>
    Visit <a href="https://vuejs.org/" target="_blank" rel="noopener">vuejs.org</a> to read the
    documentation
  </p></v-card>
  <v-btn block>doesn't do anything but 3rd color!</v-btn>
</template>

<style scoped></style>
