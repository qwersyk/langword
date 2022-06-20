import gi
import sys
import os
import random
import os.path, json
from datetime import datetime,timedelta
from urllib.parse import urlparse


gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw,Gio

#F-function
#H-Home
#N-New
#R-Repet


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(380, 720)

        self.Aplication=Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_child(self.Aplication)

        with open('dictionary.json') as f:
            self.dictionary = json.load(f)
        with open('repeated_words.json') as f:
            self.repeated_words = json.load(f)
        
        self.FBar()
        self.FHome()
        self.FNew()
        self.FRepet()
        
    def FBar(self):
        self.HeaderBar=Adw.HeaderBar()
        self.set_titlebar(self.HeaderBar)
        
        self.ToastOverlay=Adw.ToastOverlay()
        self.MainStack=Adw.ViewStack(vexpand=True)
        self.ToastOverlay.set_child(self.MainStack)
        
        self.Hbin=Adw.Bin()
        self.Hbox=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,halign=Gtk.Align.CENTER)
        self.Hbin.set_child(self.Hbox)
        self.Nbox=Gtk.Box()
        self.Rbox=Gtk.Box()
        
        self.MainStack.add_titled(self.Hbin,"Home","Главная")
        self.MainStack.add_titled(self.Nbox,"NewWords","Новые слова")
        self.MainStack.add_titled(self.Rbox,"RepetitionWords","Повторение слов")
        self.Aplication.append(self.ToastOverlay)

        self.SwitcherTitle=Adw.ViewSwitcherTitle()
        self.SwitcherTitle.set_stack(self.MainStack)
        self.SwitcherTitle.set_title("LangWord")
        self.HeaderBar.set_title_widget(self.SwitcherTitle)
        
        self.SwitcherBar=Adw.ViewSwitcherBar()
        self.SwitcherBar.set_stack(self.MainStack)
        self.SwitcherBar.set_reveal(True)
        self.Aplication.append(self.SwitcherBar)
        
        self.FMenu()

        self.SwitcherTitle.connect("notify::title-visible",self.FReloadBar)
        self.FReloadBar()
        
    def FHome(self):
        self.HRbox=Gtk.ListBox(css_classes=["boxed-list"],margin_top=20,margin_start=20,margin_bottom=20,margin_end=20,valign=Gtk.Align.START,halign=Gtk.Align.FILL,hexpand=True,selection_mode=Gtk.SelectionMode.NONE)
        self.HRbox.append(Gtk.Label(label="Слова на повторение",margin_top=10,margin_start=10,margin_bottom=10,margin_end=10,css_classes=["title-2"]))
        for index in range(min(5,len(self.repeated_words))):
            self.HRbox.append(Gtk.Label(label=list(self.repeated_words)[index],margin_top=10,margin_start=10,margin_bottom=10,margin_end=10))
        if not self.repeated_words:
            self.HRbox.append(Gtk.Label(label="Тут пока пусто",hexpand=True,css_classes=["warning"],margin_top=10,margin_start=10,margin_bottom=10,margin_end=10))
        self.HNbox=Gtk.ListBox(css_classes=["boxed-list"],margin_top=20,margin_start=20,margin_bottom=20,margin_end=20,valign=Gtk.Align.START,halign=Gtk.Align.FILL,hexpand=True,selection_mode=Gtk.SelectionMode.NONE)
        self.HNbox.append(Gtk.Label(label="Новые слова",margin_top=10,margin_start=10,margin_bottom=10,margin_end=10,css_classes=["title-2"]))
        for index in range(min(5,len(self.dictionary))):
            self.HNbox.append(Gtk.Label(label=list(self.dictionary)[index],margin_top=10,margin_start=10,margin_bottom=10,margin_end=10))
        if not self.dictionary:
            self.HNbox.append(Gtk.Label(label="Тут пока пусто",hexpand=True,css_classes=["warning"],margin_top=10,margin_start=10,margin_bottom=10,margin_end=10))
        self.Hbox.append(self.HRbox)
        self.Hbox.append(self.HNbox)
        
    def FNew(self):
        self.Nstack = Gtk.Stack()
        self.Nstack.set_transition_type(Gtk.StackTransitionType.SLIDE_UP_DOWN)
        self.Nstack.set_transition_duration(500)
        self.Nbox.append(self.Nstack)
        self.Nleaflet=Adw.Leaflet()
        self.FNReload()
    


    def FRepet(self):
        self.Rstack = Gtk.Stack()
        self.Rstack.set_transition_type(Gtk.StackTransitionType.SLIDE_UP_DOWN)
        self.Rstack.set_transition_duration(500)
        self.Rbox.append(self.Rstack)
        self.Rleaflet=Adw.Leaflet()
        self.FRReload()

    def FMenu(self):
        _=Gio.SimpleAction.new("about", None)
        _.connect("activate", self.FAbout)
        self.add_action(_)
        _=Gio.SimpleAction.new("add_dictionary", None)
        _.connect("activate", self.FAddDictionary)
        self.add_action(_)
        _=Gio.SimpleAction.new("reload_new_words", None)
        _.connect("activate", self.FNReload)
        self.add_action(_)
        
        menu = Gio.Menu.new()
        menu.append("Reload new words", "win.reload_new_words")
        menu.append("Add dictionary", "win.add_dictionary")
        menu.append("About", "win.about")
        
        self.popover = Gtk.PopoverMenu()
        self.popover.set_menu_model(menu)

        self.hamburger = Gtk.MenuButton()
        self.hamburger.set_popover(self.popover)
        self.hamburger.set_icon_name("open-menu-symbolic")
        
        self.HeaderBar.pack_end(self.hamburger)
    
    def FAddDictionary(self,*data):
        self.adddictionary = Gtk.FileChooserNative()
        self.adddictionary.set_transient_for(self)
        self.adddictionary.set_modal(self)
        self.adddictionary.connect("response",self.FOpenFile)
        _=Gtk.FileFilter()
        _.set_name("json")
        _.add_pattern("*.json")
        self.adddictionary.add_filter(_)
        self.adddictionary.show()
    def FOpenFile(self,*data):
        if(data[0].get_file()!=None):
            with open(urlparse(data[0].get_file().get_uri()).path) as f:
                file = json.load(f)
                for i in file:
                    if not((type(file[i])==type({})) and "translation" in file[i] and "option1" in file[i] and "option2" in file[i] and "option3" in file[i]):
                        _=Adw.Toast()
                        _.set_title("Error.Файл неправильный или повреждён.")
                        self.ToastOverlay.add_toast(_)
                        break
                else:
                    self.dictionary=self.dictionary|file
                    
                    with open('dictionary.json',"w") as f:
                        json.dump(self.dictionary,f)
                    _=Adw.Toast()
                    _.set_title("Успешно добавлено "+str(len(file))+" слов!")
                    self.ToastOverlay.add_toast(_)
    def FNSwipeCheck(self,*data):
        if not(self.Nleaflet.get_child_transition_running()) and self.Nleaflet.get_visible_child().get_name()!="centerbox":
            if self.Nleaflet.get_visible_child().get_name()=="leftbox":
                self.repeated_words[self.Nleaflet.get_name()]=self.dictionary[self.Nleaflet.get_name()]|{"time":str(datetime.today().strftime("%Y-%m-%d %H:%M:%S")),"repetitions":0}
                with open('repeated_words.json',"w") as f:
                    json.dump(self.repeated_words,f)
                self.dictionary.pop(self.Nleaflet.get_name())
                with open('dictionary.json',"w") as f:
                    json.dump(self.dictionary,f)
            self.FNReload()

    def FNTouchCheck(self,*data):
        if self.Nleaflet.get_visible_child().get_name()=="rightbox":
            self.Nleaflet.set_transition_type(Adw.LeafletTransitionType.UNDER)
        elif self.Nleaflet.get_visible_child().get_name()=="leftbox":
            self.Nleaflet.set_transition_type(Adw.LeafletTransitionType.OVER)

    def FNReload(self,*data):
        if(self.dictionary):
            trash=self.Nleaflet

            self.Nleaflet=Adw.Leaflet(fold_threshold_policy=True,can_navigate_back=True,can_navigate_forward=True,can_unfold=False)
            NWword=(random.choice(list(self.dictionary)))
            self.Nleaflet.set_name(NWword)
            self.Nstack.add_child(self.Nleaflet)
            self.Nstack.set_visible_child(self.Nleaflet)

            Nleftbox=Gtk.Box(name="leftbox")
            Nleftbox.append(Gtk.Label(label="Учить"))

            Ncenterbox=Gtk.Box(name="centerbox")
            NWLabel=Gtk.Label(label=str(self.dictionary[NWword]["translation"])+"\n"+str(NWword),hexpand=True,css_classes=["large-title"])
            NWButton=Gtk.Button(label=str(self.dictionary[NWword]["translation"]),hexpand=True,css_classes=["large-title","flat"])
            NWButton.connect("clicked",self.FNResponseDisclosure,Ncenterbox,NWLabel)
            Ncenterbox.append(NWButton)

            Nrightbox=Gtk.Box(name="rightbox")
            Nrightbox.append(Gtk.Label(label="Напомнить позже",xalign=1,hexpand=True))

            self.Nleaflet.append(Nleftbox)
            self.Nleaflet.append(Ncenterbox)
            self.Nleaflet.append(Nrightbox)

            self.Nleaflet.set_visible_child(Ncenterbox)
            self.Nstack.remove(trash)

            self.Nleaflet.connect("notify::child-transition-running",self.FNSwipeCheck)
            self.Nleaflet.connect("notify::visible-child",self.FNTouchCheck)

        else:
            trash=self.Nleaflet
            self.Nleaflet=Adw.Leaflet()
            self.Nleaflet.append(Gtk.Label(label="Тут пока пусто",hexpand=True,css_classes=["warning","large-title"]))
            self.Nstack.add_child(self.Nleaflet)
            self.Nstack.set_visible_child(self.Nleaflet)
            self.Nstack.remove(trash)

    def FRSwipeCheck(self,*data):
        if not(self.Rleaflet.get_child_transition_running()) and self.Rleaflet.get_visible_child().get_name()!="centerbox":
            if self.Rleaflet.get_visible_child().get_name()=="leftbox":
                if self.repeated_words[self.Rleaflet.get_name()]["repetitions"]==0:
                    self.repeated_words[self.Rleaflet.get_name()]["time"]=(datetime.now() + timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M:%S")
                elif self.repeated_words[self.Rleaflet.get_name()]["repetitions"]==1:
                    self.repeated_words[self.Rleaflet.get_name()]["time"]=(datetime.now() + timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S")
                elif self.repeated_words[self.Rleaflet.get_name()]["repetitions"]==2:
                    self.repeated_words[self.Rleaflet.get_name()]["time"]=(datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
                elif self.repeated_words[self.Rleaflet.get_name()]["repetitions"]==3:
                    self.repeated_words[self.Rleaflet.get_name()]["time"]=(datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S")
                elif self.repeated_words[self.Rleaflet.get_name()]["repetitions"]==4:
                    self.repeated_words[self.Rleaflet.get_name()]["time"]=(datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
                elif self.repeated_words[self.Rleaflet.get_name()]["repetitions"]==5:
                    self.repeated_words[self.Rleaflet.get_name()]["time"]=(datetime.now() + timedelta(days=21)).strftime("%Y-%m-%d %H:%M:%S")
                elif self.repeated_words[self.Rleaflet.get_name()]["repetitions"]==6:
                    self.repeated_words[self.Rleaflet.get_name()]["time"]=(datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d %H:%M:%S")
                elif self.repeated_words[self.Rleaflet.get_name()]["repetitions"]==7:
                    self.repeated_words[self.Rleaflet.get_name()]["time"]=(datetime.now() + timedelta(days=180)).strftime("%Y-%m-%d %H:%M:%S")
                else:
                    self.repeated_words[self.Rleaflet.get_name()]["time"]=(datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d %H:%M:%S")
                self.repeated_words[self.Rleaflet.get_name()]["repetitions"]+=1
                with open('repeated_words.json',"w") as f:
                    json.dump(self.repeated_words,f)
            elif self.Rleaflet.get_visible_child().get_name()=="rightbox":
                self.repeated_words[self.Rleaflet.get_name()]["time"]=(datetime.now() + timedelta(seconds=30)).strftime("%Y-%m-%d %H:%M:%S")
                with open('repeated_words.json',"w") as f:
                    json.dump(self.repeated_words,f)
            self.FRReload()

    def FRTouchCheck(self,*data):
        if self.Rleaflet.get_visible_child().get_name()[0]=="r":
            self.Rleaflet.set_transition_type(Adw.LeafletTransitionType.UNDER)
        elif self.Rleaflet.get_visible_child().get_name()[0]=="l":
            self.Rleaflet.set_transition_type(Adw.LeafletTransitionType.OVER)

    def FRResponseDisclosure(self,*data):
        if data[1]:
            data[0].add_css_class("suggested-action")
        else:
            data[0].add_css_class("destructive-action")

    def FRReload(self):
        datenow=datetime.today()
        for RWword in self.repeated_words:
            if(datetime.strptime(self.repeated_words[RWword]["time"], "%Y-%m-%d %H:%M:%S")<datenow):
                trash=self.Rleaflet

                self.Rleaflet=Adw.Leaflet(fold_threshold_policy=True,can_navigate_back=True,can_navigate_forward=True,can_unfold=False)
                self.Rleaflet.set_name(RWword)
                self.Rstack.add_child(self.Rleaflet)
                self.Rstack.set_visible_child(self.Rleaflet)

                Rleftbox=Gtk.Box(name="leftbox")
                Rleftbox.append(Gtk.Label(label="Вспмнил"))

                Rbutton1 = Gtk.Button(label=RWword,margin_top=10,margin_start=10,margin_bottom=10,margin_end=10,css_classes=["large-title"])
                Rbutton1.connect("clicked",self.FRResponseDisclosure,True)
                Rbutton2 = Gtk.Button(label=self.repeated_words[RWword]["option1"],margin_top=10,margin_start=10,margin_bottom=10,margin_end=10,css_classes=["large-title"])
                Rbutton2.connect("clicked",self.FRResponseDisclosure,False)
                Rbutton3 = Gtk.Button(label=self.repeated_words[RWword]["option2"],margin_top=10,margin_start=10,margin_bottom=10,margin_end=10,css_classes=["large-title"])
                Rbutton3.connect("clicked",self.FRResponseDisclosure,False)
                Rbutton4 = Gtk.Button(label=self.repeated_words[RWword]["option3"],margin_top=10,margin_start=10,margin_bottom=10,margin_end=10,css_classes=["large-title"])
                Rbutton4.connect("clicked",self.FRResponseDisclosure,False)

                Rgrid = Gtk.Grid(hexpand=True,halign=Gtk.Align.CENTER,valign=Gtk.Align.CENTER)
                Rgrid.add_css_class("card")
                position=sorted([[0,0],[0,1],[1,0],[1,1]], key=lambda A: random.random())
                Rgrid.attach(Rbutton1,*position[0],1,1)
                Rgrid.attach(Rbutton2, *position[1],1,1)
                Rgrid.attach(Rbutton3, *position[2],1, 1)
                Rgrid.attach(Rbutton4, *position[3], 1, 1)

                Rcenterbox=Gtk.Box(name="centerbox")
                RButton=Gtk.Button(label=self.repeated_words[RWword]["translation"],hexpand=True,css_classes=["large-title","flat"])
                RButton.connect("clicked",self.FNResponseDisclosure,Rcenterbox,Rgrid)
                Rcenterbox.append(RButton)

                Rrightbox=Gtk.Box(name="rightbox")
                Rrightbox.append(Gtk.Label(label="Повторить",xalign=1,hexpand=True))

                self.Rleaflet.append(Rleftbox)
                self.Rleaflet.append(Rcenterbox)
                self.Rleaflet.append(Rrightbox)

                self.Rleaflet.set_visible_child(Rcenterbox)
                self.Rstack.remove(trash)

                self.Rleaflet.connect("notify::child-transition-running",self.FRSwipeCheck)
                self.Rleaflet.connect("notify::visible-child",self.FRTouchCheck)
                break
        else:
            trash=self.Rleaflet

            self.Rleaflet=Adw.Leaflet(fold_threshold_policy=True,can_navigate_back=True,can_navigate_forward=True,can_unfold=False)
            self.Rstack.add_child(self.Rleaflet)
            self.Rstack.set_visible_child(self.Rleaflet)

            Rleftbox=Gtk.Box(name="leftreload")
            Rleftbox.append(Gtk.Label(label="Перезагрузить"))

            Rcenterbox=Gtk.Box(name="centerbox")
            Rcenterbox.append(Gtk.Label(label="Время отдыха!",hexpand=True,css_classes=["success","large-title"]))

            Rrightbox=Gtk.Box(name="rightreload")
            Rrightbox.append(Gtk.Label(label="Перезагрузить",xalign=1,hexpand=True))

            self.Rleaflet.append(Rleftbox)
            self.Rleaflet.append(Rcenterbox)
            self.Rleaflet.append(Rrightbox)

            self.Rleaflet.set_visible_child(Rcenterbox)
            self.Rstack.remove(trash)

            self.Rleaflet.connect("notify::child-transition-running",self.FRSwipeCheck)
            self.Rleaflet.connect("notify::visible-child",self.FRTouchCheck)

    def FReloadBar(self,*data):
        if self.SwitcherTitle.get_title_visible():
            self.SwitcherBar.set_reveal(True)
        else:
            self.SwitcherBar.set_reveal(False)
    def FNResponseDisclosure(self,*data):
        data[1].remove(data[0])
        data[1].append(data[2])

    def FAbout(self,*data):
        about = Gtk.AboutDialog()
        about.set_transient_for(self)
        about.set_modal(self)

        about.set_authors(["Qwersyk"])
        about.set_copyright("Copyright 2022 Egor Qwersyk")
        about.set_license_type(Gtk.License.GPL_3_0)
        about.set_website("http://langword.org")
        about.set_website_label("Website for download dictionary")
        about.set_version("0.3")
        about.set_logo_icon_name("org.example.App")

        about.show()


class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)
        if not os.path.isdir(".cache"):
            os.mkdir(".cache")
        os.chdir(".cache")
        if not os.path.isdir("org.gnome.Langword"):
            os.mkdir("org.gnome.Langword")
        os.chdir("org.gnome.Langword")
        if not os.path.exists("dictionary.json"):
            file = open("dictionary.json", "w+")
            file.write("{}")
            file.close()
        if not os.path.exists("repeated_words.json"):
            file = open("repeated_words.json", "w+")
            file.write("{}")
            file.close()


    def on_activate(self, app):

        self.win = MainWindow(application=app)
        self.win.present()


def main(version):
    app = MyApp()
    return app.run(sys.argv)

if __name__=='__main__':
    main(None)

