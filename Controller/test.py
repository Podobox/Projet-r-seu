# Python 3.x code
from gi.repository import Gtk, GLib

dialog = Gtk.MessageDialog(parent=None, modal=True, message_type=Gtk.MessageType.WARNING,
                        buttons=Gtk.ButtonsType.NONE, text="Oops you're not the owner of this tile.")
dialog.add_button("OK", Gtk.ResponseType.OK)
dialog.add_button("Demander", Gtk.ResponseType.YES)
response = dialog.run()
dialog.destroy()
# if response == Gtk.ResponseType.OK:
#     return "OK"
# elif response == Gtk.ResponseType.YES:
#     return "Demander"
