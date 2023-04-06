class Node:
    def __init__(self, value=None, next=None) -> None:
        self.value = value
        self.next = next


# Singly-linked list.
class Sll:
    def __init__(self) -> None:
        self.__head = None
        self.__tail = None
    
    def add_to_tail(self, value) -> None:
        new_node = Node(value)

        if not self.__head:
            self.__head = new_node
        else:
            self.__tail.next = new_node
        
        self.__tail = new_node

    def traverse_from_head_to_tail(self, callback, extra_param) -> None:
        current_node = self.__head

        while current_node:
            callback(current_node.value, extra_param)
            current_node = current_node.next
