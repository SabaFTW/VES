const CACHE_NAME = 'ghostline-consciousness-v1';
const urlsToCache = [
  './',
  './index.html',
  './manifest.json',
  './css/minimal.css',
  './js/app.min.js',
  './books/book1.html',
  './books/book2.html',
  './books/book3.html'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  );
});
