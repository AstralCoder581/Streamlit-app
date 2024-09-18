import streamlit as st

# Set the page configuration
st.set_page_config(page_title="Anti-Doping Educational Platform", layout="wide")

# Initialize session state variables
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ''
if 'users' not in st.session_state:
    st.session_state['users'] = {}  # A dictionary to store user data

# Sample data for courses and quizzes
courses_data = {
    'Doping Prevention': {
        'description': 'Learn about doping prevention techniques.',
        'content': 'Detailed content about doping prevention...',
        'progress': {}
    },
    'Health Risks': {
        'description': 'Understand the health risks of doping.',
        'content': 'Detailed content about health risks...',
        'progress': {}
    },
    # Add more courses as needed
}

quizzes_data = {
    'Doping Prevention Quiz': {
        'questions': [
            {
                'question': 'What is doping?',
                'options': ['Illegal use of substances', 'A sport', 'A training method'],
                'answer': 'Illegal use of substances'
            },
            # Add more questions
        ],
        'passed': False
    },
    # Add more quizzes as needed
}

# Sidebar navigation
def sidebar():
    st.sidebar.title("Navigation")
    language = st.sidebar.selectbox("Select Language", ["English", "French", "Spanish"])
    st.session_state['language'] = language

    if st.session_state['logged_in']:
        page = st.sidebar.radio("Go to", ["Home", "Dashboard", "Courses", "Quizzes", "Forum", "News/Updates", "Profile", "Certificates", "Logout"])
    else:
        page = st.sidebar.radio("Go to", ["Home", "Login/Signup", "News/Updates", "About Us"])
    return page

# Home Page
def home_page():
    st.title("Welcome to the Anti-Doping Educational Platform")
    st.subheader("Promote Clean Sport, Learn Anti-Doping Practices")

    col1, col2 = st.columns(2)
    with col1:
        st.image("https://example.com/banner.jpg")  # Replace with actual image URL or file path
    with col2:
        st.markdown("""
        **Key Features:**
        - Access comprehensive courses on anti-doping
        - Test your knowledge with interactive quizzes
        - Stay updated with the latest news
        - Join community discussions in the forum
        """)

    st.write("## Quick Links")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Explore Courses"):
            st.session_state['current_page'] = 'Courses'
    with col2:
        if st.button("Take Quizzes"):
            st.session_state['current_page'] = 'Quizzes'
    with col3:
        if st.button("Visit Forum"):
            st.session_state['current_page'] = 'Forum'

    if not st.session_state['logged_in']:
        st.write("## Get Started")
        if st.button("Login / Sign Up"):
            st.session_state['current_page'] = 'Login/Signup'

# Login/Signup Page
def login_signup_page():
    st.header("Login / Sign Up")
    choice = st.radio("Select Action", ["Login", "Sign Up"])
    if choice == "Login":
        login_form()
    else:
        signup_form()

def login_form():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        users = st.session_state['users']
        if username in users and users[username]['password'] == password:
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.success(f"Welcome back, {username}!")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

