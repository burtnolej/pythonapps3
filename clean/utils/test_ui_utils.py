from Tkinter import *
from Tkinter import Button as Tkbutton
from Tkinter import Label as Tklabel
from ttk import *
from PIL import Image, ImageTk
from image_utils import ImageCreate, rgbstr_get

import tkFont
import unittest

sys.path.append("/home/burtnolej/Development/pythonapps/clean/utils")
from format_utils import *

from ui_utils import tk_create_config, tkfrm_cfg, \
     tk_create_frame, GridTableWidget, tk_label_get_image

def _dumpwgt2(wgt):
    
    attr = ['winfo_atom', 'winfo_atomname', 'winfo_cells', 'winfo_children', 'winfo_class', 'winfo_colormapfull', 'winfo_containing', 'winfo_depth', 'winfo_exists', 'winfo_fpixels', 'winfo_geometry', 'winfo_height', 'winfo_id', 'winfo_interps', 'winfo_ismapped', 'winfo_manager', 'winfo_name', 'winfo_parent', 'winfo_pathname', 'winfo_pixels', 'winfo_pointerx', 'winfo_pointerxy', 'winfo_pointery', 'winfo_reqheight', 'winfo_reqwidth', 'winfo_rgb', 'winfo_rootx', 'winfo_rooty', 'winfo_screen', 'winfo_screencells', 'winfo_screendepth', 'winfo_screenheight', 'winfo_screenmmheight', 'winfo_screenmmwidth', 'winfo_screenvisual', 'winfo_screenwidth', 'winfo_server', 'winfo_toplevel', 'winfo_viewable', 'winfo_visual', 'winfo_visualid', 'winfo_visualsavailable', 'winfo_vrootheight', 'winfo_vrootwidth', 'winfo_vrootx', 'winfo_vrooty', 'winfo_width', 'winfo_x', 'winfo_y']
    for a in attr:
        try:
            print a.ljust(20),getattr(wgt,a)()
        except TypeError:
            print a.ljust(20),'ERROR'
            pass
        
    for k,v in wgt.config().iteritems():
        print k.ljust(20),v[4]
    
def _dumpwgt(tk):
    #tk = getattr(wgt,'tk')
    for attr in dir(tk):
        if not callable(getattr(tk,attr)):
            print attr,getattr(tk,attr)
        else:
            try:
                print attr,getattr(tk,attr)()
            except TypeError:
                print attr,"error"
    
class TestUIRoot(unittest.TestCase):

    def setUp(self):
        self.master = Tk()
        
    def test_draw_configure_root(self):
        self.master.geometry('300x200+100+100')
        self.master.configure(background='red')
        self.assertEquals(self.master.winfo_class(),'Tk')
        
    def test_draw_configure_root_with_str(self):
        cfg = '300x200+100+100'
        self.master.geometry(cfg)
        self.master.configure(background='red')
        self.assertEquals(self.master.winfo_class(),'Tk')
        
    def test_draw_configure_root_with_badstr(self):
        cfg = '300x200+100+x'
        with self.assertRaises(TclError):
            self.master.geometry(cfg)
        
    def tearDown(self):
        self.master.destroy()
        
class TestUIFrame(unittest.TestCase):
    
    def setUp(self):
        self.master = Tk()
        self.master.geometry('300x200+100+100')
        self.master.configure(background='red')
        
    def test_draw_frame(self):
        self.frame = Frame(self.master)
        
        self.assertEquals(self.frame.widgetName,'ttk::frame')
        self.assertEquals(self.frame.children,{})
        self.assertEquals(self.frame.winfo_class(),'TFrame')
        
    def test_draw_frame_manual_config(self):
        self.frame = Frame(self.master,
                           height=290,
                           width=190)
        self.frame.grid(row=5,column=5)
        self.assertEquals(self.frame.config()['height'][4],290)
        self.assertEquals(self.frame.config()['width'][4],190)
        
    def test_draw_frame_with_style(self):
        _style = Style()
        _style.configure('mystyle.TFrame',background='blue')
        self.frame = Frame(self.master,style='mystyle.TFrame')
        self.frame.place(height=180,width=280,x=10,y=10)
        self.frame.config()
        self.assertEquals(self.frame.config()['style'][4],
                          'mystyle.TFrame')

    def tearDown(self):
        self.frame.destroy()
        self.master.destroy()
         
    '''def test_draw_frame_with_config(self):
        self.frame = Frame(self.master)
        
        frame_style = Style()
        
        tk_create_config(frame_style,tkfrm_cfg,'myframe')
        tk_create_frame(self.master,'myframe')'''
 
