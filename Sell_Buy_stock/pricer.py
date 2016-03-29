import heapq
import sys
import fileinput
# http://rgmadvisors.com/problems/orderbook/
'''
Challenge:
write a program, Pricer, that analyzes such a log file. Pricer takes one command-line argument: target-size. 
Pricer then reads a market data log on standard input. 
As the book is modified, Pricer prints (on standard output) the total expense you would incur if you bought 
target-size shares (by taking as many asks as necessary, lowest first), and the total income you would receive if you sold 
target-size shares (by hitting as many bids as necessary, highest first). Each time the income or expense changes, it prints 
the changed value.

How it is Implemented?
Since the problem is to the find total income incur or gained whenever the target size is reached, the logic of the problem
is dependent on which stocks to buy and sell at right time.
To maintain the stocks in an order, a max heap and min heap is used.
The max heap is to constructed so that when the target size is reached, it's time to sell the stocks by picking the stock which has
highest value.
Similarly, to buy a set of stocks when the target size is reached, a min heap which gives the one with less value in the market is picked to 
buy the stocks.
To maintain the heap and to remove a stock whenever its share is reduced to 0, a dictionary is used to keep track of the indexes of the stock
in the heaps.

Input is read from command line argument and output is sent to a file called output.txt  
'''
'''
File handler for the output stream.
'''
output = open("output.txt", "w")

'''
Buy or sell the shares
This module 
'''
def buy_or_sell(target_size, buy_heap, sell_heap, time, buy_sell_flag):
    shares = target_size
    amount = float()
    heap_list = list()
    if buy_sell_flag == "B":
        stock_heap = buy_heap
    else:
        stock_heap = sell_heap
    while True:
        element = heapq.heappop(stock_heap)
        heap_list.append(element)
        if shares <= element[1]:
            amount += float(element[0])  * shares
            shares = 0
        else:
            shares -= element[1]
            amount += float(element[0])  * int(element[1])
        if shares == 0:
            break
    if buy_sell_flag == "B":
        output.write(time +" S " + str(-amount))
    else:
        output.write(time +" B " + str(amount))
    output.write("\n")
    for each_ele in heap_list:
            heapq.heappush(stock_heap, each_ele)

def main(target_size, data):
    '''
    This is the main function of parsing the log book.
    Each entry in the log book is parsed to find if the data is to be added "A" or reduced "R"
    If it has to be added then it is checked again on "B" buy or "S" sell.
    '''
    buy_shares = int() # Total number of shares so far seen for Buy
    sell_shares = int() # Total number of shares so far seen for Sell
    buy_heap = [] # A list that maintains the min heap for buying the stocks.
    sell_heap = [] # A list that maintians the max heap for selling the stocks
    buy_dict = dict() # A hash table that maintains the index of each element in the min heap to remove it easily
    sell_dict = dict() # A hash table that maintains the index of each element in the max heap to remove it easily
    for each_line in data:
        each_values = each_line.split()
        time = each_values[0]  # time of the entry
        literal = each_values[1] # Literal of the entry
        order_id = each_values[2] # order id of the entry
        if literal == "A":
            side = each_values[3] # side of the entry
            price = each_values[4] # price of the entry
            size = each_values[5] # size of the entry
            if side == "B":
                # Push the entry into the the min heap
                # Each node in the min heap contains, the price, size and order_id
                heapq.heappush(buy_heap, [float(price)*-1, float(size), order_id])
                # Accumulation of all buy shares
                buy_shares += int(size)
                # Tracking the index of each node in the min heap
                buy_dict = {buy_heap[index][2]: index for index in range(len(buy_heap))}
                # If the total share goes beyond target size then buy the stock
                if buy_shares >= target_size:
                    buy_or_sell(target_size, buy_heap, sell_heap, time, side)
                    buy_dict = {buy_heap[index][2]: index for index in range(len(buy_heap))}
            else:
                # same goes for "selling"
                heapq.heappush(sell_heap, [float(price), float(size), order_id])
                sell_shares += int(size)
                sell_dict = {sell_heap[index][2]: index for index in range(len(sell_heap))}
                if sell_shares >= target_size:
                    buy_or_sell(target_size, buy_heap, sell_heap, time, side)
                    sell_dict = {sell_heap[index][2]: index for index in range(len(sell_heap))}
        else:
            # Reduce 
            # Decrement the number of shares of an order id
            # If the share count goes below to 0 then remove it from the heap
            size = each_values[3]
            if order_id in buy_dict:
                index = buy_dict[order_id]
                buy_heap[index][1] -= int(size)
                prev_share = buy_shares
                buy_shares -= int(size)
                if buy_heap[index][1] <= 0:
                    buy_heap[index] = buy_heap[-1]
                    buy_heap.pop()
                    heapq.heapify(buy_heap)
                    buy_dict = {buy_heap[index][2]: index for index in range(len(buy_heap))}
                if buy_shares >= target_size:
                    buy_or_sell(target_size, buy_heap, sell_heap, time, "buy")
                    buy_dict = {buy_heap[index][2]: index for index in range(len(buy_heap))}
                elif prev_share >= target_size:
                    output.write(time + " S NA")
                    output.write("\n")
            else:
                index = sell_dict[order_id]
                sell_heap[index][1] -= int(size)
                prev_share = sell_shares
                sell_shares -=int(size)
                if sell_heap[index][1] <= 0:
                    sell_heap[index] = sell_heap[-1]
                    sell_heap.pop()
                    heapq.heapify(sell_heap)
                    sell_dict = {sell_heap[index][2]: index for index in range(len(sell_heap))}
                if sell_shares >= target_size:
                    buy_or_sell(target_size, buy_heap, sell_heap, time, "sell")
                    sell_dict = {sell_heap[index][2]: index for index in range(len(sell_heap))}
                elif prev_share >= target_size:
                    output.write(time +" B NA")
                    output.write("\n")
if __name__ == "__main__":
    target_size = int(sys.argv[1])
    data = sys.stdin.readlines()
    main(target_size, data)
