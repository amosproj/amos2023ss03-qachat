FROM python:3.10

COPY . /QAChat/Data_Processing/

WORKDIR /QAChat/Data_Processing

RUN pip install -r requirements.txt

RUN rm -f requirements.txt

RUN python -m spacy download xx_ent_wiki_sm
RUN python -m spacy download de_core_news_sm

ENV PYTHONPATH=$PYTHONPATH:/

ENTRYPOINT ["python", "main.py"]