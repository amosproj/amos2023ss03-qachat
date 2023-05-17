# QABot - Setup Guide

Author: Hafidz Arifin Date: 17.05.23
Author: Jesse Palarus Date: 17.05.23

This is a simple guide to setting up and running the QABot.

The QABot is a Python application that uses the instructor-xl for embedding from HuggingFace and the wizard-mega LLM
model to answer user questions based on the context retrieved from a Supabase database.

### Configuration

To configure the QABot you need to create a tokens.env located in the QAChat directory.

The environment variables you need to set are:

- SUPABASE_URL: The URL of your Supabase database
- SUPABASE_SERVICE_KEY: The service key for your Supabase database
- DEEPL_TOKEN: The token for DeepL translation service

You can set these variables in the tokens.env file like this:

````
SUPABASE_URL=<your-supabase-url>
SUPABASE_SERVICE_KEY=<your-supabase-service-key>
DEEPL_TOKEN=<your-deepl-token>
````

Please replace `<your-supabase-url>`, `<your-supabase-service-key>`, and `<your-deepl-token>` with your actual Supabase
URL,
Supabase service key, and DeepL token respectively.

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