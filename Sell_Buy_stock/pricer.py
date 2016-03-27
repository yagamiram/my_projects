import heapq
# http://rgmadvisors.com/problems/orderbook/

def main(target_size):
    # two variables for buy and sell
    # read the csv files
    # Use min heap for Buy and max heap for sell
    buy_shares = int() # total shares count
    sell_shares = int()
    buy = []
    sell = []
    buy_dict = dict()
    sell_dict = dict()
    input_file = open("sample.txt","r")
    #print input_file
    for each_line in input_file:
        each_values = each_line.split()
        #print each_values
        if each_values[1] == "A":
            #print "Add the share to the book"
            # check the buy shares count. If it exceeds then we can buy the share
            # add it to the min heap first
            if each_values[3] == "B":
                heapq.heappush(buy, [float(each_values[4])*-1, float(each_values[5]), each_values[2]])
                buy_shares += int(each_values[5])
                buy_dict = {buy[index][2]: index for index in range(len(buy))}
                if buy_shares >= target_size:
                    # you can buy the shares
                    shares = target_size
                    amount = float()
                    heap_list = list()
                    while True:
                        element = heapq.heappop(buy)
                        #print "element poped is", element
                        heap_list.append(element)
                        if shares <= element[1]:
                            amount += float(element[0]*-1 * shares)
                            shares = 0
                        else:
                            #print float(element[0]), int(element[1])
                            shares -= element[1]
                            amount += float(element[0])*-1 * int(element[1])
                        if shares == 0:
                            break
                        #print "amount is ", amount, shares
                    print "time S "+ str(amount)
                    for each_ele in heap_list:
                        heapq.heappush(buy, each_ele)
                        #buy.insert(each_ele)
            else:
                # Selling
                heapq.heappush(sell, [float(each_values[4]), float(each_values[5]), each_values[2]])
                sell_shares += int(each_values[5])
                sell_dict = {sell[index][2]: index for index in range(len(sell))}
                if sell_shares >= target_size:
                    # you can buy the shares
                    shares = target_size
                    amount = float()
                    heap_list = list()
                    while True:
                        element = heapq.heappop(sell)
                        heap_list.append(element)
                        if shares <= element[1]:
                            shares = 0
                            amount += float(element[0] * shares)
                        else:
                            shares -= element[1]
                            amount += float(element[0]) * int(element[1])
                        if shares == 0:
                            break
                    print "time B " + str(amount)
                    for each_ele in heap_list:
                        heapq.heappush(sell, each_ele)
                        #sell.insert(each_ele)
        else:
            #print "Reduce the share from the book"
            # remove the number of shares in the
            if each_values[2] in buy_dict:
                # the order id is in buy
                index = buy_dict[each_values[2]]
                buy[index][1] -= int(each_values[3])
                # reduce buy shares
                buy_shares -= int(each_values[3])
                if buy[buy_dict[each_values[2]]][1] <= 0:
                    # remove it
                    buy[index] = buy[-1]
                    buy.pop()
                    heapq._heapify_max(buy)
            else:
                #print "sell dict is", sell_dict
                index = sell_dict[each_values[2]]
                #print sell, sell[index][1], each_values[3]
                sell[index][1] -= int(each_values[3])
                sell_shares -=int(each_values[3])
                # reduce sell shares
                if sell[sell_dict[each_values[2]]][1] <= 0:
                    # remove it
                    sell[index] = buy[-1]
                    sell.pop()
                    heapq._heapify_max(sell)
if __name__ == "__main__":
    main(200)
