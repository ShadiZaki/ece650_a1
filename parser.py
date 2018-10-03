import re
import sys

class Parser:
    
    def __init__(self):
        pass
    
    def read_and_parse(self):
        Input = raw_input()
        
        if(Input == ''):
            sys.exit(0)
            return None
        Input = Input.lstrip()
        pattern = re.compile(r'[-+]?[0-9]*\.?[0-9]+')
        coor = pattern.findall(Input)
        coor_len = len(coor)

        invalid_chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ',', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', 
                         '-', '_', '+', '=', '/', '{', '}', '|', ':', ';', '"', '\\', '>', '<', '?', '.', '`', '~']

        paranthesis_count = 0
        for i in Input:
            if(i == "(" or i == ")"):
                paranthesis_count += 1
        
        if(paranthesis_count > coor_len):
            print "Error: invalid command"
            return None
        elif(paranthesis_count < coor_len):
            print "Error: invalid command"
            return None
        
        if(paranthesis_count == 2 and coor_len == 2):
            print "Error: invalid command"
            return None
        
        if(coor_len % 2 != 0):
            print "Error: invalid command"
            return None
        
        for i in coor:
            if("." in i):
                print "Error: invalid coordinates"
                return None
        
        command = Input[0]
        if(command != "a" and command != "c" and command != "r" and command != "g"):
            print "Error: invalid command"
            return None
        else:
            Input_list = Input[1:]
            if(command != "g"):
                Input_list1 = Input_list.split(' ', 1)
                if(Input_list1[0] != ''):
                    print "Error: invalid command"
                    return None
                else:
                    if(len(Input_list1) > 1):
                        Input_list2 = Input_list1[1].split('"', 2)
                        if(len(Input_list2) > 2):
                            if(command == "r" and Input_list2[2] != ''):
                                print "Error: invalid command"
                                return None
                            if(command == "a" and Input_list2[2] == ''):
                                print "Error: no coordinates found"
                                return None
                            if(command == "c" and Input_list2[2] == ''):
                                print "Error: no coordinates found"
                                return None
                        else:
                            print "Error: invalid command"
                            return None
                        for char in invalid_chars:
                            if(char in Input_list2[1]):
                                print "Error: invalid street name"
                                return None
                    else:
                        print "Error: invalid command"
                        return None
            elif(command == "g" and Input_list):
                print "Error: invalid command"
                return None
        
        if(command == "a" or command == "c"):
            data = [command, Input_list2[1].upper(), coor]
        elif(command == "r"):
            data = [command, Input_list2[1].upper()]
        elif(command == "g"):
            data = command
        return data
        
