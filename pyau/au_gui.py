#
# gui for an audiounit
# june 2010 - Simon Lemieux
#

try:
    import IPython
    IPython.Shell.hijack_tk()
except:
    pass

import Tkinter
Tkinter.Tk().withdraw() # hack

from Tkinter import *

class AutoScrollbar(Scrollbar):
    # from http://effbot.org/zone/tkinter-autoscrollbar.htm
    # a scrollbar that hides itself if it's not needed.  only
    # works if you use the grid geometry manager.
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            # grid_remove is currently missing from Tkinter!
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        Scrollbar.set(self, lo, hi)
    def pack(self, **kw):
        raise TclError, "cannot use pack with this widget"
    def place(self, **kw):
        raise TclError, "cannot use place with this widget"
        

def param_change_event_handler(event, param):
    param.value = event.widget.get()
    
def reset_change_event_handler(event, param):
    print 'reset'
    param.value = param.default_value


def launch_gui(au):
    """ Adds gui controls for the parameters of the audiounit `au`.
    """

    master = Tk()
    master.title(au.name)
    
    vscrollbar = AutoScrollbar(master)
    vscrollbar.grid(row=0, column=1, sticky=N+S)
    canvas = Canvas(master, yscrollcommand=vscrollbar.set)
    canvas.grid(row=0, column=0, sticky=N+S+E+W)
    
    vscrollbar.config(command=canvas.yview)
    # make the canva expandable
    master.grid_rowconfigure(0, weight=1)
    master.grid_columnconfigure(0, weight=1)
    
    frame = Frame(canvas, padx=6, pady=6)
    frame.rowconfigure(1, weight=1)
    frame.columnconfigure(1, weight=1)
    
    frame = Canvas(master)
#    frame.pack()
    for i,p in enumerate(au.get_parameters()):
        lbl_name = Label(frame, text=p.name)
        slider = Scale(frame, from_=p.range[0], to=p.range[1], orient=HORIZONTAL, resolution=(p.range[1]-p.range[0])/100.)
        slider.set(p.value)
        
        #txt_value = Entry(frame, text=p.value)
        #lbl_units = Label(frame, text=p.unit)
        #slider.bind('<ButtonRelease-1>', lambda event, param=p : param_change_event_handler(event, param))
        slider.bind('<B1-Motion>', lambda event, param=p : param_change_event_handler(event, param))
        slider.bind('d', lambda event, param=p : reset_change_event_handler(event, param))
        
        
        for j,w in enumerate([lbl_name, slider]):
            w.grid(row=i, column=j)        
            
    canvas.create_window(0, 0, anchor=NW, window=frame)
    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    
    master.mainloop()