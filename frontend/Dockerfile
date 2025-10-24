FROM node:alpine

WORKDIR /app
COPY package.json .
RUN npm build

COPY . . 
RUN npm run build

FROM nginx:stable-alpine

RUN rm -f /etc/nginx/conf.d/default.conf

COPY --from=build /app/dist /usr/share/nginx/html

RUN chown -R nginx:nginx /usr/share/nginx/html \
    && chmod -R 755 /usr/share/nginx/html

RUN mkdir -p /app/media /app/static