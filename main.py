from __future__ import division

import datetime
import time as t
import locale

locale.setlocale(locale.LC_ALL, 'US')

import Tkinter as tk
from yahoo_finance import Share

open = datetime.time(hour=9, minute=29)
close = datetime.time(hour=16, minute=0)
trading_day_length = (6 * 60) + 30



class VolumeCalculator(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.clock = tk.Label(self, text="")
        self.clock.pack()
        self.status = tk.Label(self, text="")
        self.status.pack()
        self.header = tk.Label(self, text="EOD Volume").pack()
        self.display = tk.Label(self, text="", width=10, height=2)
        self.display.config(font=("Courier", 22))
        self.display.pack()

        self.stock_object = Share('UNXL')
        self.avg_volume = self.stock_object.get_avg_daily_volume()
        self.volume = self.stock_object.get_volume()
        self.ASSUMED_TIME = datetime.time(hour=10, minute=0)

        self.update()

    def calculate_eod_volume(self, volume, time):
        diff_hour = self.ASSUMED_TIME.hour-open.hour
        diff_min = self.ASSUMED_TIME.minute-open.minute
        diff_time_length = (diff_hour * 60) + diff_min
        eod_volume = str((1 / (float(diff_time_length) / float(trading_day_length))) * volume).split('.')[0]
        self.ASSUMED_TIME = datetime.time(hour=10, minute=self.ASSUMED_TIME.minute+1)
        eod_volume = locale.format("%d", int(eod_volume), grouping=True)
        return eod_volume

    def update(self):

        dt = datetime.datetime.now()
        now = datetime.time(hour=dt.hour, minute=dt.minute)
        #if now > open and now < close:
        if True:
            self.status.configure(text="Calculating Volume")
            volume = int(self.stock_object.get_volume())
            self.display.configure(text=self.calculate_eod_volume(volume, now))
        else:
            self.status.configure(text="Not Calculating Volume")
            self.display.configure(text=self.volume)

        now = t.strftime("%H:%M:%S", t.gmtime())
        self.clock.configure(text=now)
        self.after(1000, self.update)

if __name__== "__main__":
    app = VolumeCalculator()
    app.mainloop()