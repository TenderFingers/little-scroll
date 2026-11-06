import os, re, json
D = os.path.dirname(os.path.abspath(__file__))
os.chdir(D)
OUT = os.environ.get('LS_OUT') or os.path.dirname(D)  # the repo root, where GitHub Pages serves from
s = open('little-scroll.html', encoding='utf8').read()
VER = re.search(r"var VERSION = '([^']+)'", s).group(1)
s = s.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
i = s.index('</style>') + len('</style>')
head, body = s[:i], s[i:]
head = head.replace('<style>\n', '<style>\n:root { color-scheme: light; }\n[hidden] { display: none !important; }\n', 1)
extra = ('<link rel="manifest" href="manifest.webmanifest">\n<link rel="apple-touch-icon" href="icon.png">\n'
         '<meta name="theme-color" content="#4FB5E8">\n')
reg = ("<script>if ('serviceWorker' in navigator) { window.addEventListener('load', function () { "
       "navigator.serviceWorker.register('sw.js').catch(function () {}); }); }</script>\n")
out = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
       '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
       + extra + head + '\n</head>\n<body>' + body + reg + '</body>\n</html>\n')
os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf8').write(out)
open(os.path.join(OUT, 'sw.js'), 'w', encoding='utf8').write("""var CACHE = 'little-scroll-%s';
var FILES = ['./', 'index.html', 'manifest.webmanifest', 'icon.png'];

self.addEventListener('install', function (e) {
  e.waitUntil(caches.open(CACHE).then(function (c) { return c.addAll(FILES); }).then(function () { return self.skipWaiting(); }));
});

self.addEventListener('activate', function (e) {
  e.waitUntil(caches.keys().then(function (keys) {
    return Promise.all(keys.filter(function (k) { return k.indexOf('little-scroll-') === 0 && k !== CACHE; }).map(function (k) { return caches.delete(k); }));
  }).then(function () { return self.clients.claim(); }));
});

// Open instantly from the saved copy, and refresh that copy in the background when online.
self.addEventListener('fetch', function (e) {
  var req = e.request;
  if (req.method !== 'GET' || new URL(req.url).origin !== location.origin) return;
  e.respondWith(caches.open(CACHE).then(function (cache) {
    return cache.match(req, { ignoreSearch: true }).then(function (hit) {
      var net = fetch(req).then(function (res) {
        if (res && res.ok) cache.put(req, res.clone());
        return res;
      }).catch(function () {
        return hit || (req.mode === 'navigate' ? cache.match('index.html') : undefined);
      });
      e.waitUntil(net.catch(function () {}));
      return hit || net;
    });
  }));
});
""" % VER)
open(os.path.join(OUT, 'manifest.webmanifest'), 'w', encoding='utf8').write(json.dumps({
    "name": "Little Scroll", "short_name": "Little Scroll", "start_url": "./", "scope": "./",
    "display": "standalone", "orientation": "portrait", "background_color": "#EEF0FB", "theme_color": "#4FB5E8",
    "icons": [{"src": "icon.png", "sizes": "512x512", "type": "image/png", "purpose": "any"}]}, indent=2))
if not os.path.exists(os.path.join(OUT, 'icon.png')):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page(viewport={'width': 512, 'height': 512})
        pg.set_content('<body style="margin:0"><canvas id=c width=512 height=512></canvas></body>')
        pg.evaluate("""(() => { const g = document.getElementById('c').getContext('2d');
          g.fillStyle = '#4FB5E8'; g.fillRect(0, 0, 512, 512);
          g.fillStyle = '#FFD23F'; g.beginPath(); g.arc(256, 256, 150, 0, 6.2832); g.fill();
          g.fillStyle = '#E8453A'; g.beginPath(); g.arc(346, 172, 62, 0, 6.2832); g.fill(); })()""")
        pg.screenshot(path=os.path.join(OUT, 'icon.png'), clip={'x': 0, 'y': 0, 'width': 512, 'height': 512}); br.close()
print('version', VER, {n: os.path.getsize(os.path.join(OUT, n)) for n in ('index.html', 'sw.js', 'manifest.webmanifest', 'icon.png')})
