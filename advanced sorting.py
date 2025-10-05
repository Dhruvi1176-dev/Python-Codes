import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time

# -----------------------------
# Sorting Algorithms
# -----------------------------
def color_array(length, indices=None, sorted_until=None, pivot=None, key=None):
    colors = ['skyblue'] * length
    if indices:
        for idx in indices:
            if 0 <= idx < length:
                colors[idx] = 'red'
    if sorted_until is not None:
        for i in range(sorted_until, length):
            colors[i] = 'lightgreen'
    if pivot is not None and 0 <= pivot < length:
        colors[pivot] = 'purple'
    if key is not None and 0 <= key < length:
        colors[key] = 'yellow'
    return colors

def selection_sort(data):
    comparisons = swaps = 0
    n = len(data)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            yield data, color_array(n, [i, j], i), comparisons, swaps
            if data[j] < data[min_idx]:
                min_idx = j
        data[i], data[min_idx] = data[min_idx], data[i]
        swaps += 1
        yield data, color_array(n, [i, min_idx], i), comparisons, swaps
    yield data, ['lightgreen'] * n, comparisons, swaps

def bubble_sort(data):
    comparisons = swaps = 0
    n = len(data)
    for i in range(n):
        for j in range(0, n - i - 1):
            comparisons += 1
            yield data, color_array(n, [j, j+1]), comparisons, swaps
            if data[j] > data[j+1]:
                data[j], data[j+1] = data[j+1], data[j]
                swaps += 1
                yield data, color_array(n, [j, j+1]), comparisons, swaps
        yield data, color_array(n, [], n-i-1), comparisons, swaps
    yield data, ['lightgreen'] * n, comparisons, swaps

def insertion_sort(data):
    comparisons = swaps = 0
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0 and data[j] > key:
            comparisons += 1
            data[j+1] = data[j]
            j -= 1
            swaps += 1
            yield data, color_array(len(data), [i, j], i, key=i), comparisons, swaps
        data[j+1] = key
        yield data, color_array(len(data), [i], i, key=j+1), comparisons, swaps
    yield data, ['lightgreen'] * len(data), comparisons, swaps

def partition(data, low, high, comparisons, swaps):
    pivot = data[high]
    i = low - 1
    for j in range(low, high):
        comparisons += 1
        yield data, color_array(len(data), [j, high], pivot=high), comparisons, swaps
        if data[j] < pivot:
            i += 1
            data[i], data[j] = data[j], data[i]
            swaps += 1
            yield data, color_array(len(data), [i, j], pivot=high), comparisons, swaps
    data[i+1], data[high] = data[high], data[i+1]
    swaps += 1
    yield data, color_array(len(data), [i+1], pivot=high), comparisons, swaps
    return i+1, comparisons, swaps

def quick_sort(data, low, high, comparisons=0, swaps=0):
    if low < high:
        pivot, comparisons, swaps = yield from partition(data, low, high, comparisons, swaps)
        yield from quick_sort(data, low, pivot-1, comparisons, swaps)
        yield from quick_sort(data, pivot+1, high, comparisons, swaps)
    else:
        yield data, ['lightgreen'] * len(data), comparisons, swaps

def merge_sort(data, comparisons=0, swaps=0):
    n = len(data)
    if n > 1:
        mid = n // 2
        left = data[:mid]
        right = data[mid:]
        yield from merge_sort(left, comparisons, swaps)
        yield from merge_sort(right, comparisons, swaps)
        i = j = k = 0
        while i < len(left) and j < len(right):
            comparisons += 1
            if left[i] < right[j]:
                data[k] = left[i]
                i += 1
            else:
                data[k] = right[j]
                j += 1
            swaps += 1
            k += 1
            yield data, color_array(n, [i, j]), comparisons, swaps
        while i < len(left):
            data[k] = left[i]
            i += 1
            k += 1
            swaps += 1
            yield data, color_array(n, [i]), comparisons, swaps
        while j < len(right):
            data[k] = right[j]
            j += 1
            k += 1
            swaps += 1
            yield data, color_array(n, [j]), comparisons, swaps
    yield data, ['lightgreen'] * n, comparisons, swaps

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Sorting Visualizer", page_icon="🧩", layout="wide")
st.title("🧩 Advanced Sorting Visualizer with Progress & Stats")
st.write("Visualize each step of your sorting algorithm with detailed stats!")

