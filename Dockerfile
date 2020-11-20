FROM python:3
WORKDIR /usr/
COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt
EXPOSE 8080
CMD [ "bash", "./start_flask.sh"]