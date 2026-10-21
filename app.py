
import streamlit as st
from datetime import date

# ==========================================
# STUDYFLOW AI - STUDY PLANNER
# Version 1.6
# ==========================================

# Display the application title and description
st.title("StudyFlow AI")
st.write("Your personal AI-powered study planner.")


# ==========================================
# 1. INITIALIZE ASSIGNMENT STORAGE
# ==========================================

# Create an empty list when the app first starts.
# Session state remembers assignments between reruns.
if "assignments" not in st.session_state:
    st.session_state.assignments = []


# ==========================================
# 2. ASSIGNMENT INPUT FORM
# ==========================================

st.subheader("Add an Assignment")

# Get the subject from the user
subject = st.text_input("What subject?")

# Get the assignment name
assignment = st.text_input("What assignment?")

# Get estimated study hours
# Minimum is 1 hour, and the default is 2 hours
hours = st.number_input(
    "Estimated study hours",
    min_value=1,
    value=2
)

# Allow the user to select a deadline
# Display dates in Month/Day/Year format
deadline = st.date_input(
    "Assignment deadline",
    format="MM/DD/YYYY"
)


# ==========================================
# 3. ADD ASSIGNMENT BUTTON
# ==========================================

# Run this section when the button is clicked
if st.button("Add Assignment"):

    # Check that both text fields contain information
    if subject.strip() and assignment.strip():

        # Store the assignment details in a dictionary
        new_assignment = {
            "subject": subject.strip(),
            "assignment": assignment.strip(),
            "hours": hours,
            "deadline": deadline
        }

        # Add the new assignment to our list
        st.session_state.assignments.append(new_assignment)

        # Show a confirmation message
        st.success("Assignment added!")

    else:
        # Warn the user if information is missing
        st.warning("Please enter a subject and assignment.")


# ==========================================
# 4. STUDY-HOUR DASHBOARD
# ==========================================

st.subheader("Study Dashboard")

# Count the total number of assignments
total_assignments = len(st.session_state.assignments)

# Create a variable to store total study hours
total_hours = 0

# Loop through every assignment
# and add its estimated study hours
for item in st.session_state.assignments:
    total_hours += item["hours"]

# Create two columns for the dashboard
col1, col2 = st.columns(2)

# Display the total number of assignments
with col1:
    st.metric(
        "Total Assignments",
        total_assignments
    )

# Display the total estimated study hours
with col2:
    st.metric(
        "Study Hours Needed",
        f"{total_hours} hrs"
    )


# ==========================================
# 5. SORT ASSIGNMENTS BY DEADLINE
# ==========================================

# Sort assignments by their deadlines.
# Assignments with earlier deadlines appear first.
# Older assignments without deadlines appear last.
sorted_assignments = sorted(
    st.session_state.assignments,
    key=lambda item: (
        item.get("deadline") is None,
        item.get("deadline")
    )
)


# ==========================================
# 6. DISPLAY ALL ASSIGNMENTS
# ==========================================

st.subheader("My Assignments")

# Check whether the assignment list is empty
if not sorted_assignments:
    st.info("No assignments added yet.")

else:
    # Go through each assignment in deadline order
    for item in sorted_assignments:

        # Display the subject
        st.write("Subject:", item["subject"])

        # Display the assignment name
        st.write("Assignment:", item["assignment"])

        # Display estimated study hours
        st.write("Estimated hours:", item["hours"])

        # Retrieve the assignment deadline
        due_date = item.get("deadline")

        # Check whether the assignment has a deadline
        if due_date is not None:

            # Convert the date to MM/DD/YYYY format
            formatted_date = due_date.strftime("%m/%d/%Y")

            # Display the formatted deadline
            st.write("Deadline:", formatted_date)

            # Calculate how many days remain
            days_left = (due_date - date.today()).days

            # Check whether the deadline has passed
            if days_left < 0:
                st.error(
                    f"Overdue by {abs(days_left)} day(s)!"
                )

            # Check whether the assignment is due today
            elif days_left == 0:
                st.warning(
                    "This assignment is due today!"
                )

            # Otherwise, display days remaining
            else:
                st.info(
                    f"{days_left} day(s) remaining"
                )

        else:
            # Handle older assignments without deadlines
            st.write("Deadline: Not set")

        # Separate assignments visually
        st.divider()
