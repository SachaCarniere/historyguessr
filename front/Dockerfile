# Builder
FROM node:12.18.3-alpine as builder
# Copy the package.json to install dependencies
COPY package.json package-lock.json ./
# Install the dependencies and make the folder
RUN npm install && mkdir /front && mv ./node_modules ./front

WORKDIR /front

COPY . .
# Build the project and copy the files
RUN npm run ng build --prod


FROM nginx:alpine
## Remove default nginx index page
RUN rm -rf /usr/share/nginx/html/*
RUN chmod -R 777 /usr/share/nginx/html/
# Copy from the stahg 1
COPY --from=builder /front/dist/historyguessr /usr/share/nginx/html

EXPOSE 4200 80

ENTRYPOINT ["nginx", "-g", "daemon off;"]
