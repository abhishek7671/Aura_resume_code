regex1 = r'(?:\d{1,2}[-/Th|St|Nd|Rd\s]*)?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)?[-a-z\s,.]*(?:\d{1,2}[-/Th|St|Nd|Rd)\s,]*)+(?:\d{2,4})+'
regex2 = r'D\d+@#\$\s*To\s*D\d+@#\$|D\d+@#\$\s*To\s*[a-zA-Z]'
regex3 = r'D\d+@#\$\s*–\s*D\d+@#\$|D\d+@#\$\s*–\s*[a-zA-Z]'
regex5 = r'D\d+@#\$\s*-\s*D\d+@#\$|D\d+@#\$\s*-\s*[a-zA-Z]'
regex4 = r'\d{4}\s*[-]\s*\d{4}|\d{4}\s*[T]o\s*\d{4}'
delimiter1 = "D"
delimiter2 = "@#$"