# EasyModularScripts
Tools to help me easily add scripts to make my unix workflow faster

<p align="center">
  <img src="https://github.com/dnbt777/EasyModularScripts/assets/169108635/2bd5dc2b-8df2-4731-b1f2-cf6104989f73" width="300" height="300">
</p>


## Scripts included
- `ask`   : make gpt4o output an answer in as few chars as possible
- `runit` : runs the previous `ask` output as a command in the current working dir

![image](https://github.com/dnbt777/EasyModularScripts/assets/169108635/92efb799-aa89-4ee9-8a00-85689f7b911a)


## Setup
1. git clone this into your favorite location for scripts
2. run `python3 update-all.py` to add aliases to bashrc
3. rename the .env-example in ./ask-app to .env and put your openai key in there
4. use `ask` to ask gpt4o a quick question in no-yappin mode (quick short output)
5. use `runit` to run the last output of `ask` if it was a command

## Adding your own
1. write the code
2. add an alias in alias_config.py
3. run `python3 update-all.py` to update/add new aliases in bashrc
