FROM python:3.9

WORKDIR /app
ARG requirements=requirements.txt

COPY . /app

# RUN pip install --no-cache-dir -e .
RUN pip install --no-cache-dir -r $requirements

CMD ["python3", "-u" , "__main__.py"]
