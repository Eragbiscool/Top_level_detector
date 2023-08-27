import re


module_name = []
findtop = {}
count = []
flag = False
wrapper_need = 0

file = open('file_name_here', 'r')

Lines = file.readlines()



def module_names():
    global flag
    for line in Lines:
        if(re.findall("^\s?module\s+(\D\S+)\(",line)):
            module_name.append(re.findall("module\s+(\D\S+)\(",line)[0])
        elif(re.findall("^\s?module\s+(\D\S+)",line)):
            module_name.append(re.findall("module\s+(\D\S+)",line)[0])
        elif(re.findall("^\s?module[\n]",line) or flag==True):
            if(re.findall("\s+(\D\S+)\(",line)):
                if(flag):
                    flag=False
                    module_name.append(re.findall("\s+(\D\S+)\(",line)[0])
                
            elif(re.findall("\s+(\D\S+)#",line) ):
                if(flag):
                    flag=False
                    module_name.append(re.findall("\s+(\D\S+)#",line)[0])
                
            elif(re.findall("\s+(\D\S+)\s?[\n]",line)):
                if(flag):
                    flag=False
                    module_name.append(re.findall("\s+(\D\S+)\s?[\n]",line)[0])
              
            else: 
                flag=True
              
                
        else:
            continue
   
    return module_name



def instance_count():


    for i in module_name:
        for line in Lines:
            if(re.findall(i+"\s.*\(",line)):
                count.append(re.findall((i)+"\s.*\(",line)[0])
            elif(re.findall("^.*"+(i)+"[\n]",line)):
                count.append(re.findall("^.*"+(i)+"[\n]",line)[0])
            else:
                continue
        findtop[i] = len(count)
        count.clear()
    return findtop


module_names()
instance_count()

sorted_findtop = dict(sorted(findtop.items(), key=lambda x:x[1]))

number_of_module = len(module_name)

if(number_of_module!=0):
    top = list(sorted_findtop.keys())[0]



# print(findtop)



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