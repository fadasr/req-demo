# tools/explorer/

Copied from [`autox-my/req`](https://github.com/autox-my/req) at the `rev-3294a46` release (ADR 0054, E-1), then adapted
for this demo:

- `PAGES_URL` is this site.
- The single component overlay is `docs/components.archify.json`, rendered at `components.html`.

The page is generated; run:

```bash
python3 tools/explorer/build.py --req build/req-release/req --out docs/explorer.html
python3 tools/explorer/build.py --req build/req-release/req --check docs/explorer.html
```

It reads the first line of `.req/variants` (`steering_side=left`) as its selection.
