# EasyModularScripts
makes unix workflow faster

easily add scripts/modules


<p align="center">
  <img src="https://github.com/dnbt777/EasyModularScripts/assets/169108635/2bd5dc2b-8df2-4731-b1f2-cf6104989f73" width="300" height="300">
</p>


## Modules included
### quick LLM tools
- `ask {prompt}`   : make gpt4o output an answer in as few chars as possible
- `runit` : runs the previous `ask` output as a command in the current working dir

![image](https://github.com/dnbt777/EasyModularScripts/assets/169108635/92efb799-aa89-4ee9-8a00-85689f7b911a)


### speed up coding w LLMs
 - `gmfp [filename pattern match]` : Get Multi-File Prompt turns multiple files into a prompt and auto copies to clipboard. e.g. `gmfp *` turns all files in cwd into 1 prompt
 - `gcb [n]`: Get Code Block gets the nth code block of a prompt in the clipboard. Default n is -1 (last codeblock)
 - `mkfiles [folder]`: If the clipboard contains an LLM response w multiple files, it creates them all, including dirs


### productivity stuff
 - `togglesite [domain or alias]` : blocks or unblocks a site in /etc/hosts, then restarts necessary services
![image](https://github.com/dnbt777/EasyModularScripts/assets/169108635/1421f191-810e-4af6-8ba6-1bf069de2e39)


### maintenance
 - `update-aliases` : updates aliases to modules. use after adding a new module. must manualy run `python3 update-aliases.py` on setup before you can use this.


### media stuff
- `zipmedia [media1.format] [media2.format] [output file name.output_format]` : returns a side-by-side of media1 and media2. works with video, images, or a combination of both. pads to the longest vid. requires ffmpeg.
![image](https://github.com/dnbt777/EasyModularScripts/assets/169108635/15fd08bc-cde5-4486-9b9c-c7dc60a71896)
![image](https://github.com/dnbt777/EasyModularScripts/assets/169108635/20723bbc-6ed7-4f28-91c5-1265f3e6d442)


![out2](https://github.com/dnbt777/EasyModularScripts/assets/169108635/0c2caa95-a1f5-47db-be31-3b92ff41dc8a)
![out](https://github.com/dnbt777/EasyModularScripts/assets/169108635/047a0f85-a334-4261-bdcb-b66634e9e7ba)
![out3](https://github.com/dnbt777/EasyModularScripts/assets/169108635/2e153b29-4688-4ce6-88b1-e1c28ff30e11)


## Setup
1. git clone this into your favorite location for scripts
2. run `python3 update-all.py` to add aliases to bashrc
3. rename the .env-example in ./ask-app to .env and put your openai key in there
4. run `pip install -r requirements.txt` to install requirements
5. install ffmpeg

## Adding your own
1. write the code
2. add an alias in alias_config.py
3. run `python3 update-all.py` to update/add new aliases in bashrc
