FROM python:3.9-buster

RUN mkdir /filter-deep
RUN pip install -U pip
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY ./requirements.txt ./filter-deep/requirements.txt
RUN pip install facexlib
RUN pip install basicsr
RUN pip install --no-compile  -r /filter-deep/requirements.txt
ENV PYTHONWARNINGS ignore
ENV PYTHONDONTWRITEBYTECODE=true
ENV PYTHONUNBUFFERED 1
ENV PATH="${PATH}:/root/.local/bin"
ENV PYTHONPATH=.

COPY . /filter-deep/

WORKDIR /filter-deep
CMD ["run_web.sh"]

