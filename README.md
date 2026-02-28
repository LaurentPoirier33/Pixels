Pixels, is a project I began on Febuary 19th, 2026. I found that whenever I was designing a user interface on OLEDs or LCDs I was continously making small changes,
and uploading to my microcontroller. This wastefullness of flash lifespan and time was getting redundent. So I began working on this project. It begen in c++ but quickly
switched to python as the windowed app libraries are more refined for use on MAC and windows. I will continue working through this set of files until I beleive
that it is a tool that can seemlesly be used.

Parse.py is a simple, one-time graphics command viewer that allows for quick code dumps and simulations. Begin by entering desired screen width and height (On mac windows will be corner rounded and you will lose visuals), then pasting in the code block. Finish typing with "END" and the simulated UI will show. Most likely won't be updated as UI_BUILD grows.

UI_BUILD.py is a more rounded version of parse. It includes some simple lcd visuals, easier user communication and editable canvases plus a more dynamic codebase.
