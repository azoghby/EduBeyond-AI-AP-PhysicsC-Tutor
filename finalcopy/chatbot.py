import os
import streamlit as st
from openai import OpenAI

# Get OpenRouter API key from environment variables
OPENROUTER_API_KEY = os.environ.get(
    "OPENROUTER_API_KEY",
    ""
)

# Initialize OpenRouter client using OpenAI-compatible interface
openrouter_client = None
if OPENROUTER_API_KEY:
    openrouter_client = OpenAI(base_url="https://openrouter.ai/api/v1",
                               api_key=OPENROUTER_API_KEY,
                               default_headers={
                                   "HTTP-Referer": "https://replit.com",
                                   "X-Title": "AP Physics C AI Tutor"
                               })

# Streamlit UI setup
st.set_page_config(page_title="⚛️ AP Physics C Question Generator",
                   page_icon="⚛️",
                   layout="wide")

st.title("⚛️ AP Physics C AI Tutor")
st.markdown(
    "Generate customized AP Physics C questions with step-by-step solutions")

# Check if API key is available
if not OPENROUTER_API_KEY:
    st.error(
        "⚠️ OpenRouter API key not found. Please set the OPENROUTER_API_KEY environment variable."
    )
    st.stop()

# Initialize session state for storing generated content and chat history
if 'generated_question' not in st.session_state:
    st.session_state.generated_question = ""
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Initialize gamification system
if 'user_points' not in st.session_state:
    st.session_state.user_points = 0
if 'questions_attempted' not in st.session_state:
    st.session_state.questions_attempted = 0
if 'questions_completed' not in st.session_state:
    st.session_state.questions_completed = 0
if 'chat_interactions' not in st.session_state:
    st.session_state.chat_interactions = 0
if 'achievements' not in st.session_state:
    st.session_state.achievements = []
if 'current_streak' not in st.session_state:
    st.session_state.current_streak = 0
if 'last_attempt_correct' not in st.session_state:
    st.session_state.last_attempt_correct = None
# Initialize extra gamification state
if 'is_boss' not in st.session_state:
    st.session_state.is_boss = False
if 'bosses_defeated' not in st.session_state:
    st.session_state.bosses_defeated = 0
if 'show_solution' not in st.session_state:
    st.session_state.show_solution = False

# ---- NEW: persist split question/solution across reruns ----
if 'generated_question_text' not in st.session_state:
    st.session_state.generated_question_text = ""
if 'generated_solution_text' not in st.session_state:
    st.session_state.generated_solution_text = ""
# ------------------------------------------------------------


# Gamification functions
def award_points(points, reason):
    st.session_state.user_points += points
    st.success(f"🎉 +{points} points! {reason}")


def deduct_points(points, reason):
    st.session_state.user_points = max(0,
                                       st.session_state.user_points - points)
    st.warning(f"⚠️ -{points} points! {reason}")
    # Reset streak on incorrect behavior
    st.session_state.current_streak = 0