class TestUIPack(unittest.TestCase):
    def setUp(self):
        self.master = Tk()
        self.master.geometry('300x200+100+100')
        self.master.configure(background='red')
        _style = Style()
        _style.configure('mystyle.TFrame',background='blue')
        self.frame = Frame(self.master,style='mystyle.TFrame')
        self.frame.place(height=160,width=260,x=20,y=20)
        self.frame.config()
        
    def test_pack(self):
        self.frame.pack()
        button = Button(self.master,text="Button")
        button.pack(fill=BOTH, expand=1)
        
        #_dumpwgt2(self.frame)
        #self.master.mainloop()
        
    def test_pack_sidebyside(self):
        #self.frame.pack()
        button = Button(self.master,text="Button1")
        button.pack(side=LEFT, fill=BOTH,expand=1)
        button = Button(self.master,text="Button2")
        button.pack(side=LEFT, fill=BOTH,expand=1)        
        #_dumpwgt2(self.frame)
        #self.master.mainloop()
        
    def test_pack_ontop(self):
        #self.frame.pack()
        button = Button(self.master,text="Button1")
        button.pack(fill=BOTH,expand=1)
        button = Button(self.master,text="Button2")
        button.pack(fill=BOTH,expand=1)        
        #_dumpwgt2(self.frame)
        #self.master.mainloop()
        
    def test_pack_2x2_in_frame(self):
        #self.frame.pack()
        leftframe = Frame(self.frame)
        leftframe.pack(side=LEFT,fill=BOTH,expand=1)
        button = Button(leftframe,text="butinframe1.1")
        button.pack(fill=BOTH,expand=1)
        button = Button(leftframe,text="butinframe1.1")
        button.pack(fill=BOTH,expand=1)  
        rightframe = Frame(self.frame)
        rightframe.pack(side=LEFT,fill=BOTH,expand=1)
        button = Button(rightframe,text="butinframe1.2")
        button.pack(fill=BOTH,expand=1)
        button = Button(rightframe,text="butinframe1.2")
        button.pack(fill=BOTH,expand=1) 
        #_dumpwgt2(self.frame)
        self.master.mainloop()
                
    def test_pack_2x2(self):
        #self.frame.pack()
        leftframe = Frame(self.master)
        leftframe.pack(side=LEFT,fill=BOTH,expand=1)
        button = Button(leftframe,text="Button1.1")
        button.pack(fill=BOTH,expand=1)
        button = Button(leftframe,text="Button2.1")
        button.pack(fill=BOTH,expand=1)  
        rightframe = Frame(self.master)
        rightframe.pack(side=LEFT,fill=BOTH,expand=1)
        button = Button(rightframe,text="Button1.2")
        button.pack(fill=BOTH,expand=1)
        button = Button(rightframe,text="Button2.2")
        button.pack(fill=BOTH,expand=1) 
        #_dumpwgt2(self.frame)
        #self.master.mainloop()
        
    def test_pack_20x20(self):
        widgetgrid=[]
        for column in range(20):
            widgetcolumn=[]
            frame = Frame(self.master)
            frame.pack(side=LEFT,fill=BOTH,expand=1)
            for row in range(20):
                button = Button(frame,text=str(row)+"."+str(column))
                button.pack(fill=BOTH,expand=1)
                widgetcolumn.append(button)
            widgetgrid.append(widgetcolumn)

        self.assertEquals(widgetgrid[0][0].winfo_class(),'TButton')
        #_dumpwgt2(widgetgrid[19][19])
        #_dumpwgt2(widgetgrid[0][0])
        #self.master.mainloop()

    def tearDown(self):
        try: # not every test is creating a frame
            self.frame.destroy()
        except:
            pass
        
        self.master.destroy()
        
