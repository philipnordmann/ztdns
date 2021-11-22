FROM python:3
RUN mkdir -p /opt/ztdns/
COPY requirements.txt /opt/ztdns/

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /opt/ztdns/requirements.txt

COPY entrypoint.sh /opt/ztdns/
COPY ztdns.py /opt/ztdns/
CMD [ "/opt/ztdns/entrypoint.sh" ]
