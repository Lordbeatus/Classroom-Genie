# README for Classroom Genie Website

## Overview
Classroom Genie is a web application that provides an interactive chatbot experience for users. The chatbot is designed to assist users by providing hints and guidance on various subjects, leveraging the Qwen model for text generation.

## Project Structure
The project is organized into two main parts: the client-side (React application) and the server-side (Python application). Below is the structure of the project:

```
classroom-genie-website
├── client
│   ├── public
│   │   └── index.html
│   ├── src
│   │   ├── App.jsx
│   │   ├── components
│   │   │   └── Chatbot.jsx
│   │   └── index.js
│   ├── package.json
│   └── README.md
├── prompts
│   └── Qwen.py
├── server
│   ├── app.py
│   └── requirements.txt
└── README.md
```

## Client-Side
The client-side of the application is built using React. It includes the following key files:

- **index.html**: The main HTML file that serves as the entry point for the React application.
- **App.jsx**: The main component that manages the layout and state of the application.
- **Chatbot.jsx**: A component that handles user input and displays the chatbot's responses.
- **index.js**: The entry point for the React application that renders the App component.

### Setup Instructions
1. Navigate to the `client` directory.
2. Install the required dependencies:
   ```
   npm install
   ```
3. Start the development server:
   ```
   npm start
   ```

## Server-Side
The server-side of the application is built using Python and Flask. It includes the following key files:

- **app.py**: The main entry point for the server-side application that handles incoming requests and interacts with the Qwen.py file.
- **requirements.txt**: Lists the Python dependencies required for the server-side application.

### Setup Instructions
1. Navigate to the `server` directory.
2. Create a virtual environment and activate it.
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the server:
   ```
   python app.py
   ```

## Usage
Once both the client and server are running, you can access the Classroom Genie web application in your browser. Users can send messages to the chatbot, and it will respond with hints and guidance based on the input provided.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License.