class TestUIButton(unittest.TestCase):
    def setUp(self):
        self.master = Tk()
        self.master.geometry('300x200+100+100')
        self.master.configure(background='red')
        _style = Style()
        _style.configure('mystyle.TFrame',background='blue')
        self.frame = Frame(self.master,style='mystyle.TFrame')
        self.frame.place(height=160,width=260,x=20,y=20)
        self.frame.config()
        
    def test_setgettext(self):
        
        def callback(button):
            ctext = button.cget("text")
            
            ntext = str(int(ctext) + 1)
            button.config(text=ntext)
            
        button = Button(self.master,text="0",command=lambda:callback(button))
        button.pack(fill=BOTH,expand=1)   
        
    def test_dimensions(self):
        button = Tkbutton(self.frame,text="dsds")
        button.config(height=5,width=5)
        button.pack(side=LEFT)   
        button = Tkbutton(self.frame,height = 1,width=4)
        button.pack(side=LEFT)    
        button = Tkbutton(self.frame,height = 3,width=10)
        button.pack(side=LEFT)    
        #self.master.mainloop()
        
    def test_colors(self):
        
        from random import randint

        def callback(button):

            r=randint(0,255)
            g=randint(0,255)
            b=randint(0,255)
            mycolor = '#%02x%02x%02x' % (r, g, b)
            button.config(bg=mycolor)
            button.config(text=mycolor)
        
        button = Tkbutton(self.frame,command=lambda:callback(button))
        button.pack(side=LEFT, fill=BOTH,expand=1)
        #self.master.mainloop()
        
    def test_font(self):
         
        font = tkFont.Font(family="Monospace", size=20)   
        # slant=tkFont.ITALIC
        # weight=tkFont.BOLD

        button = Tkbutton(self.frame,font=font,text='foobar')
        button.pack(side=LEFT, fill=BOTH,expand=1)
        #self.master.mainloop()
        
    def test_image(self):
        
        photo = PhotoImage(file="../scripts/buildgifs/8:30-9:10-270-68-68-rgb(97,91,92).gif")
        font = tkFont.Font(family="Monospace", size=20)   
        # slant=tkFont.ITALIC
        # weight=tkFont.BOLD

        mycolor = '#%02x%02x%02x' % (97, 91, 92) # #615b5c

        
        print mycolor
        self.master.grid()
        button = Tkbutton(self.master)
        button = Tklabel(self.master)
        button.config(image=photo,width="100",height="100",bg=mycolor)
        button.grid()
        #button.pack(side=LEFT, fill=BOTH,expand=1)
        self.master.mainloop()
        
    def tearDown(self):
        try: # not every test is creating a frame
            self.frame.destroy()
        except:
            pass
        
        self.master.destroy()
        
        
