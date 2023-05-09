# T5 with Langchain
**Author:** Amela Pucic, Hafidz Arifin, Jesse Palarus
**Date:** May 2023

## Requirements
* Import necessary python package:
    * [langchain](https://pypi.org/project/langchain/)
    * [huggingface_hub](https://pypi.org/project/huggingface-hub/)
    * [LLaMM.cpp](https://pypi.org/project/llama-cpp-python/)

## Results

We ran a benchmark to test the LLMs (language model) by creating an English and German dataset with Chatgpt. We provided the LLM with questions along with their corresponding answers and unrelated answers to see if the model outputs a correct answer. One point was awarded for each correct answer and no points were given for incorrect answers. A total of 20 points could be achieved. 
 
Additionally, we tested whether the model hallucinates, also for German and English. We gave the LLM a question and three unrelated answers and checked if the model hallucinates. If the model hallucinates, no points were awarded. If the model outputs that it does not have an answer to the question, one point was given, as the answer is correct. A total of 20 points could be achieved.


| Score                 | Alpaca | ChatGPT | OASST | GPT | Vicuna |
|-----------------------|--------|---------|-------|-----|--------|
| German                | 7      | 20      | 16    | 20  | 20     |
| English               | 11     | 20      | 20    | 20  | 19     |
| German  Hallucinating | 4      | 16      | 3     | 3   | 6      |
| English Hallucinating | 6      | 15      | 3     | 3   | 10     |


