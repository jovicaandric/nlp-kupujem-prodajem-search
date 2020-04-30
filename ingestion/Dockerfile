FROM node

# Create app directory
RUN mkdir -p /app
WORKDIR /app

# Install app dependencies
COPY package.json /app
COPY package-lock.json /app
RUN npm i
RUN npm i -g forever

# Bundle app source
COPY . /app

CMD [ "npm", "start" ]