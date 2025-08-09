# FROM node:20-alpine      # <- switch this out if you had it

FROM node:20              
 # <- use this for a more complete image with npm, git, etc.]

WORKDIR /app
COPY package.json /app/package.json
RUN npm install
COPY . /app

# expose vite port if you want
EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
