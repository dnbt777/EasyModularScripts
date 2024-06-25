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
#### multicoder

Multicoder allows you to quickly create/edit multi-file projects with LLMs, all inside your terminal

It has (simple) local version control and frictionless commands to manage the state (for backups and managing multiple generations)

![image](https://github.com/dnbt777/EasyModularScripts/assets/169108635/ca748263-2be9-4c87-9858-504d2e0bf255)


It also has cost tracking so you know how much you're spending

![image](https://github.com/dnbt777/EasyModularScripts/assets/169108635/b4fa506a-5191-4911-8b7d-f7ff8ccb7804)

It creates a workspace for each project, and stores all progress in there, rather than in memory, so you can easily pickup where you left off on multiple projects.



 - `mc get [generation count] [glob match pattern] [-r]` : Have an LLM produce [response generation number] instances of changes to your project. Opens an nvim buffer where you type in your prompt (instructions OR paste an error in) (i to start typing, esc->:wq to save and submit). A system prompt, along with any files matching the glob pattern (-r for recursive) are automatically sent off with your prompt.
 - 
![image](https://github.com/dnbt777/EasyModularScripts/assets/169108635/f696f3b6-f979-48ae-ad35-659032edc409)


 - `mc write list` : Shows available LLM completions you can write
 - `mc write [n]` : Automatically creates/updates all files from an LLM completion
![image](https://github.com/dnbt777/EasyModularScripts/assets/169108635/edf8240b-dafa-4f98-8fe5-ad09ab12ddac)


- `mc ignore 'pattern'` : Always ignores files with this pattern (for this workspace). Config is in .mcoder-workspace/.mcignore.
- `mc rmignore 'pattern'` : Removes pattern from .mcignore.
- `mc lsignores` : Lists all patterns in .mcignore.

![image](https://github.com/dnbt777/EasyModularScripts/assets/169108635/812bb177-f134-43f4-b2e8-1e41ef74602d)



 - `mc undo` : Undoes writing a completion
 - `mc rollback` : rolls back to a previous version (may break bc i havent tested it enough)
 - `mc backup` : backs up the current dir to a .zip file in the workspace folder (may break, seemed to work ok but needs more thorough testing)

the idea is that you can use some of the ideas in this paper https://eureka-research.github.io/ to exponentially increase the odds of generating what you want.

additionally, LLMs are good at generating complex programs if you get there one step at a time. this program helps automate most of the friction in doing that.

to set it up, rename .env-example to .env and add relevant API keys in



#### old
 - `gmfp [filename pattern match]` : Get Multi-File Prompt turns multiple files into a prompt and auto copies to clipboard. e.g. `gmfp *` turns all files in cwd into 1 prompt
 - `gcb [n]`: Get Code Block gets the nth code block of a prompt in the clipboard. Default n is -1 (last codeblock)
 - `mkfiles [folder]`: If the clipboard contains an LLM response w multiple files, it creates them all, including dirs


### productivity stuff
 - `togglesite [domain or alias]` : blocks or unblocks a site in /etc/hosts, then restarts necessary services
![image](https://github.com/dnbt777/EasyModularScripts/assets/169108635/1421f191-810e-4af6-8ba6-1bf069de2e39)


### maintenance
 - `update-aliases` : updates aliases to modules. use after adding a new module. must manualy run `python3 update-aliases.py` on setup before you can use this.


### media stuff

- `videdit` : opens a simple video editor that cuts segments out of your videos. run it and go to http://127.0.0.1:5000.
![image](https://github.com/dnbt777/EasyModularScripts/assets/169108635/6df0cd57-8893-466a-b6ab-01eafe7c2d84)


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
