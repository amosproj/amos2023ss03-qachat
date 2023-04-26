# Finetune LLM Models 
Author: Jesse Palarus Date: 23.04.23
### Description
Finetuning is the process of training an LLM on a smaller, task-specific dataset, allowing the model to finetune its knowledge and adapt to particular use cases.
To do so, the (some) weights of the LLM are unfrozen and trained with the task-specific dataset. 

During finetuning, the LLM is optimized to perform well on the specific task by adjusting its weights to minimize the loss function, which measures the difference between the model's predictions and the actual target outcomes in the task-specific dataset, e.g. masked language modelling.
### Advantages
- when unfreezing most of the weights and having a lot of data, the model can learn complex interrelationships between the input
- when unfreezing some weights, we can train to model to act like a real person in a QA Team 
- Prediction, when trained, is cheap
### Disadvantages
- when unfreezing all weights, it is really really expensive to train (several million euros)
- also high costs when only unfreezing a few weights (≈500€)
- when unfreezing some weights, the model will probably not learn any new information. Instead, when asking it a question without context, it will probably start hallucinating
- must be trained again when new information is available
- no access rights system
### Services
- OpenAI finetuning (Ada, Babbage, Curie, Davinici)
- ChatGPT for self-instruct finetuning
- Custom finetune of an open source model (like LLama or Alpaca) using a Cloud Provider
  - Google Cloud
  - AWS
  - Azure
  - Nvidia Dataset
### Licence
- Licences of open-source models are a little bit unclear
- OpenAIs Licence for finetuning seems to be no problem
### Customizability for own training data
- for effective finetuning of new information, a lot of own data is required and a lot of resource power
### Effort
- when using OpenAI, it should be straightforward since OpenAI does everything for us
- when using the open source model, there are tones of example codes, so the implementation should be easy, but the training will probably need a few days
### Comments
A few technical comments:
- Use a small learning rate that increases in the first epochs
- A GPU with a lot of VRAM or a lot of GPUs are required
- Use Optimizer such as ZeRO, AdamW or colossal

TLDR:

In my opinion, this approach is, with our resources, unable to learn the things needed for a Q&A Bot.
But we can combine it with another approach to improve the output format better.

For example, when the user asks what to do when I am sick, the answer from an LLM with semantic search could be: "You must submit a sick note."

With a finetuned & semantic search, we could archive something more like this: "Hallo Max, thanks for asking me that question. When you are sick, you should submit a sick note. If you have any more questions, feel free to ask."
### links / sources
- [OpenAI Finetuning](https://platform.openai.com/docs/guides/fine-tuning)
- [Guide to finetune LLama](https://lightning.ai/pages/community/tutorial/accelerating-llama-with-fabric-a-comprehensive-guide-to-training-and-fine-tuning-llama/)
- [Colossal website](https://colossalai.org/)
- [Alpaca website explaining how the use self instructions](https://crfm.stanford.edu/2023/03/13/alpaca.html)