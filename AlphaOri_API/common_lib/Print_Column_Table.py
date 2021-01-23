import cStringIO,operator
import re
import math

class TextTable():

    def __init__(self, hasHeader=True, headerChar='-', delim=' | ', justify='left',
               separateRows=True, prefix='| ', postfix=' |', wrapfunc="plain", colWidth=10):

        """Creates a Table Display of information:

           - hasHeader: True if the first row consists of the columns' names.

           - headerChar: Character to be used for the row separator line
             (if hasHeader==True or separateRows==True).

           - delim: The column delimiter.

           - justify: Determines how are data justified in their column.
             Valid values are 'left','right' and 'center'.

           - separateRows: True if rows are to be separated by a line
             of 'headerChar's.

           - prefix: A string prepended to each printed row.

           - postfix: A string appended to each printed row.

           - wrapfunc: A function f(text) for wrapping text; each element in
             the table is first wrapped by this function.
             Values: "plain", "wrap_always", "wrap_onspace", "wrap_onspace_strict"

           - colWidth : int width of the column  """

        self.hasHeader = hasHeader
        self.last_row = hasHeader                                               # if hasHeader, set this - allows for final divider line at bottom of table
        self.headerChar = headerChar
        self.delim = delim
        self.justify = justify
        self.separateRows = separateRows
        self.prefix = prefix
        self.postfix = postfix
        self.width = colWidth

        # assign the formatting function
        self.wrapfunc = {"plain" : lambda x:x,
                         "wrap_always" : lambda x: self.wrap_always(x, self.width),
                         "wrap_onspace" : lambda x: self.wrap_onspace(x, self.width),
                         "wrap_onspace_strict" : lambda x: self.wrap_onspace_strict(x, self.width)}[wrapfunc]


        self.TABLE_BLANK_LINE = [""]                                            # constant - a blank table row


    def centerLine(self, text_line, text_width):
        """return a text_line center formated

            text_line = chars to be centered
            text_width = int : width of line

            Returns a single string in a list - formatted center justified :  ["  the text_line here  "]
        """

        center_format = '{:^%s}' % text_width
        return [center_format.format(text_line)]


    def blankRow(self, num_columns):
        """return a blank row of num_columns

            num_columns = int : the number of columns to create in row

            Returns a list of blank strings -  ["", ""]
        """

        temp_list = []

        for i in range(num_columns):
            temp_list.append("")

        return temp_list


    def createTable(self, rows):
        """
            Create the ASCII table with the row data.

            - rows: A sequence of sequences of items, one sequence per row (string list of lists).

            Returns : a list of lists - the formatted table output
        """

        self.rows = rows

        # break each logical row into one or more physical ones
        logicalRows = [self.rowWrapper(row) for row in self.rows]

        # columns of physical rows
        columns = map(None, *reduce(operator.add, logicalRows))

        # get the maximum of each column by the string length of its items
        maxWidths = [max([len(str(item)) for item in column]) for column in columns]

        rowSeparator = self.headerChar * (len(self.prefix) + len(self.postfix) + sum(maxWidths) + \
                                     len(self.delim)*(len(maxWidths)-1))

        # select the appropriate justify method
        justifySetting = {'center':str.center,
                          'right' :str.rjust,
                          'left'  :str.ljust}[self.justify.lower()]

        output = cStringIO.StringIO()

        if self.separateRows or self.hasHeader:                                 # add rowSeparator for separate rows
            print >> output, rowSeparator                                       # OR topSeparator row for headers

        for physicalRows in logicalRows:
            for row in physicalRows:
                print >> output, \
                    self.prefix \
                    + self.delim.join([justifySetting(str(item),width) for (item, width) in zip(row, maxWidths)]) \
                    + self.postfix

            if self.separateRows or self.hasHeader:
                print >> output, rowSeparator
                self.hasHeader=False

        if self.last_row and not self.separateRows:                             # add final rowSeparator?
            print >> output, rowSeparator

        return output.getvalue()


    # closure for breaking logical rows to physical, using wrapfunc
    def rowWrapper(self, row):
#        print("row = ",  row)

        if len(row) == 1:                   # special case for 1 element row
            return [row]
        else:                               # multi element row - create a list of lists
            newRows = [self.wrapfunc(item).split('\n') for item in row]
