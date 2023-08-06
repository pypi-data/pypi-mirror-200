def selection_sort(unsorted_lst: list) -> list:
    '''
    How it works:
    Step 1. Find 1st smallest element in the list, swap with element list[0]
    Step 2. Find 2nd smallest element in the list, swap with element list[1]
    Step 3. Repeat, until list[n-1] element is sorted

    Pros:
    - 60% more efficient than bubble sort.
    - Easy to implement.
    - Can be used for small data sets, Insertion sort a better choice though.

    Cons:
    - Time Complexity of O(n^2).
    - Insertion sort is better.

    More Information:
    https://leetcode.com/explore/learn/card/sorting/694/comparison-based-sorts/4433/
    '''

    lst = unsorted_lst

    for i in range(len(lst)):
        smallest_index = i

        for j in range(i + 1, len(lst)):
            # Search for the smallest element
            if lst[j] < lst[smallest_index]:
                smallest_index = j

        # Swap current element with smallest element
        lst[smallest_index], lst[i] = lst[i], lst[smallest_index]

    return lst
