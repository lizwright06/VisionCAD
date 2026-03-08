<script setup lang="ts">
  import { VFileUpload, VFileUploadItem } from 'vuetify/labs/VFileUpload'
  import { useDownloadStore } from '@/stores/download';
  import { onMounted, onUnmounted, ref } from 'vue';
  
  const downloadStore = useDownloadStore();
  const socket = ref<WebSocket | null>(null);

  async function uploadFile(file: File) {
    //swap file upload and loading screens
    downloadStore.showFileUpload = false;
    downloadStore.loading = true;

    //grab file name
    downloadStore.fileName = file.name.split('.')[0] + '.step'

    //call store function to send file to backend
    downloadStore.sendFile();
  }

  async function downloadFile() {
    //call store function to get file from backend
    await downloadStore.getFile()
  }

  function reset() {
    //swap download and 
    downloadStore.showFileDownload = false;
    downloadStore.loading = true;

    downloadStore.fileName = 'VisionCAD.step';
    downloadStore.photoFile = undefined;

    downloadStore.loading = false;
    downloadStore.showFileUpload = true;
  }

  onMounted(() => {
    socket.value = new WebSocket(`ws://localhost:8000/ws`);

    socket.value.onmessage = (event) => {
      downloadStore.loading = false;
      downloadStore.showFileDownload = true;
    }
  })

  onUnmounted(() => {
    socket.value?.close();
  });
</script>

<template>
  <v-container>
    <div class="mb-5">
      <h1>INSTRUCTIONS</h1>
      <div class="ml-2">
        1. Draw an image of simple shapes <br>
        2. Upload the image in the box below<br>
        3. Click "Upload" next to the uploaded image<br>
        4. Once the file has been processed & converted, click on <span v-if="downloadStore.fileName">{{downloadStore.fileName}}</span><span v-else>the file name</span> to download your file<br>
        5. Click "Upload Another Photo" to return to the start screen
      </div>
    </div>
    <v-file-upload 
      v-model="downloadStore.photoFile" 
      density="default" 
      clearable 
      !multiple
      v-if="downloadStore.showFileUpload"
    >
      <template v-slot:browse="{ props }">
        <v-btn v-bind="props" color="secondary-darken" variant="elevated">
          Browse Files
        </v-btn>
      </template>
      
      <template v-slot:item="{ props, file }">
        <v-file-upload-item v-bind="props">
          <template v-slot:clear="{ props: clearProps }">
            <v-btn color="error" v-bind="clearProps" icon="mdi-delete"></v-btn>
          </template>  
          <template v-slot:append>
            <v-btn color="secondary-darken" @click="uploadFile(file)">Upload</v-btn>
          </template>
        </v-file-upload-item>
      </template>
    </v-file-upload>
    <v-card v-if="downloadStore.loading">
      <v-row class="justify-center ma-2">Creating your file, please wait...</v-row>
      <v-row class="justify-center ma-2">
        <v-btn color="primary" :loading="downloadStore.loading">woo</v-btn>
      </v-row>

    </v-card>
    <v-card v-if="downloadStore.showFileDownload">
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