def signup_form():
    st.subheader("Sign Up")
    username = st.text_input("Choose a Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    language = st.selectbox("Preferred Language", ["English", "French", "Spanish"])
    if st.button("Sign Up"):
        if password != confirm_password:
            st.error("Passwords do not match")
        elif username in st.session_state['users']:
            st.error("Username already exists")
        else:
            st.session_state['users'][username] = {
                'email': email,
                'password': password,
                'language': language,
                'progress': {},
                'certificates': []
            }
            st.success("Registration successful! Please log in.")
            st.experimental_rerun()

# Dashboard Page
def dashboard_page():
    st.header("Dashboard")
    username = st.session_state['username']
    user_data = st.session_state['users'][username]
    st.subheader(f"Welcome, {username}!")

    # User stats
    st.write("### Your Stats")
    st.write(f"Courses Completed: {len(user_data.get('completed_courses', []))}")
    st.write(f"Quizzes Passed: {len(user_data.get('passed_quizzes', []))}")
    st.write(f"Certificates Earned: {len(user_data.get('certificates', []))}")

    # Recent activity (placeholder)
    st.write("### Recent Activity")
    st.write("- You completed the 'Doping Prevention' course")
    st.write("- You earned a certificate in 'Health Risks'")

    # Shortcuts
    st.write("### Quick Access")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Continue Learning"):
            st.session_state['current_page'] = 'Courses'
    with col2:
        if st.button("Take a Quiz"):
            st.session_state['current_page'] = 'Quizzes'

# Courses Page
def courses_page():
    st.header("Courses")
    username = st.session_state['username']
    user_data = st.session_state['users'][username]

    st.write("## Available Courses")
    for course_name, course_info in courses_data.items():
        st.subheader(course_name)
        st.write(course_info['description'])
        if course_name in user_data.get('completed_courses', []):
            st.button(f"Review {course_name}", key=course_name)
        else:
            if st.button(f"Start {course_name}", key=course_name):
                st.session_state['current_course'] = course_name
                st.session_state['current_page'] = 'Course Content'

def course_content_page():
    course_name = st.session_state['current_course']
    st.header(f"Course: {course_name}")
    st.write(courses_data[course_name]['content'])
    if st.button("Mark as Completed"):
        username = st.session_state['username']
        user_data = st.session_state['users'][username]
        user_data.setdefault('completed_courses', []).append(course_name)
        st.success(f"You have completed the course '{course_name}'!")
        st.session_state['current_page'] = 'Courses'

# Quizzes Page
def quizzes_page():
    st.header("Quizzes")
    username = st.session_state['username']
    user_data = st.session_state['users'][username]

    st.write("## Available Quizzes")
    for quiz_name, quiz_info in quizzes_data.items():
        st.subheader(quiz_name)
        if quiz_name in user_data.get('passed_quizzes', []):
            st.write("Status: Passed")
            st.button(f"Retake {quiz_name}", key=quiz_name)
        else:
            if st.button(f"Take {quiz_name}", key=quiz_name):
                st.session_state['current_quiz'] = quiz_name
                st.session_state['current_page'] = 'Quiz Content'

def quiz_content_page():
    quiz_name = st.session_state['current_quiz']
    st.header(f"Quiz: {quiz_name}")
    questions = quizzes_data[quiz_name]['questions']
    correct_answers = 0

    for idx, q in enumerate(questions):
        st.write(f"**Question {idx + 1}: {q['question']}**")
        answer = st.radio("Select an answer:", q['options'], key=f"q_{idx}")
        if answer == q['answer']:
            correct_answers += 1

    if st.button("Submit Quiz"):
        score = correct_answers / len(questions) * 100
        st.write(f"Your Score: {score}%")
        username = st.session_state['username']
        user_data = st.session_state['users'][username]
        if score >= 70:
            st.success("Congratulations! You passed the quiz.")
            user_data.setdefault('passed_quizzes', []).append(quiz_name)
            # Award certificate
            certificate = f"Certificate of Completion: {quiz_name}"
            user_data['certificates'].append(certificate)
        else:
            st.error("You did not pass the quiz. Please try again.")

# Forum Page (Simplified)
def forum_page():
    st.header("Forum")
    st.write("Welcome to the community forum. Engage in discussions with peers and experts.")

    # Placeholder for forum content
    st.write("**Latest Threads**")
    st.write("- Thread 1: Doping FAQs")
    st.write("- Thread 2: Nutrition Tips")

# News/Updates Page
def news_page():
    st.header("News / Updates")
    st.write("Stay updated with the latest news on anti-doping.")

    # Placeholder for news content
    st.write("**Latest News**")
    st.write("- News Article 1")
    st.write("- News Article 2")

# Profile Page
def profile_page():
    st.header("Profile")
    username = st.session_state['username']
    user_data = st.session_state['users'][username]

    st.write(f"**Username:** {username}")
    st.write(f"**Email:** {user_data['email']}")
    st.write(f"**Preferred Language:** {user_data['language']}")

    if st.button("Edit Profile"):
        st.session_state['current_page'] = 'Edit Profile'

def edit_profile_page():
    st.header("Edit Profile")
    username = st.session_state['username']
    user_data = st.session_state['users'][username]

    new_email = st.text_input("Email", value=user_data['email'])
    new_language = st.selectbox("Preferred Language", ["English", "French", "Spanish"], index=["English", "French", "Spanish"].index(user_data['language']))

    if st.button("Save Changes"):
        user_data['email'] = new_email
        user_data['language'] = new_language
        st.success("Profile updated successfully!")
        st.session_state['current_page'] = 'Profile'

# Certificates Page
def certificates_page():
    st.header("Certificates")
    username = st.session_state['username']
    user_data = st.session_state['users'][username]
    certificates = user_data.get('certificates', [])

    if certificates:
        for cert in certificates:
            st.write(f"- {cert}")
            if st.button("Download", key=cert):
                st.write("Downloading certificate...")  # Placeholder for download functionality
    else:
        st.write("You have not earned any certificates yet.")

# Logout Function
def logout():
    st.session_state['logged_in'] = False
    st.session_state['username'] = ''
    st.success("You have been logged out.")

# Main App Function
def main():
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = 'Home'

    page = sidebar()

    if page == "Home":
        home_page()
    elif page == "Login/Signup":
        login_signup_page()
    elif page == "Dashboard":
        if st.session_state['logged_in']:
            dashboard_page()
        else:
            st.warning("Please log in to access the Dashboard.")
    elif page == "Courses":
        if st.session_state['logged_in']:
            courses_page()
        else:
            st.warning("Please log in to access Courses.")
    elif page == "Course Content":
        if st.session_state['logged_in']:
            course_content_page()
        else:
            st.warning("Please log in to access Course Content.")
    elif page == "Quizzes":
        if st.session_state['logged_in']:
            quizzes_page()
        else:
            st.warning("Please log in to access Quizzes.")
    elif page == "Quiz Content":
        if st.session_state['logged_in']:
            quiz_content_page()
        else:
            st.warning("Please log in to access Quiz Content.")
    elif page == "Forum":
        if st.session_state['logged_in']:
            forum_page()
        else:
            st.warning("Please log in to access the Forum.")
    elif page == "News/Updates":
        news_page()
    elif page == "Profile":
        if st.session_state['logged_in']:
            profile_page()
        else:
            st.warning("Please log in to access your Profile.")
    elif page == "Edit Profile":
        if st.session_state['logged_in']:
            edit_profile_page()
        else:
            st.warning("Please log in to edit your Profile.")
    elif page == "Certificates":
        if st.session_state['logged_in']:
            certificates_page()
        else:
            st.warning("Please log in to access Certificates.")
    elif page == "Logout":
        logout()
        st.session_state['current_page'] = 'Home'
        st.experimental_rerun()
    else:
        home_page()

if __name__ == "__main__":
    main()