def check_achievements():
    achievements_earned = []

    # First Question Achievement
    if st.session_state.questions_attempted == 1 and "First Steps" not in st.session_state.achievements:
        st.session_state.achievements.append("First Steps")
        achievements_earned.append(
            "🌟 First Steps - Generated your first physics question!")

    # Physics Explorer Achievement
    if st.session_state.questions_attempted == 5 and "Physics Explorer" not in st.session_state.achievements:
        st.session_state.achievements.append("Physics Explorer")
        achievements_earned.append(
            "🔬 Physics Explorer - Generated 5 physics questions!")

    # Physics Master Achievement
    if st.session_state.questions_attempted == 10 and "Physics Master" not in st.session_state.achievements:
        st.session_state.achievements.append("Physics Master")
        achievements_earned.append(
            "🏆 Physics Master - Generated 10 physics questions!")

    # Curious Mind Achievement
    if st.session_state.chat_interactions == 5 and "Curious Mind" not in st.session_state.achievements:
        st.session_state.achievements.append("Curious Mind")
        achievements_earned.append(
            "🤔 Curious Mind - Asked 5 questions about physics problems!")

    # Problem Solver Achievement
    if st.session_state.questions_completed == 3 and "Problem Solver" not in st.session_state.achievements:
        st.session_state.achievements.append("Problem Solver")
        achievements_earned.append(
            "🧩 Problem Solver - Successfully worked through 3 complete problems!"
        )

    # Streak achievements
    if st.session_state.current_streak == 3 and "On Fire" not in st.session_state.achievements:
        st.session_state.achievements.append("On Fire")
        achievements_earned.append("🔥 On Fire - 3 questions in a row!")

    # Boss Slayer Achievement
    if st.session_state.bosses_defeated >= 1 and "Boss Slayer" not in st.session_state.achievements:
        st.session_state.achievements.append("Boss Slayer")
        achievements_earned.append(
            "⚔️ Boss Slayer - Defeated your first boss question!")

    # Display new achievements
    for achievement in achievements_earned:
        st.balloons()
        st.success(f"🏆 NEW ACHIEVEMENT: {achievement}")


def display_gamification_sidebar():
    with st.sidebar:
        st.markdown("## 🎮 Your Progress")

        # Points display
        st.metric("Points", st.session_state.user_points)

        # Progress stats
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Questions", st.session_state.questions_attempted)
        with col2:
            st.metric("Streak", st.session_state.current_streak)

        # Progress bar
        if st.session_state.questions_attempted > 0:
            completion_rate = st.session_state.questions_completed / st.session_state.questions_attempted
            st.progress(completion_rate,
                        f"Completion Rate: {completion_rate:.1%}")

        # Achievements section
        if st.session_state.achievements:
            st.markdown("### 🏆 Achievements")
            for achievement in st.session_state.achievements:
                if achievement == "First Steps":
                    st.markdown("🌟 First Steps")
                elif achievement == "Physics Explorer":
                    st.markdown("🔬 Physics Explorer")
                elif achievement == "Physics Master":
                    st.markdown("🏆 Physics Master")
                elif achievement == "Curious Mind":
                    st.markdown("🤔 Curious Mind")
                elif achievement == "Problem Solver":
                    st.markdown("🧩 Problem Solver")
                elif achievement == "On Fire":
                    st.markdown("🔥 On Fire")

        # Reset progress button
        st.markdown("---")
        if st.button("🔄 Reset Progress"):
            for key in [
                    'user_points', 'questions_attempted',
                    'questions_completed', 'chat_interactions', 'achievements',
                    'current_streak', 'last_attempt_correct'
            ]:
                if key in st.session_state:
                    if key == 'achievements':
                        st.session_state[key] = []
                    else:
                        st.session_state[
                            key] = 0 if key != 'last_attempt_correct' else None
            st.rerun()


# Detect boss level
def is_boss_level():
    return st.session_state.questions_attempted > 0 and st.session_state.questions_attempted % 5 == 0


# Display gamification sidebar
display_gamification_sidebar()
import random
import datetime

# List of AP Physics C topics 
TOPICS_LIST = [
    "Newton's Laws", "Work, Energy and Power", "Momentum", "Rotation",
    "Oscillations", "Gravitation", "Electric Fields", "Gauss's Law",
    "Electric Potential", "Capacitance", "Current & Circuits",
    "Magnetic Fields", "Ampère's Law", "Faraday's Law", "Induction"
]

# Session state for quiz
if 'quiz_mode' not in st.session_state:
    st.session_state.quiz_mode = False
if 'quiz_topic' not in st.session_state:
    st.session_state.quiz_topic = None
if 'quiz_questions' not in st.session_state:
    st.session_state.quiz_questions = []
if 'quiz_answers' not in st.session_state:
    st.session_state.quiz_answers = []
if 'quiz_score' not in st.session_state:
    st.session_state.quiz_score = 0
if 'quiz_index' not in st.session_state:
    st.session_state.quiz_index = 0


