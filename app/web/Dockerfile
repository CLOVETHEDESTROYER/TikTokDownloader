FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY app/web/package*.json ./

# Install dependencies and update package-lock.json
RUN npm install

# Copy the Next.js configuration files
COPY app/web/next.config.js ./
COPY app/web/tsconfig.json ./
COPY app/web/tailwind.config.js ./
COPY app/web/postcss.config.mjs ./

# Copy the source code
COPY app/web/src ./src
COPY app/web/public ./public

# Build-time arguments
ARG NEXT_PUBLIC_API_URL
ARG NEXT_PUBLIC_WEBSITE_API_KEY

# Set environment variables for build time
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_WEBSITE_API_KEY=$NEXT_PUBLIC_WEBSITE_API_KEY
ENV NODE_ENV=production

# Build the application
RUN npm run build

# Production image, copy all the files and run next
FROM node:18-alpine AS runner

WORKDIR /app

# Copy built assets from builder
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public

# Runtime environment variables
ENV NODE_ENV=production
ENV PORT=3000
ENV HOSTNAME=0.0.0.0

# Start the application
CMD ["node", "server.js"] 