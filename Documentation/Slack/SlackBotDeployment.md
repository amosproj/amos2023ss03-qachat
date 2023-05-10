Author: Emanuel Erben
Date: 09.05.2023
Version:0.1

# SlackBot Deployment

There are many different ways to deploy a SlackBot. The purpose of this document is to inform the reader of the different ways to deploy your own SlackBot and make a informed decision on the way, the SlackBot should be deployed in this project.

There is also a list of Hosting providers listed on the [Slack Developer page](https://api.slack.com/docs/hosting)

## 1. Google Cloud
First of all you can create a SlackBot and Deploy it to Google Cloud. To see a more in depth how to, go to [this link](https://xebia.com/blog/how-to-create-and-deploy-a-slack-bot-on-google-cloud-platform-in-less-than-5-minutes/).
The advantage off deploying the slack bot on Google Cloud is, that the customer already has a Google Cloud Setup and therefor it could easily be added there.
The in the link decribed solution worls with a template that sets up the basic stuff like Deployment Pipeline and all. All you have to do is create the SlackBot in the Slack Settings add the credentials and your good to go to deploy it and start with implementing the logic and functionality of the ChatBot.
As Programming language it is possible to have Python Bots as well as DotNet or other Languages.

## 2. Heroku
The second solution, also something Slack itselfs describes in its development documentation is to deploy your bot to Heroku. See [Development Documentation](https://slack.dev/bolt-js/deployments/heroku). Also Heroku has its [own Documentation](https://blog.heroku.com/how-to-deploy-your-slack-bots-to-heroku) on this and I found a [Reddit post](https://www.reddit.com/r/Slack/comments/cinlbt/how_to_distribute_python_slack_bot_running_on/) where someone also created a python bot and started it on Heroku. The nice thing is, that you can start Heroku with a free account and only if you have a lot of traffic, you need to pay.


## 3. Docker - Container
Another way to deploy your own SlackBot is to start it inside a Docker-Container. With this you can start it literally on every computer or server. A huge advantage of this is its scalability and ease to change the location/hardware, where the bot is deployed. You can just simply take the dockerfile, that you need to create and start it on any PC that has a Docker instance installed. With this you can then for example host it on AWS like discribed in this [Repository](https://github.com/coldbrewcloud/tutorial-echo-slack-bot/blob/master/README.md).

# Overview:
In generall we can start when developing by hosting it on localhost. For the longrun I think we should maybe also talk to the Industry Partner or decide it when we decided on a Deploymentstrategy for the Main Application. For now using Google Cloud seems like a good idea, as it is already used by the Industry Partner and they may be more open to have it all in one place.