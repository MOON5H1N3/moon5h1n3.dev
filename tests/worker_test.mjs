// Tests for the /api/upc relay in worker.js, with UPCitemdb and Cloudflare's cache faked.  Run: node tests/worker_test.mjs
import { upc, allowedOrigin, trim } from "../worker.js";
let failed = 0;
const ok = (c, n) => { console.log((c ? "PASS " : "FAIL ") + n); if (!c) failed++; };
const store = new Map();
const cache = { match: async (k) => store.get(k.url)?.clone(), put: async (k, r) => { store.set(k.url, r); } };
let calls = 0, answer = { status: 200, body: { code: "OK", items: [{ title: "Heat [Blu-ray] [1995]", brand: "Fox", images: ["https://img/x.jpg", "https://img/y.jpg"], offers: [{ price: 9 }] }] } };
const fetcher = async () => { calls++; return new Response(JSON.stringify(answer.body), { status: answer.status }); };
const ask = (code, origin = "https://keep.moon5h1n3.dev", method = "GET") =>
  upc(new Request("https://moon5h1n3.dev/api/upc?code=" + code, { method, headers: origin ? { Origin: origin } : {} }), {}, null, fetcher, cache);

ok(allowedOrigin("https://keep.moon5h1n3.dev") && allowedOrigin("http://localhost:8787") && !allowedOrigin("https://evil.dev") && !allowedOrigin("https://moon5h1n3.dev.evil.com") && !allowedOrigin(""), "only moon5h1n3.dev and localhost may use it");
let r = await ask("5039036999999");
let b = await r.json();
ok(r.status === 200 && b.items[0].title === "Heat [Blu-ray] [1995]" && b.items[0].images.length === 1 && !("offers" in b.items[0]), "found: trimmed answer");
ok(r.headers.get("access-control-allow-origin") === "https://keep.moon5h1n3.dev", "phone allowed to read it");
await ask("5039036999999"); ok(calls === 1, "second ask comes from the cache");
r = await ask("5039036999999", "https://evil.example"); ok(r.status === 403 && !r.headers.get("access-control-allow-origin"), "other sites refused");
r = await ask("5039036999999", ""); ok(r.status === 403, "no origin refused");
r = await ask("12ab", "https://keep.moon5h1n3.dev"); ok(r.status === 400, "not a barcode refused");
r = await ask("5039036999999", "https://keep.moon5h1n3.dev", "OPTIONS"); ok(r.status === 204, "preflight answered");
answer = { status: 404, body: { code: "INVALID_UPC", items: [] } };
r = await ask("5039036000001"); b = await r.json(); ok(r.status === 200 && b.items.length === 0, "unknown barcode: empty answer");
answer = { status: 400, body: { code: "INVALID_UPC", message: "Not a valid UPC code." } };
r = await ask("5039036000009"); b = await r.json(); ok(r.status === 200 && b.items.length === 0, "invalid barcode: nothing found");
answer = { status: 400, body: { code: "SOMETHING_ELSE", message: "odd" } };
r = await ask("5039036000008"); b = await r.json(); ok(r.status === 502 && /SOMETHING_ELSE/.test(b.error), "other 400 explained");
answer = { status: 429, body: {} };
r = await ask("5039036000002"); ok(r.status === 503, "daily limit explained");
answer = { status: 500, body: {} };
r = await ask("5039036000003"); ok(r.status === 502, "UPCitemdb error passed on");
ok(trim(null).items.length === 0, "trim copes with nothing");
console.log(failed ? `\n${failed} failed.` : "\nAll passed.");
process.exit(failed ? 1 : 0);
