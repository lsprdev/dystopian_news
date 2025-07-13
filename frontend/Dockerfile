# -------- 1. Fase de deps --------
FROM node:20-alpine AS deps
WORKDIR /app

# Copia apenas manifests para cache de dependências
COPY package.json package-lock.json* pnpm-lock.yaml* yarn.lock* ./

# Instala sem libs dev — apenas para compilar
RUN npm ci --prefer-offline --no-audit --progress=false

# -------- 2. Fase de build --------
FROM node:20-alpine AS builder
WORKDIR /app

# Copia node_modules já instalados
COPY --from=deps /app/node_modules ./node_modules

# Copia todo o código
COPY . .

# Constrói a aplicação (gera .next/** e standalone/server.js)
RUN npm run build

# -------- 3. Fase de runtime --------
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV PORT=3000

# Copia apenas o que é preciso para rodar em prod
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

# Next já procura PORT
EXPOSE 3000
CMD ["node", "server.js"]
