regex2 = r'D\d+@#\$\s*To\s*D\d+@#\$'
regex3 = r'D\d+@#\$\s*–\s*D\d+@#\$|D\d+@#\$\s*–\s*[a-zA-Z]'
regex5 = r'D\d+@#\$\s*-\s*D\d+@#\$|D\d+@#\$\s*-\s*[a-zA-Z]'
regex4 = r'\d{4}\s*[-]\s*\d{4}|\d{4}\s*[T]o\s*\d{4}|\d{4}\s*[–]\s*till|\d{4}\s*[–]\s*Till'
regex6 = r'D\d+@#\$\s*—\s*D\d+@#\$|D\d+@#\$\s*—\s*[a-zA-Z]'
regex7 = r'D\d+@#\$\s*' '\s*D\d+@#\$'
regex8 = r'D\d+@#\$\s*' '\s*till|D\d+@#\$\s*' '\s*Till|D\d+@#\$\s*' '\s*TILL|D\d+@#\$\s*' '\s*Present|D\d+@#\$\s*' '\s*PRESENT|D\d+@#\$\s*' '\s*present|D\d+@#\$\s*' '\s*Current|D\d+@#\$\s*' '\s*CURRENT|D\d+@#\$\s*' '\s*current|D\d+@#\$\s*' '\s*Today|D\d+@#\$\s*' '\s*today|D\d+@#\$\s*' '\s*now|D\d+@#\$\s*' '\s*Now|D\d+@#\$\s*' '\s*NOW'
regex9 = r'D\d+@#\$\s*To\s*till|D\d+@#\$\s*To\s*Till|D\d+@#\$\s*To\s*TILL|D\d+@#\$\s*To\s*Present|D\d+@#\$\s*To\s*present|D\d+@#\$\s*To\s*PRESENT|D\d+@#\$\s*To\s*present|D\d+@#\$\s*To\s*Current|D\d+@#\$\s*To\s*CURRENT|D\d+@#\$\s*To\s*current|D\d+@#\$\s*To\s*Today|D\d+@#\$\s*To\s*today|D\d+@#\$\s*To\s*now|D\d+@#\$\s*To\s*NOW|D\d+@#\$\s*To\s*Now'                 

value_list=['To','–','-','—',' ']
delimiter1 = "D"
delimiter2 = "@#$"
delimiter3 = "sq"

########################## other method to read delimiters ############################################
value_list=['To','–','-','—',' ']
dtn = {regex2:value_list[0],regex9:value_list[0],regex3:value_list[1],regex5:value_list[2],regex6:value_list[3],regex7:value_list[4],regex8:value_list[4]}