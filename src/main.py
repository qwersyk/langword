import gi
import sys
import os
import random
import os.path, json
from datetime import datetime,timedelta


gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(380, 720)

        self.hb=Adw.HeaderBar()
        self.set_titlebar(self.hb)

        self.Aplication=Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_child(self.Aplication)

        self.MainStack=Adw.ViewStack(vexpand=True)

        self.Home=Gtk.Box()
        self.NewWords=Gtk.Box()
        self.RepetitionWords=Gtk.Box()

        self.MainStack.add_titled(self.Home,"Home","Главная")
        self.MainStack.add_titled(self.NewWords,"NewWords","Новые слова")
        self.MainStack.add_titled(self.RepetitionWords,"RepetitionWords","Повторение слов")
        self.Aplication.append(self.MainStack)

        self.SwitcherTitle=Adw.ViewSwitcherTitle()
        self.SwitcherTitle.set_stack(self.MainStack)
        self.SwitcherTitle.set_title("LangWord")
        self.hb.set_title_widget(self.SwitcherTitle)





        self.NWstack = Gtk.Stack()
        self.NWstack.set_transition_type(Gtk.StackTransitionType.SLIDE_UP_DOWN)
        self.NWstack.set_transition_duration(500)
        self.NewWords.append(self.NWstack)

        self.RWstack = Gtk.Stack()
        self.RWstack.set_transition_type(Gtk.StackTransitionType.SLIDE_UP_DOWN)
        self.RWstack.set_transition_duration(500)
        self.RepetitionWords.append(self.RWstack)


        self.NWleatflet=Adw.Leaflet()
        self.RWleatflet=Adw.Leaflet()

        self.SwitcherBar=Adw.ViewSwitcherBar()
        self.SwitcherBar.set_stack(self.MainStack)
        self.SwitcherBar.set_reveal(True)
        self.Aplication.append(self.SwitcherBar)

        with open('dictionary.json') as f:
            self.dictionary = json.load(f)
        with open('repeated_words.json') as f:
            self.repeated_words = json.load(f)

        self.c()
        self.q()
        self.SwitcherTitle.connect("notify::title-visible",self.f)
        self.f()


    def e(self,*data):
        if not(self.NWleatflet.get_child_transition_running()) and self.NWleatflet.get_visible_child().get_name()!="centerbox":
            if self.NWleatflet.get_visible_child().get_name()=="leftbox":
                self.repeated_words[self.NWleatflet.get_name()]=self.dictionary[self.NWleatflet.get_name()]|{"time":str(datetime.today().strftime("%Y-%m-%d %H:%M:%S")),"repetitions":0}
                with open('repeated_words.json',"w") as f:
                    json.dump(self.repeated_words,f)
                self.dictionary.pop(self.NWleatflet.get_name())
                with open('dictionary.json',"w") as f:
                    json.dump(self.dictionary,f)
            self.c()

    def d(self,*data):
        if self.NWleatflet.get_visible_child().get_name()=="rightbox":
            self.NWleatflet.set_transition_type(Adw.LeafletTransitionType.UNDER)
        elif self.NWleatflet.get_visible_child().get_name()=="leftbox":
            self.NWleatflet.set_transition_type(Adw.LeafletTransitionType.OVER)

    def c(self):
        if(self.dictionary):
            trash=self.NWleatflet

            self.NWleatflet=Adw.Leaflet(fold_threshold_policy=True,can_navigate_back=True,can_navigate_forward=True,can_unfold=False)
            NWword=(random.choice(list(self.dictionary)))
            self.NWleatflet.set_name(NWword)
            self.NWstack.add_child(self.NWleatflet)
            self.NWstack.set_visible_child(self.NWleatflet)

            NWleftbox=Gtk.Box(name="leftbox")
            NWleftbox.append(Gtk.Label(label="Учить"))

            NWcenterbox=Gtk.Box(name="centerbox")
            NWLabel=Gtk.Label(label=str(self.dictionary[NWword]["translation"])+"\n"+str(NWword),hexpand=True,css_classes=["large-title"])
            NWButton=Gtk.Button(label=str(self.dictionary[NWword]["translation"]),hexpand=True,css_classes=["large-title","flat"])
            NWButton.connect("clicked",self.b,NWcenterbox,NWLabel)
            NWcenterbox.append(NWButton)

            NWrightbox=Gtk.Box(name="rightbox")
            NWrightbox.append(Gtk.Label(label="Напомнить позже",xalign=1,hexpand=True))



            self.NWleatflet.append(NWleftbox)
            self.NWleatflet.append(NWcenterbox)
            self.NWleatflet.append(NWrightbox)

            self.NWleatflet.set_visible_child(NWcenterbox)
            self.NWstack.remove(trash)

            self.NWleatflet.connect("notify::child-transition-running",self.e)
            self.NWleatflet.connect("notify::visible-child",self.d)
        else:
            trash=self.NWleatflet
            self.NWleatflet=Adw.Leaflet()
            NWlabel=Gtk.Label(label="Тут пока пусто",hexpand=True,css_classes=["warning","large-title"])
            self.NWleatflet.append(NWlabel)
            self.NWstack.add_child(self.NWleatflet)
            self.NWstack.set_visible_child(self.NWleatflet)
            self.NWstack.remove(trash)




    def w(self,*data):
        if not(self.RWleatflet.get_child_transition_running()) and self.RWleatflet.get_visible_child().get_name()!="centerbox":
            if self.RWleatflet.get_visible_child().get_name()=="leftbox":
                if self.repeated_words[self.RWleatflet.get_name()]["repetitions"]==0:
                    self.repeated_words[self.RWleatflet.get_name()]["time"]=(datetime.now() + timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M:%S")
                elif self.repeated_words[self.RWleatflet.get_name()]["repetitions"]==1:
                    self.repeated_words[self.RWleatflet.get_name()]["time"]=(datetime.now() + timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S")
                elif self.repeated_words[self.RWleatflet.get_name()]["repetitions"]==2:
                    self.repeated_words[self.RWleatflet.get_name()]["time"]=(datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
                elif self.repeated_words[self.RWleatflet.get_name()]["repetitions"]==3:
                    self.repeated_words[self.RWleatflet.get_name()]["time"]=(datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S")
                elif self.repeated_words[self.RWleatflet.get_name()]["repetitions"]==4:
                    self.repeated_words[self.RWleatflet.get_name()]["time"]=(datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
                elif self.repeated_words[self.RWleatflet.get_name()]["repetitions"]==5:
                    self.repeated_words[self.RWleatflet.get_name()]["time"]=(datetime.now() + timedelta(days=21)).strftime("%Y-%m-%d %H:%M:%S")
                elif self.repeated_words[self.RWleatflet.get_name()]["repetitions"]==6:
                    self.repeated_words[self.RWleatflet.get_name()]["time"]=(datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d %H:%M:%S")
                elif self.repeated_words[self.RWleatflet.get_name()]["repetitions"]==7:
                    self.repeated_words[self.RWleatflet.get_name()]["time"]=(datetime.now() + timedelta(days=180)).strftime("%Y-%m-%d %H:%M:%S")
                else:
                    self.repeated_words[self.RWleatflet.get_name()]["time"]=(datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d %H:%M:%S")
                self.repeated_words[self.RWleatflet.get_name()]["repetitions"]+=1
                with open('repeated_words.json',"w") as f:
                    json.dump(self.repeated_words,f)
            else:
                self.repeated_words[self.RWleatflet.get_name()]["time"]=(datetime.now() + timedelta(seconds=30)).strftime("%Y-%m-%d %H:%M:%S")
                with open('repeated_words.json',"w") as f:
                    json.dump(self.repeated_words,f)
            self.q()

    def l(self,*data):
        if not(self.RWleatflet.get_child_transition_running()) and self.RWleatflet.get_visible_child().get_name()!="centerbox":
            self.q()

    def r(self,*data):
        if self.RWleatflet.get_visible_child().get_name()=="rightbox":
            self.RWleatflet.set_transition_type(Adw.LeafletTransitionType.UNDER)
        elif self.RWleatflet.get_visible_child().get_name()=="leftbox":
            self.RWleatflet.set_transition_type(Adw.LeafletTransitionType.OVER)

    def o(self,*data):
        if data[1]:
            data[0].add_css_class("suggested-action")
        else:
            data[0].add_css_class("destructive-action")


    def q(self):
        datenow=datetime.today()
        for RWword in self.repeated_words:
            if(datetime.strptime(self.repeated_words[RWword]["time"], "%Y-%m-%d %H:%M:%S")<datenow):
                trash=self.RWleatflet

                self.RWleatflet=Adw.Leaflet(fold_threshold_policy=True,can_navigate_back=True,can_navigate_forward=True,can_unfold=False)
                self.RWleatflet.set_name(RWword)
                self.RWstack.add_child(self.RWleatflet)
                self.RWstack.set_visible_child(self.RWleatflet)

                RWleftbox=Gtk.Box(name="leftbox")
                RWleftbox.append(Gtk.Label(label="Вспмнил"))

                RWbutton1 = Gtk.Button(label=RWword,margin_top=10,margin_start=10,margin_bottom=10,margin_end=10,css_classes=["large-title"])
                RWbutton1.connect("clicked",self.o,True)
                RWbutton2 = Gtk.Button(label=self.repeated_words[RWword]["option1"],margin_top=10,margin_start=10,margin_bottom=10,margin_end=10,css_classes=["large-title"])
                RWbutton2.connect("clicked",self.o,False)
                RWbutton3 = Gtk.Button(label=self.repeated_words[RWword]["option2"],margin_top=10,margin_start=10,margin_bottom=10,margin_end=10,css_classes=["large-title"])
                RWbutton3.connect("clicked",self.o,False)
                RWbutton4 = Gtk.Button(label=self.repeated_words[RWword]["option3"],margin_top=10,margin_start=10,margin_bottom=10,margin_end=10,css_classes=["large-title"])
                RWbutton4.connect("clicked",self.o,False)

                RWgrid = Gtk.Grid(hexpand=True,halign=Gtk.Align.CENTER,valign=Gtk.Align.CENTER)
                RWgrid.add_css_class("card")
                position=sorted([[0,0],[0,1],[1,0],[1,1]], key=lambda A: random.random())
                RWgrid.attach(RWbutton1,*position[0],1,1)
                RWgrid.attach(RWbutton2, *position[1],1,1)
                RWgrid.attach(RWbutton3, *position[2],1, 1)
                RWgrid.attach(RWbutton4, *position[3], 1, 1)


                RWcenterbox=Gtk.Box(name="centerbox")
                RWButton=Gtk.Button(label=self.repeated_words[RWword]["translation"],hexpand=True,css_classes=["large-title","flat"])
                RWButton.connect("clicked",self.b,RWcenterbox,RWgrid)
                RWcenterbox.append(RWButton)

                RWrightbox=Gtk.Box(name="rightbox")
                RWrightbox.append(Gtk.Label(label="Повторить",xalign=1,hexpand=True))



                self.RWleatflet.append(RWleftbox)
                self.RWleatflet.append(RWcenterbox)
                self.RWleatflet.append(RWrightbox)

                self.RWleatflet.set_visible_child(RWcenterbox)
                self.RWstack.remove(trash)

                self.RWleatflet.connect("notify::child-transition-running",self.w)
                self.RWleatflet.connect("notify::visible-child",self.r)
                break
        else:
            trash=self.RWleatflet

            self.RWleatflet=Adw.Leaflet(fold_threshold_policy=True,can_navigate_back=True,can_navigate_forward=True,can_unfold=False)
            self.RWstack.add_child(self.RWleatflet)
            self.RWstack.set_visible_child(self.RWleatflet)

            RWleftbox=Gtk.Box(name="leftbox")
            RWleftbox.append(Gtk.Label(label="Перезагрузить"))

            NWlabel=Gtk.Label(label="Время отдыха!",hexpand=True,css_classes=["success","large-title"])

            RWcenterbox=Gtk.Box(name="centerbox")
            RWcenterbox.append(NWlabel)

            RWrightbox=Gtk.Box(name="rightbox")
            RWrightbox.append(Gtk.Label(label="Перезагрузить",xalign=1,hexpand=True))



            self.RWleatflet.append(RWleftbox)
            self.RWleatflet.append(RWcenterbox)
            self.RWleatflet.append(RWrightbox)

            self.RWleatflet.set_visible_child(RWcenterbox)
            self.RWstack.remove(trash)

            self.RWleatflet.connect("notify::child-transition-running",self.l)
            self.RWleatflet.connect("notify::visible-child",self.r)

    def f(self,*data):
        if self.SwitcherTitle.get_title_visible():
            self.SwitcherBar.set_reveal(True)
        else:
            self.SwitcherBar.set_reveal(False)
    def b(self,*data):
        data[1].remove(data[0])
        data[1].append(data[2])


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
