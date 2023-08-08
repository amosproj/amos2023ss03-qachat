FROM python:3.10

COPY . /QAChat/Slack_Bot/

WORKDIR /QAChat/Slack_Bot

RUN pip install -r requirements.txt

RUN rm -f requirements.txt

ENV PYTHONPATH=$PYTHONPATH:/

ENTRYPOINT ["python", "qa_agent.py"]