# Function to start daily quiz
def start_daily_quiz():
    st.session_state.quiz_mode = True
    st.session_state.quiz_index = 0
    st.session_state.quiz_score = 0
    st.session_state.quiz_answers = []

    # Seed by date so same topic for all users each day
    today_seed = int(datetime.datetime.now().strftime("%Y%m%d"))
    random.seed(today_seed)
    topic = random.choice(TOPICS_LIST)
    st.session_state.quiz_topic = topic

    # Get topic explanation from AI
    explain_prompt = f"Explain the AP Physics C topic '{topic}' in detail, covering key formulas, principles, and common applications in exams."
    explanation = openrouter_client.chat.completions.create(
        model="google/gemma-2-9b-it:free",
        messages=[{
            "role": "system",
            "content": "You are an expert AP Physics C tutor."
        }, {
            "role": "user",
            "content": explain_prompt
        }],
        max_tokens=500,
        temperature=0.4)
    st.session_state.quiz_intro = explanation.choices[0].message.content

    # Generate 7 MCQs for the chosen topic
    questions = []
    for _ in range(7):
        prompt = f"""Generate one standard numeric based AP Physics C Multiple Choice question about {topic}.
Provide exactly 5 answer choices (A-E) and mark the correct answer clearly.
At the end, write 'Correct Answer: X' where X is the correct option."""
        resp = openrouter_client.chat.completions.create(
            model="google/gemma-2-9b-it:free",
            messages=[{
                "role": "system",
                "content": "You are an expert AP Physics C instructor."
            }, {
                "role": "user",
                "content": prompt
            }],
            max_tokens=800,
            temperature=0.3)
        questions.append(resp.choices[0].message.content)
    st.session_state.quiz_questions = questions


# Daily quiz button on homepage
if not st.session_state.quiz_mode:
    if st.button("📅 Daily Quiz", use_container_width=True):
        start_daily_quiz()

# Quiz mode UI
if st.session_state.quiz_mode:
    st.header(f"📅 Daily Quiz: {st.session_state.quiz_topic}")

    if st.session_state.quiz_index == 0:
        st.markdown("### Topic Overview")
        st.markdown(st.session_state.quiz_intro)
        st.divider()

    # Display current question
    question_text = st.session_state.quiz_questions[
        st.session_state.quiz_index]
    st.markdown(f"**Question {st.session_state.quiz_index + 1} of 7:**")
    st.markdown(question_text)

    # Extract options from AI output
    options = [
        opt.strip() for opt in question_text.split("\n")
        if opt.strip().startswith(("A", "B", "C", "D", "E"))
    ]
    user_choice = st.radio("Select your answer:",
                           options,
                           key=f"quiz_q_{st.session_state.quiz_index}")

    if st.button("Submit Answer",
                 key=f"submit_q_{st.session_state.quiz_index}"):
        # Find correct answer in text
        correct_line = [
            line for line in question_text.split("\n")
            if "Correct Answer:" in line
        ]
        if correct_line:
            correct_letter = correct_line[0].split(":")[-1].strip()
            if user_choice.startswith(correct_letter):
                st.success("✅ Correct!")
                st.session_state.quiz_score += 1
                award_points(5, "Correct quiz answer!")
            else:
                st.error(
                    f"❌ Incorrect! The correct answer was {correct_letter}.")
        st.session_state.quiz_index += 1

        # If quiz finished
        if st.session_state.quiz_index >= 7:
            st.session_state.quiz_mode = False
            st.success(
                f"🎉 Quiz Complete! You scored {st.session_state.quiz_score}/7."
            )
            award_points(st.session_state.quiz_score * 10,
                         "Daily quiz completed!")

# === Custom Question Solver ===
st.subheader("📝 Ask Your Own AP Physics C Question")

user_custom_question = st.text_area(
    "Enter your AP Physics C question here:",
    placeholder=
    "Example: A block of mass m slides down a frictionless incline of angle θ. Find its acceleration."
)

