"""

================================================================
Capsule - Qurry Data Structure Complex 

## Why Capsule?

- Mori
    There are many dedicated data structures for Qurry 🍛 
    If we say one of them like a tree in forest, 
    then all data structures combine, 
    it makes a forest or '森' read as mori in Japanese. 
    Definitely NOT because I'm a DeadBeat, 
    the fan of Hololive VTuber Mori Calliope, 
    and I didn't want to name something after her for a not short time.

- Hoshi
    I made it when I was listening the songs made by Hoshimachi Suisei, 
    a VTuber in Hololive. I was inspired by her songs, and I made this tool. 
    I named it Hoshi, which means star in Japanese. 
    I hope this tool can help you to make your code more beautiful.

    (Hint: The last sentence is auto-complete by Github Copilot from 'Hoshimachi' to the end. 
    That's meaning that Github Copilot knows VTuber, Hololive, even Suisei, 
    who trains it with such content and how. 
    "Does Skynet subscribe to Virtual Youtuber?")
    
- CapSule
    It's also not possible I named this for there is a song 
    called [Capsule](https://youtu.be/M85xU-tbQ6c?si=Ysk7pJu1eKIMOCBv)
    by Mori Calliope and Hoshimachi Suisei.
    I must be a coincidence. :3

================================================================
"""

from .jsonablize import parse as jsonablize, quickJSONExport, sort_hashable_ahead
from .quick import quickJSON, quickListCSV, quickRead
