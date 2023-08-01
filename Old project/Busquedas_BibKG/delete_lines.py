lines = []

with open('milleDB.dump', 'r+', encoding="utf8") as dp:
    lines = dp.readlines()

    dp.seek(0)

    dp.truncate()
    
    delete_list = [52195967, 56097554, 118596880, 125035954, 125109568, 125127216, 125168753, 125169020, 125243340, 125832313, 131978116]
    for number, line in enumerate(lines):
        # delete line number 5 and 8
        # note: list index start from 0
        if number not in delete_list:
            dp.write(line)
            print('deleted line')
    print('work finished')