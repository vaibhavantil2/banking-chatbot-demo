// See https://github.com/papercups-io/papercups-node#usage
const fetch = require('node-fetch');

const PAPERCUPS_API_TOKEN = 'SFMyNTY.g2gDbAAAAAJoAmQAB3VzZXJfaWRhAWgCZAAKYWNjb3VudF9pZG0AAAAkNWZhNzMzMTYtMDRkMi00OGFlLWJkM2UtNzc1OTk4MTRlM2Rlam4GAI7mxbJ8AWIAAVGA.xHwKKI-U53w2s7yUMjWljjFBZS0EA7wCTYIHIxOI7SU';

// This function will be exported to handle incoming webhook events!
exports.handler = async function ({ event, payload }) {

    switch (event) {
        // See https://docs.papercups.io/webhook-events#messagecreated
        case 'message:created':
            const { body, conversation_id, customer_id, metadata } = payload;

            if (metadata != null) {
                if (metadata.handoff) {
                    return { event, payload };
                }
            }

            const data_rasa = JSON.stringify({
                sender: 'chat_widget',
                message: body
            })

            const response_rasa = await fetch('http://banking_chatbot_chatbot:5005/webhooks/rest/webhook', {
                method: 'post',
                body: data_rasa,
                headers: { 'Content-Type': 'application/json' }
            });

            const result_rasa = await response_rasa.json();

            const data_papercups = JSON.stringify({
                message: {
                    body: getResponseMessage(result_rasa, customer_id),
                    conversation_id
                }
            });

            const response_papercups = await fetch('http://banking_chatbot_backend:4000/api/v1/messages', {
                method: 'post',
                body: data_papercups,
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + PAPERCUPS_API_TOKEN
                }
            });

            const result_papercups = await response_papercups.json();

            return result_papercups;

        // See https://docs.papercups.io/api-endpoints#messages

        default:
            return { event, payload };
    }
}


function getResponseMessage(messages, customer_id) {
    let msgtext = "";

    for (var i = 0; i < messages.length; i++) {
        switch (messages[i].text) {
            case "CUSTOMER_SERVICE_HANDOFF":
                updateCustomerMetadata(customer_id);
                return msgtext;
            default:
                msgtext += messages[i].text + "\n";
        }

    }

    return msgtext;
}


async function updateCustomerMetadata(customer_id) {
    const data_handoff = JSON.stringify({
        customer: {
            metadata: {
                handoff: true
            }
        }
    })

    const response_handoff = await fetch('http://banking_chatbot_backend:4000/api/v1/customers', {
        method: 'put',
        body: data_handoff,
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + PAPERCUPS_API_TOKEN
        }
    });

    const result_handoff = await response_handoff.json();

    return result_handoff;
}

