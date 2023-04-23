# LLM Models

# FAISS - Facebook AI Similarity Search
[FAISS](https://engineering.fb.com/2017/03/29/data-infrastructure/faiss-a-library-for-efficient-similarity-search/) is a interesting and effective library & model to do quick similarity search. It is programmed in C++ but is usable with Python.
It provides several similarity search algorithms and is optimized for memory usage & speed.

In comparison to other methods it can decrease the run time from minutes to seconds or even splitseconds and also decrease the memory usage. For a example of how to implement it and a blog see this [Medium-Article by Gabriel Salles](https://medium.com/lett-digital/nlp-efficient-semantic-similarity-search-with-faiss-facebook-ai-similarity-search-and-gpus-274771d0709a)

# Alpaca/LLaMA - Opensource LLM by Meta/Stanford
[LLaMA](https://ai.facebook.com/blog/large-language-model-llama-meta-ai/) is one of multiple variants of the alpaca model from Stanford. Its primary advantage is, that it can run on low spec hardware. It works by taking a input and predicting a next word to  generate rext recursivley. It is a versatile model that wont need to be retrained or fine-tuned to a specific task, making it more accasible to beginners.
But Non-commercial license!

# FLAN - Opensource LLM by Google
In generall more often used with Finetuning. [Documentation](https://ai.googleblog.com/2021/10/introducing-flan-more-generalizable.html)
Different Versions availabele such as:
- [BERT](https://ai.googleblog.com/2018/11/open-sourcing-bert-state-of-art-pre.html): Bidirechtional Encoder Representations from Transformers: Question answering System for Cloud TPU. The special thing apout BERT is that it is Bidirectional. Meaning each word is encoded with respect to previous and following context. But currently only in **English** available

- [T5](https://ai.googleblog.com/2020/02/exploring-transfer-learning-with-t5.html):  Flexible Text-to-Text Transformer with flexible fine-tuning options to a variety of downstram tasks. It supports multiple lanquages, such as French, German and English.