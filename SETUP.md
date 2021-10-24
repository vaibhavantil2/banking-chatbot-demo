
`docker-compose up`

<br><br><br>

#### docker services:

<br><br>

papercups + postgres db   (customer conversations backend)
- **banking_chatbot_backend**
- **banking_chatbot_backend_database**

[http://localhost:4000](http://localhost:4000)

 💡 papercups is currently built from source with deactivated `force_ssl`, otherwise cross-container API requests don't work (`network_mode: host` doesn't seem to work either)

 -> copy account_id<br>
 -> create and copy API key<br>
 -> add webhook<br>

<br><br><br>

rasa + rasa actions server   (chatbot)
- **banking_chatbot_chatbot**
- **banking_chatbot_chatbot_actions**

-> create a free account at [Nordigen](https://nordigen.com/en/) and update the API key in `./chatbot/actions/actions.py` (API_TOKEN)<br>

<br><br><br>

frontend (papercups chat widget)
- **banking_chatbot_frontend**

[http://localhost:7000](http://localhost:7000)

-> replace account_id in `./frontend/src/App.tsx` (connect chat widget with papercups backend)<br>

<br><br><br>

message forwarding webhook (customer writes a message -> papercups backend message event -> lambda function -> send message text to rasa chatbot server -> add answer text to papercups conversation)
- **banking_chatbot_lambda**

-> replace API key in `./webhook/handler.js` (PAPERCUPS_API_TOKEN)<br>
-> webhook URL `http://banking_chatbot_lambda:9001/2015-03-31/functions/webhook/invocations`<br>


<br><br><br><br>


get account_id<br>
![account_id](https://github.com/martinenzinger/banking-chatbot-demo/raw/main/docs/images/account_id.jpg "account_id")

<br><br>

get conversation_id<br>
![conversation_id](https://github.com/martinenzinger/banking-chatbot-demo/raw/main/docs/images/conversation_id.jpg "conversation_id")

<br><br>

get API key<br>
![API key](https://github.com/martinenzinger/banking-chatbot-demo/raw/main/docs/images/api_key.jpg "API key")

<br><br>

setup event subscription<br>
![webhook](https://github.com/martinenzinger/banking-chatbot-demo/raw/main/docs/images/webhook.jpg "webhook")
