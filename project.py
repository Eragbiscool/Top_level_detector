import re
import gzip


module_name = []
findtop = {}
lib_files = []
new_filelist={}
wrapper_need = 0
lib_true = 0
filelist_lines = ""
top_module = []
filelist = []




provide_filelist_path='!!!Add your filelist path here!!!'



def file_open(filelist_path):
    global filelist_lines
    file = open(filelist_path, 'r')
    filelist_lines = file.readlines()

def module_names(Lines):
    flag = False
    for line in Lines:
        if(re.findall("^\s?module\s+(\D\S+)\(",line)):
            module_name.append(re.findall("module\s+(\D\S+)\(",line)[0])
        elif(re.findall("^\s?module\s?[\n]",line) or flag==True):
            if(re.findall("\s+(\D\S+)\(",line)):
                if(flag):
                    flag=False
                    module_name.append(re.findall("(\D\S+)\(",line)[0])
            elif(re.findall("\s?(\D\S+)\(",line)):
                if(flag):
                    flag=False
                    module_name.append(re.findall("(\D\S+)\(",line)[0])
            elif(re.findall("[\t+](\D\S+)\(",line)):
                if(flag):
                    flag=False
                    module_name.append(re.findall("(\D\S+)\(",line)[0])
                
            elif(re.findall("\s+(\D\S+)#",line) ):
               
                if(flag):
                    flag=False
                    module_name.append(re.findall("(\D\S+)#",line)[0])
                
            elif(re.findall("\s+(\D\S+)\s?[\n]",line)):
                
                if(flag):
                    flag=False
                    module_name.append(re.findall("(\D\S+)\s?[\n]",line)[0])
            else:
                
                flag=True
                continue
        elif(re.findall("^\s?module\s+(\D\S+)\s?[\n]",line)):
            module_name.append(re.findall("module\s+(\D\S+)",line)[0]) 
        elif(re.findall("^\s+module\s+(\D\S+)\s?[\n]",line)):
            module_name.append(re.findall("module\s+(\D\S+)",line)[0]) 
        elif(re.findall("^\s?module\s+(\D\S+)",line)):
            module_name.append(re.findall("^\s?module\s+(\D\S+)",line)[0]) 
        else:
            continue
   
    return module_name

def instance_count(Lines,module_list,findtop):

    count = []
    for i in module_list:
        for line in Lines:
            if(re.findall((i)+"\s.*\(",line)):
                if(re.findall("^module",line)):
                    continue
                else:
                    count.append(re.findall((i)+"\s.*\(",line)[0])
            elif(re.findall("^.*"+(i)+"[\n]",line)):
                count.append(re.findall("^.*"+(i)+"[\n]",line)[0])
            else:
                continue
        findtop[i] = findtop.setdefault(i,0)+len(count)
        count=[]
    return findtop

def file_process(Lines,filelist):
    module_list = []
    counter = 0 
    if(len(Lines)==0):
        print("Please insert a valid filelist!")
    elif(len(Lines)>1):
        for i in Lines:
            j=re.split("[\n]",i)[0]
            files = open(j, 'r')
            read_line = files.readlines()
            module_list.append(module_names(read_line))
            if(len(module_name)!=len(list(filelist.keys()))):
                filelist[module_name[counter]] = i
                counter += 1
            
        for i in Lines:
            j=re.split("[\n]",i)[0]
            files = open(j, 'r')
            read_line = files.readlines()
            instance_count(read_line,module_list[-1],findtop)
    else:
        module_list = []
        if(re.split("\.",Lines[0])[-1]=='gz'):
            file=gzip.open(Lines[0],'rb')
            read_line=file.read()
        else:
            files = open(Lines[0], 'r')
            read_line = files.readlines()
        module_list.append(module_names(read_line))
        instance_count(read_line,module_list[-1],findtop)
        
    return filelist

def find_top_def(findtop,top_module):
    sorted_findtop = dict(sorted(findtop.items(), key=lambda x:x[1]))
    count= 0 
    
    for i in sorted_findtop.values():
        if(i == 0) :
            top_module.append(list(sorted_findtop.keys())[count])
            count=+1
        else:
            break

    # print(top_module)
    return top_module

def lib_finder(Lines,lib_files):
    filelist = open('new_filelist.txt',"w")
    filelist.close()

    counter = 0 
    if(len(Lines)==0):
        print("Please insert a valid filelist!")
    else:
        for i in Lines:
            j=re.split("[\n]",i)[0]
            files = open(j, 'r')
            read_line = files.readlines()
            for lines in read_line:
                if(re.findall("^\s?module.*\(",lines)):
                    
                    counter = counter +  1
                elif(re.findall("^\s?module\s?[\n]",lines)):
                    
                    counter = counter +  1
                elif(re.findall("^\s+module.*[\n]",lines)):
                    
                    counter = counter +  1
                elif(re.findall("^\s+module.*",lines)):
                    
                    counter = counter +  1

            
            if(counter==1):
                filelist = open('new_filelist.txt',"a")
                filelist.write(j+'\n')
                filelist.close()
            elif(counter>1):
                # print("Lib file path: "+j)
                lib_files.insert(0,j)
            else:
                # print("These files maybe package or other non essential files: "+j)
                lib_files.append(j)
            counter = 0

    return lib_files

def print_report(module_list,findtop,lib_files,top_module):
    sorted_findtop = dict(sorted(findtop.items(), key=lambda x:x[1]))

    number_of_module = len(module_list)


    if(number_of_module!=0):
        top = list(sorted_findtop.keys())[0]

    if(number_of_module>1):
        wrapper_need = int(list(sorted_findtop.values())[1])-int(list(sorted_findtop.values())[0])


    if(number_of_module==1):
        print("You have only one module, your module name here is: {} , and thats the top as well!!!".format(top))
    elif(number_of_module==0):
        print("Huh! Gotcha! Thought I would miss this huh? Now, Stop messing around and put a design file!!!")
    elif(wrapper_need==0):
        print("Please create a top level wrapper to the following modules, you don't have a top:")
        for i in top_module:
            print('''
                {}'''.format(i))
    else:
        print('''
            
        ##################################################################
        ######################     Report     ############################
        ##################################################################''')
        if(len(lib_files)!=0):
            if(lib_files[0]):
                print('''
        lib file path  = {}
        ------------------------------------------------------------------'''.format(lib_files[0]))
                if(len(lib_files)>=2):
                    for i in lib_files[1:-1]:
                        print('''
                            
                    Package files and miscellaneous  = {}'''.format(i))
                    print("             ------------------------------------------------------------------")
                else: 
                    print('''
                    Total module count     = {}
                    Name of The Top module = {} 
        ##################################################################
        ######################       end      ############################
        ##################################################################'''.format(number_of_module,top))
        else: 
            print('''
                        Total module count     = {}
                        Name of The Top module = {} 
            ##################################################################
            ######################       end      ############################
            ##################################################################'''.format(number_of_module,top))





file_open(provide_filelist_path)

lib_finder(filelist_lines,lib_files)

file_open("new_filelist.txt") ##Here Put the filelist name that we are getting from the "lib_finder" def. You can put it as a string or put the filename in a variable and put that variable here as argument

file_process(filelist_lines,new_filelist)

find_top_def(findtop,top_module)

print_report(module_name,findtop,lib_files,top_module)
