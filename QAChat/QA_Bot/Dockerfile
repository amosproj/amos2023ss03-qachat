FROM python:3.10

COPY . /QAChat/QA_Bot/

WORKDIR /QAChat/QA_Bot

RUN pip install -r requirements.txt

RUN rm -f requirements.txt

RUN python -m spacy download xx_ent_wiki_sm
RUN python -m spacy download de_core_news_sm

ENV PYTHONPATH=$PYTHONPATH:/

ENTRYPOINT ["python", "qa_bot.py"]