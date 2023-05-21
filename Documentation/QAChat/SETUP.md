# QABot - Setup Guide

Author: Hafidz Arifin Date: 17.05.23
Author: Jesse Palarus Date: 17.05.23

This is a simple guide to setting up and running the QABot.

The QABot is a Python application that uses the instructor-xl for embedding from HuggingFace and the wizard-mega LLM
model to answer user questions based on the context retrieved from a Supabase database.

### Requirements

* Supabase account
* Access to supabase project
* Required python packages (in QAChat\environment.yml)

### Configuration

1. Create file with the name 'tokens.env' in QAChat directory.
2. Paste the following in the newly created file:
    ````
    SUPABASE_URL=<your-supabase-url>
    SUPABASE_SERVICE_KEY=<your-supabase-service-key>
    DEEPL_TOKEN=<your-deepl-token>
    ````
3. Replace `<your-supabase-url>` and `<your-supabase-service-key>` with the actual Supabase URL and Supabase service
   key. You can find it [here](https://app.supabase.com/projects) under Project 'QAChat' > Settings > API.
4. Replace `<your-deepl-token>` with actual DeepL token that was sent to you via Email from our client.

### First Run

During the first run of the QABot, it will download the required models and embeddings, which might take some time. This
is a one-time operation, and for subsequent runs, the QABot will use the previously downloaded models and embeddings.

### Running the QABot Test

To run the QABot test, navigate to the directory QA_Bot and run the following command:

```` bash
python test_qa_bot.py
````

### Performance

Currently, for testing purposes, the LLM runs on the CPU and might therefore be slower in answering questions. However,
it can be easily configured to run on GPUs for better performance.

To do so set the please firstly install the Nvidia CUDA Toolkit (requires a Nvidia GPU).
Then you can install the required packages for GPU support by running the following command:

```` bash
CMAKE_ARGS="-DLLAMA_CUBLAS=on" FORCE_CMAKE=1 pip install llama-cpp-python
````

To create now a bot using GPU support, you can pass the `use_gpu` parameter to the constructor:

```` python
bot = QABot(use_gpu=True)
````

This can be done e.g. in line 4 of the `test_qa_bot.py` file.