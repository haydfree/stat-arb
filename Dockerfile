FROM python:3.11
WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt
EXPOSE 80
ENV FLASK_APP=app.py
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "80"]
