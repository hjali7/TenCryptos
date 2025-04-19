# ================================
# STAGE 1: Install dependencies
# ================================
FROM node:20 AS deps

WORKDIR /app

COPY package*.json ./

RUN npm install

# ================================
# STAGE 2: Development Image
# ================================
FROM node:20 AS dev

WORKDIR /app

# فقط node_modules از استیج قبل
COPY --from=deps /app/node_modules ./node_modules

# باقی کدها mount میشن از بیرون → volume
EXPOSE 3000

CMD ["npm", "run", "dev"]