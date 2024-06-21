import os

current_dir = os.path.dirname(os.path.abspath(__file__))

easy_modular_scripts_dir = current_dir

aliases = {
    # ask-app
    "ask": f"python3 {current_dir}/ask-app/ask.py",
    "runit": f"bash {current_dir}/ask-app/runit.sh",

    # content creation-tools
    "mts-zipvids": f"python3 {current_dir}/media-tools/zipmedia.py",
    "zipvids": f"mts-zipvids",
    "zipmedia": f"mts-zipvids",

    "md2doc":f"python3 {current_dir}/media-tools/markdown_from_clipboard_to_docx.py",
    "mdtodoc":f"md2doc",
    "md2pdf":f"python3 {current_dir}/media-tools/markdown_from_clipboard_to_pdf.py",

    # ai tools
    "gmfp": f"bash {current_dir}/ai-tools/get_multifile_prompt.sh", # get multifile prompt
    "cb": f"python3 {current_dir}/ai-tools/copy_codeblock_n.py", # copy codeblock n - usage: cb 0 or cb -2 or cb (default -1))
    "gcb":"cb",
    "getcb":"cb",
    "mkfiles":f"python3 {current_dir}/ai-tools/make_multifile.py", # takes clipboard and makes the multifile project
    
    # productivity stuff
    "togglesite": f"sudo python3 {current_dir}/productivity-tools/toggle_site_blocking.py", # toggles blocking a site. `togglesite [website]`. has aliases too. `togglesite x` blocks twitter/x.com. see /prod-tools/site_aliases.cfg


    # meta stuff
    "update-aliases":f"python3 {current_dir}/update-all.py;exec bash",
    "emsupdate":f"update-aliases",


    # git stuff
    "gitclone":f"bash {current_dir}/git/gitclone.sh", # gitclones using ssh an dcurrently logged in user
    "gitpushall":f"bash {current_dir}/git/gitpushall.sh", # usage: gitpushall msg -> adds . commits w msg and pushes
    "gpa":"gitpushall",

    # Add more aliases as needed
    # "alias_name": "command",
}
