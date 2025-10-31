import React, { useState, useRef, useEffect } from 'react';
import {
  Box, Button, Input, VStack, HStack, Text, Avatar, Spinner, Heading
} from '@chakra-ui/react';
import { FaRobot, FaUser } from 'react-icons/fa';
import ReactMarkdown from 'react-markdown';

function stripThinkTags(text) {
  return text.replace(/<think>[\s\S]*?<\/think>/gi, '').trim();
}


function Chatbot() {
  const [subject, setSubject] = useState('');
  const [chatStarted, setChatStarted] = useState(false);
  const [userQuestion, setUserQuestion] = useState('');
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Please provide a subject like "math," "science," "history," or "programming," and I\'ll be ready to help you!' }
  ]);
  const [loading, setLoading] = useState(false);
  const chatBottomRef = useRef(null);

  useEffect(() => {
    chatBottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const handleSubjectSubmit = (e) => {
    e.preventDefault();
    setMessages([
      ...messages,
      { sender: 'user', text: subject },
      { sender: 'bot', text: `Great! You chose "${subject}". Ask your question!` }
    ]);
    setChatStarted(true);
  };

  const handleChatSubmit = async (e) => {
    e.preventDefault();
    setMessages([...messages, { sender: 'user', text: userQuestion }]);
    setLoading(true);
    // Build chat history for memory (excluding initial subject prompt and system/confirmation messages)
    const chatHistory = messages
      .filter(msg =>
        msg.sender === 'user' ||
        (msg.sender === 'bot' && !msg.text.startsWith('Please provide a subject') && !msg.text.startsWith('Great! You chose'))
      )
      .map(msg => ({ role: msg.sender === 'user' ? 'user' : 'assistant', content: msg.text }));
    try {
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:5000';
      const response = await fetch(`${apiUrl}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userQuestion, subject, history: chatHistory })
      });
      const data = await response.json();
      // Hide the first LLM response (to the instruction prompt)
      setMessages((msgs) => {
        // If this is the first bot response after the user's first question, skip it
        if (msgs.length === 2 && msgs[1].sender === 'user') {
          return msgs;
        }
        return [...msgs, { sender: 'bot', text: stripThinkTags(data.response) }];
      });
    } catch {
      setMessages((msgs) => [...msgs, { sender: 'bot', text: 'Error: Could not get response from server.' }]);
    }
    setUserQuestion('');
    setLoading(false);
  };

  return (
    <Box w="100vw" h="100vh" minH="100vh" bg="gray.50" display="flex" flexDirection="column" alignItems="center" justifyContent="center" p={0} m={0}>
      <Box w={{ base: '100%', md: '70%', lg: '50%' }} h={{ base: '100%', md: '90%' }} maxH="100vh" display="flex" flexDirection="column" boxShadow="lg" borderRadius="xl" bg="white" p={{ base: 2, md: 6 }}>
        <Heading mb={4} textAlign="center" color="purple.600" fontSize={{ base: '2xl', md: '3xl' }}>Classroom Genie</Heading>
        <Box flex={1} overflowY="auto" bg="gray.50" borderRadius="md" p={3} mb={2}>
          <VStack spacing={4} align="stretch">
            {messages.map((msg, i) => (
              <HStack
                key={i}
                alignSelf={msg.sender === 'bot' ? 'flex-start' : 'flex-end'}
                spacing={2}
                mb={1}
              >
                {msg.sender === 'bot' && <Avatar size="sm" icon={<FaRobot />} bg="purple.200" />}
                <Box
                  bg={msg.sender === 'bot' ? 'purple.100' : 'green.100'}
                  px={4}
                  py={2}
                  borderRadius="xl"
                  maxW={{ base: '90%', md: '70%' }}
                  fontSize="md"
                  boxShadow="sm"
                >
                  <ReactMarkdown>
                    {stripThinkTags(msg.text)}
                  </ReactMarkdown>
                </Box>
                {msg.sender === 'user' && <Avatar size="sm" icon={<FaUser />} bg="green.200" />}
              </HStack>
            ))}
            {loading && (
              <HStack alignSelf="flex-start">
                <Avatar size="sm" icon={<FaRobot />} bg="purple.200" />
                <Spinner color="purple.500" size="sm" />
                <Text color="gray.500" fontSize="sm">Genie is thinking...</Text>
              </HStack>
            )}
            <div ref={chatBottomRef} />
          </VStack>
        </Box>
        <Box mt={2}>
          {!chatStarted ? (
            <form onSubmit={handleSubjectSubmit}>
              <HStack>
                <Input
                  value={subject}
                  onChange={e => setSubject(e.target.value)}
                  placeholder="Enter a subject"
                  required
                  bg="white"
                />
                <Button colorScheme="purple" type="submit">Start</Button>
              </HStack>
            </form>
          ) : (
            <form onSubmit={handleChatSubmit}>
              <HStack>
                <Input
                  value={userQuestion}
                  onChange={e => setUserQuestion(e.target.value)}
                  placeholder="Ask a question..."
                  required
                  disabled={loading}
                  bg="white"
                />
                <Button colorScheme="purple" type="submit" isLoading={loading}>Send</Button>
              </HStack>
            </form>
          )}
        </Box>
      </Box>
    </Box>
  );
}

export default Chatbot;