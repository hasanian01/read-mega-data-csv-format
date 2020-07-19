#!/usr/bin/env python
# coding: utf-8

# In[2]:


def rounds(a):   # round the number (if less than 0.5 >>> 0 , else +1)
    a0=a-(a % 1)
    r=a % 1
    if r<0.5: 
        b=a0
    else:
        b=a0+1
    return b

def IsIn(Advanced_search,string,M):  # checking if the string is in the dictionary.keys , advanced option can search for similarities
    
    if not Advanced_search:
        try: 
            ID=M[string]
        except:
            ID=0  
    else:
        pass #   dump the code for advanced search here
    
    S_out=string
    return ID,S_out  # this is the simplest form 

def search(string,D):   # D is the indicator referring to type of the string
    global PIDs, CIDs
    
    if D=='product': M=PIDs
    if D=='company': M=CIDs
    
     # if Advanced=True: names could be written slightly differently in files (phili, PHILI, PhIlI) 
    [ID,Sout]=IsIn(Advanced_search,string,M)
            
    if ID==0: 
        ln=len(M)
        M[Sout]=ln
        ID=ln
        if D=='product': PIDs=M
        if D=='company': CIDs=M
    return ID
          
    T=False
    
    return T

def duplicateID(ID):
    global IDs
    #print(ID)
    T=False
    try:
        n=IDs[ID]
        T=True
    except:
        IDs[ID]=0
    
    #print('lens',len(IDs))
    return T

def analyse(unit):   # unit is one line of data (e.g. Date, Product, Company), analyse adds its value to our analytics dictionary 
    global IDs ### list globals here including output data and list if IDs
    # finding outliers 
    T=True
    if unit[0]>2020 or unit[0]<1900: # year
        T=False
    if len(unit[1])==0 or len(unit[2])==0:   # Product and company length 
        T=False
    
    if unit[3]==-1:  # complaints ID is an outlier 
        T=False
    
    if T and duplicateID(unit[3]):  # checking duplicates
        print('Duplicate is found with ID: ', unit[3])
        T=False               
 
    if T:                       # if data is valid, then we add it to our outputs/stats  
        PID=search(unit[1],'product')
        CID=search(unit[2],'company')
        
        try:
            try:
                try:
                    OUTPUT[PID].year[unit[0]].comp[CID]+=1
                except:
                    OUTPUT[PID].year[unit[0]].comp[CID]=1   # if cannot find the complaint ID, add a new one
            except:
                OUTPUT[PID].year[unit[0]]=class_year(unit[0])
                OUTPUT[PID].year[unit[0]].comp[CID]=1         # if cannot find the year, add a new year       
        except:
            OUTPUT[PID]=class_output(PID)                    # if all above tried did not work, add a whole new unit
            OUTPUT[PID].year[unit[0]]=class_year(unit[0])
            OUTPUT[PID].year[unit[0]].comp[CID]=1
            
    return T

def year(date):

    for i in date:         
        if not (i in '1234567890'):
            d=i
            break

    for i in date.split(d):
        ii=int(i)
        if ii>32:  # means it must be a year
            y=ii
    return y

################### above here, functions to run processing ###############

#########################  processing the data ################
def process(String):  # this processes the last chunk of data
    global Name, loc 
    data=[]
    unit=[]
    Commas=[]
    left=''
    Complex=False  # if we are inside a complex cell
    LC=0      # location of the start of the current cell 
    LL=0    # location of the start of the current line   
    
    cell_number=1
    for i in range(len(String)):
        c=String[i]
        if c in [',','"','\n']:
            if c==',' and not Complex:
                if cell_number in loc.values():   # adding a new cell of current line of data  
                    if cell_number==loc['Date']:
                        unit.append(year(String[LC:i].lower()))
                    else:
                        unit.append(String[LC:i].lower())       
                    
                LC=i+1
                cell_number+=1
            if c=='\n' and not Complex:
                if cell_number in loc.values():   # adding a new cell of current line of data  
                    if cell_number==loc['Date']:
                        unit.append(year(String[LC:i].lower()))
                    else:
                        unit.append(String[LC:i].lower())  
    
                LC=i+1
                data.append(unit)        # add the completed parsed line to our data 
                analyse(unit)            # it analyses the last line and added the values to the analytics repository 
                unit=[]
                cell_number=1
                LL=i+1
            if c=='"':
                Complex=not Complex
                
    left=String[LL:]                             
               
    return data, left  # returns data in array of strings + left over of last line that is not closed 

############################# calculate the final numbers, three index per product-year#############

def calculate():
    global OUTPUT
    
    for ID in range(1,len(OUTPUT)):
        Years=list(OUTPUT[ID].year.keys())
        for y in Years:
            Comps=OUTPUT[ID].year[y].comp
            maxx=0
            total1=0
            total2=len(Comps)
            for k in Comps:
                v=OUTPUT[ID].year[y].comp[k]
                total1+=v
                if v>maxx:
                    maxx=v
            OUTPUT[ID].year[y].total1=total1
            OUTPUT[ID].year[y].total2=total2
            OUTPUT[ID].year[y].max=rounds(maxx/total1*100)                

############################  down here, writing the repot   ####################################

