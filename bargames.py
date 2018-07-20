'''
Schedule a bar games tournament.
Assumptions:
   Each team plays each sport the same number of times
   No sport can be played twice in the same round.
   The number of teams does not exceed twice the number of sports.
Requirements:
    If the number of team is even, each team plays in each round.
    If the number of teams is odd, all but one team plays in each round
    The number of times two teams meet should be minimized
'''
from dancingLinks import solve, highWater
from collections import namedtuple, defaultdict

Match = namedtuple("Match", "team1 team2 sport".split())
teams = 10  # number of teams
plays=2       # number of times each team plays each game

teams = ['T%d'%t for t in range(teams) ]
sports = ['beer pong','cornhole','darts','foosball','pool','table tennis']

def makeMatches(teams, sports, plays):
    matches = [ ]
    rounds = plays*sports
    for r in rounds:
        for p in range(len(teams)//2):
            matches.append(Match(teams[p], teams[-1-p], r))
            # rotate for the next round
        teams[1:]=[teams[-1]]+teams[1:-1]
    return matches

def auditMatches(teams, sports, plays, matches):
    answer = True
    versus = defaultdict(int)
    games = defaultdict(int)
    if len(set(matches)) != len(matches):
        answer = False
        matches = sorted(matches)
        for idx, m in enumerate(matches[:-1]):
            if m == matches[idx+1]:
                print('Duplicate match', m)
    for m in matches:
        t1, t2, s = m
        versus[t1, t2] += 1
        versus[t2, t1] += 1
        games[t1, s]    += 1
        games[t2, s]    += 1
    for t in teams:
        for s in sports:
            if games[t,s] != plays:
                answer = False
                print(t, 'plays game', s, games[t,s], 'times' )
    schedules = {t:[versus[t, t2] for t2 in teams] for t in teams }
    for t in teams:
        schedules[t]= tuple(sorted(schedules[t]))
    if len(set(schedules.values())) != 1:
        answer = False
        print('Different schedules')
        for t in teams:
            print(t, ':', schedule[t])
    return answer

def makeRounds(teams, sports, matches):
    '''
    Now we want to find legitimate rounds.  A round is a collection
    of matches in which every team participates, and no sport is
    played more than once. 
    '''
    primary = {t : {m for m in matches if t in {m.team1, m.team2}} for t in teams}
    secondary = {s :{m for m in matches if m.sport == s} for s in sports}
    primary.update(secondary)
    secondary = secondary.keys()
    rows = {m:[m.team1, m.team2, m.sport] for m in matches}
    return [r for r in solve(primary, rows, secondary)]  

def auditRounds(teams, matches, rounds):
    answer = True
    for r in rounds:
        if not all(m in matches for m in r):
            answer = False
            print(r, "does not consist of matches")
        players = {m.team1 for m in r} | {m.team2 for m in r}
        if len(players) != len(teams):
            answer = False
            print('Duplicate player in', r)
        games = {m.sport for m in r}
        if len(games) != len(r):
            answer = False
            print('Duplicate game in', r)
    return answer

def makeTournament(matches, rounds):
    '''
    Now we need to find a set of rounds that paritions the set of matches.
    The rows are rounds, and the columns are matches.
    This is an exact cover; there are only primary columns.
    '''
    rows = {t:rounds[t] for t in range(len(rounds))}
    columns = defaultdict(set)
    for m in matches:
        for t, r in enumerate(rounds):
            if m in r: columns[m].add(t)
    tournament = [rounds[t] for t in solve(columns, rows, set(), 1 )]
    return tournament

matches = makeMatches(teams, sports, plays)
if auditMatches(teams, sports, plays, matches):
    print('Matches passed audit')
rounds = makeRounds(teams, sports, matches)
if auditRounds(teams, matches, rounds):
    print('Rounds passed audit')
tournament = makeTournament(matches, rounds)