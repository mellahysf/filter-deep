FROM python:3.9

COPY . /app/filter

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install facexlib
RUN pip install basicsr==1.3.5
RUN pip install -r /app/filter/requirements.txt

RUN apt install -y curl && \
    curl -L "https://github.com/xinntao/facexlib/releases/download/v0.1.0/detection_Resnet50_Final.pth" -o "/usr/local/lib/python3.9/site-packages/facexlib/weights/detection_Resnet50_Final.pth" && \
    apt remove -y curl
    
RUN ls -l
RUN pwd

ENTRYPOINT ["python"]
CMD ["/app/filter/main.py"]

