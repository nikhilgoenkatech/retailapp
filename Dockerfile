FROM python:3.8.3-alpine


# install psycopg2 dependencies
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk del build-deps \
    && apk --no-cache add musl-dev linux-headers g++

RUN apk add --no-cache jpeg-dev zlib-dev
RUN apk add --no-cache --virtual .build-deps build-base linux-headers \
    && pip install Pillow

# install dependencies
RUN apk add git
RUN pip install --upgrade pip

RUN git clone https://github.com/nikhilgoenkatech/retailapp.git
RUN pip3 install -r retailapp/requirements.txt
RUN pip3 install uwsgi
RUN pip3 install autodynatrace

ENV STRIPE_SECRET_KEY="My-secret-key"
ENV STRIPE_PUBLISHABLE_KEY="My-stripe-key"
ENV EMAIL_HOST_USER="HOST_USER"
ENV EMAIL_HOST_PASSWORD="Password"
ENV AUTOWRAPT_BOOTSTRAP=autodynatrace

WORKDIR retailapp/src
EXPOSE 3005
CMD ["gunicorn", "--bind", "0.0.0.0:3005", "ecommerce.wsgi:application"]
