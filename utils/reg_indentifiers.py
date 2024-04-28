

#regex1 = r'(?:\d{1,2}[-/?:th|St|Nd|Rd\s]*)?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)?[-a-z\s,.]*(?:\d{1,2}[-/?:th|St|Nd|Rd)\s,]*)+(?:\d{2,4})+'
regex2 = r'D\d+@#\$\s*To\s*D\d+@#\$|D\d+@#\$\s*To\s*[a-zA-Z]|D\d+@#\$\s*to\s*D\d+@#\$|D\d+@#\$\s*to\s*[a-zA-Z]'
regex3 = r'D\d+@#\$\s*–\s*D\d+@#\$|D\d+@#\$\s*–\s*[a-zA-Z]'
regex5 = r'D\d+@#\$\s*-\s*D\d+@#\$|D\d+@#\$\s*-\s*[a-zA-Z]'
regex4 = r'\d{4}\s*[-]\s*\d{4}|\d{4}\s*[T]o\s*\d{4}|\d{4}\s*[–]\s*till|\d{4}\s*[–]\s*Till'

regex_date_identifer = [r"\b\d{1,2}[-](?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[-]\d{4}\b",
r"\b\d{4}[-](?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[-]\d{1,2}\b",
r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[-]\d{4}\b",
r"\b\d{4}[-](?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b",
r"\b\d{1,2}(?:Th|Rd|Nd|St)[\s](?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[\s]\d{4}\b",
r"\b\d{1,2}(?:Th|Rd|Nd|St)[-](?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[-]\d{4}\b",
r"\b\d{4}[-](?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[-]\d{1,2}(?:Th|Rd|Nd|St)\b",
r"\b\d{1,2}[–](?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[–]\d{4}\b",
r"\b\d{4}[–](?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[–]\d{1,2}\b",
r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[–]\d{4}\b",
r"\b\d{4}[–](?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b",
r"\b\d{1,2}(?:Th|Rd|Nd|St)[–](?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[–]\d{4}\b",
r"\b\d{4}[–](?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[–]\d{1,2}(?:Th|Rd|Nd|St)\b",
r"\b\d{1,2}[\\](?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[\\]\d{4}\b",
r"\b\d{4}[\\](?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[\\]\d{1,2}\b",
r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[\\]\d{4}\b",
r"\b\d{4}[\\](?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b",
r"\b\d{1,2}(?:Th|Rd|Nd|St)[\\](?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[\\]\d{4}\b",
r"\b\d{4}[\\](?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[\\]\d{1,2}(?:Th|Rd|Nd|St)\b",
r"\b\d{1,2}[/](?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[/]\d{4}\b",
r"\b\d{4}[/](?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[/]\d{1,2}\b",
r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[/]\d{4}\b",
r"\b\d{4}[/](?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b",
r"\b\d{1,2}(?:Th|Rd|Nd|St)[/](?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[/]\d{4}\b",
r"\b\d{4}[/](?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[/]\d{1,2}(?:Th|Rd|Nd|St)\b",
r"\b\d{1,2}[.](?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[.]\d{4}\b",
r"\b\d{4}[.](?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[.]\d{1,2}\b",
r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[.]\d{4}\b",
r"\b\d{4}[.](?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b",
r"\b\d{1,2}(?:Th|Rd|Nd|St)[.](?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[.]\d{4}\b",
r"\b\d{4}[.](?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[.]\d{1,2}(?:Th|Rd|Nd|St)\b",
r"\b\d{1,2}[\s](?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[\s]\d{4}\b",
r"\b\d{4}[\s](?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[\s]\d{1,2}\b",
r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[\s]\d{4}\b",
r"\b\d{4}[\s](?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b",
r"\b\d{4}[\s](?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[\s]\d{1,2}(?:Th|Rd|Nd|St)\b",
r"(?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[’]\d{2}\b",
r"\b\d{4}(?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\d{1,2}(?:Th|Rd|Nd|St)\b",
r"\b\d{4}(?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\d{1,2}\b",
r"\b\d{4}(?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b",
r"\b\d{1,2}(?:Th|Rd|Nd|St)(?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\d{4}\b",
r"\b\d{1,2}(?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\d{4}\b",
r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\d{4}\b",
r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\d{1,2}(?:Th|Rd|Nd|St)\d{4}\b",
r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[\s][–]\d{4}\b",
r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[–][\s]\d{4}\b",
r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[\s][–][\s]\d{4}\b",
r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[\s][-][\s]\d{4}\b",
r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[\s][-]\d{4}\b",
r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[-][\s]\d{4}\b",
r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[\s][–][\s]\d{4}\b",
r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[,]\d{4}\b",
r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[,][\s]\d{4}\b",
r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[\s]\d{1,2}(?:Th|Rd|Nd|St)[,][\s]\d{4}\b",
r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[\s][—]\d{4}\b",
r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[—][\s]\d{4}\b",
r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[\s][–][\s]\d{4}\b",
r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[\s]\d{4}\b",
r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[\s]\d{1,2}(?:Th|Rd|Nd|St)[\s]\d{4}\b",
r"\b\d{1,2}[\s](?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[,]\d{4}\b",
r"\b\d{1,2}[\s](?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[,][\s]\d{4}\b",
r"(?:january|february|march|april|may|june|july|august|september|october|november|december|sept|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\d{1,2}(?:Th|Rd|Nd|St)[\s*]\d{4}\b",
r"(?:january|february|march|april|may|june|july|august|september|october|november|december|sept|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\d{4}",                       
r"(?:January|February|March|April|May|June|July|August|September|October|November|December|Sept|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[']\d{4}\b",                       


r"\b\d{1,2}[-]\d{1,2}[-]\d{4}\b",
r"\b\d{4}[-]\d{1,2}[-]\d{1,2}\b",
r"\b\d{1,2}[-]\d{4}\b",
r"\b\d{4}[-]\d{1,2}\b",
r"\b\d{1,2}(?:Th|Rd|Nd|St)[-]\d{1,2}[-]\d{4}\b",
r"\b\d{4}[-]\d{1,2}[-]\d{1,2}(?:Th|Rd|Nd|St)\b",
r"\b\d{1,2}[–]\d{1,2}[–]\d{4}\b",
r"\b\d{4}[–]\d{1,2}[–]\d{1,2}\b",
r"\b\d{1,2}[–]\d{4}\b",
r"\b\d{4}[–]\d{1,2}\b",
r"\b\d{1,2}(?:Th|Rd|Nd|St)[–]\d{1,2}[–]\d{4}\b",
r"\b\d{4}[–]\d{1,2}[–]\d{1,2}(?:Th|Rd|Nd|St)\b",
r"\b\d{1,2}[\\]\d{1,2}[\\]\d{4}\b",
r"\b\d{4}[\\]\d{1,2}[\\]\d{1,2}\b",
r"\b\d{1,2}[\\]\d{4}\b",
r"\b\d{4}[\\]\d{1,2}\b",
r"\b\d{1,2}(?:Th|Rd|Nd|St)[\\]\d{1,2}[\\]\d{4}\b",
r"\b\d{4}[\\]\d{1,2}[\\]\d{1,2}(?:Th|Rd|Nd|St)\b",
r"\b\d{1,2}[/]\d{1,2}[/]\d{4}\b",
r"\b\d{4}[/]\d{1,2}[/]\d{1,2}\b",
r"\b\d{1,2}[/]\d{4}\b",
r"\b\d{4}[/]\d{1,2}\b",
r"\b\d{1,2}(?:Th|Rd|Nd|St)[/]\d{1,2}[/]\d{4}\b",
r"\b\d{4}[/]\d{1,2}[/]\d{1,2}(?:Th|Rd|Nd|St)\b",
r"\b\d{1,2}[.]\d{1,2}[.]\d{4}\b",
r"\b\d{4}[.]\d{1,2}[.]\d{1,2}\b",
r"\b\d{1,2}[.]\d{4}\b",
r"\b\d{4}[.]\d{1,2}\b",
r"\b\d{1,2}(?:Th|Rd|Nd|St)[.]\d{1,2}[.]\d{4}\b",
r"\b\d{4}[.]\d{1,2}[.]\d{1,2}(?:Th|Rd|Nd|St)\b",
r"\b\d{1,2}[\s]\d{1,2}[\s]\d{4}\b",
r"\b\d{4}[\s]\d{1,2}[\s]\d{1,2}\b",
r"\b\d{1,2}[\s]\d{4}\b",
r"\b\d{4}[\s]\d{1,2}\b",
r"\b\d{1,2}(?:Th|Rd|Nd|St)[\s]\d{1,2}[\s]\d{4}\b",
r"\b\d{4}[\s]\d{1,2}[\s]\d{1,2}(?:Th|Rd|Nd|St)\b"]
delimiter1 = "D"
delimiter2 = "@#$"