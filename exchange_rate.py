""" This python module uses the Bank of Canada API to look up exchange rates between the
Canadian and US dollars. Tkinter is used to construct a GUI in which the user selects
a date from a calendar dropdown, and prints out the exchange rates for that day (both USD
to CAD and CAD to USD). Noon rates are used.

Exchange rate data obtained from the Bank of Canada API at
                https://www.bankofcanada.ca/valet/observations/FXUSDCAD

Icons from https://www.iconarchive.com/

Colors from https://www.coolors.com/

Written by Rupert Bramall Feb 2021.

"""

from tkinter import messagebox, END, CENTER
import datetime, requests, json, os
from tkcalendar import DateEntry
from PIL import ImageTk, Image
from resizeimage import resizeimage
from functools import lru_cache

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

""" Define fonts and colors """

base_font = ('Times New Roman', 14)
button_font = ('Times New Roman', 12)
artichoke = "#89937c"
deep_taupe = "#715b64"
khaki_web = "#c1ae9f"
pale_silver = "#d3bdb0"
dark_byzantium = "#69385C"
light_grey = "#e0e2e6"

""" Define window """

root = tk.Tk()
root.title('Noon USD to CAD Exchange Rates')
root.config(bg=artichoke)
guiHeight = int(root.winfo_screenheight() * 0.50)
guiWidth = int(root.winfo_screenwidth() * 0.30)
guiDimensions = str(guiWidth)+'x'+str(guiHeight)
root.geometry(guiDimensions)
currentDirectory = os.getcwd()
money_img = tk.PhotoImage(file=currentDirectory + '/US-dollar-icon.png')
root.iconphoto(False, money_img)
image = Image.open(currentDirectory + '/arrow.png')
resized = resizeimage.resize_cover(image, [40, 40], validate=False)
arrow_img = ImageTk.PhotoImage(image=resized)

""" Define methods """

def clear_list():
    output_list.delete(0, END)


def error_message(msg):
    messagebox.showwarning("showwarning", msg)


def valid_date(date_to_check) -> True or None:
    """
    Validate the date.
    """
    year, month, day = map(int, date_to_check.split('-'))
    try:
        dt_date = datetime.date(year, month, day)
        if dt_date < datetime.datetime.now().date():
            return True
        else:
            error_message('Your date must be prior to today')
    except:
        error_message('No such day in calendar')


@lru_cache(maxsize=8)
def get_page(lookup_date):
    page = requests.get('https://www.bankofcanada.ca/valet/observations/FXUSDCAD'
                        '/json?start_date=' + lookup_date + '&end_date=' + lookup_date)
    return json.loads(page.content)


def lookup():
    lookup_date = input_date.get()
    submit_button.focus_set()
    input_date.delete(0, END)
    if valid_date(lookup_date):
        data = get_page(lookup_date)
        if not data['observations']:
            error_message("Date is a weekend or holiday or prior to 2017")
        else:
            exchange_rate = data['observations'][0]['FXUSDCAD']['v']
            inverse = round(1/float(exchange_rate), 4)
            output_list.insert(END, 5*' ' + lookup_date + 8*' ' +
                               exchange_rate + 11*' ' + str(inverse))


""" Define frames """
input_frame = tk.Frame(root, bg=artichoke)
output_frame = tk.Frame(root, bg=pale_silver)
heading_frame = tk.Frame(root, bg=artichoke)
button_frame = tk.Frame(root, bg=artichoke)
input_frame.pack()
heading_frame.pack()
output_frame.pack()
button_frame.pack()

""" Input frame layout """
input_prompt = tk.Label(input_frame, text="Select date", bg=artichoke,
                        fg="black", font=base_font)
input_arrow = tk.Label(input_frame, bg=artichoke, image=arrow_img)
input_date = DateEntry(input_frame, font=base_font, justify=CENTER,
                       bg=light_grey, date_pattern='YYY-MM-DD')
submit_button = tk.Button(input_frame, text="Get Rate", font=button_font,
                          fg="white", bg=dark_byzantium, command=lookup)
input_prompt.grid(row=0, column=0, padx=5, pady=5)
input_arrow.grid(row=0, column=1, padx=5, pady=5)
input_date.grid(row=0, column=2, padx=5, pady=5, ipady=10)
submit_button.grid(row=0, column=3, padx=5, pady=5)

""" Heading frame layout """
date_column = tk.Label(heading_frame, text=3*' ' + 'Date' + 10*' ' +
                        'USD to CAD' + 5*' ' + 'CAD to USD', width=46,
                        bg=pale_silver, fg="black", font=button_font)
date_column.grid(row=0, column=0)

""" Output frame layout """
output_scrollbar = tk.Scrollbar(output_frame, bg=light_grey)
output_list = tk.Listbox(output_frame, yscrollcommand=output_scrollbar.set,
                        bg=light_grey, fg="black", font=base_font, height=13,
                        width=37, borderwidth=3)
output_scrollbar.config(command=output_list.yview)
output_list.grid(row=0, column=0)
output_scrollbar.grid(row=0, column=1, sticky="NS")

""" Button frame layout """
clear_page = tk.Button(button_frame, text="Clear", font=button_font, bg=dark_byzantium,
                       fg="white", borderwidth=2, command=clear_list)
quit_button = tk.Button(button_frame, text="Quit", font=button_font, bg=dark_byzantium,
                        fg="white", borderwidth=2, command=root.destroy)
clear_page.grid(row=0, column=0, padx=2, pady=10, ipadx=10)
quit_button.grid(row=0, column=1, padx=2, pady=10, ipadx=10)

root.mainloop()