class TestUIEntry(unittest.TestCase):
    def setUp(self):
        self.master = Tk()
        self.master.geometry('300x200+100+100')
        self.master.configure(background='red')
        _style = Style()
        _style.configure('mystyle.TFrame',background='blue')
        self.frame = Frame(self.master,style='mystyle.TFrame')
        self.frame.place(height=160,width=260,x=20,y=20)
        self.frame.config()
        
    
    def test_addentry(self):
        entry = Entry(self.frame)
        entry.pack(fill=X,expand=1)
        entry = Entry(self.frame)
        entry.pack(fill=X,expand=1)
        entry = Entry(self.frame)
        entry.pack(fill=X,expand=1)
        #self.master.mainloop()
    
    def test_addentry_addtext(self):
        entry = Entry(self.frame)
        entry.pack(fill=X,expand=1)
        entry.insert(0,'default value')
        #self.master.mainloop()
        
    def test_addentry_add_delete_then_add(self):
        import time
        entry = Entry(self.frame)
        entry.pack(fill=X,expand=1)
        entry.insert(0,'default value')

        entry.delete(0,END)
        entry.insert(0,'another default value')
        
        #self.master.mainloop()
        
    def test_addentry_stringvar(self):
        
        def callback(v,y):
            v.set(y.get())
            
        v= StringVar()
        entry = Entry(self.frame, textvariable=v)
        entry.insert(0,'to be updated')
        entry.pack(fill=BOTH,expand=1)
        
        y= StringVar()
        entry = Entry(self.frame, textvariable=y)
        entry.insert(0,'input text here')
        entry.pack(fill=BOTH,expand=1)
        
        button = Button(self.frame,command=lambda:callback(v,y))
        button.pack(fill=BOTH,expand=1)
        #self.master.mainloop()
            
class TestUIGrid(unittest.TestCase):
    def setUp(self):
        self.master = Tk()
        self.master.geometry('300x200+100+100')
        self.master.configure(background='red')
        _style = Style()
        _style.configure('mystyle.TFrame',background='blue')
        self.frame = Frame(self.master,style='mystyle.TFrame')
        self.frame.place(height=160,width=260,x=20,y=20)
        self.frame.config()
        
    def test_add_grid(self):
        self.frame.grid(row=1,column=1)
        button = Button(self.master,text="NW")
        button.grid(row=1,column=1,sticky=NW) 
        button = Button(self.master,text="SW")
        button.grid(row=2,column=1,sticky=SW) 
        button = Button(self.master,text="NE")
        button.grid(row=1,column=2,sticky=NE)
        button = Button(self.master,text="SW")
        button.grid(row=3,column=3,sticky=SW)
        
        _dumpwgt2(self.frame)
        #self.master.mainloop()

    def tearDown(self):
        self.frame.destroy()
        self.master.destroy()

class TestUIWidgets(unittest.TestCase):
    def setUp(self):
        self.master = Tk()
        self.frame = Frame(self.master)
        self.frame.grid(row=2,column=2)

    def test_button(self):
        button = Button(self.frame,text="foobar")
        button.grid(row=1,column=1)   
        self.assertTrue(isinstance(self.frame.children[button._name],Button))
        
        self.assertEquals(button,'button')
        #_dumpwgt(button)
        #self.master.mainloop()

    def tearDown(self):
        self.master.destroy()
        
        
class TestUIInheritance(unittest.TestCase):
    
    class MyWgt(Frame):
        
        def __init__(self, master=None):
            _style = Style()
            _style.configure('mystyle.TFrame',background='blue')
            Frame.__init__(self, master,style='mystyle.TFrame')

            self.place(height=160,width=260,x=20,y=20)
            self.config()
            
    def setUp(self):
        self.master = Tk()
        self.master.geometry('300x200+100+100')
        self.master.configure(background='red')

    def test_(self):
        wgt = self.MyWgt(self.master)
        
        leftframe = Frame(wgt)
        leftframe.pack(side=LEFT,fill=BOTH,expand=1)
        button = Button(leftframe,text="butinframe1.1")
        button.pack(fill=BOTH,expand=1)
        button = Button(leftframe,text="butinframe1.1")
        button.pack(fill=BOTH,expand=1)  

        #self.master.mainloop()


