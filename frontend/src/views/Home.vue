<script setup lang="ts">
  import { VFileUpload, VFileUploadItem } from 'vuetify/labs/VFileUpload'
  import { ref, onMounted } from 'vue'
  import { useDownloadStore } from '@/stores/download';

  const loading = ref(false);
  const showFileUpload = ref(true);
  const showFileDownload = ref(false);
  const downloadStore = useDownloadStore();
  

  async function uploadFile(file: File) {
    showFileUpload.value = false;
    loading.value = true;
    downloadStore.fileName = file.name.split('.')[0] + '.step'
    downloadStore.sendFile();
    loading.value = false;
    showFileDownload.value = true;
  }

  async function downloadFile() {
    await downloadStore.getFile()
  }

  function reset() {
    showFileDownload.value = false;
    loading.value = true;

    downloadStore.fileName = 'VisionCAD.step';
    downloadStore.photoFile = undefined;

    loading.value = false;
    showFileUpload.value = true;
  }
</script>

<template>
  <v-container>
    <v-file-upload v-model="downloadStore.photoFile" density="default" clearable !multiple v-if="showFileUpload">
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
      <v-row class="justify-center my-2">
        <v-icon size="64">mdi-download</v-icon>
      </v-row>
      <v-row class="my-2">
        <v-col class="d-flex justify-end">
          <v-btn
            @click="downloadFile"
            class="justify-center"
            color="secondary-darken-1"
          >
            <p v-if="downloadStore.photoFile && !Array.isArray(downloadStore.photoFile)"> {{ downloadStore.fileName }}</p>
            <div v-else>Download</div>
          </v-btn>
        </v-col>
        <v-col class="d-flex justify-start">
          <v-btn color="secondary-darken-1" @click="reset">
            Upload Another Photo
          </v-btn>
        </v-col>
      </v-row>
      
    </v-card>
    
  </v-container>
</template>

<style scoped></style>
