import gi
import sys

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.newwords=["LOL","Hi","JOU","HOW?","what"]
        self.NWstack = Gtk.Stack()
        self.NWstack.set_transition_type(Gtk.StackTransitionType.SLIDE_UP_DOWN)
        self.NWstack.set_transition_duration(500)
        self.set_child(self.NWstack)
        print(dir(self.NWstack))
        self.NWleatflet=Adw.Leaflet(fold_threshold_policy=True,can_navigate_back=True,can_navigate_forward=True,can_unfold=False)
        self.c()

    def e(self,*data):
        if not(self.NWleatflet.get_child_transition_running()):
            if self.NWleatflet.get_visible_child().get_name()!="centerbox":
                print("Next")
                self.c()

    def d(self,*data):
        if self.NWleatflet.get_visible_child().get_name()=="rightbox":
            self.NWleatflet.set_transition_type(Adw.LeafletTransitionType.UNDER)
        elif self.NWleatflet.get_visible_child().get_name()=="leftbox":
            self.NWleatflet.set_transition_type(Adw.LeafletTransitionType.OVER)

    def c(self):
        trash=self.NWleatflet

        self.NWleatflet=Adw.Leaflet(fold_threshold_policy=True,can_navigate_back=True,can_navigate_forward=True,can_unfold=False)
        self.NWstack.add_child(self.NWleatflet)
        self.NWstack.set_visible_child(self.NWleatflet)

        NWleftbox=Gtk.Box(name="leftbox")
        NWleftbox.append(Gtk.Label(label="Учить"))
        NWcenterbox=Adw.Bin(name="centerbox")
        NWcenterbox.set_child(Gtk.Label(label="LOL"))
        NWrightbox=Gtk.Box(name="rightbox")
        NWrightbox.append(Gtk.Label(label="Напомнить позже",xalign=1,hexpand=True))



        self.NWleatflet.append(NWleftbox)
        self.NWleatflet.append(NWcenterbox)
        self.NWleatflet.append(NWrightbox)

        self.NWleatflet.set_visible_child(NWcenterbox)
        self.NWstack.remove(trash)

        self.NWleatflet.connect("notify::child-transition-running",self.e)
        self.NWleatflet.connect("notify::visible-child",self.d)

class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()


def main(version):
    app = MyApp()
    return app.run(sys.argv)

if __name__=='__main__':
    main(None)
