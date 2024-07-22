import streamlit as st

# Initialize session state for the to-do list if it doesn't exist
if 'todo_list' not in st.session_state:
    st.session_state.todo_list = []

# Title of the app
st.title("To-Do List App")

# Input field for a new task
task = st.text_input("Enter a task")

# Add task to the list
if st.button("Add Task"):
    if task:
        st.session_state.todo_list.append({"task": task, "completed": False})
        st.success(f"Added task: {task}")
    else:
        st.error("Please enter a task")

# Display the to-do list
st.subheader("Your To-Do List")
if st.session_state.todo_list:
    for i, item in enumerate(st.session_state.todo_list):
        col1, col2, col3 = st.columns([6, 1, 1])
        with col1:
            st.write(f"{i+1}. {item['task']}")
        with col2:
            if st.checkbox("Completed", key=f"completed_{i}", value=item['completed']):
                st.session_state.todo_list[i]['completed'] = True
            else:
                st.session_state.todo_list[i]['completed'] = False
        with col3:
            if st.button("Remove", key=f"remove_{i}"):
                st.session_state.todo_list.pop(i)
                st.experimental_rerun()
else:
    st.write("No tasks yet!")

# Display completed tasks in a separate section
st.subheader("Completed Tasks")
if any(item['completed'] for item in st.session_state.todo_list):
    for item in st.session_state.todo_list:
        if item['completed']:
            st.write(f"- {item['task']}")
else:
    st.write("No completed tasks yet!")
