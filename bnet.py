import sys,os

class Bayesian_network_class:
    def __init__(self):
        self.value = True

    # compute probability that var has the value val.  e are the list of
    # variable values we already know, and bn has the conditional probability
    # tables.
    def Pr(self,var, val, e, bn):
        parents = bn[var][0]
        #print('Pr***', var, val, e, bn, parents)
        if len(parents) == 0:
            truePr = bn[var][1][None]
        else:
            #print('   Pr*** : parents'),parents
            parentVals = [e[parent] for parent in parents]
            truePr = bn[var][1][tuple(parentVals)]
        if val==True: return truePr
        else: return 1.0-truePr

    def normalize(self,QX,wants):
        total = 0.0
        for val in QX.values():
            total += val
        for key in QX.keys():
            QX[key] /= total

        kk=QX[wants]
        return kk

    def enumerationAsk(self,X, e, bn,varss):
        QX = {}
        # X={'A':True}
        jj=X.values()
        wants=jj[0]
        ll=X.keys()
        X=ll[0]
        for xi in [False,True]:
            e[X] = xi
            QX[xi] = self.enumerateAll(varss,e,bn)
            mm=QX[xi]
            del e[X]
        #return QX
        #print 'QX',QX
        return self.normalize(QX,wants)

    def enumerateAll(self,varss, e,bn):
        #print('EnumerateAll***', varss, e, bn)
        if len(varss) == 0: return 1.0
        Y = varss.pop()
        if Y in e:
            val = self.Pr(Y,e[Y],e,bn) * self.enumerateAll(varss,e,bn)
            varss.append(Y)
            return val
        else:
            total = 0
            e[Y] = True
            total += self.Pr(Y,True,e,bn) * self.enumerateAll(varss,e,bn)
            e[Y] = False
            total += self.Pr(Y,False,e,bn) * self.enumerateAll(varss,e,bn)
            del e[Y]
            varss.append(Y)
            return total

    def find_paarents(self,var, bn):
        parents = bn[var][0]
        return parents

    def deepak(self,C1,varss,bn):
        answer=0
        ww=C1.keys()
        theseAreNotPresent=[]
        for q in varss:
            if not(q in ww):
                theseAreNotPresent.append(q)

        itneBaar=len(theseAreNotPresent)
        eee=2^itneBaar
        jj=C1
        if itneBaar==0:
            answer=answer+self.computeProbability(jj,bn,varss)
        elif itneBaar ==1:
            jj[theseAreNotPresent[0]]=True
            answer=answer+self.computeProbability(jj,bn,varss)
            jj[theseAreNotPresent[0]]=False
            answer=answer+self.computeProbability(jj,bn,varss)
        elif itneBaar==2:
            jj[theseAreNotPresent[0]]=True
            jj[theseAreNotPresent[1]]=True
            answer=answer+self.computeProbability(jj,bn,varss)
            jj[theseAreNotPresent[0]]=True
            jj[theseAreNotPresent[1]]=False
            answer=answer+self.computeProbability(jj,bn,varss)
            jj[theseAreNotPresent[0]]=False
            jj[theseAreNotPresent[1]]=True
            answer=answer+self.computeProbability(jj,bn,varss)
            jj[theseAreNotPresent[0]]=False
            jj[theseAreNotPresent[1]]=False
            answer=answer+self.computeProbability(jj,bn,varss)
        elif itneBaar==3:
            jj[theseAreNotPresent[0]]=True
            jj[theseAreNotPresent[1]]=True
            jj[theseAreNotPresent[2]]=True
            answer=answer+self.computeProbability(jj,bn,varss)
            jj[theseAreNotPresent[0]]=True
            jj[theseAreNotPresent[1]]=True
            jj[theseAreNotPresent[2]]=False
            answer=answer+self.computeProbability(jj,bn,varss)
            jj[theseAreNotPresent[0]]=True
            jj[theseAreNotPresent[1]]=False
            jj[theseAreNotPresent[2]]=True
            answer=answer+self.computeProbability(jj,bn,varss)
            jj[theseAreNotPresent[0]]=True
            jj[theseAreNotPresent[1]]=False
            jj[theseAreNotPresent[2]]=False
            answer=answer+self.computeProbability(jj,bn,varss)
            jj[theseAreNotPresent[0]]=False
            jj[theseAreNotPresent[1]]=True
            jj[theseAreNotPresent[2]]=True
            answer=answer+self.computeProbability(jj,bn,varss)
            jj[theseAreNotPresent[0]]=False
            jj[theseAreNotPresent[1]]=True
            jj[theseAreNotPresent[2]]=False
            answer=answer+self.computeProbability(jj,bn,varss)
            jj[theseAreNotPresent[0]]=False
            jj[theseAreNotPresent[1]]=False
            jj[theseAreNotPresent[2]]=True
            answer=answer+self.computeProbability(jj,bn,varss)
            jj[theseAreNotPresent[0]]=False
            jj[theseAreNotPresent[1]]=False
            jj[theseAreNotPresent[2]]=False
            answer=answer+self.computeProbability(jj,bn,varss)
        elif itneBaar==4:
            jj[theseAreNotPresent[0]]=True
            jj[theseAreNotPresent[1]]=True
            jj[theseAreNotPresent[2]]=True
            jj[theseAreNotPresent[3]]=True
            answer=answer+self.computeProbability(jj,bn,varss)
            jj[theseAreNotPresent[0]]=True
            jj[theseAreNotPresent[1]]=True
            jj[theseAreNotPresent[2]]=True
            jj[theseAreNotPresent[3]]=False
            answer=answer+self.computeProbability(jj,bn,varss)
            jj[theseAreNotPresent[0]]=True
            jj[theseAreNotPresent[1]]=True
            jj[theseAreNotPresent[2]]=False
            jj[theseAreNotPresent[3]]=True
            answer=answer+self.computeProbability(jj,bn,varss)
            jj[theseAreNotPresent[0]]=True
            jj[theseAreNotPresent[1]]=True
            jj[theseAreNotPresent[2]]=False
            jj[theseAreNotPresent[3]]=False
            answer=answer+self.computeProbability(jj,bn,varss)
            jj[theseAreNotPresent[0]]=True
            jj[theseAreNotPresent[1]]=False
            jj[theseAreNotPresent[2]]=True
            jj[theseAreNotPresent[3]]=True
            answer=answer+self.computeProbability(jj,bn,varss)
            jj[theseAreNotPresent[0]]=True
            jj[theseAreNotPresent[1]]=False
            jj[theseAreNotPresent[2]]=True
            jj[theseAreNotPresent[3]]=False
            answer=answer+self.computeProbability(jj,bn,varss)
            jj[theseAreNotPresent[0]]=True
            jj[theseAreNotPresent[1]]=False
            jj[theseAreNotPresent[2]]=False
            jj[theseAreNotPresent[3]]=True
            answer=answer+self.computeProbability(jj,bn,varss)
            jj[theseAreNotPresent[0]]=True
            jj[theseAreNotPresent[1]]=False
            jj[theseAreNotPresent[2]]=False
            jj[theseAreNotPresent[3]]=False
            answer=answer+self.computeProbability(jj,bn,varss)
            jj[theseAreNotPresent[0]]=False
            jj[theseAreNotPresent[1]]=True
            jj[theseAreNotPresent[2]]=True
            jj[theseAreNotPresent[3]]=True
            answer=answer+self.computeProbability(jj,bn,varss)
            jj[theseAreNotPresent[0]]=False
            jj[theseAreNotPresent[1]]=True
            jj[theseAreNotPresent[2]]=True
            jj[theseAreNotPresent[3]]=False
            answer=answer+self.computeProbability(jj,bn,varss)
            jj[theseAreNotPresent[0]]=False
            jj[theseAreNotPresent[1]]=True
            jj[theseAreNotPresent[2]]=False
            jj[theseAreNotPresent[3]]=True
            answer=answer+self.computeProbability(jj,bn,varss)
            jj[theseAreNotPresent[0]]=False
            jj[theseAreNotPresent[1]]=True
            jj[theseAreNotPresent[2]]=False
            jj[theseAreNotPresent[3]]=False
            answer=answer+self.computeProbability(jj,bn,varss)
            jj[theseAreNotPresent[0]]=False
            jj[theseAreNotPresent[1]]=False
            jj[theseAreNotPresent[2]]=True
            jj[theseAreNotPresent[3]]=True
            answer=answer+self.computeProbability(jj,bn,varss)
            jj[theseAreNotPresent[0]]=False
            jj[theseAreNotPresent[1]]=False
            jj[theseAreNotPresent[2]]=True
            jj[theseAreNotPresent[3]]=False
            answer=answer+self.computeProbability(jj,bn,varss)
            jj[theseAreNotPresent[0]]=False
            jj[theseAreNotPresent[1]]=False
            jj[theseAreNotPresent[2]]=False
            jj[theseAreNotPresent[3]]=True
            answer=answer+self.computeProbability(jj,bn,varss)
            jj[theseAreNotPresent[0]]=False
            jj[theseAreNotPresent[1]]=False
            jj[theseAreNotPresent[2]]=False
            jj[theseAreNotPresent[3]]=False
            answer=answer+self.computeProbability(jj,bn,varss)


        #print 'deepak: answer',answer
        return answer


    #does only the following
    #P(B, E, A, JC, MC)=P(B) * P(E) * P(A | B, E) * P(JC | A) * P(MC |A)
    def computeProbability(self,mydict,bn,varss):
        adds=1
        for v in mydict:
            if   v == 'B':
                adds=adds*self.enumerationAsk({'B':mydict[v]},{},bn,varss)
            elif v == 'E':
                adds=adds*self.enumerationAsk({'E':mydict[v]},{},bn,varss)
            elif v == 'A':
                adds=adds*self.enumerationAsk({'A':mydict[v]},{'B':mydict['B'],'E':mydict['E']},bn,varss)
            elif v == 'J':
                adds=adds*self.enumerationAsk({'J':mydict[v]},{'A':mydict['A']},bn,varss)
            elif v == 'M':
                adds=adds*self.enumerationAsk({'M':mydict[v]},{'A':mydict['A']},bn,varss)

        #print 'computeProbability:',adds
        return adds

