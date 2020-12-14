from idlelib import EditorWindow
import Pyshell
import threading,sys
try:
    import Tkinter as tk #python 3.X
except ImportError:
    import Tkinter as tk #python 2
    import tkMessageBox as messagebox
    tk.messagebox = messagebox

class ThreadShell(PyShell.PyShell):
    """mostly copied from idlelib.PyShell module but adapted to work with threads"""
    #__adapted_by__ = "Tadhg McDonald-Jensen"
    def __init__(self, tk_root,target=None):
        #not sure exactly what the FileList object is for but it is required by the shell
        flist = PyShell.PyShellFileList(tk_root)
        super(ThreadShell,self).__init__(flist)

        #internal event flag for input, allows thread waiting for input to wait until a tk event handles it
        self.__input_flag = threading.Event()
        #target is stored and called in .run_command() which also deals with finishing the shell
        self.target = target
        self.thread = threading.Thread(target=self.run_command)
        #tk_root.after makes the .start method call when the program starts (after 0 miliseconds)
        tk_root.after(0,self.start)

    def start(self):
        """starts executing the Thread"""
        super(ThreadShell,self).beginexecuting()
        try:
            self.thread.start()
        except RuntimeError:
            self.executing = 0
            self.canceled = 0
            #self.top.quit() #this causes double deletion warnings with better Implementation of mainloop

    beginexecuting = start

    def run_command(self):
        """calls target from constructor with self as argument then cleans up shell"""
        if self.target:
            self.target(self)
        self.prompt_exit()
        self.executing = 0
        self.canceled = 0
        try:
            self.text.after(1,self.close)
        except RuntimeError:
            pass #tkinter has issues with changing threads so often after closing one shell others will throw this error

    def printf(self,*stuff,**kw):
        """works just like python 3.x print function but writes to shell's .stdout file"""
        if self.executing:
##            if USING_OLD_METHOD:       #Pretty sure this would do exact same thing
##                kw.setdefault("file",self.stdout)
##                print(*stuff,**kw), self.resetoutput()
##                return
            sep = kw.get("sep"," ")
            end = kw.get("end","\n")
            text = sep.join(stuff) + end
            self.stdout.write(text)
            self.resetoutput()

    def input(self,prompt="",timeout=None):
        """python 2 equivelent to raw_input or py 3+ input
Prompts user for input and freezes thread until input is given
Will return "" if .executing is False or it timed out from optional timeout argument"""
        if self.executing or self.closing:
            if prompt:
                self.stdout.write(prompt)
            self.__in_buffer = ""
            self.__input_flag.clear()
            self.reading=True
            self.__input_flag.wait(timeout)
            #input is inserted into .__in_buffer by other events
            #then set __input_flag so that it can be delivered to thread
            self.reading = False
            return self.__in_buffer.strip("\n")
        else:
            raise RuntimeError("cannot take input after finished")

    def prompt_exit(self):
        """writes press enter to quit" to the console colour then waits for input"""
        self.executing = False
        self.closing = True
        self.console.write("\n press enter to quit")
        self.input()

    def join_thread(self,timeout=None):
        """sets .executing label to False then waits to join thead,
returns True if thread finished or False if timeout activated"""
        self.executing = False
        self.closing = True
        if self.thread:
            self.thread.join(timeout)
        return not self.thread.is_alive()

    def _close(self):
        "Extend EditorWindow._close(), joins thread to close it"

        # Restore std streams
        sys.stdout = self.save_stdout
        sys.stderr = self.save_stderr
        sys.stdin = self.save_stdin
        # Break cycles
        self.interp = None
        self.console = None
        self.flist.pyshell = None
        self.history = None
        EditorWindow.EditorWindow._close(self)
        self.join_thread()

    def stop_readline(self):
        self.__in_buffer = ""
        self.__input_flag.set()

    def update_in(self):
        """updates input from user, I think some of the labels are probably unnecessary but it is easier to leave it alone"""
        line = self.text.get("iomark", "end-1c")
        if len(line) == 0:  # may be EOF if we quit our mainloop with Ctrl-C
            line = "\n"
        self.resetoutput()
        if self.canceled:
            self.canceled = 0
        if self.endoffile:
            self.endoffile = 0
            line = ""
        self.__in_buffer = line
        self.__input_flag.set()

    def cancel_callback(self, event=None):
        try:
            if self.text.compare("sel.first", "!=", "sel.last"):
                return # Active selection -- always use default binding
        except:
            pass
        if not (self.executing or self.reading):
            return "break"
        self.endoffile = 0
        self.canceled = 1
        if self.reading:
            self.update_in()
        return "break"

    def eof_callback(self, event):
        if self.executing and not self.reading:
            return # Let the default binding (delete next char) take over
        if not (self.text.compare("iomark", "==", "insert") and
                self.text.compare("insert", "==", "end-1c")):
            return # Let the default binding (delete next char) take over
        if not self.executing:
            self.resetoutput()
            self.close()
        else:
            self.canceled = 0
            self.endoffile = 1
            self.update_in()
        return "break"

    def enter_callback(self, event):
        """called when the enter/return key is pressed,
only the recursive self.top.mainloop() / self.top.quit() had to be changed for support"""
        # it is very long to copy/paste for the one line change, so I override the method temporarily
        save = self.top.quit
        self.top.quit = self.update_in
        super(ThreadShell,self).enter_callback(event)
        self.top.quit = save


#stupid module depends on this being set from the main function, so it needs to be done manually
PyShell.use_subprocess = True

#this defines the root tkinter window and sets it up
root = tk.Tk()
EditorWindow.fixwordbreaks(root)
root.withdraw()
#I need this to work on my mac, not sure if there are other OS specific stuff that should be included
try:
    from idlelib import macosxSupport
    macosxSupport.setupApp(root, None)
except (ImportError,AttributeError):
    pass





##!!!!!!!!!!!!!!!!!!!! And This Is The Part You Need To Worry About !!!!!!!!!!!!!!!!!!!!##


switch = threading.Event()
switch.clear()

def foo(shell):
    global x
    x = shell.input("enter a message: ")
    switch.set()
    shell.printf("message sent")

def foo2(shell):
    shell.printf("waiting for message...")
    while shell.executing and not switch.is_set():
        switch.wait(2)   # by using shell.executing in the loop it will occasionally check
                         # if the program should quit because the window was closed
    if shell.executing:
        shell.printf("message recieved: ",x)

shell1 = ThreadShell(root,foo)
shell2 = ThreadShell(root,foo2)
first_time = True
while shell1.executing or shell2.executing or first_time:
    first_time = False
    root.mainloop()
root.destroy()