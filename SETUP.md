
`docker-compose up`

<br><br>

docker services:

papercups + postgres db   (customer conversations backend)
- **banking_chatbot_backend**
- **banking_chatbot_backend_database**

[http://localhost:4000](http://localhost:4000)

 💡 papercups is currently built from source with deactivated `force_ssl`, otherwise cross-container API requests don't work (`network_mode: host` doesn't seem to work either)

 -> copy account_id
 -> create and copy API key
 -> add webhook

<br><br><br>

rasa + rasa actions server   (chatbot)
- **banking_chatbot_chatbot**
- **banking_chatbot_chatbot_actions**

<br><br><br>

frontend (papercups chat widget)
- **banking_chatbot_frontend**

[http://localhost:7000](http://localhost:7000)

-> replace account_id in `./frontend/src/App.tsx` (connect chat widget with papercups backend)

<br><br><br>

message forwarding webhook (customer writes a message -> papercups backend message event -> lambda function -> send message text to rasa chatbot server -> add answer text to papercups conversation)
- **banking_chatbot_lambda**

-> replace API key in `./webhook/handler.js` (PAPERCUPS_API_TOKEN) 
-> webhook URL `http://banking_chatbot_lambda:9001/2015-03-31/functions/webhook/invocations`


<br><br><br><br><br>


get account_id 
![account_id](https://github.com/martinenzinger/banking-chatbot-demo/raw/main/docs/images/account_id.jpg "account_id")


get conversation_id
![conversation_id](https://github.com/martinenzinger/banking-chatbot-demo/raw/main/docs/images/conversation_id.jpg "conversation_id")


get API key
![API key](https://github.com/martinenzinger/banking-chatbot-demo/raw/main/docs/images/api_key.jpg "API key")


setup event subscription
![webhook](https://github.com/martinenzinger/banking-chatbot-demo/raw/main/docs/images/webhook.jpg "webhook")
