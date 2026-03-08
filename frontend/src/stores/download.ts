import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { downloadApi } from "@/api/download";

export const useDownloadStore = defineStore("download", () => {
    
    const fileName = ref('VisionCAD.step')
    const photoFile = ref<File | File[] | undefined>(undefined);

    const getFile = async() => {
        try {
            const response = await downloadApi.getFile();
            const url = window.URL.createObjectURL(new Blob([response]));

            const link = document.createElement('a');
            link.href = url;

            link.setAttribute('download', '1.png');
            document.body.appendChild(link);
            link.click();

            link.remove();
            window.URL.revokeObjectURL(url);
        } catch (error) {
            console.error('Download failed: ', error)
        }
        
    }

    const sendFile = async() => {
        if (!photoFile.value || Array.isArray(photoFile.value)) return;

        const formData = new FormData();
        formData.append('image', photoFile.value);

        try {
            downloadApi.sendFile(formData);
        } catch (error) {
            console.error('Upload failed: ', error);
        }
    }

  return { 
    fileName,
    photoFile,
    getFile,
    sendFile,
   };
});