#            print("\nnewRows = %s" % newRows)
            return [[substr or '' for substr in item] for item in map(None,*newRows)]


    # written by Mike Brown
    # http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/148061
    def wrap_onspace(self, text, width):
        """
        A word-wrap function that preserves existing line breaks
        and most spaces in the text. Expects that existing line
        breaks are posix newlines (\n).
        """

        return reduce(lambda line, word, width=width: '%s%s%s' %
                      (line,
                       ' \n'[(len(line[line.rfind('\n')+1:])
                             + len(word.split('\n',1)[0]
                                  ) >= width)],
                       word),
                      text.split(' ')
                     )


    def wrap_onspace_strict(self, text, width):
        """Similar to wrap_onspace, but enforces the width constraint:
           words longer than width are split."""

        wordRegex = re.compile(r'\S{'+str(width)+r',}')
        return self.wrap_onspace(wordRegex.sub(lambda m: self.wrap_always(m.group(), width),text),width)


    def wrap_always(self, text, width):
        """A simple word-wrap function that wraps text on exactly width characters.
           It doesn't split the text in words."""

        return '\n'.join([ text[width*i:width*(i+1)] \
                           for i in xrange(int(math.ceil(1.*len(text)/width))) ])


if __name__ == '__main__':

    labels = ('First Name', 'Last Name', 'Age', 'Position')
    data = \
    '''John,Smith,24,Software Engineer
       Mary,Brohowski,23,Sales Manager
       Aristidis,Papageorgopoulos,28,Senior Reseacher'''

    rows = [row.strip().split(',') for row in data.splitlines()]

    # test indent with different wrapping functions
    width = 10

    print rows
    print 'Without wrapping function\n'
    textObject = TextTable(headerChar='_', wrapfunc="plain", colWidth=width)
    output = textObject.createTable([labels]+rows)
    print output

    del textObject

    for wrapper in ("wrap_always", "wrap_onspace", "wrap_onspace_strict"):
        print 'Wrapping function: %s(x,width=%d)\n' % (wrapper, width)
        tableObj = TextTable(wrapfunc=wrapper, colWidth=width)
        output = tableObj.createTable([labels]+rows)
        print output
        del tableObj

    width = 45

    data = [["="*width],
            ["HGST-S3-DC01-R01-SG01 : SERVER"],
            ["ONLINE"],
            ["SPXMGMT"],
            ["f4407f29-6445-4298-86b0-6b8b45ce791e"],
            [""],
            ["10.16.110.1"],
            ["10.16.210.1"],
            ["127.0.0.1"],
            ["192.168.1.11"],
            ["="*width]
       ]

#    print data

    textObject = TextTable(hasHeader=False, headerChar='-', wrapfunc="plain", separateRows=False, colWidth=width)
    output = textObject.createTable(data)
    print output


    data = [["Blue"],
            ["Green"],
            ["Purple"],
            ["Red"]
       ]

#    print data

    width = 10
    textObject = TextTable(hasHeader=False, headerChar='-', wrapfunc="plain", colWidth=width)
    output = textObject.createTable(data)
    print output

    # output:
    #
    #Without wrapping function
    #
    #First Name | Last Name        | Age | Position
    #-------------------------------------------------------
    #John       | Smith            | 24  | Software Engineer
    #Mary       | Brohowski        | 23  | Sales Manager
    #Aristidis  | Papageorgopoulos | 28  | Senior Reseacher
    #
    #Wrapping function: wrap_always(x,width=10)
    #
    #----------------------------------------------
    #| First Name | Last Name  | Age | Position   |
    #----------------------------------------------
    #| John       | Smith      | 24  | Software E |
    #|            |            |     | ngineer    |
    #----------------------------------------------
    #| Mary       | Brohowski  | 23  | Sales Mana |
    #|            |            |     | ger        |
    #----------------------------------------------
    #| Aristidis  | Papageorgo | 28  | Senior Res |
    #|            | poulos     |     | eacher     |
    #----------------------------------------------
    #
    #Wrapping function: wrap_onspace(x,width=10)
    #
    #---------------------------------------------------
    #| First Name | Last Name        | Age | Position  |
    #---------------------------------------------------
    #| John       | Smith            | 24  | Software  |
    #|            |                  |     | Engineer  |
    #---------------------------------------------------
    #| Mary       | Brohowski        | 23  | Sales     |
    #|            |                  |     | Manager   |
    #---------------------------------------------------
    #| Aristidis  | Papageorgopoulos | 28  | Senior    |
    #|            |                  |     | Reseacher |
    #---------------------------------------------------
    #
    #Wrapping function: wrap_onspace_strict(x,width=10)
    #
    #---------------------------------------------
    #| First Name | Last Name  | Age | Position  |
    #---------------------------------------------
    #| John       | Smith      | 24  | Software  |
    #|            |            |     | Engineer  |
    #---------------------------------------------
    #| Mary       | Brohowski  | 23  | Sales     |
    #|            |            |     | Manager   |
    #---------------------------------------------
    #| Aristidis  | Papageorgo | 28  | Senior    |
    #|            | poulos     |     | Reseacher |
    #---------------------------------------------
