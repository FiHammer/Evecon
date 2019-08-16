import EveconLib.Tools.UsedPorts
import EveconLib.Tools.Browser
import EveconLib.Tools.Debugging

from EveconLib.Tools.Tools import *
from EveconLib.Tools.NonStaticTools import *
from EveconLib.Tools.EveconSpecific import *

from EveconLib.Tools.Timer import Timer
from EveconLib.Tools.GlobalMPports import GlobalMPports

import EveconLib.Tools.PCTools


if sys.platform == "win32" and False:
    import EveconLib.Tools.Windows
else: # sys.platform == "linux": # DUMMY WARE
    import EveconLib.Tools.WindowsDummy as Windows