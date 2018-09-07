# queens.py
# n queens problem 
# test generalized exact cover with dancing links

from algorithmX import solve
n = 14
# Each column and each row has exactly one queen
# Each diagonal has at most one queen
# 2n primary and 4n-2 secondary columns

# From Dancing Links paper
solutionCounts = {4:2, 5:10, 6:4, 7:40, 8:92, 9:352, 10:724, 11:2680, 
                           12:14200,  13:73712, 14:365596, 15:2279184, 
                           16:14772512, 17:95815104,  18:666090624 }

def makeRows(n):
    # There is one row for each cell.  
    # The key is "RrFf" where r is the rank and f the file
    # The value is a list of column ids    
    rows = dict()
    for rank in range(n):
        for file in range(n):
            rows["R%dF%d"%(rank,file)] = ["R%d"%rank, "F%d"%file, "S%d"%(rank+file), "D%d"%(rank-file)]
    return rows

def makePrimary(n):
    # One primary column for each rank and file
    # The key is a primary column id: either Rr or Ff
    # The value is a set of cell ids: RrFf
    prim = dict()
    for rank in range(n):
        prim["R%d"%rank] = {"R%dF%d"%(rank,file) for file in range(n)}
    for file in range(n):
        prim["F%d"%file] = {"R%dF%d"%(rank,file) for rank in range(n)}
    return prim

def makeSecondary(n):
    # One secondary column for each diagonal
    # The key is a secondary column id: Ss or Dd for the
    # sum and differnce diagonals
    # The value is a set of cell ids: RrFf
    second = dict()
    for s in range(2*n-1):
        second["S%d"%s] = {"R%dF%d"%(r, s-r) for r in range(max(0,s-n+1), min(s+1,n))}
    for d in range(-n+1, n):
        second["D%d"%(-d)]={"R%dF%d"%(r, r+d) for r in range(max(0,-d),min(n-d, n))}
    return second

def audit(rows, primary, secondary):
    cols = primary.copy()
    cols.update(secondary)
    answer = True
    for r in rows:
        for col in rows[r]:
            if r not in cols[col]:
                answer=False
                print("%s not in cols[%s]\n"%(r,col) )
    for c in cols:
        for row in cols[c]:
            if c not in rows[row]:
                answer = False
                print("%s not in rwos[%s]\n"%(c,row))
    return answer
    
rows = makeRows(n)
primary = makePrimary(n)
secondary = makeSecondary(n)
if audit(rows, primary, secondary):
    print("input passed audit")
primary.update(secondary)
secondary = secondary.keys()
solutionCount = 0
for s in solve(primary, rows, secondary, 0):
    solutionCount += 1
if solutionCount != solutionCounts[n]:
    print("actual %d expected %d"%(solutionCount, solutionCounts[n]))
