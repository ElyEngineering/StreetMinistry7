# Street Ministry 7 — build / preview

Static HTML/CSS/vanilla JS, no framework. Source here; publish tree is `dist/`.

## Build (only needed if photos or credits change)
    node scripts/check-required-files.mjs   # required-files guard (prebuild)
    python3 scripts/build-images.py         # grades assets-src/raw -> assets/img, builds credits.html
    rm -rf dist && mkdir -p dist/assets && cp index.html credits.html styles.css main.js dist/ && cp -r assets/img assets/fonts assets/favicon.svg dist/assets/

## Preview
    cd dist && nohup python3 -m http.server 4180 --bind 127.0.0.1 > ../server.log 2>&1 & echo $! > ../server.pid
    nohup ~/bin/cloudflared tunnel --no-autoupdate --protocol http2 --edge 198.41.192.7:7844 --edge 198.41.200.13:7844 --url http://127.0.0.1:4180 > tunnel.log 2>&1 & echo $! > tunnel.pid
    # URL appears in tunnel.log. The --edge pins are needed: box DNS maps the Cloudflare edge hostname to a proxy IP that cannot carry tunnel traffic.

## Cloudflare Pages (preferred, needs auth)
    CLOUDFLARE_API_TOKEN=... CLOUDFLARE_ACCOUNT_ID=... npx wrangler pages deploy dist --project-name jayson-van-bek-ministry

## Tear down
    ./TEARDOWN.sh
