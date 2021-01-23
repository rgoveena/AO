def print_dict(the_dict, str_format="%-30s %s\n"):
    """print out a dictionary key:value pairs"""

    for (key, val) in sorted(the_dict.items()):
        print(str_format % (str(key)+':', val))


def dumpObj(obj, maxlen=77, lindent=24, maxspew=600):
    """Print a nicely formatted overview of an object.

    The output lines will be wrapped at maxlen, with lindent of space
    for names of attributes.  A maximum of maxspew characters will be
    printed for each attribute value.

    You can hand dumpObj any data type -- a module, class, instance, new class.

    Note that in reformatting for compactness the routine trashes any
    formatting in the docstrings it prints.

    Example:
       >>> class Foo(object):
               a = 30
               def bar(self, b):
                   "A silly method"
                   return a*b
       ... ... ... ...
       >>> foo = Foo()
       >>> dumpObj(foo)
       Instance of class 'Foo' as defined in module __main__ with id 136863308
       Documentation string:   None
       Built-in Methods:       __delattr__, __getattribute__, __hash__, __init__
                               __new__, __reduce__, __repr__, __setattr__,
                               __str__
       Methods:
         bar                   "A silly method"
       Attributes:
         __dict__              {}
         __weakref__           None
         a                     30
    """

    import types

  # Formatting parameters.
    ltab = 2    # initial tab in front of level 2 text

  #
  # Print a readable summary of those attributes
  #
    normalwidths = [lindent, maxlen - lindent]
    tabbedwidths = [ltab, lindent-ltab, maxlen - lindent - ltab]

#  print("normalwidths = %s" % normalwidths)
#  print("tabbedwidths = %s\n" % tabbedwidths)

  # There seem to be a couple of other types; gather templates of them
    method_wrapper_type = type(object().__hash__)

  #
  # Gather all the attributes of the object
  #
    objclass = None
    objdoc = None
    objmodule = '<None defined>'

    methods = []
    builtins = []
    classes = []
    attrs = []

    for slot in dir(obj):

        attr = getattr(obj, slot)

        if   slot == '__class__':
            objclass = attr.__name__

        elif slot == '__doc__':
            objdoc = attr

        elif slot == '__module__':
            objmodule = attr

        elif (isinstance(attr, types.BuiltinMethodType) or
              isinstance(attr, method_wrapper_type)):
            builtins.append(slot)

        elif (isinstance(attr, types.MethodType) or
              isinstance(attr, types.FunctionType)):
            methods.append((slot, attr))

        elif isinstance(attr, types.TypeType):
            classes.append((slot, attr))

        else:
            attrs.append((slot, attr))

  #
  # Sort the lists
  #
    methods.sort()
    builtins.sort()
    classes.sort()
    attrs.sort()


    def truncstring(the_string, maxlen):
        """truncate a string at a maxlen value"""

        if len(the_string) > maxlen:
            return the_string[0:maxlen] + ' ...(%d more chars)...' % (len(the_string) - maxlen)
        else:
            return the_string

    # Summary of introspection attributes
    if objclass == '':
        objclass = type(obj).__name__

    intro = "\nInstance of class '%s' as defined in module %s with id %d\n" % (objclass, objmodule, id(obj))
    print '\n'.join(prettyPrint(intro, maxlen))

    # Object's Docstring
    if objdoc is None:
        objdoc = str(objdoc)
    else:
        objdoc = ('"""' + objdoc.strip()  + '"""')

    print
    print prettyPrintCols(('Documentation string:\n', truncstring(objdoc, maxspew)),
                          normalwidths, ' ')

    # Built-in methods
    if builtins:
        bi_str = delchars(str(builtins), "[']") or str(None)
        print
        print prettyPrintCols(('Built-in Methods:\n', truncstring(bi_str, maxspew)),
                              normalwidths, ', ')

    # Classes
    if classes:
        print
        print 'Classes:\n'

    for (classname, classtype) in classes:
        classdoc = getattr(classtype, '__doc__', None) or '<No documentation>'
        print prettyPrintCols(('', classname, truncstring(classdoc, maxspew)),
                              tabbedwidths, ' ')

    # User methods
    if methods:
        print
        print 'Methods:\n'

    for (methodname, method) in methods:
        methoddoc = getattr(method, '__doc__', None) or '<No documentation>'
        print prettyPrintCols(('', methodname, truncstring(methoddoc, maxspew)),
                              tabbedwidths, ' ')

    # Attributes
    if attrs:
        print
        print 'Attributes:\n'

    for (attr, val) in attrs:
  #    print("\n\n  Type == %s   BuiltIn : %s  method : %s  MethodType %s") % (type(val), isinstance(val,types.BuiltinFunctionType), isinstance(val,types.BuiltinMethodType), isinstance(val,types.MethodType))

        if isinstance(val, types.InstanceType):  # recurse into dumpObj with instance
            print
            print("="*maxlen)
            print("\n\nRecurse into Instance : -->  %s : %s\n") % (attr, type(val))
            dumpObj(val, maxlen, lindent, maxspew)
            print("\n\n<--\n")
            print("="*maxlen)
            print

        else:                                    # print data in columns

            print prettyPrintCols(('', attr, truncstring(unicode(val), maxspew)),
                                  tabbedwidths, ' ')


def prettyPrintCols(strings, widths, split=' '):
    """Pretty prints text in colums, with each string breaking at
    split according to prettyPrint.  margins gives the corresponding
    right breaking point."""

    assert len(strings) == len(widths)

    strings = map(nukenewlines, strings)
#  print("\nstrings = %s" % strings)
#  print("widths = %s\n" % widths)

    # pretty print each column
    cols = [''] * len(strings)

    for i in range(len(strings)):
        cols[i] = prettyPrint(strings[i], widths[i], split)

#  print("cols = %s\n" % cols)

    # prepare a format line
    the_format = ''.join(["%%-%ds" % width for width in widths[0:-1]]) + "%s"


    def formatline(*cols):
        """format at line"""
        return the_format % tuple(map(lambda s: (s or ''), cols))

    # generate the formatted text
    return '\n'.join(map(formatline, *cols))


def prettyPrint(string, maxlen=75, split=' '):
    """Pretty prints the given string to break at an occurrence of
    split where necessary to avoid lines longer than maxlen.

    This will overflow the line if no convenient occurrence of split
    is found"""

    # Tack on the splitting character to guarantee a final match
    string += split

    lines = []
    oldeol = 0
    eol = 0

    while not (eol == -1 or eol == len(string)-1):
        eol = string.rfind(split, oldeol, oldeol+maxlen+len(split))
        lines.append(string[oldeol:eol])
        oldeol = eol + len(split)

    if len(lines) > 1:           # if there are multiple lines formated - add CR
        lines.append("\n")

    return lines


def nukenewlines(string):
    """Strip newlines and any trailing/following whitespace; rejoin
    with a single space where the newlines were.

    Bug: This routine will completely butcher any whitespace-formatted
    text."""

    if not string:
        return ''

    lines = string.splitlines()
    return ' '.join([line.strip() for line in lines])


def delchars(the_string, chars):
    """Returns a string for which all occurrences of characters in
    chars have been removed."""

    # Translate demands a mapping string of 256 characters;
    # whip up a string that will leave all characters unmolested.
    identity = ''.join([chr(x) for x in range(256)])

    return the_string.translate(identity, chars)
