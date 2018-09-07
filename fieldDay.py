'''
Schedule games for a field day.
8 games, 8 teams, 8 rounds
Each team plays every game, and plays every other team at
least once, so one team twice.
'''
from algorithmX import solve
from collections import namedtuple, defaultdict
from functools import reduce

Match = namedtuple('Match', 'team1 team2 sport round'.split())

def makeMatches():
    sports = 'ABCDEFGH'
    answer = set()
    for team1 in range(7):
        for team2 in range(team1+1, 8):
            for sport in sports:
                answer.add(Match(team1, team2, sport, team1^team2))
    for sport in sports:
        answer.add(Match(0,1,sport,0))
        answer.add(Match(2,3,sport,0))
        answer.add(Match(4,5,sport,0))
        answer.add(Match(6,7,sport,0))
    return {Match(m.team1+1, m.team2+1, m.sport, m.round+1) for m in answer}

def makeRows(matches):
    '''
    Answer is a dict with key rowID and value a list
    of the appropriate column IDs
    '''
    answer = { }
    for m in matches:
        answer[m] = ['T%d%s'%(m.team1,m.sport), 'T%d%s'%(m.team2,m.sport), 
                             'R%s%d'%(m.sport, m.round),'M%d%d%d'%(m.team1,m.team2,m.round)]
    return answer

def makeColumns(matches):
    '''
    Answer is a dict with key columnID and value the set of
    appropriate rowIDs.  
    '''
    answer = { }
    for t1 in range(1,8):
        for t2 in range(t1+1, 9):
            for r in range(1,9):
                columnID = 'M%d%d%d'%(t1,t2,r)
                val= {m for m in matches if m.team1==t1 
                                                  and m.team2==t2 and m.round==r}
                if val: answer[columnID]=val
    for team in range(1,9):
        for sport in 'ABCDEFGH':
            columnID = 'T%d%s'%(team, sport)
            answer[columnID] = {m for m in matches if m.sport==sport and 
                                            team in (m.team1, m.team2)}
        for sport in 'ABCDEFGH':
            for round in range(1,9):
                columnID = 'R%s%d'%(sport, round)
                answer[columnID]={m for m in matches if m.sport==sport and m.round==round}        
    return answer
            
def makeSecondary(matches):
    '''
    Answer is the set of secondary column ID's
    These columns have at most one 1.  
    '''    
    answer = set()
    for round in range(1,9):
        for sport in 'ABCDEFGH':
            answer.add('R%s%d'%(sport, round))
    return answer

def union(X):
    return reduce(lambda x,y:x|y, X, set())

def auditSolution(solution):
    '''
    Each team plays every other team 
    Each team plays every sport
    No sport is played twice in the same round
    '''
    answer = True
    sports = 'ABCDEFGH'
    matchups = [{m.team1, m.team2} for m in solution]
    for team in range(1,9):
        players = [m for m in matchups if team in m]
        players = union(players)
        if len(players) != 8:
            print("Team %d doesn't play all opponents")
            answer = False
    for team in range(1,9):
        s = [m.sport for m in solution if team in (m.team1, m.team2)]
        if len(s) != 8:
            print("Team $d doesn't play all sports")
            answer = False
    for round in range(1,9):
        games = [m.sport for m in solution if m.round==round]
        if len(games) != 4:
            print('Duplicate game in round %d'%round)
            answer =False
    return answer

matches = makeMatches()
rows = makeRows(matches)
cols = makeColumns(matches)
secondary = makeSecondary(matches)
solutions = list(solve(cols, rows, secondary, 1))

if solutions:
    solution = solutions[0]
    assert auditSolution(solution)
    for round in range(1,9):
        print("Round", round)
        for m in {m for m in solution if m.round == round}:
            print("Team %d vs. Team %d in game %s"%(m.team1, m.team2, m.sport))
        print()
else:
    print('No solutions')
    from dancingLinks import highWater
    print(highWater)
    
        
 