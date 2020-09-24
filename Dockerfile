FROM node:12-slim

# Non-root user `app`
RUN useradd --create-home -s /bin/bash app
WORKDIR /home/app

# Install dependencies and build
COPY package.json .
COPY yarn.lock .
RUN yarn

COPY . .
RUN yarn build
RUN yarn --production

# Change to user `app`
RUN chown -R app:app /home/app
USER app

CMD [ "yarn", "start" ]
