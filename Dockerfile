FROM python:3.12.2-bookworm

COPY ./site /site

RUN pip install flask gunicorn

WORKDIR /site

EXPOSE 8000

ENTRYPOINT [ "gunicorn", "-w", "5", "-b", "0.0.0.0", "app:app" ]    