# EduBeyond-AI-AP-PhysicsC-Tutor
HUVTSP/EduBeyond -- A research and ideation project for building an AI chatbot to support AP Physics C students.

![AP Physics C](https://img.shields.io/badge/Subject-AP%20Physics%20C-blue)
![Python](https://img.shields.io/badge/Python-3.11+-green)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red)
![OpenRouter](https://img.shields.io/badge/AI-OpenRouter-purple)

**EduBeyond AI** is an intelligent tutoring system designed to support AP Physics C students with personalized question generation, step-by-step solutions, and interactive learning features.

## Features

### Question Generation
- **15 AP Physics C Topics**: Newton's Laws, Work/Energy/Power, Momentum, Rotation, Oscillations, Gravitation, Electric Fields, Gauss's Law, Electric Potential, Capacitance, Current & Circuits, Magnetic Fields, Ampère's Law, Faraday's Law, and Induction
- **Multiple Question Types**: Multiple Choice Questions (MCQ) and Free Response Questions (FRQ)
- **Difficulty Levels**: Easy, Medium, and Hard problems
- **Answer Formats**: Numeric calculations, mathematical derivations, and concept-based explanations

### Interactive Learning
- **Custom Question Solver**: Submit your own physics problems for AI-powered solutions
- **Real-time Chat**: Ask follow-up questions about generated problems
- **Step-by-step Solutions**: Detailed explanations with physics principles, equations, and mathematical work

### Gamification System
- **Points & Achievements**: Earn points for generating questions, solving problems, and engaging with content
- **Progress Tracking**: Monitor your learning journey with completion rates and streaks
- **Achievement Badges**: Unlock achievements like "Physics Explorer," "Problem Solver," and "On Fire"

### Technical Features
- **Responsive Web Interface**: Built with Streamlit for an intuitive user experience
- **AI-Powered**: Utilizes OpenRouter's free tier with Google's Gemma 2 model
- **Session Management**: Persistent chat history and progress tracking
- **Error Handling**: Comprehensive error messages and helpful tips

## Prerequisites

- Python 3.11 or higher
- Internet connection for AI model access
- OpenRouter API key (free tier available)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/HUVTSP/EduBeyond.git
   cd EduBeyond
   ```

2. **Install required packages**
   ```bash
   pip install streamlit openai
   ```

3. **Set up API key**
   - Get a free API key from [OpenRouter](https://openrouter.ai)
   - Option 1: Set as environment variable
     ```bash
     set OPENROUTER_API_KEY=your_api_key_here
     ```
   - Option 2: Edit `chatbot.py` line 7 to include your API key directly

## Running the Application

### Method 1: Using the Batch File (Windows)
Double-click `run_app.bat` or run in terminal:
```bash
./run_app.bat
```

### Method 2: Direct Command
```bash
cd "path/to/your/project"
python -m streamlit run chatbot.py
```

### Method 3: Using Streamlit Command
```bash
streamlit run chatbot.py
```

The application will open in your default web browser at `http://localhost:8501`

## How to Use

### 1. Generate Physics Questions
1. Select your desired topic from the dropdown menu
2. Choose question type (MCQ or FRQ)
3. Pick difficulty level
4. Select answer format
5. Click "Generate Tagged Question"

### 2. Solve Custom Problems
1. Navigate to the "Ask Your Own AP Physics C Question" section
2. Enter your physics problem
3. Click "Solve My Question" for AI-powered solutions

### 3. Interactive Learning
1. After generating a question, use the chat feature to ask follow-up questions
2. Submit your own answers to test understanding
3. Earn points and unlock achievements as you progress

## Gamification Features

| Achievement | Requirement | Points |
|-------------|-------------|---------|
| First Steps | Generate first question | 10 pts |
| Physics Explorer | Generate 5 questions | 50 pts |
| Physics Master | Generate 10 questions | 100 pts |
| Curious Mind | Ask 5 questions in chat | 25 pts |
| Problem Solver | Complete 3 problems | 75 pts |
| On Fire | 3 question streak | 30 pts |

## Project Structure

```
EduBeyond-AI-AP-PhysicsC-Tutor/
├── chatbot.py              # Main application file
├── run_app.bat             # Windows batch file for easy startup
├── .env                    # Environment variables (optional)
├── README.md              # Project documentation
└── requirements.txt       # Python dependencies (if needed)
```

## Configuration

### API Key Setup
The application uses OpenRouter for AI capabilities. You can:
1. Set the `OPENROUTER_API_KEY` environment variable
2. Modify line 7 in `chatbot.py` to include your API key
3. Use the free tier which provides 50 requests per day

### Customization Options
- **Topics**: Modify the topic list in `chatbot.py` around line 240
- **Models**: Change the AI model in the `openrouter_client.chat.completions.create()` calls
- **Styling**: Customize the Streamlit interface by modifying the UI components

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **OpenRouter** for providing free AI model access
- **Streamlit** for the excellent web framework
- **Google Gemma 2** for the underlying AI model
- **AP Physics C Community** for inspiration and feedback

## Support

If you encounter any issues or have questions:

1. **Check the Issues tab** on GitHub for existing solutions
2. **Create a new issue** if your problem isn't already addressed
3. **Include error messages** and steps to reproduce the problem

## Future Development

- Support for additional physics courses (AP Physics 1, AP Physics 2)
- Integration with learning management systems
- Mobile app development
- Advanced analytics and learning insights
- Collaborative study features
- Video explanation generation

---

**Built for AP Physics C students by the EduBeyond team**

*Helping students excel in physics through intelligent tutoring*
