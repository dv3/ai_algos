#!/usr/bin/python

import sys
import heapq

#Parsing the commandline arguments and checking for errors
#find_route input_filename origin_city destination_city
totalArguments=len(sys.argv)
if(totalArguments != 4 ):
	print ("Arguments not equal to 4")
	print ("Usage: find_route input_filename origin_city destination_city.")
	sys.exit("Exiting")


input_filename=str(sys.argv[1])
origin_city=str(sys.argv[2])
destination_city=str(sys.argv[3])

#cmdArguments=str(sys.argv)
#print ("The total numbers of args: %d " % totalArguments)
#print ("Args list: %s " % cmdArguments)

#global dict for saving the map
grap={}


#this functions checks if the given city is goal state or not
#it expands and returns newer nodes
#it returns the cost between given inputs
def finds(keyswods,forMe,fromMe):
  if keyswods is 'isGoal':
    if forMe == destination_city:
      return True
    else: 
      return False
  if keyswods is 'successors':
    if forMe in grap:
      return grap[forMe].keys()
    else:
      return None
  if keyswods is 'cost':
    tempValue = grap[forMe]
    if tempValue :
      if fromMe in tempValue:
        return tempValue[fromMe]
    else:
      return None   

#It uses the Uniform cost algorithm to find shortest route
def uniform_cost(start_state):
  #q should act as prioritqueue.heapq is used to implement one in this python
  q = [(0, ((),start_state)) ]
  explored=set()
  while q:
    (cost, path) = heapq.heappop(q)
    state = path[-1]
    #print ("checking state: %s , cost:%s" % (state,cost)) 
    if not state in explored:
      explored.add(state)
      if finds("isGoal",state,0):
        #print path,cost
        return path,cost
      ee = finds("successors",state,0)
      if ee:
        for x in finds("successors",state,0):#state.successors():
          #x is kids of state
          yy=finds("cost",x,state)
          if x not in explored: 
            heapq.heappush(q, (cost + yy, (path, x)))
      else:
        return None

#Takes the file name as input to read and fill the global dict 'grap'
def fileRead(input_file):
  #print ("lets start reading: %s" % input_file)
  fout = open(input_file, "r")
  try:
    #print "filling list"
    for line in fout:
      #print line
      if "END OF INPUT" not in line:
        hmm=line.rsplit(' ')
        src=hmm[0]
        desti=hmm[1]
        aa=hmm[2]
        dist=int(aa)
        #print ("src:%s..desti:%s.. " %(src,desti))

        if src in grap:
          if desti in grap:
            #update src
            tempa=grap[src]
            tempa[desti]=dist
            grap[src]=tempa
            #update desti
            tempa=grap[desti]
            tempa[src]=dist
            grap[desti]=tempa
            #input repeated or we have this taken care of, but have we joined
          else:
            grap[desti]={src:dist}
            tempa=grap[src]
            tempa[desti]=dist
            grap[src]=tempa
            #src in grap and desti not in grap. update src
        else:
          if desti in grap:
            grap[src]={desti:dist}
            tempa=grap[desti]
            tempa[src]=dist
            grap[desti]=tempa
            #src not in grap and desti in grap. update desti
          else:
            grap[src]   = {desti:dist}
            grap[desti] = {src:dist}
            #src not in grap and desti not in grap. create both
      else:
        break
  finally:
    fout.close()

def main():
  #print ("inputs are: %s %s %s" %(input_filename,origin_city,destination_city) )
  fileRead(input_filename)
  #print grap
  oo=uniform_cost(origin_city)
  if oo is None:
    print "distance: infinity"
    print "route:"
    print "none"
  else:
    L=oo[0]
    ans = []
    while len(L) > 0:
      ans.append(L[-1])
      L = L[0]
    finale=ans[::-1]
    print ("distance: %s km" % oo[1])
    print "route:"
    if len(finale) is 1:
      print ("%s to %s, 0 km" % (finale[0],finale[0] ) )
    else:
      for m in range(len(finale)-1):
        yy=finds("cost",finale[m+1],finale[m])
        print ("%s to %s, %s km" % (finale[m],finale[m+1],yy ) )

if __name__ == '__main__':
  main()