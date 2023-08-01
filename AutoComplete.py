class Node:
    """
    A node class used in a trie. Count to store the frequency of words

    Input:
        size: The size of the children array and count array. Determined by the number of characters in the
              language of the words stored. Since English has 26 alphabets, the size is 27 including the
              terminal character $

    Space complexity: Since size is a constant for a particular language, it is O(1).
    """
    def __init__(self, size=27):
        self.children = [None] * size
        self.count = 0
        self.terminal = False

class CatsTrie:
    """
    A trie class used to store cat sentences

    Input:
        sentences: A list of cat sentences. Each cat sentence is represented by a string of 26 alphabets
                   of the English language

    Time complexity: O(NM), where N is the number of cat sentences and M is the number of characters in the
                    longest cat sentence

    Space complexity: O(NM)
    """
    def __init__(self, sentences):
        self.root = Node()

        # Generate the trie
        # Time complexity: O(NM)
        self.generate_trie(sentences)

    """
    Generate the trie.
    
    Input:
        sentences: A list of cat sentences 
        
    Output: None, since the method does not return anything.
    
    Postcondition: A trie is generated. Can be accessed through self.root
    
    Time complexity: O(NM), where N is the number of cat sentences and M is the number of characters in the
                    longest cat sentence

    Space complexity: O(NM)    
    """
    def generate_trie(self, sentences):
        for sentence in sentences:
            self.insert(sentence)

    """
    Insert a cat sentence into the trie iteratively. Update the count of each letter of that sentence after 
    insertion.
    
    Input:
        sentence: A cat sentence represented using the 26 alphabets of the English language
    
    Output: None, since the method does not return anything.
    
    Postcondition: A branch of nodes representing the sentence inserted in the trie
    
    Time complexity: O(M), where M is the number of characters in the longest cat sentence. Although the same
                     sentence is traversed twice, the complexity is still bounded by O(M)
                    
    Space complexity: O(M)
    """
    def insert(self, sentence: str):
        current_node = self.root

        # Insert each character in the sentence iteratively. If the sentence exists, traverse through the trie
        # to the end of that sentence
        # Time complexity: O(M)
        for letter in sentence:
            children_index = ord(letter) - 96

            if current_node.children[children_index] is None:
                current_node.children[children_index] = Node()
                current_node = current_node.children[children_index]
            else:
                current_node = current_node.children[children_index]

        # End the sentence with a terminal character if the sentence did not exist before insertion
        # Time complexity: O(1)
        if current_node.children[0] is not None:
            current_node = current_node.children[0]
            current_node.count += 1
        else:
            current_node.children[0] = Node()
            current_node = current_node.children[0]
            current_node.terminal = True
            current_node.count += 1

        max_count = current_node.count
        current_node = self.root

        # Update the count of each character in that sentence. Each character's count will lead to the terminal character
        # of a sentence with the highest frequency
        # Time complexity: O(M)
        for letter in sentence:
            children_index = ord(letter) - 96
            current_node = current_node.children[children_index]
            if current_node.count < max_count:
                current_node.count = max_count

    """
    Autocomplete a sentence. The selection for sentence is based on the frequency of each sentence and the 
    prompt given. 
    
    Input:
        prompt: A string of characters. Can be an empty string
        
    Output: A cat sentence that has the highest frequency and has the prompt in its prefix. If multiple sentences
            have the same frequency, return the sentence that is lexicographically smaller.
    
    Time complexity: O(X+Y), where X is the length of the prompt and Y is the length of the longest cat
                     sentence in the trie.
    """
    def autoComplete(self, prompt):
        current_node = self.root
        result_string = [prompt]

        # Traverse through the trie based on the prompt. If the prompt is not a prefix for any sentence, return None
        # Time complexity: O(X), where X is the length of the prompt
        for letter in prompt:
            if current_node.children[ord(letter) - 96] is not None:
                current_node = current_node.children[ord(letter) - 96]
            else:
                return None

        # Traverse from where the prompt left off until reaching a terminal character. By traversing through
        # one of current_node.children with the highest count, one will eventually reach the terminal character
        # of the sentence with the highest frequency.
        # Time complexity: O(Y), where Y is the length of the longest cat sentence in the trie
        while not current_node.terminal:
            max_count = 0
            next_letter_index = 0
            for index in range(len(current_node.children)):
                if current_node.children[index] is not None:
                    if current_node.children[index].count > max_count:
                        max_count = current_node.children[index].count
                        next_letter_index = index

            if not next_letter_index == 0:
                result_string.append(chr(next_letter_index + 96))

            current_node = current_node.children[next_letter_index]
            max_count = 0

        return "".join(result_string)
