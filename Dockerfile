FROM python:3.8
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
ENV NAME AutoLink
EXPOSE 3000
CMD ["python", "autolink.py"]