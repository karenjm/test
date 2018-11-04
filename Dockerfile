FROM python:3.6-alpine

WORKDIR /opt/app
COPY pip-packages.txt views.py actions.py ./

RUN pip install --no-cache-dir -r pip-packages.txt

CMD ["flask", "run"
ENTRYPOINT ["flask", "run"]
