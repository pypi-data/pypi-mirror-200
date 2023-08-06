import sys, os

def clip(content, no_os_error = False):
    if sys.platform == "win32":
        try:
            os.system(f'echo {content} | clip')
            return 
        except Exception as e: raise e
    elif no_os_error == False:
        raise OSError("Currently only win32 systems are supported!")