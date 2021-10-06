import numpy as np
import pandas as pd 

def attach_instance (device, date, last_seen, f):
    #global last_seen
    # see if a device has appeared previously. If so, create a directed link
    # from previous instance to this instance.
    # time difference between the two instances
    previous_date=last_seen[device]
    if (previous_date != "")and (previous_date!= date):
        diff = abs(date - previous_date);
        #print (device,",",previous_date,",",device,",",date,",",diff,"\n")
        f.write("%s_%d,%s_%d,%d \r\n"%(device,previous_date,device,date,diff))
    last_seen[device]=date;

def preprocess(data, input_file):
    f= open("tempdata.txt","w+")
    column_values = data[["Sender", "Receiver"]].values.ravel()
    unique_values =  pd.unique(column_values)
    #last_seen=dict.fromkeys(['"A"','"B"','"C"','"D"','"E"'],"")
    last_seen = dict.fromkeys((unique_values),'')
    #previous_date=0
    try:
        next(input_file)
        for i, line in enumerate (input_file):
            line=line.replace('"', '').strip()
            items=line.split(';')
            date=int(items[2])
            sender = str(items[0])
            recepient = str(items[1].replace("\n",""))
            attach_instance(sender,date, last_seen, f)
            attach_instance(recepient,date, last_seen, f)
            f.write("%s_%d,%s_%d,0 \r\n"%(sender,date,recepient,date))
            f.write("%s_%d,%s_%d,0 \r\n"%(recepient,date,sender,date))
            
            
    finally:
        input_file.close()
        f.close()
        
    return 0