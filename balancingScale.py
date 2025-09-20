# Boothbay Problem Solve
# Author: Aishwarya Afzulpurkar
# 09.20.2025


class TestBalancingScale():

    def __init__(self):
        self.tree = {}
        self.root = None
        self.stack = [] #last in, first out
        self.filelines = []
        self.outputMap = {}

    def readFileIntoMap(self, inputFile):
        children = set()
        parents = set()
        with open(inputFile) as f:
            while True:
                content = f.readline().rstrip()
                if content.startswith('#'):
                    continue
                if content == '':
                    break
                else:
                    key, left, right = content.split(',')
                    self.tree[key] = [left, right]

                    children.add(left)
                    children.add(right)
                    parents.add(key)
                    self.filelines.append(key)

        referenceCount = parents.difference(children)
        self.root = referenceCount.pop()
        # Check that all referenced scales are in fact mapped
        if referenceCount:
            raise Exception('References to scales were not found in map. Check input')

    def addToStack(self):
        node, i = self.root, 0
        self.stack.append([node, None, None])
        while i < len(self.stack):
            node = self.stack[i][0]
            left, right = self.tree[node]
            if not left.isnumeric():
                self.stack.append([left, node, 'left'])
            if not right.isnumeric():
                self.stack.append([right, node, 'right'])
            i+=1


    def calcWeightDiff(self, left, right):
        left, right = int(left), int(right)
        if left > right:
            return 0, left-right
        elif left < right:
            return right-left, 0
        else:
            return 0, 0

    def calcTotalWeight(self, left, right):
        return max(int(left), int(right)) * 2 + 1

    def parseMapBottomUp(self):
        while self.stack:
            key, parent, side = self.stack.pop()
            weight = self.calcTotalWeight(*self.tree[key])

            outLeft, outRight = self.calcWeightDiff(*self.tree[key])
            self.outputMap[key] = [str(outLeft), str(outRight)]

            if side == 'left':
                self.tree[parent][0] = weight
            if side == 'right':
                self.tree[parent][1] = weight

    def printOutput(self):
        for key in self.filelines:
            print(key + ',' + self.outputMap[key][0] + ',' + self.outputMap[key][1])

def main():
    bs = TestBalancingScale()
    bs.readFileIntoMap('inputFilePlayground.txt')
    bs.addToStack()
    bs.parseMapBottomUp()
    bs.printOutput()

if __name__ == "__main__":
    main()