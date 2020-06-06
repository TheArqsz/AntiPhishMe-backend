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

RUN pip install --no-cache-dir -r requirements.txt 
    
ENV PATH="/home/gunicorn/.local/bin:${PATH}"

COPY --chown=gunicorn:gunicorn ./ /home/gunicorn/

EXPOSE 5000

ENTRYPOINT ["gunicorn"]

CMD ["-c=antiphishme/src/gunicorn.conf.py", "antiphishme.src.app:connexion_app"]