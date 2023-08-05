
class ArgConstant():
    def __init__(self, shortForm, longForm, help, id):
        self.shortForm = shortForm
        self.longForm = longForm
        self.help = help
        self.id = id


ARGS_HELP, ARGS_NUMBER, ARGS_ENDS, ARGS_TABS, ARGS_SQUEEZE = range(0, 5)
ARGS_REVERSE, ARGS_COUNT, ARGS_BLANK, ARGS_FILES, ARGS_INTERACTIVE = range(5, 10)
ARGS_CLIP, ARGS_CHECKSUM, ARGS_DEC, ARGS_HEX, ARGS_BIN = range(10, 15)
ARGS_VERSION, ARGS_DEBUG, ARGS_CUT, ARGS_REPLACE, ARGS_DATA = range(15, 20)
ARGS_CONFIG, ARGS_LLENGTH, ARGS_ONELINE, ARGS_PEEK, ARGS_NOCOL = range(20, 25)
ARGS_EOF, ARGS_B64E, ARGS_B64D, ARGS_FFILES, ARGS_GREP = range(25, 30)
ARGS_NOBREAK, ARGS_ECHO, ARGS_CCOUNT, ARGS_HEXVIEW, ARGS_BINVIEW = range(30, 35)
ARGS_NOKEYWORD, = range(35, 36)

ALL_ARGS = [[['-h', '--help'], 'show this help message and exit', ARGS_HELP],
            [['-v', '--version'], 'output version information and exit', ARGS_VERSION],
            [['-d', '--debug'], 'show debug information', ARGS_DEBUG],
            [['-n', '--number'], 'number all output lines', ARGS_NUMBER],
            [['-l', '--linelength'], 'display the length of each line', ARGS_LLENGTH],
            [['-e', '--ends'], 'display $ at the end of each line', ARGS_ENDS],
            [['-t', '--tabs'], 'display TAB characters as ^I', ARGS_TABS],
            [['--eof', '--eof'], 'display EOF characters as ^EOF', ARGS_EOF],
            [['-u', '--unique'], 'suppress repeated output lines', ARGS_SQUEEZE],
            [['-b', '--blank'], 'hide empty lines', ARGS_BLANK],
            [['-r', '--reverse'], 'reverse output', ARGS_REVERSE],
            [['-p', '--peek'], 'only print the first and last lines', ARGS_PEEK],
            [['-s', '--sum'], 'show sum of lines', ARGS_COUNT],
            [['-S', '--SUM'], 'ONLY show sum of lines', ARGS_CCOUNT],
            [['-f', '--files'], 'list applied files', ARGS_FILES],
            [['-F', '--FILES'], 'ONLY list applied files and file sizes', ARGS_FFILES],
            [['-g', '--grep'], 'only show lines containing queried keywords', ARGS_GREP],
            [['-i', '--interactive'], 'use stdin', ARGS_INTERACTIVE],
            [['-o', '--oneline'], 'take only the first stdin-line', ARGS_ONELINE],
            [['-E', '--ECHO'], 'handle every following parameter as stdin', ARGS_ECHO],
            [['-c', '--clip'], 'copy output to clipboard', ARGS_CLIP],
            [['-m', '--checksum'], 'show the checksums of all files', ARGS_CHECKSUM],
            [['-a', '--attributes'], 'show meta-information about the files', ARGS_DATA],
            [['--dec', '--DEC'], 'convert decimal numbers to hexadecimal and binary', ARGS_DEC],
            [['--hex', '--HEX'], 'convert hexadecimal numbers to decimal and binary', ARGS_HEX],
            [['--bin', '--BIN'], 'convert binary numbers to decimal and hexadecimal', ARGS_BIN],
            [['--b64e', '--b64e'], 'encode the input to base64', ARGS_B64E],
            [['--b64d', '--b64d'], 'decode the input from base64', ARGS_B64D],
            [['--hexview', '--HEXVIEW'], 'display the raw byte representation in hexadecimal', ARGS_HEXVIEW],
            [['--binview', '--binview'], 'display the raw byte representation in binary', ARGS_BINVIEW],
            [['--nc', '--nocolor'], 'disable colored output', ARGS_NOCOL],
            [['--nb', '--nobreak'], 'do not interrupt the output on queried keywords', ARGS_NOBREAK],
            [['--nk', '--nokeyword'], 'inverse the grep output', ARGS_NOKEYWORD],
            [['--config', '--config'], 'change color configuration', ARGS_CONFIG]]

ALL_ARGS = [ArgConstant(x[0][0], x[0][1], x[1], x[2]) for x in ALL_ARGS]
HIGHEST_ARG_ID = max([m.id for m in ALL_ARGS])
