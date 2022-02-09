FROM python:3.8

COPY . /app/filter

RUN apt-get update && apt-get install -y pylint graphviz
RUN pip install facexlib
RUN pip install basicsr
RUN pip install -r /app/filter/requirements.txt

CMD ["run_web.sh"]

