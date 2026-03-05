Pixels, is a project I began on Febuary 19th, 2026. I found that whenever I was designing a user interface on OLEDs or LCDs I was continously making small changes,
and uploading to my microcontroller. This wastefullness of flash lifespan and time was getting redundent. So I began working on this project. It begen in c++ but quickly
switched to python as the windowed app libraries are more refined for use on MAC and windows. I will continue working through this set of files until I beleive
that it is a tool that can seemlesly be used.

The requirments are simple:
	
	* Python 3 installed
	
	* pygame installed
	
	* UI_BUILD.py, parse.py or build_pages.py installed (your choice)
	
	* diffscreens.py installed (display visualization)
Warning: I have not gone and tested every single possible combination of entries for every possible input. I have built safetys everywhere I could and if you find a sneaky bug, feel free to share so it may be fixed and this project can grow!

Parse.py is a simple, one-time graphics command viewer that allows for quick code dumps and simulations. Begin by entering desired screen width and height (On mac windows will be corner rounded and you will lose visuals), then pasting in the code block. Finish typing with "END" and the simulated UI will show. Most likely won't be updated as UI_BUILD grows.

UI_BUILD.py is a more rounded version of parse. It includes some simple display visuals, easier user communication and editable canvases plus a more dynamic codebase. Beware, I am still working towards ignoring drawn pixels outside of the round lcd. Pygame does not contain circle drawing surfaces, but ill continue trying until I find a way.

build_pages.py is the tool of all tools. It houses the editability and flexibility of a single screen, but expands it so you can work on multiple differents "pages". This vastly increases productivity and flips a new page in the next implementations of this project.

I will continue working on this project, adding and fixing until it is acceptable.