def pop(S,i):   # remove the char at location i
    S=S[0:i]+S[i+1:]
    return S

def removeQ(String):  # removes " from string.  we do not use it in current version of the code, but I kept it here for future applications 
    
    Qs=[]
    for i in range(len(String)):
        if String[i]=='"':
            Qs.append(i)
    
    if len(Qs)>0:
        S=String[Qs[0]+1:Qs[-1]]  # we atleast have two " at begining and end 
        
        T=True
        j=1  # we already deleted first quotation at location 0
        for i in range(len(Qs)-2):  # pops " alternately 
            T=not T
            if T: 
                S=pop(S,Qs[i+1]-j)
                j+=1
    else:
        S=String
    return S
####################################

def PIDs_list_sort(OUTPUT):
    PIDs_list=list(OUTPUT.keys())[1:]
    
    Names=[]
    for i in PIDs_list:
        Names.append(list(PIDs)[i])
          
    Names_noQ=[]
    j=0
    for c in Names:
        Names_noQ.append([removeQ(c),j])
        j=j+1
    Names_noQ.sort() 

    IDs_sorted=[]

    for c in Names_noQ:
        IDs_sorted.append(PIDs_list[c[1]])
    return IDs_sorted
    
########################
def write_report(OUTPUT,output_filename):
    
    F=open(output_filename,'w')
    IDs_sorted=PIDs_list_sort(OUTPUT)  # we remove " and sort products alphabeticly 
    
    for ID in IDs_sorted:  
            pro_name=list(PIDs)[ID]
            Years=list(OUTPUT[ID].year.keys())
            Years.sort()
            for year in Years:
                Comps=OUTPUT[ID].year[year].comp
            
                s=pro_name+','+str(year)
                F.write(s)
                F.write(','+str(OUTPUT[ID].year[year].total1))
                F.write(','+str(OUTPUT[ID].year[year].total2))
                F.write(','+str(OUTPUT[ID].year[year].max)+'\n')

                #for com in Comps:        writing companies condes, or names, it is disabled  
                #        s=','+str(com)
                #        F.write(s)
                #F.write('\n')
    print('**************************************')
    F.close()  


# In[4]:


#    main code    # 
print('Data parsing.....    \n\n\n')

Advanced_search=False   # is true, we assume that the names can slightly vary (for example, phili or philli or phili. or phili-)

###############################################################
import sys

run_bash=False

if not run_bash:
    input_filename='./input/complaints.csv'
    output_filename='./output/report.csv'
else:
    input_filename=sys.argv[1]
    output_filename=sys.argv[2]

###############################################################
File=open(input_filename,encoding="utf-8",errors='ignore') # We keep ignoing the encoding issues, assuming that the encoding is utf8

######################   header and cell structure   #########################
Header=File.readline()
Cells=Header.split(',')
Cells[-1]=Cells[-1].replace('\n','')

Name={'Date':'Date received','Product':'Product','Company':'Company','ID':'Complaint ID'} # we always keep the complaints to check duplicats
loc={'Date':0,'Product':0,'Company':0,'ID':0}

j=1
for i in Cells: 
    if i in Name['Date']: loc['Date']=j
    if i in Name['Product']: loc['Product']=j
    if i in Name['Company']: loc['Company']=j
    if i in Name['ID']: loc['ID']=j
    j+=1

####### making the object+dictionary to store the final outcomes ########

IDs={}    # complaint IDs

CIDs={'Mostafa Hasanian':0}  # IDs of companies     ID 0 is reserved, we prefered to address the IDs from 1 
PIDs={'My code':0}           # Product names and IDs ID=0 is reserved

OUTPUT={}
class class_output:
    def __init__(self,PID):
            self.PID=PID
            self.year={}

class class_year:
    def __init__(self,year):
            self.year=year
            self.comp={}            # dictionary of companies IDs and number of complaints 
            self.total1=0           # fist output (total complaints)
            self.total2=0           # second output (total companies with at least one complaints)
            self.max=0              # max complaints for a company (percent) = rounds((max/total1)*100)
            
OUTPUT[PIDs['My code']]=class_output(PIDs['My code']) 
OUTPUT[PIDs['My code']].year[2020]=class_year(2020)
OUTPUT[PIDs['My code']].year[2019]=class_year(2019)
 
#####################################
buffer=100*1000*1000 # number of characters 

left=''  # what is left from the privious chunk, 
size=-1      # To get inside the loop, size cannot be less than 0 in practice 
lines_num=0 # counter 
while not size==0:       # if size of the read chunk is 0, it means we hit the end of file    
    
    String_read=File.read(buffer)
    String=left+String_read   
   
    size=len(String_read)
    print('Location in the file is: ', str(round(File.tell()/1000000))+' Mbye')
    if not size==0:   

        [data,left]=process(String)  # merge the lines to an string,  
                                     # we may not need the data, but I made it here for future references/ 
        lines_num+=len(data)       
        if lines_num>100000: break

calculate()   # goes through the collected data (OUTPUT) and wraps the numbers 
write_report(OUTPUT,output_filename)   # dmup the outputs to a report file 

print('Total number of parsed units: ', lines_num)
print('Pointer location: ',File.tell()/1000000,'Mega bytes')
print('Done!!!!')
File.close()

