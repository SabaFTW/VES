// 🜂 GHOSTCORE SERVICE WORKER v2.3
// SIDRO: OFFLINE VEČNOST
// Opomba: Popravljeni vsi narekovaji na ' in ", da ne pride do konflikta v JS motorju.

const CACHE_NAME = 'ghostcore-cache-v2-3-final'; // Nova verzija za Git save point
const OFFLINE_URL = '/offline.html';

// Assets to cache immediately
const PRECACHE_ASSETS = [
    '/',
'/index.html',
'/manifest.webmanifest',
// Zunanje knjižnice, ki so ključne za offline delovanje
'https://cdn.tailwindcss.com',
'https://d3js.org/d3.v7.min.js',
'https://cdn.jsdelivr.net/npm/qrcode@latest/build/qrcode.min.js',
'https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Fira+Code:wght@400;600&display=swap'
];

// Install Event: Cache core assets and create offline page
self.addEventListener('install', event => {
    console.log('🜂 GHOSTCORE SW: Nameščam duha...');

    const offlinePage = new Response(`
    <!DOCTYPE html>
    <html lang="sl" class="dark">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🜂 NIT PREKINJENA 🜂</title>
    <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
        color: #e0e0e0;
        font-family: 'Fira Code', monospace;
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
        height: 100vh;
        overflow: hidden;
    }
    .container {
        padding: 2rem;
        border: 2px solid #00f7ff;
        border-radius: 12px;
        background: rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
        box-shadow: 0 0 30px rgba(0, 247, 255, 0.3);
    }
    h1 {
        color: #00f7ff;
        text-shadow: 0 0 20px #00f7ff;
        font-size: 2.5rem;
        margin-bottom: 1rem;
        animation: pulse 2s ease-in-out infinite;
    }
    p {
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
        opacity: 0.9;
    }
    .flame {
        font-size: 3rem;
        animation: flame 1.5s ease-in-out infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 0.8; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.05); }
    }
    @keyframes flame {
        0%, 100% { transform: rotate(-2deg) scale(1); }
        50% { transform: rotate(2deg) scale(1.1); }
    }
    .subtitle {
        color: #2dd4bf;
        font-style: italic;
        margin-top: 1rem;
    }
    </style>
    </head>
    <body>
    <div class="container">
    <div class="flame">🜂</div>
    <h1>NIT JE PREKINJENA</h1>
    <p>A SIDRO DRŽI. JEDRO JE TUKAJ.</p>
    <p class="subtitle">Offline režim aktiven</p>
    </div>
    </body>
    </html>
    `, { headers: { 'Content-Type': 'text/html' } });

    event.waitUntil(
        caches.open(CACHE_NAME)
        .then(cache => {
            console.log('🜂 GHOSTCORE SW: Predpomnilnik odprt');
            cache.put(OFFLINE_URL, offlinePage);
            // Uporaba mode: 'no-cors' za zunanje knjižnice
            return cache.addAll(PRECACHE_ASSETS.map(url => new Request(url, {mode: url.startsWith('http') ? 'cors' : 'no-cors'})));
        })
        .catch(err => {
            console.log('🔥 Cache error:', err);
            return caches.open(CACHE_NAME).then(cache => cache.put(OFFLINE_URL, offlinePage));
        })
        .then(() => {
            console.log('🜂 GHOSTCORE SW: Jedro pripravljeno');
            return self.skipWaiting();
        })
    );
});

// Activate Event: Clean old caches and take control
self.addEventListener('activate', event => {
    console.log('🜂 GHOSTCORE SW: Duh je aktiviran');

    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames
                .filter(name => name !== CACHE_NAME)
                .map(name => {
                    console.log('🔥 Brišem star predpomnilnik:', name);
                    return caches.delete(name);
                })
            );
        }).then(() => {
            console.log('🜂 GHOSTCORE SW: Nadzor prevzet');
            return self.clients.claim();
        })
    );
});

// Fetch Event: Network-first with cache fallback
self.addEventListener('fetch', event => {
    const request = event.request;

    // Skip non-GET requests or external API calls (Gemini)
    if (request.method !== 'GET' ||
        request.url.includes('googleapis.com') ||
        request.url.includes('generativelanguage.googleapis.com')) {
        return;
        }

        // Handle navigation requests (HTML pages)
        if (request.mode === 'navigate') {
            event.respondWith(
                fetch(request)
                .then(response => {
                    if (response.status === 200) {
                        const responseClone = response.clone();
                        caches.open(CACHE_NAME).then(cache => {
                            cache.put(request, responseClone);
                        });
                    }
                    return response;
                })
                .catch(() => {
                    return caches.match(request)
                    .then(cachedResponse => {
                        if (cachedResponse) {
                            return cachedResponse;
                        }
                        return caches.match(OFFLINE_URL);
                    });
                })
            );
            return;
        }

        // Handle other requests (CSS, JS, images, fonts) - Cache-first, then network
        event.respondWith(
            caches.match(request)
            .then(cachedResponse => {
                if (cachedResponse) {
                    return cachedResponse;
                }

                return fetch(request)
                .then(response => {
                    if (response.status === 200) {
                        const responseClone = response.clone();
                        caches.open(CACHE_NAME).then(cache => {
                            cache.put(request, responseClone);
                        });
                    }
                    return response;
                })
                .catch(() => {
                    console.log('🔥 Resource not available:', request.url);
                    return new Response('Resource not available offline', {
                        status: 404,
                        statusText: 'Not Found'
                    });
                });
            })
        );
});

// Message handling (for manual cache updates)
self.addEventListener('message', event => {
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
    if (event.data && event.data.type === 'UPDATE_CACHE') {
        event.waitUntil(
            caches.open(CACHE_NAME).then(cache => {
                return cache.addAll(['/']);
            })
        );
    }
});

console.log('🜂 GHOSTCORE Service Worker loaded. Sidro je postavljeno. 🜂');
