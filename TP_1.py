import numpy as np

# Define array sizes
array_sizes = [10**3, 10**4, 10**5, 10**6]

# Generate sorted arrays
sorted_arrays = [np.sort(np.random.rand(size)) for size in array_sizes]

def simple_sequential_search(arr, target):
    comparisons = 0
    for value in arr:
        comparisons += 1
        if value == target:
            return True, comparisons
    return False, comparisons

def optimized_sequential_search(arr, target):
    comparisons = 0
    for value in arr:
        comparisons += 1
        if value == target:
            return True, comparisons
        elif value > target:
            return False, comparisons
    return False, comparisons

def iterative_binary_search(arr, target):
    left, right = 0, len(arr) - 1
    comparisons = 0
    while left <= right:
        comparisons += 1
        mid = (left + right) // 2
        if arr[mid] == target:
            return True, comparisons
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return False, comparisons

def recursive_binary_search(arr, target, left=0, right=None, comparisons=0):
    if right is None:
        right = len(arr) - 1

    if left > right:
        return False, comparisons

    comparisons += 1
    mid = (left + right) // 2

    if arr[mid] == target:
        return True, comparisons
    elif arr[mid] < target:
        return recursive_binary_search(arr, target, mid + 1, right, comparisons)
    else:
        return recursive_binary_search(arr, target, left, mid - 1, comparisons)
#قياس الوقت التنفيذ 
import time
import tracemalloc

def run_experiment(search_function, arr, target, trials=30):
    comparisons_list = []
    times_list = []
    memory_list = []

    for _ in range(trials):
        tracemalloc.start()
        start_time = time.perf_counter()

        _, comparisons = search_function(arr, target)

        end_time = time.perf_counter()
        _, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        comparisons_list.append(comparisons)
        times_list.append(end_time - start_time)
        memory_list.append(peak_memory / 1024)  # Convert to KB

    return {
        "comparisons": np.mean(comparisons_list),
        "time": np.mean(times_list),
        "memory": np.mean(memory_list),
        "comparisons_variance": np.var(comparisons_list),
        "time_variance": np.var(times_list),
        "memory_variance": np.var(memory_list)
    }
# إجراء الاختبارات
results = {}
target_value = np.random.rand()  

for size, arr in zip(array_sizes, sorted_arrays):
    print(f"Testing array of size {size}")
    results[size] = {
        "simple_sequential": run_experiment(simple_sequential_search, arr, target_value),
        "optimized_sequential": run_experiment(optimized_sequential_search, arr, target_value),
        "iterative_binary": run_experiment(iterative_binary_search, arr, target_value),
        "recursive_binary": run_experiment(lambda x, y: recursive_binary_search(x, y), arr, target_value)
    }
#تصور النتائج وإعداد التقرير
import matplotlib.pyplot as plt


array_sizes_labels = [str(size) for size in array_sizes]
simple_comparisons = [results[size]["simple_sequential"]["comparisons"] for size in array_sizes]
optimized_comparisons = [results[size]["optimized_sequential"]["comparisons"] for size in array_sizes]
iterative_comparisons = [results[size]["iterative_binary"]["comparisons"] for size in array_sizes]
recursive_comparisons = [results[size]["recursive_binary"]["comparisons"] for size in array_sizes]

plt.figure(figsize=(10, 6))
plt.plot(array_sizes_labels, simple_comparisons, label="Simple Sequential Search")
plt.plot(array_sizes_labels, optimized_comparisons, label="Optimized Sequential Search")
plt.plot(array_sizes_labels, iterative_comparisons, label="Iterative Binary Search")
plt.plot(array_sizes_labels, recursive_comparisons, label="Recursive Binary Search")
plt.xlabel("Array Size")
plt.ylabel("Average Comparisons")
plt.title("Comparisons of Search Algorithms")
plt.legend()
plt.show()
