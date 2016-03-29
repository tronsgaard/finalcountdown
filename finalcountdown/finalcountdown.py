#!/usr/bin/env python3

# For API documentation, see https://developer.ubuntu.com/api/devel/ubuntu-12.04/python/AppIndicator3-0.1.html

from sys import exit
import os
import signal
from datetime import date
from gi.repository import Gtk, GObject
from gi.repository import AppIndicator3 as appindicator

# Config
FINAL_DATE = date(2016,6,16)  # The date we are counting down to
REFRESH_INTERVAL = 60  # seconds

class FinalCountdown:

  def __init__(self, finaldate):
    self.finaldate = finaldate

    # Initialize AppIndicator
    self.indicator = appindicator.Indicator.new (
      "countdown",
      os.path.abspath('icon.svg'),
      appindicator.IndicatorCategory.OTHER
    )
    self.indicator.set_status (appindicator.IndicatorStatus.ACTIVE)

    # Set the label
    self.update()

    # Define menu
    menu = Gtk.Menu()

    menu_item = Gtk.MenuItem("Time is flying..")
    menu_item.set_sensitive(0)
    menu_item.show()
    menu.append(menu_item)
    

    menu_item = Gtk.MenuItem("{:%A, %d %B %Y}".format(self.finaldate))
    menu_item.set_sensitive(0)
    menu_item.show()
    menu.append(menu_item)

    menu_item = Gtk.MenuItem("Quit")
    menu_item.connect("activate", self.quit)
    menu_item.show()
    menu.append(menu_item)

    self.indicator.set_menu(menu)

  def update(self):
    # Calculate the difference in days
    delta = self.finaldate - date.today()
    days = delta.days
    # Update the indicator
    if days > 1:
      label = "{} days..".format(days)
    elif days == 1:
      label = "1 day..".format(days)
    elif days == 0:
      label = "It's today!"
    else:
      print('Exiting (final date is in the past)')
      self.quit()
    self.indicator.set_label(label, '')
    # Set timer for next update
    GObject.timeout_add(REFRESH_INTERVAL * 1000, self.update)

  def quit(self, *args):
    Gtk.main_quit()

if __name__ == "__main__":
  signal.signal(signal.SIGINT, signal.SIG_DFL)
  countdown = FinalCountdown(FINAL_DATE)
  Gtk.main()

