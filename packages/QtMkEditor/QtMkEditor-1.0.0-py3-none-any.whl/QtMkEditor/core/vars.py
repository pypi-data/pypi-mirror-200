import os



class Vars:
    
    abs_path = os.path.abspath(__file__).split('\\vars.py')[0]
    css_path = os.path.join(abs_path,'view\\style\\style.css')
    css_dir = os.path.join(abs_path,'view\\style')
    
    textArea = None
    view = None
    
    # QMarkdownEditor :
    MarkEditor = None
    
    # ToolBar :
    toolBar = None
    
    # MenuBar :
    MenuBar = None
    
    # Save Button :
    saveButton = None
    
    # cancel Button :
    cancelButton = None
    
    
    