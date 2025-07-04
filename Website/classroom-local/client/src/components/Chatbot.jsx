import React, { useState } from 'react';

const Chatbot = () => {
    const [userQuestion, setUserQuestion] = useState('');
    const [chatbotResponse, setChatbotResponse] = useState('');
    
    const handleSubmit = async (e) => {
        e.preventDefault();
        const response = await fetch('http://localhost:5000/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: userQuestion }),
        });
        const data = await response.json();
        setChatbotResponse(data.response);
        setUserQuestion('');
    };

    return (
        <div>
            <h1>Chatbot</h1>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={userQuestion}
                    onChange={(e) => setUserQuestion(e.target.value)}
                    placeholder="Ask me anything..."
                    required
                />
                <button type="submit">Send</button>
            </form>
            <div>
                <h2>Response:</h2>
                <p>{chatbotResponse}</p>
            </div>
        </div>
    );
};

export default Chatbot;