FROM node:20-alpine AS builder

WORKDIR /app

COPY . .

WORKDIR /app/quizhub

RUN npm install
RUN npm run build

FROM nginx:alpine

COPY --from=builder /app/quizhub/build /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]