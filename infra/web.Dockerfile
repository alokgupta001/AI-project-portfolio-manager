ARG NODE_IMAGE=node:24-bookworm-slim@sha256:0e0ff40c39bc087845bfb27465a0df4ea419520094bc35842ff83dd8cbe6f9b6
FROM ${NODE_IMAGE}
ENV NEXT_TELEMETRY_DISABLED=1
WORKDIR /app
COPY package.json package-lock.json ./
COPY apps/web/package.json apps/web/package.json
COPY packages/contracts/package.json packages/contracts/package.json
RUN npm ci --no-audit --no-fund
COPY apps/web ./apps/web
COPY packages/contracts ./packages/contracts
RUN npm run build && chown -R node:node /app/apps/web/.next
USER node
ENV NODE_ENV=production
EXPOSE 3000
CMD ["npm", "run", "start"]
