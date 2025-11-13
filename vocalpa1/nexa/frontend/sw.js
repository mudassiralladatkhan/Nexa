// Nexa Voice Assistant - Service Worker

const CACHE_NAME = 'nexa-v1.0.0';
const STATIC_CACHE = 'nexa-static-v1';
const DYNAMIC_CACHE = 'nexa-dynamic-v1';

// Files to cache for offline functionality
const STATIC_FILES = [
    '/',
    '/index.html',
    '/css/styles.css',
    '/css/animations.css',
    '/js/config.js',
    '/js/utils.js',
    '/js/api.js',
    '/js/speech.js',
    '/js/app.js',
    '/manifest.json',
    'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap',
    'https://fonts.googleapis.com/icon?family=Material+Icons'
];

// API endpoints to cache
const API_CACHE_PATTERNS = [
    /\/api\/v1\/status/,
    /\/api\/v1\/preferences/,
    /\/health/
];

// Install event - cache static files
self.addEventListener('install', (event) => {
    console.log('Service Worker: Installing...');
    
    event.waitUntil(
        caches.open(STATIC_CACHE)
            .then((cache) => {
                console.log('Service Worker: Caching static files');
                return cache.addAll(STATIC_FILES);
            })
            .then(() => {
                console.log('Service Worker: Static files cached');
                return self.skipWaiting();
            })
            .catch((error) => {
                console.error('Service Worker: Failed to cache static files', error);
            })
    );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
    console.log('Service Worker: Activating...');
    
    event.waitUntil(
        caches.keys()
            .then((cacheNames) => {
                return Promise.all(
                    cacheNames.map((cacheName) => {
                        if (cacheName !== STATIC_CACHE && cacheName !== DYNAMIC_CACHE) {
                            console.log('Service Worker: Deleting old cache', cacheName);
                            return caches.delete(cacheName);
                        }
                    })
                );
            })
            .then(() => {
                console.log('Service Worker: Activated');
                return self.clients.claim();
            })
    );
});

// Fetch event - serve cached files or fetch from network
self.addEventListener('fetch', (event) => {
    const { request } = event;
    const url = new URL(request.url);
    
    // Skip non-GET requests
    if (request.method !== 'GET') {
        return;
    }
    
    // Skip chrome-extension requests
    if (url.protocol === 'chrome-extension:') {
        return;
    }
    
    // Handle different types of requests
    if (isStaticFile(request.url)) {
        // Static files - cache first strategy
        event.respondWith(cacheFirst(request));
    } else if (isAPIRequest(request.url)) {
        // API requests - network first strategy
        event.respondWith(networkFirst(request));
    } else {
        // Other requests - stale while revalidate strategy
        event.respondWith(staleWhileRevalidate(request));
    }
});

// Cache first strategy - for static files
async function cacheFirst(request) {
    try {
        const cachedResponse = await caches.match(request);
        if (cachedResponse) {
            return cachedResponse;
        }
        
        const networkResponse = await fetch(request);
        
        // Cache successful responses
        if (networkResponse.status === 200) {
            const cache = await caches.open(STATIC_CACHE);
            cache.put(request, networkResponse.clone());
        }
        
        return networkResponse;
    } catch (error) {
        console.error('Cache first strategy failed:', error);
        
        // Return offline fallback if available
        if (request.destination === 'document') {
            return caches.match('/index.html');
        }
        
        throw error;
    }
}

// Network first strategy - for API requests
async function networkFirst(request) {
    try {
        const networkResponse = await fetch(request);
        
        // Cache successful API responses
        if (networkResponse.status === 200) {
            const cache = await caches.open(DYNAMIC_CACHE);
            cache.put(request, networkResponse.clone());
        }
        
        return networkResponse;
    } catch (error) {
        console.warn('Network request failed, trying cache:', error);
        
        const cachedResponse = await caches.match(request);
        if (cachedResponse) {
            return cachedResponse;
        }
        
        throw error;
    }
}

// Stale while revalidate strategy - for other requests
async function staleWhileRevalidate(request) {
    const cache = await caches.open(DYNAMIC_CACHE);
    const cachedResponse = await cache.match(request);
    
    const networkResponsePromise = fetch(request)
        .then((networkResponse) => {
            if (networkResponse.status === 200) {
                cache.put(request, networkResponse.clone());
            }
            return networkResponse;
        })
        .catch((error) => {
            console.warn('Network request failed:', error);
            return null;
        });
    
    return cachedResponse || networkResponsePromise;
}

