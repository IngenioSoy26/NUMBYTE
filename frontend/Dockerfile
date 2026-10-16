# ---------- Etapa 1: compilar la app de React con Vite ----------
FROM node:22-alpine AS build
WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

# Railway inyecta las variables del servicio como build args cuando se declaran
# con ARG. Vite solo expone al bundle las variables con prefijo VITE_.
# Ejemplo en Railway: VITE_API_URL=https://numbyte-backend.up.railway.app/api
ARG VITE_API_URL
ENV VITE_API_URL=${VITE_API_URL}

RUN npm run build

# ---------- Etapa 2: servir los estáticos con nginx ----------
FROM nginx:1.27-alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx/default.conf.template /etc/nginx/templates/default.conf.template

# El entrypoint de nginx sustituye ${PORT} en la plantilla. Railway define PORT;
# en local se usa 80.
ENV PORT=80
EXPOSE 80
