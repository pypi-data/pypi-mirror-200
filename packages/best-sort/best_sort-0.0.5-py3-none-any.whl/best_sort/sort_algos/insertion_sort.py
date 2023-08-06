def insertion_sort(lst: list) -> list:
    '''
    How it works:
    Step 1. Iterate over set starting at element[1], for loop
    Step 2. Set Current index to iterator value.
    Step 3. Start nested while loop.
    Step 4. If current index[i - 1] > current index[i], swap
    Step 5. If swap occured, decrement current index and repeat while
    Step 6. Continue until final iteration of for loop

    Pros:
    - Stable, keeps items in order unless they need swapped.
    - Easy to implement.
    - Space complexity of O(1), only uses input array.
    - Best when input is small
    - Best when input almost sorted already

    Cons:
    - Not as performant with large collections of data.
    - Time complexity is O(n^2). Depends on size of data.

    More Information:
    https://leetcode.com/explore/learn/card/sorting/694/comparison-based-sorts/4435/
    '''

    for i in range(1, len(lst)):
        index = i

        while (index > 0 and lst[index - 1] > lst[index]):
            lst[index], lst[index - 1] = lst[index - 1], lst[index]
            index -= 1

    return lst
