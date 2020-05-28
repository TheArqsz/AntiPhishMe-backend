FROM python:3.8-alpine

USER root

RUN apk upgrade --update && \
    apk add --no-cache postgresql-dev gcc python3-dev musl-dev

# Add dependencies for crt.sh
RUN apk add --no-cache libxml2-dev libxslt-dev

RUN mkdir -p /home/gunicorn && \
    adduser --home /home/gunicorn --disabled-password gunicorn 

USER gunicorn
WORKDIR /home/gunicorn

COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt 
    
ENV PATH="/home/gunicorn/.local/bin:${PATH}"

COPY --chown=gunicorn:gunicorn ./antiphishme/src/ /home/gunicorn/

EXPOSE 5000

ENTRYPOINT ["gunicorn"]

CMD ["-c=gunicorn.conf.py", "app:connexion_app"]