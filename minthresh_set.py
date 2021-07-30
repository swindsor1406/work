import datetime

#Set the expiration date for the thresholds
def setMinthreshexpdt(date = (datetime.datetime.now().strftime("%m") + datetime.datetime.now().strftime("%d") + datetime.datetime.now().strftime("%y"))):
    #set newMonth to 3 months from now
    date = str(date)
    newMonth = date[0:2]
    newMonth = int(newMonth) + 3
    
    #check to see if it's past the 15th
    if int(date[2:4]) > 15:
        #if yes, add a fourth month
        newMonth = newMonth + 1
    
    #make sure the month isn't over 12
    if (newMonth > 12): newMonth = newMonth % 12
    
    #add the new month to the date string
    if newMonth < 10:
        #make sure there's a leading 0
        newMonth = str(newMonth)
        newMonth = "0" + newMonth
    else:
        #no leading 0
        newMonth = str(newMonth)
    
    newDate = newMonth + "01" + date[4:6]
    return newDate