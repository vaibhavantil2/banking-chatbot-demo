import React from 'react';
import { ChatBuilder, ChatToggle } from '@papercups-io/chat-builder';
import Header from './Header';
import Body from './Body';
import Footer from './Footer';

// NB: during development, replace this with a valid account ID from your dev db
const TEST_ACCOUNT_ID = '5fa73316-04d2-48ae-bd3e-77599814e3de';

const config = {
  title: 'Welcome!',
  subtitle: 'This is a simple banking chatbot demo 🥳',
  accountId: TEST_ACCOUNT_ID,
  greeting: 'Hi there! How can I help you?',
  customer: {
    name: 'Test User',
    email: 'test@test.com',
    external_id: '123',
    // Ad hoc metadata
    metadata: {
      plan: 'starter',
      registered_at: '2020-09-01',
      age: 25,
      valid: true,
    },
  },
  // NB: we override these values during development -- note that the
  // baseUrl: 'http://localhost:4000',
  baseUrl: 'http://localhost:4000',
};

const App = () => {
  return (
    <div>
      <ChatBuilder
        config={config}
        isOpenByDefault
        header={({ config, state, onClose }) => {
          return <Header config={config} state={state} onClose={onClose} />;
        }}
        body={({ config, state, scrollToRef }) => {
          return (
            <Body config={config} state={state} scrollToRef={scrollToRef} />
          );
        }}
        footer={({ config, state, onSendMessage }) => {
          return (
            <Footer
              config={config}
              state={state}
              onSendMessage={onSendMessage}
            />
          );
        }}
        toggle={({ state, onToggleOpen }) => {
          const { isOpen } = state;

          return <ChatToggle isOpen={isOpen} onToggleOpen={onToggleOpen} />;
        }}
        notifications={({ unread = [] }) => {
          return (
            <div>
              {unread.map((message) => {
                return (
                  <div
                    key={message.id}
                    style={{
                      padding: 16,
                      margin: 8,
                      border: '1px solid rgb(245, 245, 245)',
                      borderRadius: 4,
                      boxShadow: 'rgba(35, 47, 53, 0.09) 0px 2px 8px 0px',
                      maxWidth: '84%',
                    }}
                  >
                    {message.body}
                  </div>
                );
              })}
            </div>
          );
        }}
      />
    </div>
  );
};

export default App;
