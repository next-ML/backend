FROM python:3.6
COPY . /server
WORKDIR /server
RUN pip install --upgrade pip && \
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

EXPOSE 8080

CMD ["python", "run.py", "--host", "0.0.0.0"]

# sudo docker run --name mlservice --net nextml-net -p 38383:80 xiaoziyang/nextml_backend