if st.button("💡 Solve My Question", use_container_width=True):
    st.session_state.questions_attempted += 1
    st.session_state.current_streak += 1
    award_points(20, "Solved your custom physics problem!")
    check_achievements()
    if user_custom_question.strip():
        with st.spinner("Solving your question..."):
            try:
                if not openrouter_client:
                    st.error(
                        "⚠️ OpenRouter client not initialized. Please check your API key."
                    )
                else:
                    # Prompt to solve user's custom question
                    solve_prompt = f"""
Requirements:
1. Provide a comprehensive step by step solution to the given AP Physics C problem with:
   - Clear identification of given information
   - Background information on relevant physics concepts
   - Relevant physics principles and equations
   - Detailed mathematical work
   - Final answer with appropriate units and sisgnificant figures
2. For derivation format: Show complete mathematical derivations
3. For numeric format: Focus on quantitative problem-solving
4. For concept-based format: Emphasize theoretical understanding and explanations

Problem:
{user_custom_question}
"""

                    response = openrouter_client.chat.completions.create(
                        model="google/gemma-2-9b-it:free",
                        messages=[{
                            "role":
                            "system",
                            "content":
                            "You are a highly skilled AP Physics C tutor who explains solutions clearly. In your solutions, you always include relevant background knowledge on key physics concepts and formulas, and you provide detailed mathematical work."
                        }, {
                            "role": "user",
                            "content": solve_prompt
                        }],
                        max_tokens=1500,
                        temperature=0.2)

                    bot_solution = response.choices[0].message.content
                    st.success("✅ Solution Ready!")
                    st.markdown(bot_solution)

                    # Gamification hook
                    st.session_state.questions_completed += 1

            except Exception as e:
                st.error(f"⚠️ Error solving question: {str(e)}")
    else:
        st.warning("Please enter a question before submitting.")
# Create two columns for better layout
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Question Parameters")

    # Selection menus for metadata
    topic = st.selectbox("Select Topic", [
        "", "Newton's Laws", "Work, Energy and Power", "Momentum", "Rotation",
        "Oscillations", "Gravitation", "Electric Fields", "Gauss's Law",
        "Electric Potential", "Capacitance", "Current & Circuits",
        "Magnetic Fields", "Ampère's Law", "Faraday's Law", "Induction"
    ])

    question_type = st.selectbox("Question Type",
                                 ["", "Multiple Choice", "Free Response"])

    difficulty = st.selectbox("Difficulty Level",
                              ["", "easy", "standard", "hard"])

    answer_format = st.selectbox(
        "Answer Format",
        ["", "numeric based", "derivation based", "concept-based"])

    # Generate button
    generate = st.button("🎯 Generate Tagged Question",
                         type="primary",
                         use_container_width=True)

