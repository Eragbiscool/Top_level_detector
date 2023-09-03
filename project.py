import re
import gzip


module_name = []
findtop = {}
new_filelist = {}
wrapper_need = 0
filelist_lines = ""




provide_filelist_path='!!put_your_filepath_here!!'





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


def print_report(module_list,findtop):
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
        print("Please create a top level wrapper to the module, you dont have a top")
    else:
        print('''
            
        ##################################################################
        ######################     Report     ############################
        ##################################################################
                    Total module count     = {}
                    Name of The Top module = {} 
        ##################################################################
        ######################       end      ############################
        ##################################################################'''.format(number_of_module,top) )



# def print_filelist(findtop,filelist):
#     sorted_findtop = dict(sorted(findtop.items(), key=lambda x:x[1],reverse = True))
#     file = open('G:/Projects/top_level_detector/sorted_filelist.txt','w')
#     file.close()
#     print(sorted_findtop)
    
#     for i in sorted_findtop:
#         file = open('G:/Projects/top_level_detector/sorted_filelist.txt','a')
#         file.write(filelist.get(i))
#         file.close()



file_open(provide_filelist_path)

file_process(filelist_lines,new_filelist)


print_report(module_name,findtop)



# print(new_filelist)


# print_filelist(findtop,new_filelist)