// Helper functions
function isStaticFile(url) {
    return STATIC_FILES.some(file => url.includes(file)) ||
           url.includes('.css') ||
           url.includes('.js') ||
           url.includes('.png') ||
           url.includes('.jpg') ||
           url.includes('.svg') ||
           url.includes('.woff') ||
           url.includes('.woff2');
}

function isAPIRequest(url) {
    return url.includes('/api/') || 
           url.includes('/health') ||
           API_CACHE_PATTERNS.some(pattern => pattern.test(url));
}

// Background sync for offline actions
self.addEventListener('sync', (event) => {
    console.log('Service Worker: Background sync triggered', event.tag);
    
    if (event.tag === 'background-sync-commands') {
        event.waitUntil(syncOfflineCommands());
    }
});

async function syncOfflineCommands() {
    try {
        // Get offline commands from IndexedDB or localStorage
        const offlineCommands = await getOfflineCommands();
        
        for (const command of offlineCommands) {
            try {
                // Try to send the command to the backend
                const response = await fetch('/api/v1/commands/process', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(command)
                });
                
                if (response.ok) {
                    // Remove from offline storage
                    await removeOfflineCommand(command.id);
                    console.log('Offline command synced:', command);
                }
            } catch (error) {
                console.warn('Failed to sync offline command:', error);
            }
        }
    } catch (error) {
        console.error('Background sync failed:', error);
    }
}

async function getOfflineCommands() {
    // This would typically use IndexedDB
    // For now, return empty array
    return [];
}

async function removeOfflineCommand(commandId) {
    // This would typically remove from IndexedDB
    console.log('Removing offline command:', commandId);
}

// Push notifications
self.addEventListener('push', (event) => {
    console.log('Service Worker: Push notification received');
    
    const options = {
        body: 'You have a new message from Nexa',
        icon: '/icons/icon-192.png',
        badge: '/icons/icon-192.png',
        vibrate: [100, 50, 100],
        data: {
            dateOfArrival: Date.now(),
            primaryKey: 1
        },
        actions: [
            {
                action: 'explore',
                title: 'Open Nexa',
                icon: '/icons/checkmark.png'
            },
            {
                action: 'close',
                title: 'Close',
                icon: '/icons/xmark.png'
            }
        ]
    };
    
    event.waitUntil(
        self.registration.showNotification('Nexa Voice Assistant', options)
    );
});

// Notification click handling
self.addEventListener('notificationclick', (event) => {
    console.log('Service Worker: Notification clicked');
    
    event.notification.close();
    
    if (event.action === 'explore') {
        // Open the app
        event.waitUntil(
            clients.openWindow('/')
        );
    } else if (event.action === 'close') {
        // Just close the notification
        return;
    } else {
        // Default action - open the app
        event.waitUntil(
            clients.matchAll().then((clientList) => {
                if (clientList.length > 0) {
                    return clientList[0].focus();
                }
                return clients.openWindow('/');
            })
        );
    }
});

// Message handling from main thread
self.addEventListener('message', (event) => {
    console.log('Service Worker: Message received', event.data);
    
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
    
    if (event.data && event.data.type === 'CACHE_URLS') {
        event.waitUntil(
            caches.open(DYNAMIC_CACHE)
                .then((cache) => cache.addAll(event.data.urls))
        );
    }
});

// Periodic background sync (if supported)
self.addEventListener('periodicsync', (event) => {
    console.log('Service Worker: Periodic sync triggered', event.tag);
    
    if (event.tag === 'background-health-check') {
        event.waitUntil(performHealthCheck());
    }
});

async function performHealthCheck() {
    try {
        const response = await fetch('/health');
        if (response.ok) {
            console.log('Health check passed');
        } else {
            console.warn('Health check failed:', response.status);
        }
    } catch (error) {
        console.error('Health check error:', error);
    }
}

// Error handling
self.addEventListener('error', (event) => {
    console.error('Service Worker error:', event.error);
});

self.addEventListener('unhandledrejection', (event) => {
    console.error('Service Worker unhandled rejection:', event.reason);
});

// Cleanup on beforeunload
self.addEventListener('beforeunload', () => {
    console.log('Service Worker: Cleaning up before unload');
});

console.log('Service Worker: Script loaded');
