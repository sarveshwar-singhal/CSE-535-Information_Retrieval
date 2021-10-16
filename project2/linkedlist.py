'''
@author: Sougata Saha
Institute: University at Buffalo
'''

import math


class Node:

    def __init__(self, value=None, next=None, freq = 0, skip = None, tf =0):
        """ Class to define the structure of each node in a linked list (postings list).
            Value: document id, Next: Pointer to the next node
            Add more parameters if needed.
            Hint: You may want to define skip pointers & appropriate score calculation here"""
        self.value = value  #docId
        self.next = next    #next node address
        self.freq = freq    #no of times that doc appeared
        self.skip = skip    #skip postings
        self.tf = tf        #tf score of each node


class LinkedList:
    """ Class to define a linked list (postings list). Each element in the linked list is of the type 'Node'
        Each term in the inverted index has an associated linked list object.
        Feel free to add additional functions to this class."""
    def __init__(self):
        self.start_node = None
        self.end_node = None
        self.length, self.n_skips, self.idf = 0, 0, 0.0 #length: len of linked list, n_skips: skip count
        self.skip_length = None

    def traverse_list(self):
        traversal = []
        if self.start_node is None:
            return traversal
        else:
            a = self.start_node
            while a is not None:
                traversal.append(a.value)
                a = a.next
            """ Write logic to traverse the linked list.
                To be implemented."""
            # raise NotImplementedError
            return traversal

    def traverse_skips(self):
        traversal = []
        if self.start_node is None:
            return traversal
        else:
            a = self.start_node
            while a is not None:
                traversal.append(a.value)
                a = a.skip
            """ Write logic to traverse the linked list using skip pointers.
                To be implemented."""
            # raise NotImplementedError
            return traversal

    def add_skip_connections(self):
        # print("value of LinkedList length is",self.length)
        n_skips = math.floor(math.sqrt(self.length))
        if n_skips * n_skips == self.length:
            n_skips = n_skips - 1
        self.n_skips = n_skips
        a = self.start_node
        prev_node = self.start_node
        temp_count = 0
        for _ in range(self.length):
            a = a.next
            temp_count += 1
            if temp_count == n_skips:
                prev_node.skip = a
                prev_node = a
                temp_count = 0
        """ Write logic to add skip pointers to the linked list. 
            This function does not return anything.
            To be implemented."""
        # raise NotImplementedError

    def insert_at_end(self, value):
        # print("insert value ",value)
        new_node = Node(value=value, freq=1)
        n = self.start_node
        self.length += 1

        if self.start_node is None:
            self.start_node = new_node
            self.end_node = new_node
            return

        elif self.start_node.value >= value:
            self.start_node = new_node
            self.start_node.next = n
            return

        elif self.end_node.value <= value:
            self.end_node.next = new_node
            self.end_node = new_node
            return

        else:
            while n.value < value < self.end_node.value and n.next is not None:
                n = n.next

            m = self.start_node
            while m.next != n and m.next is not None:
                m = m.next
            m.next = new_node
            new_node.next = n
            return
        """ Write logic to add new elements to the linked list.
            Insert the element at an appropriate position, such that elements to the left are lower than the inserted
            element, and elements to the right are greater than the inserted element.
            To be implemented. """
        # raise NotImplementedError

    def find_an_element(self, value):
        a = self.start_node
        while a is not None:
            if a.value == value:
                return a
            a = a.next
        return False
