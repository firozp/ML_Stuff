from random import shuffle

def readFile(filename):
    file = open("D:\\Work\\myStuff\\pythonPlayground\\data\\377\\" + filename +".log","r")
    user_map={}
    op_identity_map={}
    cli_address_map={}
    count_lines=0
    i=0
    j=0
    k=0
    processed_lines=[]
    for line in file:
        if(line.split("|")[2] == " AUDIT_SUCCESS "):
            a_state="0"
        else:
            a_state="1"
        time_stamp=line.split("|")[0][11:19]
        hours=int(time_stamp[0:2])
        mins=int(time_stamp[3:5])
        total_mins = hours * 60 + mins 
        time_of_day = (total_mins / 1440)*100
        #print (time_of_day)

        user_name=line.split("|")[6]
        user_name=user_name[16:len(user_name)-2]

        op_id=line.split("|")[7]
        op_id=op_id[23:len(op_id)-2]

        cli_address=line.split("|")[12]
        cli_address=cli_address[17:len(cli_address)-2]
      
        if not user_name in user_map:
            user_map[user_name]=i
            i=i+1        

        if not op_id in op_identity_map:
            op_identity_map[op_id]=j
            j=j+1        
        if not cli_address in cli_address_map:
            cli_address_map[cli_address]=k
            k=k+1        
        count_lines=count_lines+1
        processed_lines.append('%d,%s,%s,%s,%s' %(time_of_day, user_map.get(user_name) , op_identity_map.get(op_id) ,cli_address_map.get(cli_address),a_state))
        #print ('%d,%s,%s,%s,%s' %(time_of_day, a_state,user_map.get(user_name) , op_identity_map.get(op_id) ,cli_address_map.get(cli_address) ) )
    file.close
    
    shuffle(processed_lines)

    print("Generated data in format: TimeOfDay, username, op_id, cli_address, op_result")
    print("User details:")
    prettyPrintMap(user_map)
    print("OP_Id:")
    prettyPrintMap(op_identity_map)
    print("CLI_Add:")
    prettyPrintMap(cli_address_map)
    print("OP_Result:\n0 : Success\n1 : Failure\n")

    print("Total lines: %s" %(count_lines))
    train_file = open("D:\\Work\\myStuff\\pythonPlayground\\data\\run_data\\train.csv","w")
    train_file.write("%d,%d,%s,%s\n" %(count_lines*.90,4,'Correct','Wrong'))

    for l in range(int(count_lines*.90)):
        train_file.write(processed_lines[l]+"\n")
    train_file.close

    test_file = open("D:\\Work\\myStuff\\pythonPlayground\\data\\run_data\\test.csv","w")
    test_file.write("%d,%d,%s,%s\n" %(count_lines*.10,4,'Correct','Wrong'))

    for l in range(int(count_lines*.90),count_lines):
        test_file.write(processed_lines[l]+"\n")
    test_file.close

    print("Output files written at %s" %(train_file.name))

def prettyPrintMap(mapToPrint):
    for entry in mapToPrint:
        print(str(mapToPrint.get(entry)) + " : " + entry )
    print ("==============================================")

readFile("sys_sec")

