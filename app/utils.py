from django.conf import settings
import mimetypes, os
from django.core.files import File

class FileComparator:
    def __init__(self, new_file, dr):
        self.old_file = None
        self.new_file = new_file
        self.dr = dr
        self.is_same = False
        self.get_old_file()
    
    def are_files_same(self):
        if self.old_file.size != self.new_file.size:
            return False
        
        old_content = self.old_file.read()
        new_content = self.new_file.read()
        
        return old_content == new_content
    
    def get_file_type(self, file):
        mime_type, _ = mimetypes.guess_type(file.name)
        if mime_type:
            main_type, sub_type = mime_type.split('/')
            return sub_type
        return "unknown"
        
    def get_old_file(self):
         files = os.walk(os.path.join(settings.MEDIA_ROOT, self.dr))
         for f, _, files in files:
             for file in files:
                 with open(os.path.join(f, file), "rb") as file:
                     self.old_file = File(file)
                     if self.are_files_same():
                         self.is_same = True
                     
                     
                     

# Usage example:
#old_file = ContentFile(b"Sample PDF content.")
#new_file = ContentFile(b"Sample audio content.")

#file_comparator = FileComparator(old_file, new_file)
#files_are_same = file_comparator.are_files_same()
#file_type_old = file_comparator.get_file_type(old_file)
#file_type_new = file_comparator.get_file_type(new_file)

#print("Files are same:", files_are_same)
#print("Old file type:", file_type_old)
#print("New file type:", file_type_new)
