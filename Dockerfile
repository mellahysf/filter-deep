FROM python:3.8

COPY . /app/filter

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install facexlib
RUN pip install basicsr
RUN pip install -r /app/filter/requirements.txt


ENTRYPOINT ["python"]
CMD ["/app/filter/main.py"]

