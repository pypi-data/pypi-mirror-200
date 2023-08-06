FROM node:18-alpine

RUN apk add --no-cache py3-pip g++ make libc6-compat
WORKDIR /app

COPY package.json yarn.lock* ./
RUN yarn --frozen-lockfile;
#RUN npm install -g env-cmd;

COPY . .
RUN yarn build

CMD ["yarn", "env-cmd", "-f", ".env.local", "next", "dev"]