# When generating a question
with col2:
    st.subheader("Generated Question & Solution")

    if generate:
        # Boss logic
        st.session_state.is_boss = is_boss_level()
        boss_note = ""
        if st.session_state.is_boss:
            difficulty = "hard"  # Override to hard
            boss_note = "🛡️ **BOSS LEVEL!** This is a tougher, multi-part challenge worth double points."

        prompt = f"""Generate one {difficulty} {answer_format} AP Physics C {question_type} question about {topic} with the following requirements:

{'Make it multi-part and especially challenging.' if st.session_state.is_boss else ''}

Requirements:
1. Create an authentic AP Physics C level question appropriate for the {difficulty} difficulty level
2. For MCQ: Provide 5 answer choices (A-E) with plausible distractors with the correct answer.
3. For FRQ: Create a multi-part question typical of AP Physics C exams
4. Include relevant physics constants and formulas when needed
5. Present the question clearly with proper mathematical notation
6. Provide a comprehensive step-by-step solution with:
   - Clear identification of given information
   - Relevant physics principles and equations
   - Detailed mathematical work
   - Final answer with appropriate units and significant figures
7. For derivation format: Show complete mathematical derivations
8. For numeric format: Focus on quantitative problem-solving
9. For concept-based format: Emphasize theoretical understanding and explanations

Format your response with:
**QUESTION:**
[Present the question here]

**SOLUTION:**
[Provide step-by-step solution here]
"""

        with st.spinner("🔄 Generating physics question..."):
            try:
                # Ensure we have a valid client before making API call
                if not openrouter_client:
                    st.error(
                        "⚠️ OpenRouter client not initialized. Please check your OpenRouter API key."
                    )
                    st.stop()

                # Use OpenRouter's free model for physics question generation
                response = openrouter_client.chat.completions.create(
                    model="google/gemma-2-9b-it:free",
                    messages=[{
                        "role":
                        "system",
                        "content":
                        "You are an expert AP Physics C instructor with extensive experience in creating high-quality exam questions. You understand the AP Physics C curriculum, appropriate difficulty levels, and effective pedagogical approaches. Generate questions that are authentic, challenging, and educationally valuable."
                    }, {
                        "role": "user",
                        "content": prompt
                    }],
                    max_tokens=2000,
                    temperature=0.2)

                output = response.choices[0].message.content
                st.success("✅ Question Generated Successfully!")
                topic = ""
                question_type = ""
                difficulty = ""
                answer_format = ""
                if boss_note:
                    st.warning(boss_note)

                # STORE outputs and gamification state
                # Split question/solution and save to session_state so they persist across reruns
                if "**SOLUTION:**" in output:
                    question_part, solution_part = output.split(
                        "**SOLUTION:**", 1)
                else:
                    question_part = output
                    solution_part = ""

                # Save question-only (used by chat) and the two parts for display
                st.session_state.generated_question = question_part.strip()
                st.session_state.generated_question_text = question_part.strip(
                )
                st.session_state.generated_solution_text = solution_part.strip(
                )

                st.session_state.questions_attempted += 1
                st.session_state.current_streak += 1
                award_points(
                    20 if st.session_state.is_boss else 10,
                    "Generated a physics question!" if
                    not st.session_state.is_boss else "Faced a boss question!")
                check_achievements()
                st.session_state.show_solution = False

            except Exception as e:
                st.error(f"⚠️ Error generating question: {str(e)}")

                # Provide helpful error messages based on common issues
                if "api_key" in str(e).lower():
                    st.info(
                        "💡 **Tip:** Make sure your OpenRouter API key is valid. Get one free at https://openrouter.ai"
                    )
                elif "rate" in str(e).lower():
                    st.info(
                        "💡 **Tip:** You may have hit the rate limit (50 requests/day). Try again later or upgrade your OpenRouter account."
                    )
                elif "quota" in str(e).lower() or "limit" in str(e).lower():
                    st.info(
                        "💡 **Tip:** Daily quota exceeded. OpenRouter free tier allows 50 requests/day."
                    )
                else:
                    st.info(
                        "💡 **Tip:** Check your internet connection and try again."
                    )

    else:
        # Display instructions when no question is generated
        st.info("""
        **Instructions:**
        1. Select your desired topic from the 15 AP Physics C areas
        2. Choose between Multiple Choice (MCQ) or Free Response (FRQ) questions
        3. Pick your preferred difficulty level
        4. Select the answer format that matches your learning goals
        5. Click "Generate Tagged Question" to create a custom physics problem

        The AI tutor will provide a complete question with detailed step-by-step solutions including:
        - Clear problem statement
        - Relevant physics principles
        - Mathematical derivations
        - Final answers with proper units
        """)

    # -----------------------
    # PERSISTENT DISPLAY AREA
    # -----------------------
    # This runs on every rerun and shows the saved question + solution toggle + answer box
    if st.session_state.generated_question_text:
        # Show the saved/generated question text
        st.markdown(st.session_state.generated_question_text)

        # Persistent Show Solution button (survives reruns)
        if st.button("👀 Show Solution", key="show_solution_persistent"):
            st.session_state.show_solution = True

        # If toggled, show the saved solution
        if st.session_state.show_solution and st.session_state.generated_solution_text.strip(
        ):
            st.markdown("**SOLUTION:**")
            st.markdown(st.session_state.generated_solution_text)

        # User attempts answer (persisted)
        user_answer = st.text_area("Enter your answer or approach...",
                                   key="user_answer_textarea")
        if st.button("✅ Submit Answer", key="submit_answer_persistent"):
            if user_answer.strip():
                if st.session_state.is_boss:
                    award_points(40, "Defeated a boss question!")
                    st.session_state.bosses_defeated += 1
                else:
                    award_points(15, "Completed a question!")
                st.session_state.questions_completed += 1
                st.session_state.last_attempt_correct = True
                check_achievements()
            else:
                st.warning("Please enter an answer first.")

