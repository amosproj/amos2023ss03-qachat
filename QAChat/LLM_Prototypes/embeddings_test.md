# Embeddings Test

To test the different embedding algorithms, we have created three datasets with question and answer pairs (200 each). One consists of English questions, one of German questions, and the other is the German translated into English using DeepL.

We have now embedded all the answers and checked how close the embedding of the question is to the correct answer. (3 points if it was the closest, 2 points if it was the second closest, and 1 point if it was the third closest)

In total, one can achieve a maximum score of 600 points.

## Results

| Score                 | OpenAI | LLaMA | Instruct | E5  | Gecko |
|-----------------------|--------|-------|----------|-----|-------|
| English               | 563    |   34  | 576      | 525 | 562   |
| German                | 501    |   63  | 473      | 355 | 462   |
| German + DeepL        | 476    |       | 491      | 424 | 494   |
