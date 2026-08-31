// static/sw.js
const CACHE_NAME = 'sao-do-cache-v1';

self.addEventListener('install', (event) => {
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    event.waitUntil(clients.claim());
});

self.addEventListener('fetch', (event) => {
    let url = new URL(event.request.url);

    // [VÁ LỖI]: Bỏ qua hoàn toàn các yêu cầu xuất file hoặc gọi API động
    if (url.pathname.includes('/export_') || url.pathname.includes('/api/')) {
        return; // Trình duyệt sẽ tự xử lý kết nối trực tiếp với server, không qua Service Worker
    }

    event.respondWith(
        fetch(event.request).catch(() => {
            // Dự phòng khi mất mạng
            return caches.match(event.request);
        })
    );
});