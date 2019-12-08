# Invoice Parser
A script which parses text file and outputs key:value data as defined in
invoice_mode/config.py file

##WHAT?
A python3 script that helps you find a relevant payment information in your
text. It allows automation in bulk parsing

##HOW?
Script parses text file and retrieves information according to the rules which
are defined in config.py file.
config.MAP contains a mapping between keywords of interest, e.g.
'Summa inkl. moms' and regex pattern to extract that value from the text.
Mapping extended and adjusted accordingly, for example, if you want to find
OCR numbers in the document, you can add mapping `'OCR': <pattern>'` to the
`config.MAP` dictionary

##WHY?
Automation==Profit