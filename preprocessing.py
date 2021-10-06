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

def preprocess(data, input_file, seperator, schooldata):
    f= open("tempdata.txt","w+")
    if schooldata:
        column_values = data[["tagX", "tagY"]].values.ravel()
        
    else: 
        column_values = data[["Sender", "Receiver"]].values.ravel()

    unique_values =  pd.unique(column_values)
    last_seen = dict.fromkeys((unique_values),'')

    try:
        next(input_file)
        for i, line in enumerate (input_file):
            line=line.replace('"', '').strip()
            items=line.split(seperator)

            if schooldata:
                date=int(items[4])
                sender = int(items[1])
                recepient = int(items[2].replace("\n",""))
            else: 
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

def find_interactions(edge_file):
    data = edge_file.copy()
    tagx = np.unique(data.tagX)
    tagy = np.unique(data.tagY)
    database = pd.DataFrame(columns = ['tagX', 'tagY', 'StartTime', 'Weight'])
    cntr = 0 
    for y in tagy:
        for x in tagx:
            temp = data[(data.tagX==x)&(data.tagY==y)].copy()
            temp = temp.reset_index(drop=True)

            if len(temp)>0:
                try: 
                    indx = list(np.squeeze(np.where(np.diff(temp.time)>1)))
                except: 
                    indx = np.squeeze(np.where(np.diff(temp.time)>1))
                    # print('0: ', indx)
                    if np.shape(indx)==0:
                        indx = [0,len(temp)]
                        # print('1: ', indx)
                    else:
                        indx = [np.squeeze(np.where(np.diff(temp.time)>1)).tolist()]
                        # print('2: ', indx)

                # final index
                indx.append(len(temp))
                # first index 
                indx.insert(0,0)
                
                for i in range(0,len(indx)-1): 

                    if i==0:
                        temp1 = temp.loc[indx[i]:indx[i+1],:]
                        temp1 = temp1.reset_index(drop=True)
                        if len (temp1)>0:
                            database.loc[cntr, 'tagX'] = temp1['tagX'][0]
                            database.loc[cntr, 'tagY'] = temp1['tagY'][0]
                            database.loc[cntr, 'StartTime'] = temp1['time'][0]
                            database.loc[cntr, 'Weight'] = len(temp1['time'])
                            cntr = cntr+1
                        
                    else:
                        temp1 = temp.loc[indx[i]+1:indx[i+1],:]
                        temp1 = temp1.reset_index(drop=True)
                        if len (temp1)>0:
                            database.loc[cntr, 'tagX'] = temp1['tagX'][0]
                            database.loc[cntr, 'tagY'] = temp1['tagY'][0]
                            database.loc[cntr, 'StartTime'] = temp1['time'][0]
                            database.loc[cntr, 'Weight'] = len(temp1['time'])
                            cntr = cntr+1

    file_name = 'edge_new.csv'
    database.to_csv(file_name)
    return database, file_name