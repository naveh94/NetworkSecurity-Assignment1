# Naveh Marchoom, 312275746, Miriel Jerbi 314733890
import hashlib
import math


class MerkleNode:
    """
    creates a merkle tree node.
    a leaf node will be constructed with only one value.
    when constructed with 2 children nodes, concatenate their values and hash them, and save that as value.
    """

    def __init__(self, value=None, left_child=None, right_child=None):
        self.father = None
        self.side = None
        if value is None:
            self.left_child = left_child
            self.left_child.set_father(self, "l")
            self.right_child = right_child
            self.right_child.set_father(self, "r")
            self.value = hashlib.sha256(left_child.value.encode() + right_child.value.encode()).hexdigest()
        else:
            self.value = value
            self.left_child = None
            self.right_child = None

    def set_father(self, node, side):
        self.father = node
        self.side = side


class MerkleTree:
    """
    represents a merkle tree.
    constructed with a list of power of 2 parameters.
    """

    def __init__(self, parameters):
        tree_height = math.log(len(parameters), 2)
        if not tree_height.is_integer():
            raise Exception("The number of arguments is not a power of 2")
        self.first_level = current_level = list(map(lambda val: MerkleNode(value=val), parameters))
        while len(current_level) > 1:
            next_level = []
            for i in range(0, len(current_level), 2):
                next_level.append(MerkleNode(left_child=current_level[i], right_child=current_level[i + 1]))
            current_level = next_level
        self.root = current_level[0]

    """
    returns the string value of the tree's root.
    """

    def get_root(self):
        return self.root.value

    """
    returns the proof of inclusion for a given index in the tree leaves.
    """

    def get_proof(self, index):
        node = self.first_level[index]
        ret = ""
        while node.father is not None:
            if node.side == "l":
                ret = ret + " r " + node.father.right_child.value
            elif node.side == "r":
                ret = ret + " l " + node.father.left_child.value
            node = node.father
        return ret.strip(" ")


class Main:
    def __init__(self):
        self.mt = None
        self.commands = {1: self.option1, 2: self.option2, 3: self.option3, 4: self.option4}

    def run(self):
        # The program loop:
        while True:
            user_input = input()
            temp = user_input.split()
            command = int(temp[0])
            args = temp[1:]
            if command == 5:
                break
            self.commands[command](args)

    def option1(self, args):
        self.mt = MerkleTree(args)
        print(self.mt.root.value)

    def option2(self, args):
        if not self.mt:
            raise Exception("A Merkle Tree was not created")
        print(self.mt.get_proof(int(args[0])))

    def option3(self, args):
        str_to_proof = args[0]
        tree_root = args[1]
        proof_of_inclusion = args[2:]
        proof_result = str_to_proof
        proof_index = 0
        # run over the proof_of_inclusion and check the direction and the value of the item
        while proof_index < len(proof_of_inclusion):
            direction = proof_of_inclusion[proof_index]
            proof_index += 1
            item = proof_of_inclusion[proof_index]
            proof_index += 1

            if direction == 'l':
                proof_result = hashlib.sha256(item.encode() + proof_result.encode()).hexdigest()
            elif direction == 'r':
                proof_result = hashlib.sha256(proof_result.encode() + item.encode()).hexdigest()
            else:
                raise Exception("Direction string is missing.")
        # if the proof_result is identical to the root of the tree then the str_to_ptoof id in the tree
        if proof_result == tree_root:
            print('True')
        else:
            print('False')

    def option4(self, args):
        # if there is no merkele tree we finish the program
        if self.mt is None:
            raise Exception("First enter Merkrle Tree")

        hardness = args[0]
        if int(hardness) > 64:
            raise Exception("String len in sha256 is 64 ,than prefix can be maximum 64 ")

        hash_num = 0
        # first we will check for the 0 index and the current root node
        hash_value = hashlib.sha256(str(hash_num).encode() + self.mt.root.value.encode()).hexdigest()
        while not (hash_value.startswith("0"*int(hardness))):
            # update the the number we check with root
            hash_num = hash_num + 1
            # try with the new hash_number
            hash_value = hashlib.sha256(str(hash_num).encode() + self.mt.root.value.encode()).hexdigest()
        print(hash_num, hash_value)


if __name__ == "__main__":
    try:
        Main().run()
    except:
        exit(-1)
