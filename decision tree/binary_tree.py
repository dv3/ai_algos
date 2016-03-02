#bst
import Queue

class BinaryTree:

    def __init__(self,featureID,threshold,gain,distributions):
      self.left = None
      self.right = None
      self.featureID=featureID
      self.threshold = threshold
      self.gain= gain
      self.distributions=distributions

    def getNodeValue(self):
        return self.featureID,round(self.threshold,4),round(self.gain,6),self.distributions

    def BFS(self,tree_id):
        if self is None:
            print 'naah'
        else:
            nodeID=1
            q=Queue.Queue()
            currLevelCount = 1
            nextLevelCount = 0
            print 'tree= ',tree_id,'node=',nodeID,' feature=',self.featureID,' thr=',round(self.threshold,4),' gain:',round(self.gain,6),' distri=',self.distributions
            q.put(self.left)
            q.put(self.right)
            while not q.empty():
                root = q.get()
                currLevelCount -= 1
                if root is not None:
                    nodeID=nodeID+1
                    print 'tree= ',tree_id,' node=',nodeID,' feature=',root.featureID,' thr=',round(root.threshold,4),' gain:',round(root.gain,6),' distri=',root.distributions
                    q.put(root.left)
                    q.put(root.right)
                    nextLevelCount += 2
                if currLevelCount is 0:
                    print ""
                    currLevelCount = nextLevelCount
                    nextLevelCount = 0
