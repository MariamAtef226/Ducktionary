# DUCKTIONARY - an offline English Dictionary
# Dictionary source: Merriam-Webster
# Version 1.1 - Finished on 30/4/2022
# Mariam Atef Hassan
# Contact: mariamatef226@gmail.com
# ALL COPYRIGHTS RESERVED

from tkinter import*
import os

# RedBlack Tree implementation


class RBNode:
    def __init__(self, word, meaning):
        self.red = False
        self.parent = None
        self.word = word
        self.meaning = meaning
        self.left = None
        self.right = None


class RBTree:
    def __init__(self):
        self.nil = RBNode(0, 0)  # nil nodes are of value 0
        self.root = self.nil  # root = nil until a node is inserted

    def search_value(self, word):
        current = self.root
        while current != self.nil:
            if word == current.word:
                return current.meaning
            elif word < current.word:
                current = current.left
            else:
                current = current.right
        return "SORRY, WORD DOESN'T EXIST IN DICTIONARY!"

    def insert_node(self, word, meaning):
        new_node = RBNode(word, meaning)
        new_node.left = self.nil
        new_node.right = self.nil
        new_node.red = True  # new node must be red

        # determining who will be the parent
        parent = None
        current = self.root
        while current != self.nil:
            parent = current
            if new_node.word < current.word:
                current = current.left
            elif new_node.word > current.word:
                current = current.right
            else:
                return

        # assigning correct parent to the new node
        new_node.parent = parent
        if parent == None:
            self.root = new_node

        elif new_node.word < parent.word:
            parent.left = new_node
        else:
            parent.right = new_node

        # Fix up the tree to maintain red-black property
        self.fixup_tree(new_node)

    def fixup_tree(self, node):
        while node != self.root and node.parent.red:
            if node.parent == node.parent.parent.left:  # if the parent is a left child
                uncle = node.parent.parent.right
                if uncle.red:  # case 1: color flip
                    uncle.red = False
                    node.parent.red = False
                    node.parent.parent.red = True
                    node = node.parent.parent
                else:
                    if node == node.parent.right:  # case 2
                        node = node.parent
                        self.rotate_left(node)
                    # case 3 is executed either ways
                    node.parent.red= False
                    node.parent.parent.red = True
                    self.rotate_right(node.parent.parent)
            else:  # if parent is a right child
                uncle = node.parent.parent.left
                if uncle.red:
                    uncle.red = False
                    node.parent.red = False
                    node.parent.parent.red = True
                    node = node.parent.parent
                else:
                    if node == node.parent.left:  # case 2
                        node = node.parent
                        self.rotate_right(node)
                    # case 3 is executed either ways
                    node.parent.red = False
                    node.parent.parent.red = True
                    self.rotate_left(node.parent.parent)
        self.root.red = False

    # rotate left about node x
    def rotate_left(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.nil:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    # rotate right about node x
    def rotate_right(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.nil:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def count_node(self, root):
        if root == self.nil:
            return 0
        return 1 + self.count_node(root.left) + self.count_node(root.right)

    def tree_height(self, root):
        if root == self.nil:
            return 0
        right = 1 + self.tree_height(root.right)
        left = 1 + self.tree_height(root.left)
        return max(right, left)


# application

def dic_loader(words):  # load dictionary into the tree
    if os.path.exists("Merriam-Webster.txt"):  # check if file exists or not
        file = open("Merriam-Webster.txt", "r")
        for l in file:
            line = l.lower()
            q = line.find("\"")  # in the attached formatted text file with the project, the word is included between double quotes.
            line = line[q+1:]  # So, extract what comes after the first met double quotes.
            parts = line.split("\"", 2)  # delimiting at "
            word = parts[0]  # the word
            meaning = parts[2][:-3]  # it's meaning (exclude last 3 characters: ", new line and ',')
            words.insert_node(word, meaning)
    else:
        print("FAILED TO LOAD FILE")


def search_gui(tree, word, disp):  # handles the search process
    returned_text = tree.search_value(word)
    sentence_words = returned_text.split()
    string = ""
    i = 0
    while i < len(sentence_words):
        for j in range(0, 16):
            if i+j >= len(sentence_words):
                break
            w = sentence_words[i+j] + " "
            string = string + w
        string = string + "\n"
        i = i+16
    disp.delete('1.0', END)
    disp.insert(END, string)


def gui_home():
    words = RBTree()
    window = Tk()  # instantiate a window
    window.geometry("850x620")
    window.title("Ducktionary")
    window.config(background="white")
    duck = PhotoImage(file='rubber-duck1.png')
    window.iconphoto(False, duck)
    label = Label(window, text="DuckTionary!", font=('Comic Sans MS', 20, 'bold'),
                  pady=20, image=duck, compound='bottom', bg="white", fg="#ff7600")
    label.pack()
    dic_loader(words)
    if words.root != words.nil:  # dictionary is loaded successfully
        text = "Welcome to Ducktionary!\n" + "Size of Dictionary = " + str(words.count_node(words.root))
        size = Label(window, text=text, bg="white", font=('Comic Sans MS',15), fg="#ff7600")
        size.pack()
        text = Text(window, width=100)
        prompt = Label(window, fg="#ff7600", text="Enter the word you'd like to find its definition then click on Quack:", bg="white", font=('Comic Sans MS',15))
        entry = Entry(window, font="5")
        submit = Button(window, bg="yellow", fg="#ff4e00", text="Quack!", font="5", command=lambda: search_gui(words, entry.get().lower(), text))
        definition = Label(window, text="Result:", font=('Comic Sans MS',15), bg='white', fg="#ff7600")
        prompt.pack()
        entry.pack()
        submit.pack()
        definition.pack()
        text.pack()
    else:  # failed to load dictionary
        failed = Label(window, text="PROGRAM HAS FAILED", bg="white")
        failed.pack()
    window.mainloop()


# application run
gui_home()