# Sidebar
st.sidebar.header("⚙️ Settings")
algo = st.sidebar.selectbox("Choose Sorting Algorithm", ["Selection Sort", "Bubble Sort", "Insertion Sort", "Quick Sort", "Merge Sort"])
data_option = st.sidebar.radio("📊 Choose Data Source", ["Generate Random Data", "Enter Your Own Data"])

if data_option == "Generate Random Data":
    size = st.sidebar.slider("Number of elements", 5, 100, 30)
    if "data" not in st.session_state:
        st.session_state.data = np.random.randint(1, 100, size)
    if st.sidebar.button("🔁 Generate New Random Data"):
        st.session_state.data = np.random.randint(1, 100, size)
else:
    user_input = st.sidebar.text_input("Enter numbers (comma-separated):", "5, 2, 9, 1, 8")
    try:
        st.session_state.data = [int(x.strip()) for x in user_input.split(",")]
    except ValueError:
        st.sidebar.error("Please enter valid integers separated by commas!")

view_mode = st.sidebar.radio("🎨 Display Mode", ["Normal List", "Bar Chart"])
speed = st.sidebar.slider("Animation Speed (seconds per frame)", 0.01, 0.5, 0.05)
start = st.sidebar.button("🚀 Start Sorting")

data = st.session_state.data
chart = st.empty()
stats_placeholder = st.empty()
text_placeholder = st.empty()
progress_placeholder = st.empty()

if not start:
    st.info("👈 Choose your settings and click 'Start Sorting' to begin!")
    if view_mode == "Bar Chart":
        plt.figure(figsize=(10,4))
        plt.bar(range(len(data)), data, color='skyblue')
        plt.title("Initial Data")
        chart.pyplot(plt)
    else:
        st.write("### Current Data:", data)
else:
    arr = list(data)
    if algo == "Selection Sort":
        generator = selection_sort(arr)
    elif algo == "Bubble Sort":
        generator = bubble_sort(arr)
    elif algo == "Insertion Sort":
        generator = insertion_sort(arr)
    elif algo == "Quick Sort":
        generator = quick_sort(arr, 0, len(arr)-1)
    else:
        generator = merge_sort(arr)

    prev_state = arr.copy()
    step = 1
    total_steps = len(arr)**2  # rough estimate for progress

    for state, colors, comparisons, swaps in generator:
        progress = min(100, int((step/total_steps)*100))
        progress_placeholder.progress(progress)

        stats_placeholder.markdown(
            f"<div style='display:flex;gap:15px;'>"
            f"<div style='background-color:#3498db;padding:10px;border-radius:8px;color:white;'>🔵 Comparisons<br>{comparisons}</div>"
            f"<div style='background-color:#2ecc71;padding:10px;border-radius:8px;color:white;'>🟢 Swaps<br>{swaps}</div>"
            f"<div style='background-color:#e67e22;padding:10px;border-radius:8px;color:white;'>⚡ Speed<br>{speed}s/frame</div>"
            f"</div>", unsafe_allow_html=True
        )

        if view_mode == "Bar Chart":
            plt.figure(figsize=(10,4))
            plt.bar(range(len(state)), state, color=colors)
            plt.title(f"{algo} in Progress (Step {step})")
            chart.pyplot(plt)
            plt.close()
        else:
            text_placeholder.markdown(
                f"#### Step {step}\n"
                f"#### Before: `{[int(x) for x in prev_state]}`\n"
                f"#### After:  `{[int(x) for x in state]}`\n"
                f"**Progress:** {progress}%"
            )
            prev_state = list(state)
        step += 1
        time.sleep(speed)

    st.success("✅ Sorting Completed Successfully!")
    st.balloons()
