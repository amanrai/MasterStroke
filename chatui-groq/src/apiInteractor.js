import axios from 'axios';

export const getSettings = async () => {
    try {
        const response = await axios.get('http://localhost:8000/settings');
        return response.data;
    } catch (error) {
        console.log(error)
        throw error;
    }
    
};