class TestUITable(unittest.TestCase):

    class MyTblWgt(Frame):

        def __init__(self,master=None,width=5,height=5):
            _style = Style()
            _style.configure('mystyle.TFrame',background='blue')

            self.widgetgrid=[]
            # add on 1 for title row/column
            for column in range(width+1):
                widgetcolumn=[]
                frame = Frame(master)
                frame.pack(side=LEFT,fill=Y,expand=1,anchor='n')                  
                for row in range(height+1):
                    if row==0 and column==0:                        
                        button = Tkbutton(frame,text='',height=1,anchor='n')
                        button.pack(side=TOP)
                    elif row==0:
                        button = Tkbutton(frame,text='')
                        button.pack(fill=X)
                    elif column==0:
                        button = Tkbutton(frame,text='')
                        button.pack(fill=Y,expand=1)
                    else:
                        cellouterframe = Frame(frame,style='mystyle.TFrame')
                        cellouterframe.pack(fill=BOTH,expand=1,anchor='w')
                        
                        cellinnerframe = Frame(cellouterframe)
                        cellinnerframe.pack(side=LEFT,fill=BOTH,expand=1)
                        
                        topbutton=Tkbutton(cellinnerframe,width=50,height=2,text='')
                        topbutton.pack(fill=Y,expand=1,)
                        midbutton=Tkbutton(cellinnerframe,width=50,height=2,text='')
                        midbutton.pack(fill=Y,expand=1,)
                        botbutton=Tkbutton(cellinnerframe,width=50,height=2,text='')
                        botbutton.pack(fill=Y,expand=1,)
                    widgetcolumn.append(button)
                self.widgetgrid.append(widgetcolumn)
                
    def setUp(self):
        self.master = Tk()
        self.master.geometry('2200x1000+100+100')

    def test_create(self):
        wgt = self.MyTblWgt(self.master,5,5)
        for row in wgt.widgetgrid:
            for w in row:
                self.assertTrue(isinstance(w,Tkbutton))
        self.master.mainloop()
        
    '''def test_update(self):
        wgt = self.MyTblWgt(self.master,5,5)
        
        for row in wgt.widgetgrid:
            for w in row:
                self.assertTrue(isinstance(w,Tkbutton))
        self.master.mainloop()
        
    def test_controls(self):
        controlframe = Frame(self.master)
        controlframe.pack(side=RIGHT)          
        gridframe = Frame(self.master)
        gridframe.pack(side=LEFT,fill=BOTH,expand=1)        

        wgt = self.MyTblWgt(gridframe,5,5)
        
        for row in wgt.widgetgrid:
            for w in row:
                self.assertTrue(isinstance(w,Tkbutton))
                
   
        entry = Entry(controlframe)
        entry.pack(side=TOP)
        entry.insert(0,'default value')
        entry = Entry(controlframe)
        entry.pack(side=TOP)
        entry.insert(0,'default value')
        self.master.mainloop()       ''' 
     
class TestUIGridTableBasic(unittest.TestCase):
    

    def setUp(self):
        self.master = Tk()
        
    def test_create_small_dump_details(self):
        wgt = GridTableWidget(self.master,2,2)
        wgt.table_update_all_text('foobar')
        #font = tkFont.Font(family="Helvetica", size=16)
        #wgt.table_update_all_fonts(font)
        wgt.table_dump_info(wgt)
        wgt.table_dump_header_info()
        self.master.mainloop()
        
    
