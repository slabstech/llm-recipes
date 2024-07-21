# Stage 1: Build
FROM node:alpine as builder

WORKDIR /app

COPY package*.json ./

RUN npm install -g typescript vite
RUN npm install

COPY . .

RUN npm run build

## Stage 2 : deploy

FROM nginx:latest as prod

COPY --from=builder /app/dist /usr/share/nginx/html

CMD ["nginx", "-g", "daemon off;"]
