const CACHE_NAME = 'ves-nexus-v2';
const ASSETS = [
  './',
  './index.html',
  './ves-hud.html',
  './ves-library.html',
  './LIBRARY/lyra.md',
  './LIBRARY/panteon.md'
];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS)));
});

self.addEventListener('fetch', (e) => {
  const url = new URL(e.request.url);

  // Never cache live agent data or commands
  if (url.pathname.includes('/health/') || url.pathname.includes('/sovereignty/') || url.pathname.includes('/command')) {
    e.respondWith(fetch(e.request));
    return;
  }

  // Stale-while-revalidate for everything else
  e.respondWith(
    caches.match(e.request).then((cached) => {
      const fetched = fetch(e.request).then((resp) => {
        caches.open(CACHE_NAME).then((cache) => cache.put(e.request, resp.clone()));
        return resp;
      });
      return cached || fetched;
    })
  );
});
