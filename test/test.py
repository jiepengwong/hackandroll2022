def text(data): #@Wkaggin owes @Chun_yangg $117.00 @jpoggers owes @Chun_yangg $117.00
    list = []
    sum = "@"+ str(data['owner'][1]) + " owes "
    if data['splitMethod'] == 'Manually':
        for value in data['payableAmount']:
            sum = sum + str(value) + " $" + str(data['payableAmount'][value])
            list.append(sum)
            sum = "@"+ str(data['owner'][1]) + " owes "
    else:
        for name in data['listing']:
            roundoff = round(data['payableAmount'],2)
            sum = sum + str(name) + " $" + str(roundoff)
            list.append(sum)
            sum = "@"+ str(data['owner'][1]) + " owes "
        #print(data['payableAmount'])

    return list



dicttest = {'owner': [861768079, 'Wkaggin'], 'listing': ['cy', 'jp'], 'total': 100, 'totalNumofPpl': 3,
            'splitMethod': 'Evenly', 'payableAmount': 33.333333333333336}
dicttest1 ={'owner': [861768079, 'Wkaggin'], 'listing': ['jp', 'cy'], 'total': 100, 'totalNumofPpl': 3, 
            'splitMethod': 'Manually', 'payableAmount': {'jp': '50', 'cy': '50'}}
#emptystr = ""
#print(dicttest1['splitMethod'])
print(text(dicttest))

    #print(key)
    #print(value)
#print(emptystr)