def main(argv):
    # Make sure we have enough command-line arguments
    if len(argv) >7 or len(argv) <2:
        print '1 to 6 command-line arguments only:'
        print('Usage: %s Jt given Bt Ef' % argv[0])
        sys.exit(2)

    C1={}
    C2={}
    coun=0
    for x in argv[1::1]:
        coun=coun+1
        if not(x == 'given'):
            y=list(x)
            if y[1] == 't':
                C1[y[0].upper()]=True
            elif y[1] == 'f':
                C1[y[0].upper()]=False
        else:
            break

    if coun != 0:
        for n in range(coun+1,len(argv)):
            m=argv[n]
            y=list(m)
            if y[1] == 't':
                C2[y[0].upper()]=True
            elif y[1] == 'f':
                C2[y[0].upper()]=False

    print 'C1:',C1
    print 'C2:',C2

    varss = ['M','J','A','B','E']

    for x in C1:
        if not(x in varss):
            print 'wrong inputs in C1.should be from these symbols [M,J,A,B,E].exiting'
            sys.exit(2)

    for x in C2:
        if not(x in varss):
            print 'wrong inputs in C2.should be from these symbols [M,J,A,B,E].exiting'
            sys.exit(2)

    BayesNet = Bayesian_network_class()

    bn = {'B':[[],{None:.001}],
          'E':[[],{None:.002}],
          'A':[['B','E'],
                   {(False,False):.001,(False,True):.29,
                    (True,False):.94,(True,True):.95}],
          'J':[['A'],
                       {(False,):.05,(True,):.90}], #note: (False,) is a tuple with just the value False.  (False) would not be, python makes that just False, and that would not be good because the code above assumes it is a tuple.
          'M':[['A'],
                       {(False,):.01,(True,):.70}]}

    answer=0
    if len(C2) !=0:
        C3 = dict(C1.items() + C2.items())
        part1=(BayesNet.deepak(C3,varss,bn))
        part2=(BayesNet.deepak(C2,varss,bn))
        answer=part1/float(part2)
    else:
        answer=(BayesNet.deepak(C1,varss,bn))

    print "Probability is:",answer

    print '\n finished'

if __name__ == '__main__':
    main(sys.argv)