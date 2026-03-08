import axios from 'axios';

export const downloadApi = {
    async getFile() {
        const response = await axios.get('http://localhost:8080/download-step-file', {responseType: 'blob'})
        console.log(response.data);
        return response.data;
    },
    async sendFile(formData: FormData) {
        const response = await axios.post('http://localhost:8080/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        })
        console.log(response.data);
        return response.data;
    }
}

