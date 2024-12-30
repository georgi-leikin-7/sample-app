FROM node:20-buster-slim

RUN apt-get -y update

WORKDIR /app

COPY frontend ./

RUN npm install

EXPOSE 5173

ENTRYPOINT ["npm", "run", "dev", "--", "--host", "0.0.0.0"]