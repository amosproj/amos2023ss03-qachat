# Dummy Dataset
The dummy dataset consists of three csv files (separated by a semicolon)
1. qa.csv: Question and answer pairs in english
2. qa_german.csv: Question and answer pairs in german
3. qa_translated_by_deepl: the german dataset translated by DeepL

each dataset contains of two columns one "Question" and one "Answer".
The question column consists of questions that a user can ask in our chatbot.
And the answer column contains the corresponding answer which could be somewhere in the confluence wiki.

In python you can load the data as following.
```` python
df = pd.DataFrame(columns=['Question', 'Answer'])
for index, row in data.iterrows():
    # Access the values in each row using the column names
    question = row['Question']
    answer = row['Answer']
````

(When considering the dataprepocessing (and saving new information in the vector database) the questions should of course be ignored and the answers should be considered)