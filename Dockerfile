FROM python:3.8 AS build
WORKDIR ./autolink
ADD . .
RUN pip install --no-cache-dir -r requirements.txt
ENV NAME AutoLink
EXPOSE 3000
CMD ["python", "autolink.py"]