// The site is static files (dist/), served by Cloudflare. This script only adds one small thing:
//
//   /api/upc?code=5051892225610  → what UPCitemdb knows about that barcode
//
// It's a relay for the Worth Keeping phone app. UPCitemdb (the free barcode database that covers DVDs and
// Blu-rays) doesn't let web apps call it directly, so the phone asks here instead. Only Worth Keeping on a
// moon5h1n3.dev address (or a computer's own localhost) may use it, answers are trimmed to what the app
// needs, and they're kept for a month so the same barcode never uses up UPCitemdb's daily allowance twice.

const UPSTREAM = "https://api.upcitemdb.com/prod/trial/lookup?upc=";
const FOUND_FOR = 30 * 86400;   // seconds a found barcode is kept
const MISSING_FOR = 86400;      // a barcode UPCitemdb doesn't know is asked again after a day

export function allowedOrigin(origin) {
  if (!origin) return false;
  return /^https:\/\/([a-z0-9-]+\.)*moon5h1n3\.dev$/.test(origin) || /^https?:\/\/(localhost|127\.0\.0\.1)(:\d+)?$/.test(origin);
}

function reply(body, status, origin, maxAge) {
  const headers = { "content-type": "application/json; charset=utf-8", "vary": "Origin" };
  if (origin) headers["access-control-allow-origin"] = origin;
  if (maxAge) headers["cache-control"] = `public, max-age=${maxAge}`;
  return new Response(JSON.stringify(body), { status, headers });
}

// Keep only what the app uses: title, brand and one image per item.
export function trim(data) {
  const items = (data && data.items) || [];
  return { items: items.slice(0, 3).map((it) => ({ title: String(it.title || ""), brand: String(it.brand || ""),
    images: (it.images || []).filter((u) => /^https?:\/\//.test(u)).slice(0, 1) })) };
}

export async function upc(request, env, ctx, fetcher = fetch, cache = caches.default) {
  const origin = request.headers.get("Origin") || "";
  if (!allowedOrigin(origin)) return reply({ error: "not allowed" }, 403, "");
  if (request.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: { "access-control-allow-origin": origin, "access-control-allow-methods": "GET",
      "access-control-max-age": "86400", "vary": "Origin" } });
  }
  if (request.method !== "GET") return reply({ error: "GET only" }, 405, origin);
  const code = (new URL(request.url).searchParams.get("code") || "").replace(/[^0-9]/g, "");
  if (code.length < 8 || code.length > 14) return reply({ error: "not a barcode" }, 400, origin);

  const key = new Request(`https://moon5h1n3.dev/api/upc?code=${code}`);
  const kept = await cache.match(key);
  if (kept) return reply(await kept.json(), 200, origin);

  let res;
  try {
    res = await fetcher(UPSTREAM + code, { headers: { "accept": "application/json", "user-agent": "worth-keeping-relay" } });
  } catch (e) {
    return reply({ error: "couldn't reach UPCitemdb" }, 502, origin);
  }
  if (res.status === 429) return reply({ error: "UPCitemdb's daily limit is used up; try again later" }, 503, origin);
  if (res.status === 404) res = null;  // UPCitemdb's way of saying it doesn't know the code
  else if (res.status === 400) {      // INVALID_UPC: not a real barcode (or one it can't read), so nothing to find
    const why = await res.json().catch(() => ({}));
    if (why.code === "INVALID_UPC" || why.code === "INVALID_QUERY") res = null;
    else return reply({ error: `UPCitemdb answered 400 ${why.code || ""} ${why.message || ""}`.trim() }, 502, origin);
  } else if (!res.ok) return reply({ error: `UPCitemdb answered ${res.status}` }, 502, origin);
  const body = trim(res ? await res.json().catch(() => ({})) : {});
  const keep = new Response(JSON.stringify(body), { headers: { "content-type": "application/json",
    "cache-control": `public, max-age=${body.items.length ? FOUND_FOR : MISSING_FOR}` } });
  const save = cache.put(key, keep);
  if (ctx && ctx.waitUntil) ctx.waitUntil(save); else await save;
  return reply(body, 200, origin);
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    if (url.pathname === "/api/upc") return upc(request, env, ctx);
    return env.ASSETS.fetch(request);
  },
};
