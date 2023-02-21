FROM python:3.8

COPY . /app/filter

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install facexlib
RUN pip install basicsr==1.3.5
RUN pip install -r /app/filter/requirements.txt

RUN ls -l
RUN pwd

ENTRYPOINT ["python"]
CMD ["/app/filter/main.py"]