class TestUIGridTable(unittest.TestCase):

    def setUp(self):
        self.master = Tk()
        self.test_text = [[['david','',''],['brian','',''],['phil','',''],['bruce','',''],['peter','','']],
                [['basil','',''],['tim','',''],['gary','',''],['steve','',''],['paul','','']],
                [['val','',''],['nancy','',''],['grace','',''],['jane','',''],['jon','','']],
                [['turnip','',''],['potato','',''],['radisch','',''],['lettuce','',''],['beetroot','','']],
                [['bill','',''],['damian','',''],['barry','',''],['dave','',''],['luke','','']],
                [['jamie','',''],['larry','',''],['harry','',''],['george','',''],['matilda','','']],
                [['james','',''],['briece','',''],['bonny','',''],['sanjay','',''],['sachin','','']],
                [['graham','',''],['banana','',''],['pony','',''],['wellies','',''],['beans','','']]]

        
        #self.master.geometry('2200x1000+100+100')

    def test_create(self):
        wgt = GridTableWidget(self.master,5,8)
        
        self.assertEquals(len(wgt.widget),8)
        self.assertEquals(len(wgt.widget[0]),5)
        self.assertEquals(len(wgt.widget[0][0]),3)
        #self.master.mainloop()
        
        ''' 
        def test_update_text(self):
    
        
        wgt = GridTableWidget(self.master,5,8)   
        wgt.table_update_content(self.test_text)

        self.assertEquals(wgt.table_get_content(),text)'''

        
        ''' 
        def test_update_text(self):
    
        
        wgt = GridTableWidget(self.master,5,8)   
        wgt.table_update_content(self.test_text)

        self.assertEquals(wgt.table_get_content(),text)'''
        
    '''def test_init_datagrid(self):
        wgt = GridTableWidget(self.master,5,8) 
        exp_res = [[['','',''],['','',''],['','',''],['','',''],['','','']],
                   [['','',''],['','',''],['','',''],['','',''],['','','']],
                   [['','',''],['','',''],['','',''],['','',''],['','','']],
                   [['','',''],['','',''],['','',''],['','',''],['','','']],
                   [['','',''],['','',''],['','',''],['','',''],['','','']],
                   [['','',''],['','',''],['','',''],['','',''],['','','']],
                   [['','',''],['','',''],['','',''],['','',''],['','','']],
                   [['','',''],['','',''],['','',''],['','',''],['','','']]]
        
        self.assertEquals(wgt._init_datagrid(),exp_res)'''
        
    '''def test_update_color(self):
        wgt = GridTableWidget(self.master,5,8)
        wgt.table_update_content(self.test_text)
        colors = wgt._init_datagrid()
        colors[0][0][0] = whiteblack14i
        colors[1][0][0] = burgundywhite18
        colors[7][3][0] = yellowburgundy14
        wgt.table_update_colors(colors)

    def test_update_text(self):
        wgt = GridTableWidget(self.master,5,8)
        wgt.table_update_content(self.test_text)

        self.assertEquals(wgt.table_get_content(),self.test_text)
        
    def test_update_font(self):
        wgt = GridTableWidget(self.master,5,8)
        wgt.table_update_content(self.test_text)
        
        mono20 = tkFont.Font(family="Monospace", size=20)
        mono10 = tkFont.Font(family="Monospace", size=8)
        #mono15b = tkFont.Font(family="Monospace", size=8,weight=tkFont.BOLD)
        #mono20i = tkFont.Font(family="Monospace", size=8,slant=tkFont.ITALIC)
        
        fonts = wgt._init_datagrid()
        fonts[0][0][0] = mono20
        #fonts[1][0][0] = mono10
        #fonts[7][3][0] = mono15b
        #fonts[7][4][0] = mono20i
        wgt.table_update_font(fonts)
        
    def test_update_all_font(self):
        helv36 = tkFont.Font(family="Helvetica", size=18)
        wgt = GridTableWidget(self.master,5,8)
        wgt.table_update_all_text('foobar')
        wgt.table_update_all_fonts(helv36)
        self.master.mainloop()
        
    def test_update_all_text(self):
        wgt = GridTableWidget(self.master,5,8)
        wgt.table_update_all_text('foobar')
        self.master.mainloop()'''
        
    '''def test_update_top_label_text(self):
        wgt = GridTableWidget(self.master,5,8)
        
        helv36 = tkFont.Font(family="Helvetica", size=18)
        wgt.table_update_all_fonts(helv36)
        labels = ['Monday','Tuesday','Wednesday','Thursday','Friday']
        for i in range(len(labels)):
            
            wgt.columnheaderwidget[i].config(text=labels[i])
            wgt.columnheaderwidget[i].config(font=helv36)     
        self.master.mainloop()'''
        
    def test_update_top_label_image(self):
        
        fontfamily = "Helvetica"
        fontsize=12
        tkrgb = '#%02x%02x%02x' % (214, 210, 208)
        
        photo = PhotoImage(file="/tmp/foobar.gif")
        wgt = GridTableWidget(self.master,5,8)
        #font = tkFont.Font(family=fontfamily, size=fontsize)
        #wgt.table_update_all_fonts(font)
        wgt.table_update_all_text('foobar')

        rowheaderimages=[]
        labels = ['Monday','Tuesday','Wednesday','Thursday','Friday']
        for i in range(len(labels)):
            
            rowheaderimages.append(tk_label_get_image(wgt.columnheaderwidget[i],
                                       labels[i],
                                       pointsize=fontsize,
                                       font=fontfamily,
                                       background=tkrgb,
                                       gravity='center'))
            
        for i in range(len(rowheaderimages)):
            
            wgt.columnheaderwidget[i].config(image=rowheaderimages[i])
            #wgt.columnheaderwidget[i].config(width=206,height=21)
            #wgt.columnheaderwidget[i].update_idletasks()

        
        colheaderimages=[]
        labels = ['0830-915','0915-1000','1000-1045','1045-1130',
                  '1130-1215','1215-1300','1300-1345','1345-1430']
        for i in range(len(labels)):
            
            colheaderimages.append(tk_label_get_image(wgt.rowheaderwidget[i],
                                       labels[i],
                                       pointsize=fontsize,
                                       font=fontfamily,
                                       background=tkrgb,
                                       rotate=90,
                                       gravity='center'))
            
        for i in range(len(colheaderimages)):
            #wgt.rowheaderwidget[i].config(image=photo)
            wgt.rowheaderwidget[i].config(image=colheaderimages[i])
            
            #wgt.rowheaderwidget[i].config(width=12,height=79)
            #wgt.rowheaderwidget[i].update_idletasks()
        self.master.mainloop()

    def tearDown(self):
        self.master.destroy()
        
        
