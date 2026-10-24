// Service worker: la app abre sin conexión.
// La página se pide primero a la red (así llegan las actualizaciones solas)
// y, si no hay red, sale de la caché. El resto (iconos, tipografías) va de caché.
const CACHE = "cubos-v5";
const BASICOS = ["./", "index.html", "manifest.webmanifest", "icono-192.png", "icono-512.png", "icono-180.png"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(BASICOS)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", e => {
  e.waitUntil(
    caches.keys()
      .then(claves => Promise.all(claves.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;

  if (e.request.mode === "navigate") {
    e.respondWith(
      fetch(e.request)
        .then(r => { const copia = r.clone(); caches.open(CACHE).then(c => c.put("index.html", copia)); return r; })
        .catch(() => caches.match("index.html"))
    );
    return;
  }

  e.respondWith(
    caches.match(e.request).then(guardada => guardada || fetch(e.request).then(r => {
      if (r.ok || r.type === "opaque") { const copia = r.clone(); caches.open(CACHE).then(c => c.put(e.request, copia)); }
      return r;
    }))
  );
});
