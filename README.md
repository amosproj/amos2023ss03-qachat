# QAChat in Cooperation with QAWARE (AMOS SS 2023)

<p align="center">
  <img src="./QAChat/assets/QAware.png" alt="" width="250"/>
</p>

## Quicklinks
- [About](#About)
- [Vision](#Vision)
- [Setup](#Setup)
- [Documentation](#Documentation)
- [Development-Rules](#Development-Rules)
- [LLM-Research](/Documentation/LLM-Research/LLM-Research.md)
- [Slackbot](/QAChat/SlackBot/README.md)

## About
*QAChat* evaluates newly developed LLMs for the use in a chatbot. The best suited network is trained on provided data that is collected from existing communication and documentation sources. The model is available for users to ask questions through a Slack bot integration.

## Vision
In recent times, LLMs have evolved rapidly, opening up new, previously unimagined areas of application. *QAChat* takes advantage of these developments to provide users with a simple and convenient point of contact. This allows a general language model to be trained on specific knowledge and thus answer context-specific questions through an interface integrated into an already used communication tool.


## Setup
1. First Step

## Documentation
- For the Team Google Sheet go to: [Google Sheet](https://docs.google.com/spreadsheets/d/1YPjbiAhNvHcSZrW76hD67fqGCg3-shARfk5d4C8jOtA)

- For other Documentation go to: [Documentation Folder](/Documentation/README.md)

## Development-Rules

*Branch Rules & Integration*

1. When developing a new Feature / Working on an Issue with fragments that get uploaded, create a new brnach from the main branch with follwing naming shema: **category/IssueNumber_Feature_name**

- category is one of the following: fix / feature / refactoring / doc 
- IssueNumber: The number the issue has in the github project board, to better track branches to issues
-  Feature_name: the last part of the branch name is the feature name. This should give a short understandable summary of the feature/issue

2. Before integrating the code into the main-branch, a Pull-Request must be created, that at least one other developer reviews with a an "Approve"-Review and no outstanding requested changes.

3. Furthermore a branch is only then merged into main, when it is tested and will not break the project.

4. If checks are implemented, check if they run sucessfully

*Coding Guidelines*

1. Name variables and class names with a fitting and meaningfull name.

2. Use CamelCase-Naming for names with multiple parts.

3. ...

