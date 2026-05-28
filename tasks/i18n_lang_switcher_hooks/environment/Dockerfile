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

# Scaffold a minimal SvelteKit project (Svelte 5 + Node adapter) at /home/user/sveltekit-i18n.
# The executor will implement the i18n behaviour inside this scaffold.
RUN mkdir -p /home/user/sveltekit-i18n/src/routes && \
    mkdir -p /home/user/sveltekit-i18n/static

RUN cat > /home/user/sveltekit-i18n/package.json <<'EOF'
{
  "name": "sveltekit-i18n",
  "private": true,
  "version": "0.0.1",
  "type": "module",
  "scripts": {
    "dev": "vite dev",
    "build": "vite build",
    "preview": "vite preview",
    "start": "node build"
  },
  "devDependencies": {
    "@sveltejs/adapter-node": "^5.2.12",
    "@sveltejs/kit": "^2.20.0",
    "@sveltejs/vite-plugin-svelte": "^5.0.3",
    "svelte": "^5.20.0",
    "typescript": "^5.5.0",
    "vite": "^6.0.0"
  }
}
EOF

RUN cat > /home/user/sveltekit-i18n/svelte.config.js <<'EOF'
import adapter from '@sveltejs/adapter-node';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
    preprocess: vitePreprocess(),
    kit: {
        adapter: adapter()
    }
};

export default config;
EOF

RUN cat > /home/user/sveltekit-i18n/vite.config.js <<'EOF'
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
    plugins: [sveltekit()]
});
EOF

RUN cat > /home/user/sveltekit-i18n/jsconfig.json <<'EOF'
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
EOF

RUN cat > /home/user/sveltekit-i18n/src/app.html <<'EOF'
<!doctype html>
<html lang="en">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        %sveltekit.head%
    </head>
    <body data-sveltekit-preload-data="hover">
        <div style="display: contents">%sveltekit.body%</div>
    </body>
</html>
EOF

RUN cat > /home/user/sveltekit-i18n/src/routes/+page.svelte <<'EOF'
<h1>Hello from SvelteKit. Implement the i18n switcher here.</h1>
EOF

RUN cat > /home/user/sveltekit-i18n/.gitignore <<'EOF'
node_modules
/build
/.svelte-kit
/package
.env
.env.*
!.env.example
vite.config.js.timestamp-*
vite.config.ts.timestamp-*
EOF

# Install dependencies so the project is ready for the executor to build immediately.
RUN cd /home/user/sveltekit-i18n && \
    npm install --no-audit --no-fund && \
    npx svelte-kit sync || true

LABEL Author="generate-harbor-tasks"
LABEL Description="SvelteKit i18n locale switcher task: pre-scaffolded SvelteKit (Svelte 5 + adapter-node) project under /home/user/sveltekit-i18n with browser verification stack."

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]

# Container contents:
#   - always required apt packages: curl wget ca-certificates git python3 python3-pip python3-pytest bash ripgrep
#   - always required pip3 packages: pytest-json-ctrf
#   - Node.js v24, npm
#   - browser verification dependencies: agent-browser, pochi-verifier, ffmpeg, X11/GTK shared libs
#   - python helpers for tests: requests, pytest-xprocess
#   - /home/user/sveltekit-i18n: pre-scaffolded SvelteKit project (Svelte 5 + @sveltejs/adapter-node)
#     containing package.json, svelte.config.js, vite.config.js, src/app.html, src/routes/+page.svelte,
#     and a populated node_modules/ directory ready for `npm run build`.
