FROM node:alpine AS builder

WORKDIR /app
COPY . .
RUN npm install && npm run build

FROM nginx:alpine
COPY --from=builder /app/dist/* /usr/share/nginx/html/
COPY start.sh /usr/share/nginx/html/start.sh

CMD ["/bin/sh",  "/usr/share/nginx/html/start.sh"]
