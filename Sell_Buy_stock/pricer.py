import heapq
# http://rgmadvisors.com/problems/orderbook/
output = open("output.txt", "w")
def buy_shares_action(buy_shares, target_size, buy, time):
    #print "buy is ", buy
    buy_set = set()
    if buy_shares >= target_size:
        # you can buy the shares
        shares = target_size
        amount = float()
        heap_list = list()
        while True:
            element = heapq.heappop(buy)
            # print "element poped is", element
            heap_list.append(element)
            buy_set.add(element[2])
            if shares <= element[1]:
                amount += float(element[0])  * shares
                shares = 0
            else:
                # print float(element[0]), int(element[1])
                shares -= element[1]
                amount += float(element[0])  * int(element[1])
            if shares == 0:
                break
                # print "amount is ", amount, shares 
        output.write(time +" S " + str(-amount))
        output.write("\n")
        for each_ele in heap_list:
            heapq.heappush(buy, each_ele)
            # buy.insert(each_ele)
    return buy_set
def sell_shares_action(sell_shares, target_size, sell, time):
    #print "sell is", sell
    sell_set = set()
    if sell_shares >= target_size:
        # you can buy the shares
        shares = target_size
        amount = float()
        heap_list = list()
        while True:
            element = heapq.heappop(sell)
            heap_list.append(element)
            sell_set.add(element[2])
            #print element
            if shares <= element[1]:
                amount += float(element[0]) * shares
                shares = 0
            else:
                shares -= element[1]
                amount += float(element[0]) * int(element[1])
            if shares <= 0:
                break
        output.write(time +" B " + str(amount))
        output.write("\n")
        for each_ele in heap_list:
            heapq.heappush(sell, each_ele)
            # sell.insert(each_ele)
    return sell_set
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
    input_file = open("sample2.txt","r")
    #print input_file
    for each_line in input_file:
        each_values = each_line.split()
        #print each_values
        if each_values[1] == "A":
            #print "Add the share to the book"
            # check the buy shares count. If it exceeds then we can buy the share
            # add it to the min heap first
            if each_values[3] == "B":
                #print "B"
                heapq.heappush(buy, [float(each_values[4])*-1, float(each_values[5]), each_values[2], each_values[0]])
                buy_shares += int(each_values[5])
                buy_dict = {buy[index][2]: index for index in range(len(buy))}
                buy_set = buy_shares_action(buy_shares, target_size, buy, each_values[0])
                buy_dict = {buy[index][2]: index for index in range(len(buy))}
            else:
                # Selling
                #print "S"
                heapq.heappush(sell, [float(each_values[4]), float(each_values[5]), each_values[2], each_values[0]])
                sell_shares += int(each_values[5])
                sell_dict = {sell[index][2]: index for index in range(len(sell))}
                sell_set = sell_shares_action(sell_shares, target_size, sell, each_values[0])
                sell_dict = {sell[index][2]: index for index in range(len(sell))}
        else:
            #print "Reduce the share from the book"
            # remove the number of shares in the
            #print buy_dict, buy
            if each_values[2] in buy_dict:
                # the order id is in buy
                index = buy_dict[each_values[2]]
                buy[index][1] -= int(each_values[3])
                # reduce buy shares
                prev_share = buy_shares
                buy_shares -= int(each_values[3])
                if buy[index][1] <= 0:
                    # remove it
                    buy[index] = buy[-1]
                    buy.pop()
                    heapq.heapify(buy)
                    buy_dict = {buy[index][2]: index for index in range(len(buy))}
                if buy_shares >= target_size:
                    buy_set = buy_shares_action(buy_shares, target_size, buy, each_values[0])
                    buy_dict = {buy[index][2]: index for index in range(len(buy))}
                elif prev_share >= target_size:
                    output.write(each_values[0] + " S NA")
                    output.write("\n")
                #print buy_dict
            else:
                index = sell_dict[each_values[2]]
                sell[index][1] -= int(each_values[3])
                prev_share = sell_shares
                sell_shares -=int(each_values[3])
                # reduce sell shares
                if sell[index][1] <= 0:
                    # remove it
                    sell[index] = sell[-1]
                    sell.pop()
                    heapq.heapify(sell)
                    sell_dict = {sell[index][2]: index for index in range(len(sell))}
                '''
                Before calling the function , u have to check if it is needed or not
                this case isn't handled
                '''
                if sell_shares >= target_size:
                    sell_set = sell_shares_action(sell_shares, target_size, sell, each_values[0])
                    sell_dict = {sell[index][2]: index for index in range(len(sell))}
                elif prev_share >= target_size:
                    output.write(each_values[0] +" B NA")
                    output.write("\n")
if __name__ == "__main__":
    target_size = int(raw_input("Enter the target size"))
    main(target_size)
