import EveconLib.Tools.UsedPorts
import EveconLib.Tools.Browser

from EveconLib.Tools.Tools import *
from EveconLib.Tools.NonStaticTools import *
from EveconLib.Tools.EveconSpecific import *

from EveconLib.Tools.Timer import Timer
from EveconLib.Tools.GlobalMPports import GlobalMPports

import EveconLib.Tools.PCTools

from EveconLib.Tools.MPlayer import MPlayer
from EveconLib.Tools.SZip import SZip

if sys.platform == "win32":
    import EveconLib.Tools.Windows
elif sys.platform == "linux": # DUMMY WARE
    import EveconLib.Tools.WindowsDummy