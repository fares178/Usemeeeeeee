// Backend configuration for Hugging Face Spaces
// Using Hugging Face Space URL
const BACKEND_URL = localStorage.getItem('backendUrl') || 'https://ankarasui-business-chatbot-caeb2a6.hf.space';

// For local development with Flask backend
const USE_LOCAL_BACKEND = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
const LOCAL_BACKEND_URL = 'http://localhost:8000';

const ACTIVE_BACKEND = USE_LOCAL_BACKEND ? LOCAL_BACKEND_URL : BACKEND_URL;

console.log('Backend URL:', BACKEND_URL);
console.log('Local development:', USE_LOCAL_BACKEND);
console.log('Active backend:', ACTIVE_BACKEND);
