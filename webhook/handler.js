// See https://github.com/papercups-io/papercups-node#usage
const papercups = require('@papercups-io/papercups')(
    process.env.PAPERCUPS_API_KEY,
    { host: 'http://banking_chatbot_backend:4000' }
);

const http = require('http');

// This function will be exported to handle incoming webhook events!
exports.handler = async function ({ event, payload }) {
    switch (event) {
        // See https://docs.papercups.io/webhook-events#messagecreated
        case 'message:created':
            const { body, conversation_id } = payload;

            const data = JSON.stringify({
                sender: 'chat_widget',
                message: body
            })

            const options = {
                hostname: 'banking_chatbot_chatbot',
                port: 5005,
                path: '/webhooks/rest/webhook',
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Content-Length': data.length
                }
            }

            const req = http.request(options, res => {
                res.on('data', response => {
                    return papercups.messages.create({
                        body: getResponseMessage(response),
                        type: 'bot',
                        conversation_id,
                    });
                })
            })

            req.on('error', error => {
                console.error(error)
                return { event, payload };
            })

            req.write(data)
            req.end()

        // See https://docs.papercups.io/api-endpoints#messages

        default:
            return { event, payload };
    }
}

function getResponseMessage(text) {
    const messages = JSON.parse(text);
    let msgtext = "";

    for (var i = 0; i < messages.length; i++) {
        msgtext += messages[i].text + "\n";
    }

    return msgtext;
}