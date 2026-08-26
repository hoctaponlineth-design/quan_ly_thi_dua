// static/sw.js
const CACHE_NAME = 'sao-do-cache-v1';

self.addEventListener('install', (event) => {
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    event.waitUntil(clients.claim());
});

self.addEventListener('fetch', (event) => {
    // Để trống hoặc thiết lập cache cơ bản. 
    // Trình duyệt sẽ chạy app mượt mà hơn nhờ có file này.
    event.respondWith(fetch(event.request));
});