class TestUILabel(unittest.TestCase):
    def setUp(self):
        self.master = Tk()
        #self.master.geometry('300x200+100+100')
        #self.master.configure(background='red')
        #_style = Style()
        #_style.configure('mystyle.TFrame',background='blue')
        #self.frame = Frame(self.master,style='mystyle.TFrame')
        #self.frame.place(height=160,width=260,x=20,y=20)
        #self.frame.config()
        
    def test_drawlabel(self):
        
        lbl = Tklabel(self.master,text='text')
        lbl.pack(fill=BOTH,expand=1)
        #self.master.mainloop()
        self.master.update_idletasks()
        
        #self.assertEquals(lbl.winfo_width(),28)
        #self.assertEquals(lbl.winfo_height(),28)
        
    def test_drawbiggerlabel(self):
        
        lbl = Tklabel(self.master,text='text',width=10,height=10)
        lbl.pack(fill=BOTH,expand=1)

        self.master.update_idletasks()
        #self.master.mainloop()
        
        #self.assertEquals(lbl.winfo_width(),154)
        #self.assertEquals(lbl.winfo_height(),154)
    
    def test_drawlabel_font(self):
        
        self.master.geometry('500x500+10+10')
        font = tkFont.Font(family="Monospace", size=20)  
        lbl = Tklabel(self.master,text='text', font=font)
        lbl.pack(fill=BOTH,expand=1)

        #self.master.mainloop()
        
        #self.master.update_idletasks()
        #self.master.mainloop()
        
        #self.assertEquals(lbl.winfo_width(),154)
        #self.assertEquals(lbl.winfo_height(),154)
        
        
    def test_draw_expand(self):

        _style = Style()
        _style.configure('mystyle.TFrame',background='blue')
        self.frame = Frame(self.master,style='mystyle.TFrame')
        self.frame.place(height=500,width=500,x=20,y=20)
        self.frame.config()
        
        self.master.update_idletasks()
        lbl = Tklabel(self.frame,text='text')
        lbl.pack(fill=BOTH,expand=1)  

        self.frame.update_idletasks()
        
        self.assertEquals(lbl.winfo_width(),500)
        self.assertEquals(lbl.winfo_height(),500)
        
    def test_draw_expand_image(self):
        self.master.geometry('500x500+10+10')
        
        _style = Style()
        _style.configure('mystyle.TFrame',background='blue')
        self.frame = Frame(self.master,style='mystyle.TFrame')
        self.frame.pack(fill=BOTH,expand=1)

        lbl = Tklabel(self.frame,text='text')
        lbl.pack(fill=BOTH,expand=1)  

        self.frame.update_idletasks()
        
        w = lbl.winfo_width()
        h = lbl.winfo_height()

        geom = "{0}x{1}".format(w,h)
        ic = ImageCreate()
        outputfiles = ic.create_image_file('label image',
                             pointsize=64,
                             size=geom,
                             gravity='center')
        
        
        photo = PhotoImage(file=outputfiles[0])
        lbl.config(image=photo)
  
    def test_draw_expand_image_rotate(self):
        self.master.geometry('500x500+10+10')
        
        _style = Style()
        _style.configure('mystyle.TFrame',background='blue')
        self.frame = Frame(self.master,style='mystyle.TFrame')
        self.frame.pack(fill=BOTH,expand=1)

        lbl = Tklabel(self.frame,text='text')
        lbl.pack(fill=BOTH,expand=1)  

        photo = tk_label_get_image(lbl,'text',rotate=90)

        lbl.config(image=photo)
        
    def test_draw_expand_image_2labels(self):
        self.master.geometry('500x500+10+10')
        
        fontfamily = "Helvetica"
        fontsize=48
        tkrgb = '#%02x%02x%02x' % (214, 210, 208)

        _style = Style()
        _style.configure('mystyle.TFrame',background='blue')
        self.frame = Frame(self.master,style='mystyle.TFrame')
        self.frame.pack(fill=BOTH,expand=1)

        lbl = Tklabel(self.frame)
        lbl.place( width=500,height=250,x=0,y=0)

        font = tkFont.Font(family=fontfamily, size=fontsize)  
        lbl2 = Tklabel(self.frame,text='label text',font=font,background=tkrgb)
        lbl2.place( width=500,height=250,x=0,y=250)

        photo = tk_label_get_image(lbl,
                                   'label image',
                                   pointsize=fontsize,
                                   font=fontfamily,
                                   background=tkrgb,
                                   gravity='center')
        lbl.config(image=photo)
        
    def test_draw_expand_image_2labels_both_images(self):
        self.master.geometry('500x500+10+10')
        
        fontfamily = "Helvetica"
        fontsize=48
        tkrgb = '#%02x%02x%02x' % (214, 210, 208)

        _style = Style()
        _style.configure('mystyle.TFrame',background='blue')
        self.frame = Frame(self.master,style='mystyle.TFrame')
        self.frame.pack(fill=BOTH,expand=1)

        lbl = Tklabel(self.frame)
        lbl.place( width=500,height=250,x=0,y=0)

        lbl2 = Tklabel(self.frame)
        lbl2.place( width=500,height=250,x=0,y=250)

        photo = tk_label_get_image(lbl,
                                   'label image',
                                   pointsize=fontsize,
                                   font=fontfamily,
                                   background=tkrgb,
                                   gravity='center')
        lbl.config(image=photo)
        
        photo2 = tk_label_get_image(lbl2,
                                   'label image2',
                                   pointsize=fontsize,
                                   font=fontfamily,
                                   background=tkrgb,
                                   gravity='center')
        lbl2.config(image=photo2)
        
        self.master.mainloop()
        
    def tearDown(self):
        self.master.destroy()
        

if __name__ == "__main__":

    suite = unittest.TestSuite()
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIRoot))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIFrame))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIGrid))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIPack))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIEntry))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIWidgets))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIInheritance))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUITable))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIButton))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIGridTable))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIGridTableBasic))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUILabel))
    
    
    
    unittest.TextTestRunner(verbosity=2).run(suite)
