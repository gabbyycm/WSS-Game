# Music AI Assistant — Assignment 2 Prototype

## Project Overview

This is a prototype AI assistant built in Java.
The assistant simulates a music recommendation system that interacts with users, identifies their mood based on text input, and returns a suggested playlist. Further development will seek to expand this feature to existing playlists on Spotify app.

## Assistant Type

MusicAssistant  
- Recommends playlists based on mood detected in user input  
- Uses user preferences to personalize responses  
- Accepts input via the console for both profile creation and music requests

### Part 1 Data Type Design
- UserProfile Custom class holding name, age, preferences (Map), and premium status
- Request Stores user input, timestamp (`LocalDateTime`), and command type (Enum)
- Response Stores output message, confidence score (float), and success flag
- CommandType Enum used to classify request types

### Part 2 OOP Structure
- AIAssistant (abstract class) defines structure with methods like `greetUser()` and `handleRequest()`
- MusicAssistant (subclass) overrides behavior and adds a unique method `recommendPlaylist(mood)`
- Demonstrates inheritance, polymorphism, encapsulation, and class abstraction

### Part 3 Functional Simulation
- Prompts for user profile via console input (`Scanner`)
- Repeatedly accepts user music requests
- Matches mood using basic AI logic (see below)
- Responds with personalized playlist message

## Bonus Feature AI Mood Detection (Simulated)

This assistant includes a method `extractMood()` that uses simple string parsing to detect moods from user input like

- `I'm feeling sad` - `sad`
- `play something energetic` - `energetic`
- `I need study music` - `focused`

The project also includes a full OpenAI GPT API integration (currently commented out) for final submission, allowing real natural language understanding and mood detection.

## Sample Interaction
Welcome! What's your name gabby
How old are you 23
What's your favorite genre (e.g., Pop, Lo-Fi, Rock) rock
Hey gabby, ready for some music

Enter your music request (or type 'exit' to quit) i'm feeling sad
Assistant Playing playlist rock - sad vibes

## How to Compile and Run

### 1. Open your terminal or VS Code terminal  
Navigate to the `src` folder of your project
Open the terminal cd src
                    javac model.java assistant.java Main.java
                    java Main

