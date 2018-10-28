"""Basic example of an adapter class to provide a stack interface to Python's list."""


# from ..exceptions import Empty

class ArrayStack:
    """LIFO Stack implementation using a Python list as underlying storage."""

    def __init__(self):
        """Create an empty stack."""
        self._data = []  # nonpublic list instance

    def __len__(self):
        """Return the number of elements in the stack."""
        return len(self._data)

    def is_empty(self):
        """Return True if the stack is empty."""
        return len(self._data) == 0

    def push(self, e):
        """Add element e to the top of the stack."""
        self._data.append(e)  # new item stored at end of list

    def top(self):
        """Return (but do not remove) the element at the top of the stack.

        Raise Empty exception if the stack is empty.
        """
        if self.is_empty():
            raise Exception('Stack is empty')
        return self._data[-1]  # the last item in the list

    def pop(self):
        """Remove and return the element from the top of the stack (i.e., LIFO).

        Raise Empty exception if the stack is empty.
        """
        if self.is_empty():
            raise Exception('Stack is empty')
        return self._data.pop()  # remove last item from list


class ArrayQueue:
    """FIFO queue implementation using a Python list as underlying storage."""
    DEFAULT_CAPACITY = 10  # moderate capacity for all new queues

    def __init__(self):
        """Create an empty queue."""
        self._data = [None] * ArrayQueue.DEFAULT_CAPACITY
        self._size = 0
        self._front = 0

    def __len__(self):
        """Return the number of elements in the queue."""
        return self._size

    def is_empty(self):
        """Return True if the queue is empty."""
        return self._size == 0

    def first(self):
        """Return (but do not remove) the element at the front of the queue.

        Raise Empty exception if the queue is empty.
        """
        if self.is_empty():
            raise Exception('Queue is empty')
        return self._data[self._front]

    def dequeue(self):
        """Remove and return the first element of the queue (i.e., FIFO).

        Raise Empty exception if the queue is empty.
        """
        if self.is_empty():
            raise Exception('Queue is empty')
        answer = self._data[self._front]
        self._data[self._front] = None  # help garbage collection
        self._front = (self._front + 1) % len(self._data)
        self._size -= 1
        return answer

    def enqueue(self, e):
        """Add an element to the back of queue."""
        if self._size == len(self._data):
            self._resize(2 * len(self.data))  # double the array size
        avail = (self._front + self._size) % len(self._data)
        self._data[avail] = e
        self._size += 1

    def _resize(self, cap):  # we assume cap >= len(self)
        """Resize to a new list of capacity >= len(self)."""
        old = self._data  # keep track of existing list
        self._data = [None] * cap  # allocate list with new capacity
        walk = self._front
        for k in range(self._size):  # only consider existing elements
            self._data[k] = old[walk]  # intentionally shift indices
            walk = (1 + walk) % len(old)  # use old size as modulus
        self._front = 0  # front has been realigned


def radixSort(a):
    # Creates several buckets in which to store the values while being sorted at each digit
    arrOfQs = [ArrayQueue(), ArrayQueue(), ArrayQueue(), ArrayQueue(), ArrayQueue(), ArrayQueue(), ArrayQueue(),
               ArrayQueue(), ArrayQueue(), ArrayQueue()]

    max = a[0];  # Finds the max value of array
    for i in range(1, len(a)):
        if (a[i] > max):
            max = a[i];

    count = 0  # Finds the highes amount of digits (10^i) of the max number in array
    while max > 0:

        if max == 0:
            count += 1
        count += 1
        # Integer divide by ten in order to "count" each digit
        max = max // 10

    # For each value from zero to the amount of digits of our highest value
    for i in range(1, count + 1):
        cnt = 0;  # -Keeps track of how many are currently in "buckets"
        # For each item in array
        for j in range(len(a)):
            # Set the bucket whose index is equal to the value of the digit in question to the value of item in the array
            arrOfQs[a[j] % (10 ** i) // 10 ** (i - 1)].enqueue(a[j])
        # For each bucket
        for j in range(len(arrOfQs)):
            # While there are values in the bucket
            while (not arrOfQs[j].is_empty()):
                # Cycle pur each value back into the array
                a[cnt] = arrOfQs[j].dequeue()
                # Note which value we are examining
                cnt += 1;


def postFixConvert(e):
    numStack = ArrayStack();

    for i in range(len(e)):  # For every char in the string
        if e[i] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:  # If the char in question is a number
            numStack.push(int(e[i]))  # Add it to the stack
        else:  # Otherwise (if the value is an operator)

            val1 = numStack.pop()  # Remove the digits it from the stack and store them
            val2 = numStack.pop()  # (This is also so we can subtract and divide with out worrying about the order)
            if e[i] == "+":  # If the operator is 'Add'
                numStack.push(val2 + val1)  # Push the sum of the two values to the stack
            if e[i] == "−":  # If the operator is 'Subtract'
                numStack.push(val2 - val1)  # Push the difference to the stack
            if (e[i] == "∗"):  # If the operator is 'Multiply'
                numStack.push(val2 * val1)  # Push the product to the stack
            if e[i] == "/":  # If the operator is 'Divide'
                numStack.push(val2 / val1)  # Push the 'Quotient' to the stack

    # This ensures that every two values before an operator condensed into one, ensuring we will only have one value at the end
    return numStack.pop()  # return only value in the stack


if __name__ == '__main__':
    Q = [35, 53, 55, 33, 52, 32, 25]  # Makes array
    print(Q)
    radixSort(Q);
    print(Q)
    print(postFixConvert("52+83−∗4/"))



