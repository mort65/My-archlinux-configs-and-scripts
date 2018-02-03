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
    silent = False
    
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
        if not self.silent:
            if not self.sort:
                print(result_link)

    def add_dir(self,new_dir):
        result_dir = ""
        if self.mark:
            result_dir = "\""+new_dir+"\"d"
        else:
            result_dir = "\""+new_dir+"\""
        self.result.append(result_dir)
        if not self.silent:
            if not self.sort:
                print(result_dir)

    def add_file(self,new_file):
        result_file = ""
        if self.mark:
            result_file = "\""+new_file+"\"f"
        else:
            result_file = "\""+new_file+"\""
        self.result.append(result_file)
        if not self.silent:
            if not self.sort:
                print(result_file)
            
    def __init__(self,Main_Dir='.',Pattern='.*',Recursive=False,Ignorecase=False,Searchdir=False,Searchfile=False,Searchlink=False,Onlyname=False,Mark=False,Sort=False,Silent=False):
        self.main_dir = Main_Dir
        self.pattern = Pattern
        self.recursive = Recursive
        self.ignorecase = Ignorecase
        self.searchdir = Searchdir
        self.searchfile = Searchfile
        self.searchlink = Searchlink
        self.onlyname = Onlyname
        self.mark = Mark
        self.sort = Sort
        self.silent = Silent
        if self.searchdir is False and self.searchlink is False and self.searchfile is False:
            return
        if self.main_dir == '':
            return
        if self.pattern == '':
            return

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
                if not self.silent:
                    for i in self.result:
                        print(i)
        except:
            pass

def show_usage():
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

if __name__ == "__main__":
    Main_Dir = ''
    Text = ''
    Pattern = ''
    Recursive = False
    Ignorecase = False
    Searchdir = False
    Searchfile = False
    Onlyname = False
    Searchlink = False
    Mark = False
    Usage = False
    Sort = False
    if len(sys.argv) > 1:
        for i in range(1,len(sys.argv)):
            if len(sys.argv[i]) > 0:
                if sys.argv[i][0] == '-':
                    if (Main_Dir != '') or (Text != ''):
                        show_usage()
                        exit(1)
                    elif sys.argv[i][1] == '-':
                        if sys.argv[i] == '--help':
                            Usage = True
                        elif sys.argv[i] == '--Recursive':
                            Recursive = True
                        elif sys.argv[i] == '--ignore-case':
                            Ignorecase = True
                        elif sys.argv[i] == '--link':
                            Searchlink = True                   
                        elif sys.argv[i] == '--dir':
                            Searchdir = True
                        elif sys.argv[i] == '--name':
                            Onlyname = True
                        elif sys.argv[i] == '--file':
                            Searchfile = True
                        elif sys.argv[i] == '--Mark':
                            Mark = True
                        elif sys.argv[i] == '--Sort':
                            Sort = True
                        else:
                            show_usage()
                            exit(1)
                    else:
                        for c in range(1,len(sys.argv[i])):
                            if sys.argv[i][c] == 'h':
                                Usage = True
                            elif sys.argv[i][c] == 'r':
                                Recursive = True
                            elif sys.argv[i][c] == 'i':
                                Ignorecase = True
                            elif sys.argv[i][c] == 'l':
                                Searchlink = True                                              
                            elif sys.argv[i][c] == 'd':
                                Searchdir = True
                            elif sys.argv[i][c] == 'n':
                                Onlyname = True
                            elif sys.argv[i][c] == 'f':
                                Searchfile = True
                            elif sys.argv[i][c] == 'm':
                                Mark = True 
                            elif sys.argv[i][c] == 's':
                                Sort = True
                            else:
                                show_usage()
                                exit(1)
                elif i == ( len(sys.argv) - 2 ):
                    Main_Dir = sys.argv[i]
                elif i == ( len(sys.argv) - 1 ):
                    Text = sys.argv[i]
                    if Ignorecase:
                        Pattern = Text.lower()
                    else:
                        Pattern = Text
                else:
                    show_usage()
                    exit(1)
    if Usage:
        show_usage()
        exit(0)
    if Searchdir is False and Searchlink is False and Searchfile is False:
        Searchdir,Searchfile,Searchlink = True,True,True
    if Main_Dir == '':
        Main_Dir ='.'
    if Pattern == '':
        Pattern = '.*'
    pys = Py_Search(Main_Dir,Pattern,Recursive,Ignorecase,Searchdir,Searchfile,Searchlink,Onlyname,Mark,Sort,Silent=False)
    pys.main()
