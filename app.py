
import streamlit as st
from datetime import date

# ==========================================
# STUDYFLOW AI - STUDY PLANNER
# Version 1.5
# ==========================================

# Display the application title and description
st.title("StudyFlow AI")
st.write("Your personal AI-powered study planner.")


# ==========================================
# 1. INITIALIZE ASSIGNMENT STORAGE
# ==========================================

# Create an empty list when the app starts.
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
hours = st.number_input(
    "Estimated study hours",
    min_value=1,
    value=2
)

# Display a calendar for selecting a deadline
# format controls how the date appears in the input
deadline = st.date_input(
    "Assignment deadline",
    format="MM/DD/YYYY"
)


# ==========================================
# 3. ADD ASSIGNMENT BUTTON
# ==========================================

if st.button("Add Assignment"):

    # Check that the required fields aren't empty
    if subject.strip() and assignment.strip():

        # Store the assignment details in a dictionary
        new_assignment = {
            "subject": subject.strip(),
            "assignment": assignment.strip(),
            "hours": hours,
            "deadline": deadline
        }

        # Add the assignment to our list
        st.session_state.assignments.append(new_assignment)

        # Display a confirmation message
        st.success("Assignment added!")

    else:
        # Warn the user about missing information
        st.warning("Please enter a subject and assignment.")


# ==========================================
# 4. SORT ASSIGNMENTS BY DEADLINE
# ==========================================

# Sort assignments by their deadlines.
# Assignments without deadlines appear last.
sorted_assignments = sorted(
    st.session_state.assignments,
    key=lambda item: (
        item.get("deadline") is None,
        item.get("deadline")
    )
)


# ==========================================
# 5. DISPLAY ALL ASSIGNMENTS
# ==========================================

st.subheader("My Assignments")

# Check whether the assignment list is empty
if not sorted_assignments:
    st.info("No assignments added yet.")

else:
    # Go through each assignment
    for item in sorted_assignments:

        # Display the subject and assignment name
        st.write("Subject:", item["subject"])
        st.write("Assignment:", item["assignment"])

        # Display estimated study hours
        st.write("Estimated hours:", item["hours"])

        # Retrieve the deadline, if available
        due_date = item.get("deadline")

        if due_date is not None:

            # Convert the date to MM/DD/YYYY format
            formatted_date = due_date.strftime("%m/%d/%Y")

            # Display the formatted deadline
            st.write("Deadline:", formatted_date)

            # Calculate days remaining until deadline
            days_left = (due_date - date.today()).days

            # Check whether the deadline has passed
            if days_left < 0:
                st.error(
                    f"Overdue by {abs(days_left)} day(s)!"
                )

            # Check whether the assignment is due today
            elif days_left == 0:
                st.warning("This assignment is due today!")

            # Otherwise, display days remaining
            else:
                st.info(f"{days_left} day(s) remaining")

        else:
            # Handle assignments created without deadlines
            st.write("Deadline: Not set")

        # Add a divider between assignments
        st.divider()
