import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time

# -----------------------------
# Sorting Algorithms Utilities
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

# -----------------------------
# Sorting Algorithm Generators
# -----------------------------
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
        key_val = data[i]
        j = i - 1
        while j >= 0 and data[j] > key_val:
            comparisons += 1
            data[j+1] = data[j]
            j -= 1
            swaps += 1
            yield data, color_array(len(data), [i, j], i, key=i), comparisons, swaps
        data[j+1] = key_val
        yield data, color_array(len(data), [i], i, key=j+1), comparisons, swaps
    yield data, ['lightgreen'] * len(data), comparisons, swaps

def quick_sort(data, low=0, high=None, comparisons=0, swaps=0):
    if high is None:
        high = len(data) - 1

    def partition_gen(data, low, high, comparisons, swaps):
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

    if low < high:
        partition_generator = partition_gen(data, low, high, comparisons, swaps)
        for state, colors, comparisons, swaps in partition_generator:
            yield state, colors, comparisons, swaps
        pivot = low
        for i in range(low, high+1):
            if data[i] == data[high]:
                pivot = i
                break
        yield from quick_sort(data, low, pivot-1, comparisons, swaps)
        yield from quick_sort(data, pivot+1, high, comparisons, swaps)
    else:
        yield data, ['lightgreen'] * len(data), comparisons, swaps

def merge_sort(data, comparisons=0, swaps=0):
    if len(data) > 1:
        mid = len(data)//2
        left = data[:mid]
        right = data[mid:]

        for state, colors, comparisons, swaps in merge_sort(left, comparisons, swaps):
            yield state, colors, comparisons, swaps
        for state, colors, comparisons, swaps in merge_sort(right, comparisons, swaps):
            yield state, colors, comparisons, swaps

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
            yield data, color_array(len(data), [k-1]), comparisons, swaps

        while i < len(left):
            data[k] = left[i]
            i += 1
            k += 1
            swaps += 1
            yield data, color_array(len(data), [k-1]), comparisons, swaps

        while j < len(right):
            data[k] = right[j]
            j += 1
            k += 1
            swaps += 1
            yield data, color_array(len(data), [k-1]), comparisons, swaps

    yield data, ['lightgreen'] * len(data), comparisons, swaps

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Sorting Visualizer", page_icon="🧩", layout="wide")
st.title("🧩 Advanced Sorting Visualizer with Comparison Mode")
st.write("Visualize each step of your sorting algorithm with detailed stats!")

# -----------------------------
# Reset / Restart Button
# -----------------------------
if st.sidebar.button("🔄 Reset / Restart"):
    if "data" in st.session_state:
        del st.session_state.data
    st.experimental_rerun()

# -----------------------------
# Sidebar Settings
# -----------------------------
compare_mode = st.sidebar.checkbox("⚖️ Compare Two Algorithms")

if compare_mode:
    algo1 = st.sidebar.selectbox("Algorithm 1", ["Selection Sort", "Bubble Sort", "Insertion Sort", "Quick Sort", "Merge Sort"], key="a1")
    algo2 = st.sidebar.selectbox("Algorithm 2", ["Selection Sort", "Bubble Sort", "Insertion Sort", "Quick Sort", "Merge Sort"], key="a2")
else:
    algo = st.sidebar.selectbox("Choose Sorting Algorithm", ["Selection Sort", "Bubble Sort", "Insertion Sort", "Quick Sort", "Merge Sort"])

# -----------------------------
# Data Input
# -----------------------------
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

# -----------------------------
# Single Algorithm Mode
# -----------------------------
if not compare_mode:
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
        generator = globals()[algo.replace(" ", "_").lower()](arr)
        prev_state = arr.copy()
        step = 1
        total_steps = len(arr)**2  # rough estimate

        for state, colors, comparisons, swaps in generator:
            progress_placeholder.progress(min(100, int((step/total_steps)*100)))
            stats_placeholder.markdown(
                f"<div style='display:flex;gap:15px;'>"
                f"<div style='background-color:#3498db;padding:10px;border-radius:8px;color:white;'>🔵 Comparisons<br>{comparisons}</div>"
                f"<div style='background-color:#2ecc71;padding:10px;border-radius:8px;color:white;'>🟢 Swaps<br>{swaps}</div>"
                f"<div style='background-color:#e67e22;padding:10px;border-radius:8px;color:white;'>⚡ Speed<br>{speed}s/frame</div>"
                f"</div>", unsafe_allow_html=True
            )

            if view_mode == "Bar Chart":
                fig, ax = plt.subplots(figsize=(10,4))
                ax.bar(range(len(state)), state, color=colors)
                ax.set_title(f"{algo} in Progress (Step {step})")
                chart.pyplot(fig)
                plt.close(fig)
            else:
                text_placeholder.markdown(
                    f"#### Step {step}\n"
                    f"#### Before: `{[int(x) for x in prev_state]}`\n"
                    f"#### After:  `{[int(x) for x in state]}`\n"
                    f"**Progress:** {min(100, int((step/total_steps)*100))}%"
                )
                prev_state = list(state)
            step += 1
            time.sleep(speed)

        st.success("✅ Sorting Completed Successfully!")
        st.balloons()

# -----------------------------
# Compare Two Algorithms Mode
# -----------------------------
if compare_mode and start:
    arr1 = list(data)
    arr2 = list(data)
    gen1 = globals()[algo1.replace(" ", "_").lower()](arr1)
    gen2 = globals()[algo2.replace(" ", "_").lower()](arr2)

    col1, col2 = st.columns(2)
    chart1 = col1.empty()
    chart2 = col2.empty()
    stats1 = col1.empty()
    stats2 = col2.empty()
    progress = st.progress(0)
    step = 1
    total_steps = max(len(arr1)**2, len(arr2)**2)

    while True:
        try:
            state1, colors1, comp1, swap1 = next(gen1)
        except StopIteration:
            state1, colors1, comp1, swap1 = arr1, ['lightgreen']*len(arr1), comp1, swap1
        try:
            state2, colors2, comp2, swap2 = next(gen2)
        except StopIteration:
            state2, colors2, comp2, swap2 = arr2, ['lightgreen']*len(arr2), comp2, swap2

        # Plot both
        fig1, ax1 = plt.subplots(figsize=(6,3))
        ax1.bar(range(len(state1)), state1, color=colors1)
        ax1.set_title(f"{algo1} Step {step}")
        chart1.pyplot(fig1)
        plt.close(fig1)

        fig2, ax2 = plt.subplots(figsize=(6,3))
        ax2.bar(range(len(state2)), state2, color=colors2)
        ax2.set_title(f"{algo2} Step {step}")
        chart2.pyplot(fig2)
        plt.close(fig2)

        stats1.markdown(f"**Comparisons:** {comp1} | **Swaps:** {swap1}")
        stats2.markdown(f"**Comparisons:** {comp2} | **Swaps:** {swap2}")

        progress.progress(min(100, int((step/total_steps)*100)))
        step += 1
        if state1 == sorted(arr1) and state2 == sorted(arr2):
            break
        time.sleep(speed)

    st.success("✅ Comparison Completed!")
    st.balloons()
    progress.progress(100)
