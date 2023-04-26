

# LLM Using a Search API

**Author:** Felix Nützel  
**Date:** April 2023

## Method description

- LLM gets instructions on how to send requests to an index search API, [Example](https://github.com/T-Lycett/Auto-GPT/blob/master/scripts/data/prompt.txt)
- Search API returns result based on provided key words
- LLM generates a response based on the provided result
- also possible to have a separate application that handles the search and the LLM only gets the resulting document and a prompt, [Example](https://medium.com/@imicknl/how-to-create-a-private-chatgpt-with-your-own-data-15754e6378a1)

## Advantages

- Simplicity: This method can be seen as the simpler variant of the semantic search approach
- No additional training required
- Extraction and augmentation of data not necessarily needed, since confluence already offers an [index search API](https://developer.atlassian.com/server/confluence/confluence-server-rest-api/)
- Allows for rights management of the accessed data

## Disadvantages

- Would only provide data found by keyword matching
- LLM needs to be able to follow instructions to make API calls

## Required Services

- LLM that can follow instructions / can make API calls
  - [GPT-4](https://openai.com/research/gpt-4): The popular LLM by OpenAI
  - [Alpaca](https://github.com/tatsu-lab/stanford_alpaca): Instruction following variant of  LLaMA developed by Stanford   
  - [Dolly 2.0](https://huggingface.co/databricks/dolly-v2-7b): Instruction following LLM by databricks 
  - [LlamaIndex](https://github.com/jerryjliu/llama_index?ref=mattboegner.com): Interface to connect a LLM with external data
- Perhaps something like the [retrieval plugin](https://github.com/openai/chatgpt-retrieval-plugin), or our own implementation of such a plugin, see [Intro](https://platform.openai.com/docs/plugins/introduction), [Example](https://platform.openai.com/docs/plugins/examples)

## Licence Restrictions

- Alpaca License: CC BY NC 4.0, which means it cannot be used for commercial purposes, but freely for research purposes
- Dolly 2.0 License: MIT
- GPT-4 License: Proprietary
- LlamaIndex License: MIT

## Customizability for Own Training Data

- Limited, preamble instructions can modify the output and search queries to a degree

## Cost for Training & Training Effort

- No explicit training of the weights would be needed

## Development Effort

- Among our three proposed approaches, this one would probably require the least amount of effort

## Comment

During my research on this topic, it became apparent that most sources view index search as merely the "first step" of the semantic search approach. Most of the time, articles which discussed using an LLM in combination with a search API culminated in using semantic search or just used semantic search in the first place. Therefore, starting with the easier index search and refining it into semantic search seems like a possible approach for us. Generally, there don't seem to be many resources out there that focus on index search, the vast majority of it is related to semantic search.

Also, we could write something similar to the retrieval-plugin by OpenAI, or [port it to another LLM](https://blog.lastmileai.dev/using-openais-retrieval-plugin-with-llama-d2e0b6732f14), or just use the retrieval-plugin itself.
The most straightforward approach without relying on OpenAI would probably be: 
Give a LLM instructions how to make confluence API calls &rarr; LLM summarizes the result document &rarr; Provides answer to user. However, this will probably not be enough to achieve a satisfactory level of performance. Therefore, we should rather use the semantic search approach in my opinion.
