# Build stage
FROM --platform=linux/amd64 node:20-alpine AS builder

WORKDIR /app

COPY hardware-telemetry-ui/package*.json ./
RUN npm ci

COPY hardware-telemetry-ui/ ./
RUN npm run build

# Production stage
FROM node:20-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production

RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 sveltekit

COPY --from=builder /app/build /app/build
COPY --from=builder /app/package*.json ./

USER sveltekit

EXPOSE 3000

CMD ["node", "build/index.js"]
