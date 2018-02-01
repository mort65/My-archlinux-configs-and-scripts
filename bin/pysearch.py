#!/usr/bin/env python3
import sys
import os
import re

class Py_Search:
    main_dir = ''
    text = ''
    pattern = ''
    result = []
    recursive = False
    ignorecase = False
    searchdir = False
    searchfile = False
    onlyname = False
    searchlink = False
    mark = False
    usage = False
    sort = False

    def show_usage(self):
            print("""Usage: pysearch [OPTION]... [PATH] [TEXT]
search for TEXT in the given PATH.
Text can be a regular expression.

  -h, --help                 display this help 
  -r, --recursive            search recursively  
  -f, --file                 search for files
  -l, --link                 search for links
  -d, --dir                  search for directories
  -m, --mark                 mark files and dirs with f and d
  -i, --ignore-case          ignore case in the search result    
  -n, --name                 don't show fullpath in the result
  -s, --sort                 sort the search result alphabetically 
  
Examples:
  pysearch -if /usr/bin vim    "Find files in bin dir that have 
  'vim' in their names and ignore case sensitivity."
  pysearch -lr /usr/bin 'vim$' "Recursively find all links in 
  bin dir that have 'vim' at the end of their names.
  pysearch -rs /usr/bin '^im'  "Find recursively everything 
  in bin that starts with 'im' and only write short names."
  pysearch -dr /usr/bin '.*'   "Recursively find all dirs in bin" """)

    def add_result(self,parent_dir,new_result,is_dir):
        if self.recursive:
            if is_dir:
                if os.path.islink(os.path.join(parent_dir,new_result)):
                    if self.searchlink:
                        if self.onlyname:
                            self.add_link(new_result,os.path.realpath(os.path.join(parent_dir,new_result)),is_dir)
                        else:
                            self.add_link(os.path.join(parent_dir,new_result),os.path.realpath(os.path.join(parent_dir,new_result)),is_dir)
                elif self.searchdir:  
                    if self.onlyname:
                        self.add_dir(new_result)
                    else:
                        self.add_dir(os.path.realpath(os.path.join(parent_dir,new_result)))
            else:
                if os.path.islink(os.path.join(parent_dir,new_result)):
                    if self.searchlink:
                        if self.onlyname:
                            self.add_link(new_result,os.path.realpath(os.path.join(parent_dir,new_result)),is_dir)
                        else:
                            self.add_link(os.path.join(parent_dir,new_result),os.path.realpath(os.path.join(parent_dir,new_result)),is_dir)
                elif self.searchfile: 
                    if self.onlyname:
                        self.add_file(new_result)
                    else:
                        self.add_file(os.path.realpath(os.path.join(parent_dir,new_result)))
        else:
            if is_dir:
                if os.path.islink(os.path.join(parent_dir,new_result)):
                    if self.searchlink:
                        if self.onlyname:
                            self.add_link(new_result,os.path.realpath(os.path.join(parent_dir,new_result)),is_dir)
                        else:
                            self.add_link(os.path.join(parent_dir,new_result),os.path.realpath(os.path.join(parent_dir,new_result)),is_dir)
                elif self.searchdir:
                    if self.onlyname:
                        self.add_dir(new_result)
                    else:
                        self.add_dir(os.path.realpath(os.path.join(parent_dir,new_result)))
            else:
                if os.path.islink(os.path.join(parent_dir,new_result)):
                    if self.searchlink:
                        if self.onlyname:
                            self.add_link(new_result,os.path.realpath(os.path.join(parent_dir,new_result)),is_dir)
                        else:
                            self.add_link(os.path.join(parent_dir,new_result),os.path.realpath(os.path.join(parent_dir,new_result)),is_dir)                      
                elif self.searchfile:
                    if self.onlyname:
                        self.add_file(new_result)
                    else:
                        self.add_file(os.path.realpath(os.path.join(parent_dir,new_result)))

    def add_link(self,new_link,target,is_target_dir):
        result_link = ""
        if self.onlyname:
            result_link = "\"" + new_link + "\" -> \""+ os.path.basename(target) +"\""
        else:
            result_link = "\"" + new_link + "\" -> \""+ target +"\""
        if self.mark:
            if is_target_dir:
                result_link += "d"
            else:
                result_link += "f"
        self.result.append(result_link)
        if not self.sort:
            print(result_link)

    def add_dir(self,new_dir):
        result_dir = ""
        if self.mark:
            result_dir = "\""+new_dir+"\"d"
        else:
            result_dir = "\""+new_dir+"\""
        self.result.append(result_dir)
        if not self.sort:
            print(result_dir)

    def add_file(self,new_file):
        result_file = ""
        if self.mark:
            result_file = "\""+new_file+"\"f"
        else:
            result_file = "\""+new_file+"\""
        self.result.append(result_file)
        if not self.sort:
            print(result_file)
            
    def __init__(self,args):
        if len(args) > 1:
            for i in range(1,len(args)):
                if args[i][0] == '-':
                    if (self.main_dir != '') or (self.text != ''):
                        self.show_usage()
                        exit(1)
                    elif args[i][1] == '-':
                        if args[i] == '--help':
                            self.usage = True
                        elif args[i] == '--recursive':
                            self.recursive = True
                        elif args[i] == '--ignore-case':
                            self.ignorecase = True
                        elif args[i] == '--link':
                            self.searchlink = True                   
                        elif args[i] == '--dir':
                            self.searchdir = True
                        elif args[i] == '--name':
                            self.onlyname = True
                        elif args[i] == '--file':
                            self.searchfile = True
                        elif args[i] == '--mark':
                            self.mark = True
                        elif args[i] == '--sort':
                            self.sort = True
                        else:
                            self.show_usage()
                            exit(1)
                    else:
                        for c in range(1,len(args[i])):
                            if args[i][c] == 'h':
                                self.usage = True
                            elif args[i][c] == 'r':
                                self.recursive = True
                            elif args[i][c] == 'i':
                                self.ignorecase = True
                            elif args[i][c] == 'l':
                                self.searchlink = True                                              
                            elif args[i][c] == 'd':
                                self.searchdir = True
                            elif args[i][c] == 'n':
                                self.onlyname = True
                            elif args[i][c] == 'f':
                                self.searchfile = True
                            elif args[i][c] == 'm':
                                self.mark = True 
                            elif args[i][c] == 's':
                                self.sort = True
                            else:
                                self.show_usage()
                                exit(1)
                elif i == ( len(args) - 2 ):
                    self.main_dir = args[i]
                elif i == ( len(args) - 1 ):
                    self.text = args[i]
                    if self.ignorecase:
                        self.pattern = self.text.lower()
                    else:
                        self.pattern = self.text
                else:
                    self.show_usage()
                    exit(1)
        if self.usage:
            self.show_usage()
            exit(0)
        if self.searchdir is False and self.searchlink is False and self.searchfile is False:
            self.searchdir,self.searchfile,self.searchlink = True,True,True
        if self.main_dir == '':
            self.main_dir =os.path.realpath('.')
        if self.pattern == '':
            self.pattern = '.*'
    def main(self):
        try:
            if self.recursive:
                if self.searchdir or self.searchlink:
                    for root, directories, filenames in os.walk(self.main_dir):
                        for dirname in directories:
                            if self.ignorecase:
                                if re.search(self.pattern,dirname.lower()):
                                    self.add_result(root,dirname,True)
                            else:
                                if re.search(self.pattern,dirname):
                                    self.add_result(root,dirname,True)
                if self.searchfile or self.searchlink:
                    for root, directories, filenames in os.walk(self.main_dir):
                        for filename in filenames:
                            if self.ignorecase:
                                if re.search(self.pattern,filename.lower()):
                                    self.add_result(root,filename,False)
                            else:
                                if re.search(self.pattern,filename):
                                    self.add_result(root,filename,False)
            else:
                if self.searchdir or self.searchlink:
                    for name in os.listdir(self.main_dir):
                        if self.ignorecase:
                            if re.search(self.pattern,os.path.basename(name).lower()):
                                if os.path.isdir(os.path.join(self.main_dir,name)):
                                    self.add_result(self.main_dir,name,True)
                        else:
                            if re.search(self.pattern,os.path.basename(name)):
                                if os.path.isdir(os.path.join(self.main_dir,name)):
                                    self.add_result(self.main_dir,name,True)
                if self.searchfile or self.searchlink:
                    for name in os.listdir(self.main_dir):
                        if self.ignorecase:
                            if re.search(self.pattern,os.path.basename(name).lower()):
                                if not os.path.isdir(os.path.join(self.main_dir,name)):
                                    self.add_result(self.main_dir,name,False)
                        else:
                            if re.search(self.pattern,os.path.basename(name)):
                                if not os.path.isdir(os.path.join(self.main_dir,name)):
                                    self.add_result(self.main_dir,name,False)
            if self.sort:
                if self.ignorecase:
                    self.result = sorted(self.result,key=str.lower)
                else:
                    self.result = sorted(self.result)
                for i in self.result:
                    print(i)
        except:
            pass

if __name__ == "__main__":
    pys = Py_Search(sys.argv)
    pys.main()
