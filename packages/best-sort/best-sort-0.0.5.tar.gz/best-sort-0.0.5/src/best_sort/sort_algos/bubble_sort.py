def bubble_sort(list: list) -> list:
    '''
    How it works:
    Step 1. Start While Loop
    Step 2. Set Swapped Flag False
    Step 3. For each element[i] compare to element[i + 1]
    Step 4. If element[i] > element[i + 1], swap them
    Step 5. Set Swapped Flag True
    Step 6. Continue until loop traversed and Swapped Flag is False

    Pros:
    - Stable, keeps items in order unless they need swapped.
    - Easy to implement.
    - Space complexity of O(1), only uses input array.

    Cons:
    - Time Complexity of O(n^2) in worst case.
    - One of the least efficient sorting algorithms.
    - Not really used in industry, except in very specific circumstances.

    More Information:
    https://leetcode.com/explore/learn/card/sorting/694/comparison-based-sorts/4434/
    '''

    has_swapped = True

    while has_swapped:
        has_swapped = False

        for i in range(len(list) - 1):
            if list[i] > list[i + 1]:
                list[i], list[i + 1] = list[i + 1], list[i]
                has_swapped = True

    return list
