FROM python:3.6.4


# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# add requirements
COPY ./requirements.txt /usr/src/app/requirements.txt

# install requirements
RUN pip install -r requirements.txt

# add app
COPY . /usr/src/app


EXPOSE 5000

# run server
CMD ["gunicorn", "m_blog.wsgi"]