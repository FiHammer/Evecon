import EveconLib.Tools.UsedPorts
import EveconLib.Tools.Browser
import EveconLib.Tools.Debugging

from EveconLib.Tools.Tools import *
from EveconLib.Tools.NonStaticTools import *
from EveconLib.Tools.EveconSpecific import *

from EveconLib.Tools.Timer import Timer
from EveconLib.Tools.GlobalMPports import GlobalMPports

import EveconLib.Tools.PCTools


if sys.platform == "win32":
    import EveconLib.Tools.Windows
else: # sys.platform == "linux": # DUMMY WARE
    if EveconLib.Config.suppressErros:
        print("Platform not supported! Now using a dummy for some functions. Crashes are coming!")
    import EveconLib.Tools.WindowsDummy as Windows