/* Zero-dependency static server for the built kit. Binds 0.0.0.0 so the
   preview proxy (and a phone on the same network) can reach it. */
import { createServer } from 'node:http';
import { readFileSync, createReadStream, existsSync, statSync } from 'node:fs';
import { join, extname, normalize, resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const DIST = join(ROOT, process.argv[2] || 'dist');
const PORT = Number(process.env.PORT || 5173);
const HOST = process.env.HOST || '0.0.0.0';

const TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.png': 'image/png',
  '.webp': 'image/webp',
  '.ico': 'image/x-icon',
  '.txt': 'text/plain; charset=utf-8',
  '.xml': 'application/xml; charset=utf-8',
  '.webmanifest': 'application/manifest+json',
};

const send = (res, code, body, type = 'text/html; charset=utf-8') => {
  res.writeHead(code, { 'content-type': type, 'cache-control': 'no-store' });
  res.end(body);
};

createServer((req, res) => {
  const url = new URL(req.url, 'http://localhost');
  let p = decodeURIComponent(url.pathname);
  if (p.endsWith('/')) p += 'index.html';
  const wanted = resolve(join(DIST, normalize(p)));
  if (!wanted.startsWith(DIST)) return send(res, 403, 'forbidden');
  let target = wanted;
  if (existsSync(target) && statSync(target).isDirectory()) target = join(target, 'index.html');
  if (!existsSync(target)) {
    const notFound = join(DIST, '404.html');
    const body = existsSync(notFound)
      ? readFileSync(notFound, 'utf8')
      : `<pre style="font:14px ui-monospace;padding:2rem">404 — ${p}\nroot: ${DIST}</pre>`;
    return send(res, 404, body);
  }
  res.writeHead(200, {
    'content-type': TYPES[extname(target).toLowerCase()] || 'application/octet-stream',
    'content-length': statSync(target).size,
    'cache-control': 'no-cache',
    'x-content-type-options': 'nosniff',
  });
  if (req.method === 'HEAD') return res.end();
  createReadStream(target).pipe(res);
}).listen(PORT, HOST, () => {
  console.log(`Levain Kit → http://${HOST === '0.0.0.0' ? 'localhost' : HOST}:${PORT}  (serving ${DIST})`);
});
