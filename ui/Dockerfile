FROM node:20

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY src ./src
COPY index.html ./
COPY vite.config.ts ./
COPY postcss.config.js ./
COPY tailwind.config.js ./

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
