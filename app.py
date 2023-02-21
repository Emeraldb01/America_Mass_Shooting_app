import psycopg2
from datetime import date

# for colored text
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    OKMAGENTA = '\033[35m'
    FAIL = '\033[91m'
    ENDC = '\033[0m' # standard
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# print out details of one chosen case
# input = all attributes of one case
def print_case(ans):
    print(bcolors.OKBLUE + "Case name: " + bcolors.ENDC, end='')
    print(bcolors.OKBLUE + ans[0] + bcolors.ENDC)
    print(bcolors.OKMAGENTA + "Location: " + bcolors.ENDC, end='')
    print(ans[1])
    print(bcolors.OKMAGENTA + "Date: " + bcolors.ENDC, end = '')
    print(str(ans[3]))
    print(bcolors.OKMAGENTA + "Fatality: " + bcolors.ENDC, end = '')
    print(str(ans[6]))
    print(bcolors.OKMAGENTA + "Injured: " + bcolors.ENDC, end = '')
    print(str(ans[7]))
    print(bcolors.OKMAGENTA + "\nSummary: " + bcolors.ENDC)
    print(ans[5])
    print(bcolors.OKMAGENTA + "\nLocation of shooting: " + bcolors.ENDC, end='')
    print(ans[8])
    print(bcolors.OKMAGENTA + "Prior sign of mental illness: " + bcolors.ENDC,end='')
    print(ans[10])
    print(bcolors.OKMAGENTA + "Weapon type: " + bcolors.ENDC,end='')
    print(ans[13])

    # looking up firearm law table
    sql ="""SELECT "lawtotal" FROM "Firearm_law" WHERE "state" = %(sta)s and "year" = %(yr)s;"""
    cursor.execute(sql,{"sta" : ans[2], "yr" : ans[4]})
    ans = cursor.fetchone()

    if(ans is None):
        print("No record for firearm law for this year")
    else:
        print(bcolors.OKMAGENTA + "\nState's total numbers of firearm law of that year: "+ bcolors.ENDC, end = '')
        print(str(ans[0]))

# for leaving message
# input = all attributes of one case
def send_prey(ans):
    print(bcolors.OKCYAN + "\nDo you want to leave a message?")
    print("(y) yes")
    print("(n) no" + bcolors.ENDC)
    a = input()

    if(a == 'y'):
        print(bcolors.HEADER + "----------Send prayer-----------")
        print("Type in a username: ", end='')
        n = input()
        print("Leave some message: ")
        print(bcolors.OKGREEN + "(Please leave positive messages only.)" + bcolors.ENDC)
        m = input()

        # to compute the current message index
        sql ="""SELECT COUNT(*) FROM preyers"""
        cursor.execute(sql)
        len_pray = cursor.fetchone()

        # to insert new message into the table
        sql ="""INSERT INTO PREYERS ("case", "username", "today", "preyers", "index") VALUES (%(cas)s, %(nam)s, %(dat)s, %(pre)s, %(len)s);"""
        cursor.execute(sql, {"cas" : ans[0], "nam" : n, "dat" : date.today(), "pre" : m, "len" : len_pray[0]})

        # commit the changes
        conn.commit()

# list all the states in state_code table
def list_states():
    print("These are all the states in America:")
    cursor = conn.cursor()
    sql ="""SELECT "State" FROM "State_code";"""
    cursor.execute(sql)
    rows = cursor.fetchall()

    c = 0
    for row in rows:
        # line them up by every 22 spaces
        print(f"{row[0] : <22}", end='')
        c = c + 1
        if(c == 3):
            print("")
            c = 0

    # search for perticualr state
    print(bcolors.OKCYAN + "\n\nType in the state you want to look up for: " + bcolors.ENDC)
    x = input()
    # return chosen state
    return x

# at the bottom of each page, to go back or reload
def go_back(n):
    print(bcolors.OKCYAN + "\n(a) Search again")
    print("(b) Back to main page" + bcolors.ENDC)
    x = input()

    if(x == 'a'):
        page = n
    elif(x == 'b'):
        page = 0
    return page

# main part of code start here:
# connecting to database
conn = psycopg2.connect(host = "dbmshw3.cokp1jqlur2w.us-east-1.rds.amazonaws.com" ,
                        database = "postgres",user = "postgres",password = "ji394su3",port = "5432")