# Chat section for asking questions about generated physics problems
if st.session_state.generated_question:
    st.markdown("---")
    st.subheader("💬 Ask Questions About This Physics Problem")
    st.markdown(
        "Have questions about the physics problem above? Ask the AI tutor for clarification, alternative solutions, or related concepts!"
    )

    # Display chat history
    for i, (user_msg, bot_msg) in enumerate(st.session_state.chat_history):
        with st.chat_message("user"):
            st.write(user_msg)
        with st.chat_message("assistant"):
            st.write(bot_msg)

    # Chat input
    if user_question := st.chat_input(
            "Ask a question about this physics problem..."):
        # Add user message to chat history
        with st.chat_message("user"):
            st.write(user_question)

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    if not openrouter_client:
                        st.error(
                            "⚠️ OpenRouter client not initialized. Please check your OpenRouter API key."
                        )
                    else:
                        # Create context-aware prompt
                        chat_prompt = f"""You are an expert AP Physics C tutor. A student has asked a question about this physics problem:

PHYSICS PROBLEM:
{st.session_state.generated_question}

STUDENT QUESTION:
{user_question}

Please provide a helpful, educational response that:
1. Directly addresses the student's question
2. Explains concepts clearly and simply
3. Provides additional insights or alternative approaches when relevant
4. Encourages deeper understanding of the physics principles involved

Be encouraging and educational in your response."""

                        response = openrouter_client.chat.completions.create(
                            model="google/gemma-2-9b-it:free",
                            messages=[{
                                "role":
                                "system",
                                "content":
                                "You are a helpful AP Physics C tutor who provides clear, educational explanations to student questions about physics problems."
                            }, {
                                "role": "user",
                                "content": chat_prompt
                            }],
                            max_tokens=1000,
                            temperature=0.7)

                        bot_response = response.choices[0].message.content
                        st.write(bot_response)

                        # Award points for chat interaction
                        st.session_state.chat_interactions += 1
                        award_points(5, "Asked a thoughtful question!")
                        check_achievements()

                        # Add to chat history
                        st.session_state.chat_history.append(
                            (user_question, bot_response))

                except Exception as e:
                    error_msg = f"⚠️ Error generating response: {str(e)}"
                    st.error(error_msg)

                    if "api_key" in str(e).lower():
                        st.info(
                            "💡 **Tip:** Make sure your OpenRouter API key is valid. Get one free at https://openrouter.ai"
                        )
                    elif "rate" in str(e).lower():
                        st.info(
                            "💡 **Tip:** You may have hit the rate limit (50 requests/day). Try again later or upgrade your OpenRouter account."
                        )
                    elif "quota" in str(e).lower() or "limit" in str(
                            e).lower():
                        st.info(
                            "💡 **Tip:** Daily quota exceeded. OpenRouter free tier allows 50 requests/day"
                        )

    # Clear chat history button
    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()

# Add footer with information
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9em;'>
    <p>🎓 AP Physics C AI Tutor | Powered by OpenRouter</p>
    <p>Covering Mechanics and Electricity & Magnetism topics</p>
</div>
""",
            unsafe_allow_html=True)

