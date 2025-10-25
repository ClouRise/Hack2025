FROM node:alpine as build

WORKDIR /app
COPY package.json package-lock.json ./

RUN npm install 

COPY . . 
RUN npm run build

FROM nginx:stable-alpine

RUN rm -rf /etc/nginx/conf.d/*

COPY --from=build /app/dist /usr/share/nginx/html

# COPY ./nginx/nginx.conf /etc/nginx/nginx.conf

RUN chown -R nginx:nginx /usr/share/nginx/html \
    && chmod -R 755 /usr/share/nginx/html

RUN mkdir -p /app/media /app/static