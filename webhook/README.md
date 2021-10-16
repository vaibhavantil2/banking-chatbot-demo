# Papercups webhook
forwards messages to Rasa chatbot


update Papercups API key in package.json

`npm install`
`npm run deploy`



 💡 '2015-03-31' is the lambda API version

```curl -d '{
  "event": "message:created",
  "payload": {
    "account_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "attachments": [],
    "body": "Hey there!",
    "conversation_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "created_at": "2021-02-24T00:10:45",
    "customer": {
      "browser": "Chrome",
      "company_id": null,
      "created_at": "2021-02-02T20:35:01",
      "current_url": "http://myapp.co/account",
      "email": "joe@example.com",
      "external_id": "a1b2c3d4e5",
      "host": "myapp.co",
      "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "metadata": {
        "plan": "premium"
      },
      "name": "Joe",
      "object": "customer",
      "os": "Mac OS X",
      "pathname": "/account",
      "phone": null,
      "profile_photo_url": null,
      "updated_at": "2021-02-24T00:10:43"
    },
    "customer_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "object": "message",
    "private": false,
    "seen_at": null,
    "sent_at": "2021-02-24T00:10:45Z",
    "type": "reply",
    "user": null,
    "user_id": null
  }
}' http://localhost:9001/2015-03-31/functions/webhook/invocations```



