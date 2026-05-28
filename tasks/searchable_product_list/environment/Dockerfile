FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl wget ca-certificates git python3 python3-pip python3-pytest bash ripgrep \
        ffmpeg libxcb-shm0 libx11-xcb1 libx11-6 libxcb1 libxext6 libxrandr2 libxcomposite1 libxcursor1 libxdamage1 libxfixes3 libxi6 libgtk-3-0t64 libpangocairo-1.0-0 libpango-1.0-0 libatk1.0-0t64 libcairo-gobject2 libcairo2 libgdk-pixbuf-2.0-0 libxrender1 libasound2t64 libfreetype6 libfontconfig1 libdbus-1-3 libnss3 libnspr4 libatk-bridge2.0-0t64 libdrm2 libxkbcommon0 libatspi2.0-0t64 libcups2t64 libxshmfence1 libgbm1 && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm i -g agent-browser && \
    agent-browser install && \
    pip3 install --break-system-packages pytest-json-ctrf pochi-verifier requests pytest-xprocess && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

# Pre-scaffold a minimal SvelteKit (Svelte 5) project skeleton with adapter-node.
RUN mkdir -p /home/user/sveltekit-search/src/routes && \
    mkdir -p /home/user/sveltekit-search/static && \
    cat >/home/user/sveltekit-search/package.json <<'JSON'
{
  "name": "sveltekit-search",
  "version": "0.0.1",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite dev",
    "build": "vite build",
    "preview": "vite preview"
  },
  "devDependencies": {
    "@sveltejs/adapter-node": "^5.2.0",
    "@sveltejs/kit": "^2.8.0",
    "@sveltejs/vite-plugin-svelte": "^4.0.0",
    "svelte": "^5.0.0",
    "vite": "^5.4.0"
  }
}
JSON

RUN cat >/home/user/sveltekit-search/svelte.config.js <<'JS'
import adapter from '@sveltejs/adapter-node';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

const config = {
    preprocess: vitePreprocess(),
    kit: {
        adapter: adapter()
    }
};

export default config;
JS

RUN cat >/home/user/sveltekit-search/vite.config.js <<'JS'
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
    plugins: [sveltekit()]
});
JS

RUN cat >/home/user/sveltekit-search/jsconfig.json <<'JSON'
{
    "extends": "./.svelte-kit/tsconfig.json",
    "compilerOptions": {
        "allowJs": true,
        "checkJs": true,
        "esModuleInterop": true,
        "forceConsistentCasingInFileNames": true,
        "resolveJsonModule": true,
        "skipLibCheck": true,
        "sourceMap": true,
        "strict": true,
        "moduleResolution": "bundler"
    }
}
JSON

RUN cat >/home/user/sveltekit-search/src/app.html <<'HTML'
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8" />
        <link rel="icon" href="%sveltekit.assets%/favicon.png" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        %sveltekit.head%
    </head>
    <body data-sveltekit-preload-data="hover">
        <div style="display: contents">%sveltekit.body%</div>
    </body>
</html>
HTML

RUN cat >/home/user/sveltekit-search/src/routes/+page.svelte <<'SVELTE'
<h1>Welcome</h1>
<p>Replace this page with the searchable product list implementation.</p>
SVELTE

RUN cd /home/user/sveltekit-search && \
    npm install --no-audit --no-fund --silent

LABEL Author="generate-harbor-tasks"
LABEL Description="SvelteKit (Svelte 5) project skeleton with adapter-node pre-installed at /home/user/sveltekit-search for the searchable product list task, plus the browser verification environment."

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]

# Container contents:
#   - always required apt packages: curl wget ca-certificates git python3 python3-pip python3-pytest bash ripgrep
#   - always required pip3 packages: pytest-json-ctrf
#   - Node.js v24 for the SvelteKit task environment
#   - Browser verification dependencies: pochi-verifier, agent-browser, ffmpeg, and Chromium runtime libs
#   - Python verification deps: requests, pytest-xprocess
#   - /home/user/sveltekit-search: pre-scaffolded SvelteKit (Svelte 5) project with:
#     - package.json declaring svelte ^5, @sveltejs/kit ^2, @sveltejs/adapter-node ^5
#     - svelte.config.js using adapter-node
#     - vite.config.js with the SvelteKit Vite plugin
#     - jsconfig.json
#     - src/app.html and a placeholder src/routes/+page.svelte
#     - node_modules already installed
