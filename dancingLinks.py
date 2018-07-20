# dancingLinks.pRows
# Retrieved from http://www.cs.mcgill.ca/~aassaf9/pRowsthon/algorithm_Cols.html
# on 18 December 2014
# Link no longer works

'''
In the set exact cover problem we are have a familiy F of subsets of a  set S,
and we seek to proude a subset of F that partitions S.
In the matrix formulation, Cols represents the columns of a 0-1 matrix, 
and Rows its rows.  The problem is to choose a subset of the rows, such that 
a one appears exactly once in each column of the submatrix comprising those rows.  

This script solves a generalized version of the exact cover problem.  Exactly one
one must appear in each primary column and at most one one must appear in each
secondary column.

Both Cols and Rows are implemented as dicts, with the key a column id in the
case of Cols or a row id in the case of Rows.  In Cols the value is a set of row ids, 
and for Rows the value is a list of column ids.  The ids in the collection are those
with a one in the indicated line of the matrix.

The only changes I've made to Ali Assaf's implementation, other than giving more
meaningful names to the variables, and expanding the comments, is to add the little 
wrapper to specify the maximumnumber of solutions to generate, and to extend it 
to handle secondary columns.
'''
global highWater
highWater = 0

def solve(Cols,  Rows, SecondaryIDs=set(), limit = 0):
    '''
    SecondaryIDs is an iterable of IDs for the secondary columns
    limit is the maximum number of solutions to generate.
    0 means generate all solutions
    '''
    for soln in solver(Cols, Rows, SecondaryIDs):
        yield soln
        limit -= 1
        if limit == 0: raise StopIteration
        
def solver(Cols, Rows, SecondaryIDs, solution=[]):
    global highWater
    live=[col for col in Cols if col not in SecondaryIDs] 
    if not live:
        yield list(solution)
    else:
        col = min(live, key = lambda col: len(Cols[col]))        # hardest primary column to cover is best for branching
        for row in list(Cols[col]):                                          # for each row with a 1 in the current column
            solution.append(row)                                            # tentatively add it to the solution
            level=len(solution)
            highWater = max(highWater, level)
            columns = select(Cols, Rows, row)                        
            for soln in solver(Cols, Rows, SecondaryIDs, solution):
                yield soln
            deselect(Cols, Rows, row, columns)
            solution.pop()
                    
def select(Cols, Rows, row):
    # row has just been tenatively added to the solution 
    # we need to remove any column with a 1 in row from the matrix,
    # since it's been covered.  For each such column, we need to
    # remove any row that has a 1 in the column, since adding that
    # row to the solution would cover the column a second time.
    # For any column with a 1 in such a removed row, we have to 
    # remove the 1, since it can no longer be covered by that row.
    # Finally, we return a list of the deleted columns, so that they
    # can be restored during backtrack.
    columns = []
    for col in Rows[row]:
        for rrow in Cols[col]:
            for ccol in Rows[rrow]:
                if ccol != col:
                    Cols[ccol].remove(rrow)
        columns.append(Cols.pop(col))  # the column is removed here
    return columns

def deselect(Cols, Rows, row, columns):
    # This is the inverse of select, where we remove row
    # from the solution, and put back the columns and rows
    # that were deleted from the matrix.  
    for col in reversed(Rows[row]):
        Cols[col] = columns.pop()
        for rrow in Cols[col]:
            for ccol in Rows[rrow]:
                if ccol != col:
                    Cols[ccol].add(rrow)
