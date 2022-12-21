FROM python:3.7.14

COPY requirements.txt /
ADD ./mask /mask
ADD ./data /data
ADD ./nerm /nerm
COPY index.py /

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN set -ex && \ 
    pip install -r requirements.txt

CMD ["python", "index.py"]