# ---------- Stage 1: build Vue ----------
FROM node:22-slim AS builder
WORKDIR /app

COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

COPY frontend/ .
RUN npm run build

# ---------- Stage 2: nginx runtime ----------
FROM nginx:1.27-alpine-slim

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx/default.conf /etc/nginx/conf.d/default.conf

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s \
    CMD wget -qO- http://localhost/ || exit 1

EXPOSE 80