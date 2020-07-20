



                                           ****  how to run the code  ****

Navigate to directory that run.sh resides.  Make the run.sh file executable and then run it. 

-   cd /path/to/file
-    chmod +x run.sh
-    ./run.sh

                                       **** Actions make the code efficient ****
Objective: make the code efficient assuming that the data can be much larger than the memory size. 
The code must be as fast as possible and keeps the minimum amount of data in the memory while does not elongate the processing time. To get to this: 

1- We read chunks of data from the file, sparse it, digest it, get the final numbers, and toss the rest of data. Then we read another chunk and so on. I
2- We define a list of IDs for Products and Companies, so we save the names once, and then address them by IDs wherever needed. 
3- We avoid loops, and instead for searching I devised the following rules: 
       a- I used dictionary as much as I could, so I avoid making duplicates, and it is way faster and easier to look up in data and check if any key already exists. 
       b- Using dictionaries, it is easy to check new key/values and add up new data. How? We use try/except method. Example here, we want to add/update number of complaints against one company:

Try:   dictionary[company]+=1
Except: dictionary[company]=1   

4- We use a class of object to pour our data in, each object is designated to a certain product. So, if a product does not exist in the data, we make a new object. Using the combinations of objects and dictionary, makes addressing the data easier and searching through the collected info considerably faster. The structure of data is as:
“Company ID (dictionary)”>>”Years (dictionaries)”>>”Companies IDs: number of complaints” 

                                            **** points and comments on the approach *****

1->>>> Short review on the Algorithm:
                A- Open the file and setup the parameters and variables (define templates for example).
                B- Read N chars at each step until reaching end of file. 
                                 a- Process the chars and extract lines
                                 b- Find outliers and duplicates 
                                 c- Find out new Products and Companies
                                 d- Add data to OUTPUT (Product ID, Year, +Company ID)
                C- Calculate the numbers of interest by reviewing the collected data in built objects (statistical analysis)
                D- Write the report in csv format,
                                  a- Sort the Product list and Years
                                  b- Write in csv format

2->>>>How to check the end of the file? 
The end of the file is where reading new batch does not move the location of the reading point. Therefore, if the size of the read data is zero, it means we hit the end of the file. 

3->>>> We assumed the encoding is utf8 and then we ignore the encoding errors. 
4->>>> csv structure can be tricky; these are some hints to read csv files:
              a- If a cell has <,> or <”>, we consider it as a complex cell. 
              b- complex cells are enclosed by quotations “. Also any <”> is followed by another one. So if you open a csv file in text format, you may see extra quotation marks <”>, that are inserted in the original data to make it structured. We need to understand how to define the  original <”>s from the ones added secondary. 
              c- if we hit a <”> in a cell, we consider a yes/no rule for erasing the <”> inside the complex cell. 
             d- If we hit a <”>, we flip the erasing Boolean yes/not. Thus, we erase the quotation marks ***alternately***. 

5->>>>> *** alert *** do not use “x in dictionary.values()” it converts the values to list and then searches in a list, this means it incorporates a loop! This elongates the searching time a lot!!!! Keep with try function
6->>>> Assumption, we assume complaint ID can be any string including alphabets. So, we intentionally refused to use single indexing to find duplicates. Instead we use dictionary. We also assume that the complaint ID  
7->>>>> using list(dictionary) is tricky, it can disturb the order of units. Python does not take a consistent action toward this, so do not rely on it 
8->>>>> We improvised and “Advanced_option”, then we can add up more codes search for similarities by checking the names one by one via a loop (For example phili philia phili phili. phili,)

9->>>>> The standard round function in Python does not satisfy your request. To turn #.5 value to #+1, I defined a new function. 

Mostafa Hasanian
hasanian.mostafa@gmail.com

https://www.linkedin.com/in/mostafa-hasanian-82b21261/ 



