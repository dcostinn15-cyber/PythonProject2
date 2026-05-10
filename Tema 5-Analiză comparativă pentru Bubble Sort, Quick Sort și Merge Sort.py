import random
import time
import sys

sys.setrecursionlimit(10000)

# 1. BUBBLE SORT
def bubble_sort(arr):
    n = len(arr)
    comparisons = 0
    swaps = 0

    for i in range(n):
        for j in range(0, n - i - 1):
            comparisons += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1

    return comparisons, swaps


# 2. QUICK SORT (FIXAT)
def quick_sort(arr):
    comparisons = 0
    swaps = 0
    recursive_calls = 0

    def _quick_sort(a, low, high):
        nonlocal comparisons, swaps, recursive_calls
        recursive_calls += 1

        if low < high:
            pivot_index = partition(a, low, high)
            _quick_sort(a, low, pivot_index - 1)
            _quick_sort(a, pivot_index + 1, high)

    def partition(a, low, high):
        nonlocal comparisons, swaps

        #pivot random (fix principal)
        pivot_index = random.randint(low, high)
        a[pivot_index], a[high] = a[high], a[pivot_index]

        pivot = a[high]
        i = low - 1

        for j in range(low, high):
            comparisons += 1
            if a[j] <= pivot:
                i += 1
                a[i], a[j] = a[j], a[i]
                swaps += 1

        a[i + 1], a[high] = a[high], a[i + 1]
        swaps += 1

        return i + 1

    _quick_sort(arr, 0, len(arr) - 1)
    return comparisons, swaps, recursive_calls


# 3. MERGE SORT
def merge_sort(arr):
    comparisons = 0
    swaps = 0
    recursive_calls = 0

    def _merge_sort(a):
        nonlocal comparisons, swaps, recursive_calls
        recursive_calls += 1

        if len(a) > 1:
            mid = len(a) // 2
            left = a[:mid]
            right = a[mid:]

            _merge_sort(left)
            _merge_sort(right)

            i = j = k = 0

            while i < len(left) and j < len(right):
                comparisons += 1
                if left[i] < right[j]:
                    a[k] = left[i]
                    i += 1
                else:
                    a[k] = right[j]
                    j += 1
                swaps += 1
                k += 1

            while i < len(left):
                a[k] = left[i]
                i += 1
                k += 1
                swaps += 1

            while j < len(right):
                a[k] = right[j]
                j += 1
                k += 1
                swaps += 1

    _merge_sort(arr)
    return comparisons, swaps, recursive_calls


# 4. GENERARE DATE
def generate_data(size, case_type):
    if case_type == "random":
        return [random.randint(0, 1000) for _ in range(size)]

    elif case_type == "sorted":
        return list(range(size))

    elif case_type == "reverse":
        return list(range(size, 0, -1))

    elif case_type == "duplicates":
        return [random.choice([1, 2, 3, 4, 5]) for _ in range(size)]

    elif case_type == "almost_sorted":
        arr = list(range(size))
        for _ in range(size // 10):
            i = random.randint(0, size - 1)
            j = random.randint(0, size - 1)
            arr[i], arr[j] = arr[j], arr[i]
        return arr


# 5. VERIFICARE
def is_sorted(arr):
    return all(arr[i] <= arr[i+1] for i in range(len(arr)-1))


# 6. TESTARE
def test_algorithms():
    random.seed(42)

    sizes = [100, 500, 1000]  # sigur pentru Bubble Sort
    cases = ["random", "sorted", "reverse", "duplicates", "almost_sorted"]

    runs = 3
    results = []

    for size in sizes:
        for case in cases:
            base_data = generate_data(size, case)

            for algo in ["Bubble", "Quick", "Merge"]:
                total_time = 0
                total_comp = 0
                total_swaps = 0
                total_rec = 0

                for _ in range(runs):
                    data = base_data.copy()

                    start = time.time()

                    if algo == "Bubble":
                        comp, swaps = bubble_sort(data)
                        rec = 0
                    elif algo == "Quick":
                        comp, swaps, rec = quick_sort(data)
                    else:
                        comp, swaps, rec = merge_sort(data)

                    end = time.time()

                    if not is_sorted(data):
                        print("Eroare sortare!")
                        return

                    total_time += (end - start)
                    total_comp += comp
                    total_swaps += swaps
                    total_rec += rec

                results.append({
                    "algoritm": algo,
                    "dim": size,
                    "caz": case,
                    "timp": total_time / runs,
                    "comp": total_comp // runs,
                    "swap": total_swaps // runs,
                    "rec": total_rec // runs
                })

    return results


# 7. AFIȘARE
def print_results(results):
    print(f"{'Algoritm':<10} {'Dim':<6} {'Caz':<15} {'Timp':<10} {'Comp':<12} {'Swap':<12} {'Rec':<10}")
    print("-" * 80)

    for r in results:
        print(f"{r['algoritm']:<10} {r['dim']:<6} {r['caz']:<15} "
              f"{r['timp']:<10.6f} {r['comp']:<12} {r['swap']:<12} {r['rec']:<10}")


# MAIN
if __name__ == "__main__":
    results = test_algorithms()
    print_results(results)