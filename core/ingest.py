import os
import PyPDF2

"""
────────────────────────────────────────────────────
MODULE 1: INGEST
────────────────────────────────────────────────────
File:           core/ingest.py
Class:          NoteIngester
Responsibility: Read files and extract raw text
Input:          File path (string)
Output:         Raw text (string)
Supports:       .txt  .md  .pdf
Dependencies:   os, PyPDF2

Algorithm:
  1. Validate file exists on disk
  2. Read and validate file extension
  3. Route to correct reader method
  4. Extract all text content
  5. Validate output is not empty
  6. Return raw text string           

Error Cases:
  File not found    →  FileNotFoundError
  Wrong format      →  ValueError
  Empty file        →  ValueError"""

class NoteIngester :

    def __init__(self , file_path :str) :
        self.file_path = file_path 

   # extension 
    SUPPORTED_EXTENSIONS = {".pdf", ".txt" , ".md" }
   
    def load_file (self) -> str :

        self._validate_file_exists()
        extension = self._validate_file_extension()

        if extension in {".txt", ".md"}:
            content = self._read_text_file()
        
        elif extension == ".pdf":
            content = self._read_pdf_file()
        
        else:
            raise ValueError("Unsupported file type.")

        self._validate_not_empty(content)

        return content


    

    # check file exist 
    def _validate_file_exists(self) -> None: 
         
         # if file not exist return Error 
        if not os.path.isfile(self.file_path):
                raise FileNotFoundError(f"File not found: {self.file_path}")
        
    # check validate file extensio
    def _validate_file_extension (self) -> str :
         
        _, extension = os.path.splitext(self.file_path)
        extension = extension.lower()

        if extension not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type: {extension}. "
                f"Supported: {self.SUPPORTED_EXTENSIONS}"
            )
        return extension
        
    

    def _read_pdf_file(self) -> str :

        pages_text = []

        with open(self.file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)

            for page in reader.pages:
                page_text = page.extract_text()

                if page_text:
                    pages_text.append(page_text)

        return "\n".join(pages_text)

    def _read_text_file (self) -> str : 

        with open(self.file_path , "r" , encoding = "utf-8") as file :
            
            return file.read()
    
    def _validate_not_empty (self , content :str) : 

        if not content.strip(): 
            raise ValueError(f"File {self.file_path} Is Empty.... ")





            

        

         
         
         
        
         

        
    



    
        

    
    
    


    


    