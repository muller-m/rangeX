import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# init variables
debugMode = False
checkBuy = False
boughtCurrentCandle = False
listTrades = []
listRanges = []
numRanges = 7
counter = 0
range = 0
sl = 0.05 

# read data
data = pd.read_csv("data/spy.csv")
if debugMode: print(data.head(7)) 

# iterate over data
if debugMode: print(type(data))
while counter < len(data):
    if debugMode: print("Iteration number: {}".format(counter)) 
    if checkBuy:
        # add buy
        newBuy = {
            "counterBuy": len(listTrades) + 1,
            "openDate": data.at[counter, 'Date'],
            "open": data.at[counter, 'Open'],
            "sl": round(data.at[counter, 'Open'] * (1 - sl), 2),
            "closeDate": None,
            "close": None,
            "profit": None
        }

        if debugMode: print("Add new buy to list") 
        listTrades.append(newBuy)

        boughtCurrentCandle = True
        checkBuy = False

    # checkSl
    if debugMode: print("Check SL for all open trades") 
    counter2 = counter
    while counter2 < len(listTrades):
        if data.at[counter2, 'Low'] <= listTrades[counter2]['sl']:
            listTrades[counter2]['close'] = listTrades[counter2]['sl']
            listTrades[counter2]['closeDate'] = data.at[counter2, 'Date']
            listTrades[counter2]['profit'] = listTrades[counter2]['open'] - listTrades[counter2]['close']
        counter2 += 1


    # compute range
    if debugMode: print("Compute range") 
    range = data.at[counter, 'High'] - data.at[counter, 'Low']
    listRanges.append(range)
    if len(listRanges) > numRanges:
        listRanges.pop(0)

    # skip check range?
    if debugMode: print("Check buy condition") 
    if boughtCurrentCandle == False:
        # check range
        minValueIndex = listRanges.index(min(listRanges))
        if minValueIndex == numRanges - 1:
            # set checkBuy
            checkBuy = True
    
    # check sell condition
    if debugMode: print("Check sell condition") 
    if counter > 0:
        if data.at[counter, 'Close'] >= data.at[counter - 1, 'High']:
            # 7.1 sell all open positions
            if debugMode: print("Sell all open positions") 
            close = data.at[counter, 'Close']
            for trade in listTrades:
                if trade["profit"] == None:
                    trade["closeDate"] = data.at[counter, 'Date']
                    trade["close"] = close
                    trade["profit"] = close - trade["open"]

    # increment counter
    counter += 1
    boughtCurrentCandle = False

# statistics
sumProfit = 0
numTrades = len(listTrades)
numWin = 0
maxWin = 0
maxLose = 0
sumAllWins = 0
sumAllLoses = 0
listDataGraph = [0]
for trade in listTrades:
    sumProfit += trade["profit"]
    print(trade)
    if trade["profit"] > 0:
        numWin += 1
        maxWin = max(maxWin, trade["profit"])
        sumAllWins += trade["profit"]
    else:
        maxLose = min(maxLose, trade["profit"])
        sumAllLoses += trade["profit"]

    # get data for graph
    listDataGraph.append(round(listDataGraph[len(listDataGraph) - 1] + trade["profit"], 2))


print("Number candles: {}".format(counter))
print("Sum profit: {}".format(round(sumProfit, 2)))
print("Hit rate: {} %".format(round((numWin/numTrades)*100, 2)))
print("Profit factor: {}".format(round(sumAllWins/abs(sumAllLoses), 2)))
print("Number trades: {}".format(round(numTrades, 2)))
print("Number winners: {}".format(numWin))
print("Largest win: {}".format(round(maxWin, 2)))
print("Largest lose: {}".format(round(maxLose, 2)))
print("Sum all wins: {}".format(round(sumAllWins, 2)))
print("Sum all loses: {}".format(round(sumAllLoses, 2)))

# graph
xpoints = np.arange(len(listDataGraph))
ypoints = np.array(listDataGraph)

plt.plot(xpoints, ypoints)
plt.title("rangeX")
plt.xlabel("Number Trades")
plt.ylabel("Profit")
plt.grid()
plt.show()