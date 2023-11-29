FROM node:19 as frontend-env

WORKDIR /frontend
ADD . /frontend

RUN npm install

FROM frontend-env as test

CMD ["npm", "run", "test"]

FROM frontend-env as lint

CMD ["npm", "run", "lint"]

FROM frontend-env as frontend-build

RUN npm run build

FROM nginx:1.15 as frontend

COPY --from=frontend-build /frontend/build/ /usr/share/nginx/html
COPY --from=frontend-build /frontend/nginx.conf /etc/nginx/conf.d/default.conf
