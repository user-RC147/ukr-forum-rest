# ---------- Stage 1: deps ----------
FROM node:22-trixie-slim AS deps

WORKDIR /app

COPY package.json package-lock.json ./

RUN --mount=type=cache,target=/root/.npm \
    npm ci

# ---------- Stage 2: dev runtime ----------
FROM node:22-trixie-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd -r appgroup && useradd -r -g appgroup -m appuser

WORKDIR /app

COPY --from=deps --chown=appuser:appgroup /app/node_modules ./node_modules
COPY --chown=appuser:appgroup . .

ENV NODE_ENV=development \
    PATH=/app/node_modules/.bin:$PATH

USER appuser

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s \
    CMD curl -f http://localhost:5173 || exit 1

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]