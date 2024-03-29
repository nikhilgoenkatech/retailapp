FROM ubuntu:20.04

RUN echo "locales locales/locales_to_be_generated multiselect en_US.UTF-8 UTF-8" | debconf-set-selections \
    && echo "locales locales/default_environment_locale select en_US.UTF-8" | debconf-set-selections \
    && apt-get update \
    && apt-get --yes --no-install-recommends install \
        locales tzdata ca-certificates sudo \
        bash-completion iproute2 tar unzip curl rsync vim nano tree \
    && rm -rf /var/lib/apt/lists/*
ENV LANG en_US.UTF-8


# Install Python stack
RUN apt-get update \
    && apt-get --yes --no-install-recommends install \
        python3 python3-dev \
        python3-pip python3-venv python3-wheel python3-setuptools \
        build-essential cmake \
        graphviz git openssh-client \
            libjpeg-turbo-progs \
    libjpeg8-dev \
    liblcms2-dev \

        libssl-dev libffi-dev \
    && rm -rf /var/lib/apt/lists/*


RUN apt-get install python3.6

RUN pip3 install pillow
# install dependencies
RUN apt-get install git
RUN pip install --upgrade pip

RUN git clone https://github.com/nikhilgoenkatech/retailapp.git
RUN pip3 install -r retailapp/requirements.txt
RUN pip3 install uwsgi
RUN pip3 install autodynatrace
RUN pip3 install whitenoise

ENV STRIPE_SECRET_KEY="My-secret-key"
ENV STRIPE_PUBLISHABLE_KEY="My-stripe-key"
ENV EMAIL_HOST_USER="HOST_USER"
ENV EMAIL_HOST_PASSWORD="Password"
ENV AUTOWRAPT_BOOTSTRAP=autodynatrace

WORKDIR retailapp/src
RUN python3.8 manage.py collectstatic --noinput

EXPOSE 3005
CMD ["gunicorn", "--bind", "0.0.0.0:3005", "ecommerce.wsgi:application"]
