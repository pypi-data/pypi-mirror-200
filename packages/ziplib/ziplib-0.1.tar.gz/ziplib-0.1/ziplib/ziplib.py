import zipfile 
import pyminizip 
import os 

class Zipper:
    
    """Adds a file or directory of files to a zip file with an option to enable password protection.
    
        :param input_file_name: The name of the file that you want to add to the zip folder. This will be ignored if you set compress_multiple=True.
        :param zip_file_name: The name of the zip file that you want to create. Defaults to 'Data.zip'
        :param is_password_protected: True or False depending on whether or not you want to password protect the zip file. Defaults to False
        :param password: (optional) The password for the zip file. Defaults to None
        :param compress_multiple: (optional) True or false depending on whether you want to zip the contents of an entire directory. 
                                    In that case, everything in the current working directory will be compressed.
        
        :returns: None
        
    """
    
    def __init__(self, input_file_name = None, zip_file_name = "Data.zip", is_password_protected = False, password = None, compress_multiple = False):
        
        if not input_file_name and not compress_multiple:
            
            raise Exception("You need to provide an input_file_name if you are not compressing a directory.")
        
        self.input_file_name = input_file_name
        self.zip_file_name = zip_file_name
        self.is_password_protected = is_password_protected
        self.password = password
        self.compress_multiple = compress_multiple
        
        #Check that file exists
        if not self.compress_multiple:
            
            try:
                open(self.input_file_name)
                
            except FileNotFoundError:
                raise Exception(f"Could not locate '{input_file_name}'. Make sure the file exists and you are pointing to the right directory.")
        
        #If the provided password is numeric, convert it to string
        if not isinstance(self.password, str) and self.password != None:
            self.password = str(self.password)
        
        #If user wants a password protected file but did not provide a password, raise an exception
        if self.is_password_protected and self.password == None:
            
            raise Exception("A password must be provided.")
    
        if self.is_password_protected:
            
            self.zip_with_password()
        
        if not self.is_password_protected:
            
            self.zip_without_password()
            
    def zip_with_password(self):
        
        print(f'''---\nZipping {self.input_file_name} into password protected file {self.zip_file_name}.\nThe password for the file is: {self.password}''' )
    
        if not self.compress_multiple:
            try:
                pyminizip.compress(self.input_file_name, 
                                   None,
                                   self.zip_file_name,
                                   self.password,
                                   4)
                
            except Exception as e:
                print(e)
        
        else:
            
            try:
                
                files = os.listdir()
                
                #Check if current directory contains any sub-directories. We will not zip the sub-directories. 
                if any([not os.path.isfile(file) for file in files]):
                    
                    print(f"The directory {os.getcwd()} contains sub-directories. These will be ignored.")
                
                #Only compress files, not directories
                files_to_compress = [file for file in files if file[0] != '.' and os.path.isfile(file)]
                
                pyminizip.compress_multiple(files_to_compress, 
                                           ["" for _ in range(len(files_to_compress))],
                                           self.zip_file_name,
                                           self.password,
                                           4)
                
            except Exception as e:
                print(e)
                
            print("---")
    
    def zip_without_password(self):
        
        print(f'''---\nZipping {self.input_file_name} into unprotected file {self.zip_file_name}''' )
        
        if not self.compress_multiple:
            with zipfile.ZipFile(self.zip_file_name, 'w') as zipobj:        
                
                zipobj.write(self.input_file_name)
                
        else:
            
            files = os.listdir()
                
            #Check if current directory contains any sub-directories. 
            if any([not os.path.isfile(file) for file in files]):
                
                print(f"The directory {os.getcwd()} contains sub-directories. These will be ignored.")
                    
            files_to_compress = [file for file in files if file[0] != '.' and os.path.isfile(file)]
            
            with zipfile.ZipFile(self.zip_file_name, 'w') as zipobj:        
                
                for file in files_to_compress:
                    
                    zipobj.write(file)
                    
            print("---")
            

