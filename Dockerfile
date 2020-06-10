FROM python:3.7-alpine
WORKDIR /home/minibank
ADD . /home/minibank
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python3","app.py"]
