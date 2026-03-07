<script setup lang="ts">
  import { VFileUpload, VFileUploadItem } from 'vuetify/labs/VFileUpload'
  import { ref, onMounted } from 'vue'


  const loading = ref(false);
  const showFileUpload = ref(true);
  const showFileDownload = ref(false);
  const photoFile = ref<File | File[] | undefined>(undefined);


  async function uploadFile(file: File) {
    showFileUpload.value = false;
    loading.value = true;
    //TODO save file to path 
    //TODO api call here
    loading.value = false;
    showFileDownload.value = true;
  }

  async function downloadFile() {

  }


  onMounted(() => {
  })
</script>

<template>
  <v-container>
    <v-file-upload v-model="photoFile" density="default" clearable !multiple v-if="showFileUpload">
      <template v-slot:browse="{ props }">
        <v-btn v-bind="props" color="secondary-darken-1" variant="elevated">
          Browse Files
        </v-btn>
      </template>
      
      <template v-slot:item="{ props, file }">
        <v-file-upload-item v-bind="props">
          <template v-slot:clear="{ props: clearProps }">
            <v-btn color="error" v-bind="clearProps" icon="mdi-delete"></v-btn>
          </template>  
          <template v-slot:append>
            <v-btn color="secondary-darken-1" @click="uploadFile(file)">Upload</v-btn>
          </template>
        </v-file-upload-item>
      </template>
    </v-file-upload>
    <v-card v-if="loading">
      wooooo
    </v-card>
    <v-card v-if="showFileDownload">

    </v-card>
    
  </v-container>
</template>

<style scoped></style>
