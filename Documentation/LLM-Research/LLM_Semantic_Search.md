

# LLM Using Semantic Search

**Author:** Amela Pucic
**Date:** April 2023

## Method description

- Searching by meaning (No Strg F)
- represent words as vectors in an embedding Space
- vectors that are close to each other represent similar context (words with similar Context: Tea, Coffee, words with not so similar Contex: Tea, Pea)
- compare vector with [cosine similarity](https://en.wikipedia.org/wiki/Cosine_similarity)

## Adventages

- Tools and Youtube contant available
- price
- improves quality of search
- good results
- possibility to add Data

## Disadvantages

- requieres large amonts of data
- lack of transparency (complex algorithm)
- can not create new Informations

## Requiered Services
  
- LLM (resource to train effectively)
  - GPT-3, text-davinci-003, tokenlimit: 4,000
  - OpenAi
  - Cohere
  - Huggingfaces
  - Alpaca
  - Llama
- Model to create Embeddings 
  - OpenAI
  - Word2Vec 
  - GloVe  
  - Bert
- Vectordatabase for the Embeddings
  - Apache Lucene 
  - Supabase 
  - ElasticSearch 
  - Faiss
- [Langchain](https://python.langchain.com/en/latest/index.html)
  - Tool to create and save embeddings and ask questions

## Licence Restrictions

- MIT License (Langchain, OpenAI, Alpaca, faiss, Cohere)
- GNU General Public License v3.0 (Llama)
- Apache License 2.0 (Supabase, Word2Vec, GloVe, Bert, Lucene, Huggingfaces)
- Elastic-Lizenz (ElasticSearch)

## Cost for Training 

- [Supa Base](https://supabase.com/pricing)
- Open AI
  - You need a OpenAI Key (I think its for free at the moment with OpenAI Account) 
- [Price Azure Microsoft](https://azure.microsoft.com/de-de/pricing/details/search/)

## Training/Development Effort

- available Data
- choice of model
- hardware resources

## Comments
It would be quite important to speak about the Data
  - where do we get the data from?
  - which database does the customer want us to use
  
Maybe we should speak about the Pre-Transforming
  - where do we want to split the data (after a token limit, after each sentence)
