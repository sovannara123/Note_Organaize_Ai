import re 
import unicodedata

class TextCleaner : 
    """Create TextCleaner class
  •   Write clean() main method
  •   Write remove_extra_spaces() method
  •   Write remove_special_chars() method
  •   Write fix_line_breaks() method
  •   Write normalize_encoding() method
  •   Add empty output validation
  •   Add docstrings to all methods"""
    def __init__(
        self,
        keep_ascii_only: bool = True,
        join_single_lines: bool = True,
        max_blank_lines: int = 2,
    ):
        
        self.keep_ascii_only = keep_ascii_only
        self.join_single_lines = join_single_lines
        self.max_blank_lines = max_blank_lines

    def clean(self , raw_text :str )-> str:
    
        if not isinstance(self.raw_text , str) : 
            raise TypeError("Input must be a String.")
    
        text = raw_text 

        text = self.normalize_encoding(text)
        text = self.fix_line_breaks(text)
        text = self.remove_extra__space(text)
        text = self.remove_special_chars(text)

        if not text.strip():
            raise ValueError ("Text is empty after cleaning") 
        
        return text
    
    
    def remove_extra__space (self , text : str) -> str :
    # remove unessary space , tab , and extra blank line 
     # arge : text (str) input text 
     # return str : text with normalized spacing 

        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r" *\n *", "\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()

    def remove_special_chars(self , text :str ) -> str :
        cleaned = []

        for char in text :
            if ord (char) <128:  # ord function = convert caracter into a number (unicode code)
                cleaned.append(char)
            elif unicodedata.category(char)[0] != "C":
                pass
        return "".join(cleaned)  # concept join turn list back into one string 
    
    def fix_line_breaks(self , text : str) -> str : 
        # 
        # arges : text(str ) :input text 
        # 
        # return string encoding_cleaned text. 

        text = text.replace("\r\n", "\n").replace("\r", "\n")

        # Preserve paragraphs
        text = re.sub(r"\n{3,}", "\n\n", text)

        # Join single line breaks
        text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)

        return text
    
    def normalize_encoding(self , text : str) -> str:
    
        # Nornalize text to UTF-8 # fiix common mojibake errors 
        text = text.encode("utf-8" , errors="ignore").decode("utf-8")  

        replacements = {
            "â€™": "'",
            "â€œ": '"',
            "â€\x9d": '"',
            "â€“": "-",
            "â€”": "-",
            "â€¦": "...",
        }
        
        for bad,good in replacements.items():
            text = text.replace(bad , good)
        
        return text 