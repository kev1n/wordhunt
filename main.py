import numpy as np
import requests
import random
import pandas as pd
import time
import multiprocessing

url = 'https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt'
existingWords = requests.get(url)
existingWords = existingWords.text.split()
existingWords = [word for word in existingWords if (len(word) == 4 or len(word) == 5 or len(word) == 6)]

def genLetter():
  alphabet = 'abcdefghijklmnopqrstuvwxyz'
  randletter = random.choice(alphabet)
  return randletter

def createboard(rand=False, dimensions = '4x4'):
  if rand == True:
    indexableboard = np.array([
                [genLetter(), genLetter(), genLetter(), genLetter()],
                [genLetter(), genLetter(), genLetter(), genLetter()],
                [genLetter(), genLetter(), genLetter(), genLetter()],
                [genLetter(), genLetter(), genLetter(), genLetter()],
                ])
    df = pd.DataFrame(data=indexableboard)
  else:
    line1 = input("Input letters:\n\n").lower()
    line2 = input().lower()
    line3 = input().lower()
    line4 = input().lower()

    indexableboard = np.array([		
        [line1[0], line1[1], line1[2], line1[3]],
        [line2[0], line2[1], line2[2], line2[3]],
        [line3[0], line3[1], line3[2], line3[3]],
        [line4[0], line4[1], line4[2], line4[3]]
    ])

    df = pd.DataFrame(data=indexableboard)
  return df

def getSurrounding(df, row, column):
  possible = []
  if row+1 < 4:
    possible.append([row+1, column])
  if row-1 > -1:
    possible.append([row-1, column])
  if column +1 < 4:
    possible.append([row, column+1])
  if column -1 > -1:
    possible.append([row, column-1])
  if row+1 < 4 and column +1 < 4:
    possible.append([row+1, column+1])
  if row+1 < 4 and column -1 > -1:
    possible.append([row+1, column-1])
  if row-1 > -1 and column +1 < 4:
    possible.append([row-1, column+1])
  if row-1 > -1 and column -1 > -1:
    possible.append([row-1, column-1])
  return possible


def solveBoard(df, beginningval, return_list):
    words = []

    board = df.copy()
    row = beginningval[0]
    column = beginningval[1]
    surroundings = getSurrounding(board, row, column)
    letter1 = board.iloc[row, column]
    board.iloc[row, column] = np.NaN

    for level1 in surroundings:
      wordlist = ''
      wordlist+=letter1
      row = level1[0]
      column = level1[1]

      if type(board.iloc[row, column]) == str:
        
        letter2 = board.iloc[row, column]
        surroundings1 = getSurrounding(board, row, column)
        board.iloc[row, column] = np.NaN
        wordlist+=letter2
        for level2 in surroundings1:
          board2 = board.copy()
          wordlist2 = wordlist

          row = level2[0]
          column = level2[1]
          if type(board2.iloc[row, column]) == str:
            letter3 = board2.iloc[row, column]
            wordlist2+=letter3
            surroundings2 = getSurrounding(board2, row, column)
            board2.iloc[row, column] = np.NaN
            words.append(wordlist2)
            for level3 in surroundings2:
              board3 = board2.copy()
              wordlist3 = wordlist2
    
              row = level3[0]
              column = level3[1]
              if type(board3.iloc[row, column]) == str:
                letter4 = board3.iloc[row, column]
                wordlist3+=letter4
                surroundings3 = getSurrounding(board3, row, column)
                board3.iloc[row, column] = np.NaN
                words.append(wordlist3)
                for level4 in surroundings3:
                  board4 = board3.copy()
                  wordlist4 = wordlist3
        
                  row = level4[0]
                  column = level4[1]
                  if type(board4.iloc[row, column]) == str:
                    letter5 = board4.iloc[row, column]
                    wordlist4+=letter5
                    surroundings4 = getSurrounding(board4, row, column)
                    board4.iloc[row, column] = np.NaN
                    words.append(wordlist4)
                    for level5 in surroundings4:
                      board5 = board4.copy()
                      wordlist5 = wordlist4
            
                      row = level5[0]
                      column = level5[1]
                      if type(board5.iloc[row, column]) == str:
                        letter6 = board5.iloc[row, column]
                        wordlist5+=letter6
                        board5.iloc[row, column] = np.NaN
                        words.append(wordlist5)
                        #print(words)

    possible = [word for word in words if word in existingWords]
    return_list += possible

if __name__ == '__main__':
  yes = []
  for i in range(4):
      for z in range(4):
          yes.append((i,z))
  processes = []
  board = createboard(rand=False)

  startime = time.time()
  manager = multiprocessing.Manager()
  return_list = manager.list()
  for m in yes:
      p = multiprocessing.Process(target=solveBoard, args=(board, m, return_list))
      processes.append(p)
      p.start()
   
  for process in processes:
      process.join()
  endtime = time.time()
  print(f'Finished successfully in {endtime-startime}')
  print(sorted(return_list, key=len, reverse=True))