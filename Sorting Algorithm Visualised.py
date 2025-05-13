import random, copy
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
import matplotlib.cm as cm


class Sort:

    def __init__(self, len = 1, sorttype = "bogosort"):

        self.len = len
        self.num_list = []
        self.attempts = 0
        self.unsorted = []
        self.sorttype = sorttype
        self.x = list(range(1, self.len+1))

        self.list_creation()

    def list_creation(self):
        the_list = []
        for i in range(self.len):
            the_list.append(random.randint(1, 100))
        self.unsorted = the_list
        self.num_list = the_list
        
    def unsorted_list(self):
        return f"Unsorted list = {self.num_list}"

    def sorting_type(self):
        if self.sorttype == "bubble sort":
            self.bubble_sort_fast()
        
        elif self.sorttype == "selection sort":
            self.selection_sort()
        
        elif self.sorttype == "insertion sort":
            self.insertion_sort()
        else:
            self.bogosort()

    def selection_sort(self):
        
        selection_list = self.num_list[:]
        history = History()

        history.record(selection_list)

        for pass_num in range(len(selection_list) -1, 0, -1):
        
            position_largest = 0
            for i in range(1, pass_num + 1):
                history.add_comparison()
                if selection_list[i] > selection_list[position_largest]:
                    position_largest = i
            selection_list[position_largest], selection_list[i] = selection_list[i], selection_list[position_largest]
            
            history.add_swap()
            history.record(selection_list)

        anim = MatPlot(self.x, history)
        anim.bar_print()
        self.num_list = selection_list

    def bogosort(self):

        bogo_list = self.num_list[:]
        sorted_list = sorted(bogo_list)
        history = History()

        history.record(bogo_list)

        while bogo_list != sorted_list:
            
            history.add_swap()
            history.record(bogo_list)
            random.shuffle(bogo_list)
            self.attempts += 1

        
        history.record(bogo_list)
        anim = MatPlot(self.x, history)
        anim.bar_print()
        self.num_list = bogo_list

    def bubble_sort_fast(self):

        bubble_list = self.num_list[:]
        history = History()

        history.record(bubble_list)

        for pass_num in range(len(bubble_list) - 1, 0, -1):
            for i in range(0, pass_num):
                if bubble_list[i] > bubble_list[i+1]:
                    bubble_list[i], bubble_list[i+1] = bubble_list[i+1], bubble_list[i]
                    history.add_swap()
                history.add_comparison()
                history.record(bubble_list)

        anim = MatPlot(self.x, history)
        anim.bar_print()
        self.num_list = bubble_list
    

    def insertion_sort(self):

        a_list = self.num_list[:]
        history = History()

        history.record(a_list)

        def compare(value, item_to_insert):
            history.add_comparison()
            return value > item_to_insert
        
        
        
        for index in range(1, len(a_list)):
            item_to_insert = a_list[index]
            i = index - 1
            
            while i >= 0 and compare(a_list[i], item_to_insert):
                a_list[i + 1] = a_list[i]
                history.add_swap()
                i -= 1
                history.record(a_list)
            a_list[i + 1] = item_to_insert
            history.record(a_list)
        
        anim = MatPlot(self.x, history)
        anim.bar_print()
        self.num_list = a_list
            

    def __str__(self):
        if self.len > 5 and self.sorttype == "bogosort":
            return f"\nUnsorted list = {self.unsorted}\n, Final List = {self.num_list}\n \nI told you no more than 5\n"
        else:
            return f"\nUnsorted list = {self.unsorted}\n, Final List = {self.num_list}\n"

class MatPlot:

    def __init__(self, x, list_history):
        self.x = x
        self.history = list_history
        self.anim = None

    def bar_print(self):
        fig, ax = plt.subplots()
        bar_rects = ax.bar(self.x, self.history[0], color="red")
        ax.set_ylim(0, 110)

        def update(frame):
            heights = self.history[frame]
            metadata = self.history.get_metadata(frame)

            
            for i, rect in enumerate(bar_rects):
                rect.set_height(heights[i])
                rect.set_color(cm.cool(heights[i] / 100))

            ax.set_title(f"Comparisons: {metadata['comparisons']} | Swaps: {metadata['swaps']}")

            return bar_rects

        self.anim = animation.FuncAnimation(
            fig, update, frames=len(self.history), repeat=False, blit=False, interval=5
        )

        plt.show()

class History:

    def __init__(self):
        self.states = []
        self.comparisons = 0
        self.swaps = 0
    
    def record(self, state):
        snapshot = copy.deepcopy(state)
        metadata = {'comparisons': self.comparisons, 'swaps': self.swaps}

        self.states.append((snapshot, metadata))

    def add_comparison(self):
        self.comparisons += 1
    
    def add_swap(self):
        self.swaps += 1

    def __getitem__(self, index):
        return self.states[index][0]

    def get_metadata(self, index):
        return self.states[index][1]

    def __len__(self):
        return len(self.states)


sort_type = input("What type of sorting algorithm do you want to do? \n \n(valid = 'selection sort', 'bubble sort', 'insertion sort' or 'bogosort')")
if sort_type == "bogosort":
    length = int(input("How many digits long do you want the list to be? (please no more than 5) "))
else:
    length = int(input("How many digits long do you want the list to be? "))
get = Sort(length, sort_type)
get.sorting_type()
print(get)
