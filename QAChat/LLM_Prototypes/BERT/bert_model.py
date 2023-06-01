# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Jesse Palarus

import torch
from transformers import AutoTokenizer, AutoModelForQuestionAnswering


def get_reply(question, context):
    tokenizer = AutoTokenizer.from_pretrained(
        "bert-large-uncased-whole-word-masking-finetuned-squad"
    )
    model = AutoModelForQuestionAnswering.from_pretrained(
        "bert-large-uncased-whole-word-masking-finetuned-squad"
    )

    inputs = tokenizer(
        question, context, return_tensors="pt", truncation=True, padding=True
    )

    # Get the model's predictions
    outputs = model(**inputs)

    # Get the predicted start and end positions of the answer
    answer_start = torch.argmax(outputs.start_logits, dim=-1).item()
    answer_end = torch.argmax(outputs.end_logits, dim=-1).item()

    # Tokenize the input without special tokens to map the positions back to the input
    tokens = tokenizer.tokenize(context)

    # Check if the answer is valid (start position is before the end position)
    if answer_start <= answer_end:
        # Get the answer from the context
        input_ids = inputs["input_ids"][0]
        answer = tokenizer.decode(
            input_ids[answer_start : answer_end + 1], skip_special_tokens=True
        )
    else:
        answer = "I'm not sure."

    return answer


if __name__ == "__main__":
    context = (
        "QAware manages SAP upgrades by evaluating the current system,"
        " identifying the required changes, and following a thorough planning"
        " and execution process to ensure a seamless transition.\n"
        "QAware assists clients with SAP integration by designing tailored solutions,"
        " leveraging appropriate middleware, and ensuring seamless data flow between SAP"
        " and external systems.\nQAware offers SAP consulting services, assisting clients in"
        " selecting suitable SAP modules, optimizing processes, and developing strategies for "
        "successful SAP adoption.\nTo develop a new SAP IDoc, access transaction WE31 and "
        "follow the necessary steps to create a new segment, then use transaction WE30 to create "
        "the IDoc type and assign the new segment."
    )

    question = "How does QAware handle SAP system upgrades for its clients?"
    print(get_reply(question, context))
