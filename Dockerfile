FROM previ/opencv

#FROM lucas/opencv

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . /usr/src/app

EXPOSE 80

CMD ["./run_app.sh"]