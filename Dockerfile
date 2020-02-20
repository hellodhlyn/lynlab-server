FROM node:12-slim

WORKDIR /usr/src/app

COPY package.json .
COPY yarn.lock .
RUN yarn --production

COPY . .
RUN yarn build

EXPOSE 1337
ENV NODE_ENV production

CMD ["yarn", "start"]
