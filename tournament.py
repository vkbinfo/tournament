#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db=connect()
    cursor=db.cursor()
    cursor.execute("update matchRecord set totalMatch=0 , win=0")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("delete from matchRecord;")
    db.commit()
    cursor.execute("delete from match;")
    db.commit()
    cursor.execute("delete from player;")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("select * from player;")
    data=cursor.fetchall()
    db.close()
    return len(data)

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    cursor = db.cursor()
    cursor.execute("insert into player(name) values(%s) returning id",(name,))
    db.commit()
    cursor.execute("select max(id) from player")
    id=cursor.fetchone()[0]
    cursor.execute("insert into matchRecord(id,totalmatch,win) values(%(int)s, %(totalmatch)s, %(win)s)",
                   {'int':id,'totalmatch':0,'win':0})
    db.commit()
    db.close()



def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db=connect()
    cursor=db.cursor()
    cursor.execute('select player.id,player.name,matchRecord.win,matchRecord.totalMatch'+
                   ' from player join matchRecord on player.id=matchRecord.id order by matchRecord.win;')
    data=cursor.fetchall()
    db.close()
    return data

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db=connect()
    cursor=db.cursor()
    cursor.execute('select matchRecord.totalMatch,matchRecord.win from matchRecord where id='+str(winner))
    winnerTotalMatch,winnerWin=cursor.fetchall()[0]
    winnerTotalMatch +=1
    winnerWin +=1
    cursor.execute('select matchRecord.totalMatch from matchRecord where id=' + str(loser))
    loserTotalMatch=cursor.fetchall()[0][0]
    loserTotalMatch +=1
    cursor.execute('update matchRecord SET totalMatch='+str(winnerTotalMatch)+' ,win='+str(winnerWin)+
                   ' where id = '+str(winner))
    cursor.execute('update matchRecord SET totalMatch=' + str(loserTotalMatch) +
                   ' where id = ' + str(loser))
    db.commit()
    db.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    data=playerStandings()
    pairs=[]
    while len(data):
        x=data.pop()
        id1=x[0]
        name1=x[1]
        y=data.pop()
        id2=y[0]
        name2=y[1]
        pairs.append((id1,name1,id2,name2))
    return pairs