ext = 0
page = 0
while(ext != 1):
    # main page
    if(page == 0):
        print(bcolors.OKBLUE + "------America Mass Shooting Data------" + bcolors.ENDC) 
        # total case
        cursor = conn.cursor()
        sql ="""SELECT count(*) FROM "Mass_shoot";"""
        cursor.execute(sql)
        row = cursor.fetchone()
        print(row[0], end = '')
        print(" mass shootings had occured between 1982 to 2022")
    
        # total death
        cursor = conn.cursor()
        sql ="""SELECT SUM(fatalities) FROM "Mass_shoot";"""
        cursor.execute(sql)
        row = cursor.fetchone()
        print(row[0], end = '')
        print(" people were killed.")
    
        # total victim
        cursor = conn.cursor()
        sql ="""SELECT SUM(fatalities) + SUM(injured)  FROM "Mass_shoot";"""
        cursor.execute(sql)
        row = cursor.fetchone()
        print(row[0], end = '')
        print(" people were effected.")

        # menu
        print(bcolors.OKCYAN + '\n(a) Check by state')
        print('(b) Check by year')
        print('(c) Check Firearm Law and Shooting Fatalities By State')
        print('(d) Check Firearm Law and Suicide Rate By State')
        print('(e) See the prayers')
        print('(exit) To exit' + bcolors.ENDC)
        x = input()
    
        if(x == 'a'):
            page = 1
        elif(x == 'b'):
            page = 2
        elif(x == 'c'):
            page = 3
        elif(x == 'd'):
            page = 4
        elif(x == 'e'):
            page = 5
        elif(x == 'exit'):
            ext = 1
    
    elif(page == 1):
        print(bcolors.OKBLUE + "------America Mass Shooting Data by States------" + bcolors.ENDC) 

        # list all the state
        x = list_states()

        # select all cases from x(state)
        sql ="""SELECT "case", "date" FROM "Mass_shoot" WHERE "state" = %(sta)s;"""
        cursor.execute(sql,{"sta" : x})
        rows = cursor.fetchall()

        if len(rows) == 0: # wrong input
            print(bcolors.OKGREEN + "NO CASES DOCUMENTED FOR " + bcolors.ENDC, end = '')
            print(x)

        else:
            # list all cases from x(state)
            i = 1
            for row in rows:
                print("(" + str(i) + ")", end= ' ')
                print(row[1], end = '\t')
                print(row[0])
                i = i + 1

            # select the case which fit that index
            print(bcolors.OKCYAN + "\nWhich case do you want to look into?" + bcolors.ENDC)
            id = input()
            lookup_case = rows[int(id) - 1][0]
            sql ="""SELECT * FROM "Mass_shoot" WHERE "case" = %(cas)s;"""
            cursor.execute(sql,{"cas" : lookup_case})
            ans = cursor.fetchone()

            if len(ans) == 0: # wrong input
                print(bcolors.OKGREEN + "INVALID INDEX NUMBER" + bcolors.ENDC, end = '')
                print(id)

            else:
                # list all info for that case
                print_case(ans)

                # enable to send message
                send_prey(ans)

        # chose next action
        page = go_back(1)

    elif(page == 2):
        print(bcolors.OKBLUE + "------America Mass Shooting Data by Year------" + bcolors.ENDC) 
        
        # list all the state
        print("The data range from ", end = '')

        # find the oldest year in the mass shooting record
        cursor = conn.cursor()
        sql ="""SELECT min(year) FROM "Mass_shoot";"""
        cursor.execute(sql)
        myr = cursor.fetchall()
        for m in myr:
            print(m[0], end = '')
        print(" to ", end = '')

        # find the latest year in the mass shooting record
        cursor = conn.cursor()
        sql ="""SELECT max(year) FROM "Mass_shoot";"""
        cursor.execute(sql)
        Myr = cursor.fetchall()
        for M in Myr:
            print(M[0])

        # search for perticualr year
        print(bcolors.OKCYAN + "\nType in the year you want to look up for: " + bcolors.ENDC)
        x = input()

        # select all cases of that specific year
        sql ="""SELECT "case", "date" FROM "Mass_shoot" WHERE "year" = %(yr)s;"""
        cursor.execute(sql,{"yr" : x})
        rows = cursor.fetchall()

        if len(rows) == 0: # wrong input
            print("NO CASES DOCUMENTED FOR ", end = '')
            print(x)

        else:
            # list all the cases of that specific year
            i = 1
            for row in rows:
                print("(" + str(i) + ")", end= ' ')
                print(row[1], end = '\t')
                print(row[0])
                i = i + 1

            # select the case which fit that index
            print("Which case do you want to look into?")
            id = input()
            lookup_case = rows[int(id) - 1][0]
            sql ="""SELECT * FROM "Mass_shoot" WHERE "case" = %(cas)s;"""
            cursor.execute(sql,{"cas" : lookup_case})
            ans = cursor.fetchone()

            if len(ans) == 0: # wrong input
                print("INVALID INDEX NUMBER", end = '')
                print(id)

            else:
                # list all info for that case
                print_case(ans)

                # enable to send message
                send_prey(ans)

        # chose next action
        page = go_back(2)

    elif(page == 3):
        print(bcolors.OKBLUE + "--------Firearm Law and Shooting Fatalities By State---------" + bcolors.ENDC)

        # list all the states
        x = list_states()

        # select firearm law, mass shooting fatalities from that state
        sql ="""WITH t1 AS( SELECT "state", year, sum("fatalities") as death FROM public."Mass_shoot" GROUP BY state, year) SELECT t1.state, t1.year, t1.death, F."lawtotal" FROM t1 LEFT JOIN public."Firearm_law" as F ON t1."state" = F."state" and t1."year" = F."year" WHERE t1."state" = %(sta)s ORDER BY year DESC;"""
        cursor.execute(sql, {"sta" : x})
        rows = cursor.fetchall()

        if len(rows) == 0: # wrong input
            print(bcolors.OKGREEN + "NO CASES DOCUMENTED FOR " + bcolors.ENDC, end = '')
            print(x)

        else:
            i = 1
            print("Year\tKilled  Firearm law number")
            for row in rows:
                print(row[1], end = '\t')
                print(row[2], end = '\t')
                if(row[3] is None):
                    print("No record is found")
                else:
                    print(row[3])
                i = i + 1
        # chose next action
        page = go_back(3)

    elif(page == 4):
        print(bcolors.OKBLUE + "--------Firearm Law and Suicide Rate By State---------" + bcolors.ENDC)

        # list all the states
        x = list_states()

        # select firearm law, suicide rate for that state
        sql ="""WITH t1 AS( SELECT "State", year, rate, death FROM public."Suicide_data" as A LEFT JOIN public."State_code" ON A."state" = "State_code"."Code" ) SELECT "State", t1.year, "rate", "death", "lawtotal" FROM t1 LEFT JOIN public."Firearm_law" ON t1."State" = "Firearm_law"."state" and t1.year = "Firearm_law"."year" WHERE t1."State" = %(sta)s ORDER BY t1."year" DESC;"""
        cursor.execute(sql, {"sta" : x})
        rows = cursor.fetchall()

        if len(rows) == 0: # wrong input
            print(bcolors.OKGREEN + "NO CASES DOCUMENTED FOR " + bcolors.ENDC, end = '')
            print(x)
        else:
            i = 1
            print("Year\tSuicide Rate    Suicide Death   Firearm law number")
            for row in rows:
                print(row[1], end = '\t')
                print(row[2], end = '\t\t')
                print(row[3], end = '\t\t')
                if(row[4] is None):
                    print("No record is found")
                else:
                    print(row[4])
                i = i + 1
        print(bcolors.OKGREEN + "(Suicide rate is calculated by number of death/100000)\n" + bcolors.ENDC)
        
        # chose next action
        page = go_back(4)


    elif(page == 5):
        print(bcolors.OKBLUE + "--------Prayers to the victims---------" + bcolors.ENDC)

        # select all messages from preyers table
        sql ="""SELECT * FROM "preyers" ORDER BY INDEX ASC;"""
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            print("To victim of ", end='')
            print(row[0])
            print("Username: ", end='')
            print(row[1])
            print("Date: ", end='')
            print(row[2])
            print(bcolors.OKCYAN + "\"" + row[3] + "\"" + bcolors.ENDC + "\n")

        # go back to main page
        print("Click anything to go back to main page")
        x = input()
        page = 0

# close cursor
cursor.close()
# close connection
conn.close()