# Build stage
FROM node:18-alpine as build

WORKDIR /app

ARG BUILD_DATE
ENV BUILD_DATE=$BUILD_DATE

COPY package*.json ./
RUN npm ci

COPY . .

# Pass build arguments to environment variables
ARG REACT_APP_API_URL
ARG REACT_APP_GOOGLE_ANALYTICS_ID
ENV REACT_APP_API_URL=$REACT_APP_API_URL
ENV REACT_APP_GOOGLE_ANALYTICS_ID=$REACT_APP_GOOGLE_ANALYTICS_ID

# Build the app
RUN npm run build

# Production stage
FROM node:18-alpine

WORKDIR /app

COPY --from=build /app/build ./build
COPY --from=build /app/package.json ./
COPY --from=build /app/package-lock.json ./

RUN npm install -g serve

EXPOSE 3000

CMD ["serve", "-s", "build", "-l", "3000"]

LABEL org.opencontainers.image.source https://github.com/mrcord/howtofinddrugsonline