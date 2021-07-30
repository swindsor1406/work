#not for maintenance script
#put in new max
#linepoint = newLinepoint
#if max is greater than 0, set to stock. Otherwise, set to OAN
#if linepoint > 0:
#	statustype = 'S'
#else:
#	statustype = 'O'

#actual maintenance script starts

#make sure taxable type is "taxable"
taxablety = 'Y'

#unitbuy check
#if unitbuy doesn't match unitstock or a uom, match to unitstock
if (unitbuy != unitstock or unitbuy != units): unitbuy = unitstock

#unitstnd check
list1 = [1, 2, 3] #this value needs to be assigned from the icsw table
list2 = [list1[0]] #adding the first value from the list to the shortened list of unique values
notInList2 = true #boolean for maintaining uniqueness of list2 items
for i in range(0, len(list1)-1):
    for j in range(0, len(list2)-1):
        #if list1[i] matches any value from list2[j], it skips the append statement
        if list1[i] == list2[j]:
            notInList2 = false 
    if notInList2:
        list2.append(list1[i])
    #prep notInList2 for use in the next iteration
    notInList2 = true 

#Now that list2 has been populated, we check for the count of each item in list2
itemCount = 0 #current highest count of items in list1
mostCommon #current most common item in list1
for i in range(0, len(list2)-1):
    tempCount = list1.count(list2[i])
    #if the current item is in list1 more than the last item, it will become the mostCommon, and itemCount will be updated
    if tempCount > itemCount:
        itemCount = tempCount
        mostCommon = list2[i]
#unitstnd gets matched to the most common value across whses
unitstnd = mostCommon

#ordcalcty check
#midstream whses should be set to M
if whse[0] == '2' or whse[0] == '4' or whse[0:3] == 'PV' or whse == 'ELPP':
    ordcalcty = 'M'

#up/downstream whses should be set to E
if whse[0] == '1' or whse[0] = '5' or whse[0] == '3' or whse == 'ELIP':
    ordcalcty = 'E'

#class check
#class always set to 1
itemClass = 1
#class is a keyword in python, so we can't use the same fieldname as SXe

#unitwt
#if unitwt is numeric, set to blank
tempWt = str(unitwt)
if tempWt.isnumeric():
    unitwt = ''

#usagectrl always B
usagectrl = 'B'

#countfl check
#Set to N for all whses except ELPP and ELIP
if !(whse == 'ELPP' or whse == 'ELIP'):
    countfl = 'N'

#not for maintenance script
#whserank check
#if whserank = 'F': whserank = 'C'

#asqfl check
#hi5fl check
#always Y
asqfl = 'Y'
hi5fl = 'Y'

#not for maintenance script
#minthreshold check

#not for maintenance script
#minthreshexpdt check

#asqdiff check
#hi5diff check
#always 0
asqdiff = 0
hi5diff = 0

#asqdifffl check
#hi5difffl check
#always N
asqdifffl = 'N'
hi5difffl = 'N'

#not for maintenance script
#threshrefer change0