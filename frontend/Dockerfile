FROM node:18-alpine

WORKDIR /app

COPY package.json package-lock.json /app/
# Use npm ci for reproducible installs now that package-lock.json exists
RUN npm ci --silent

COPY . /app

EXPOSE 3000

CMD ["sh", "-c", "npm run dev -- --host 0.0.0.0 --port 3000"]
