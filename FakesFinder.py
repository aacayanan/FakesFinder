# This program is used to see who is not following you back on Instagram.
# Script created by: Aaron J. Cayanan

# import libraries
import pandas as pd
import json
from tkinter import *
from tkinter import filedialog

# create a function to open the directory
def openDirectory():
    directory = filedialog.askdirectory()
    directory_var.set(directory)
    label.config(text="Done! You can now close the window.")

# create a GUI window
window = Tk()
window.geometry("240x80")
window.title("FakesFinder")
directory_var = StringVar()

open_label = Label(window, text="Upload your followers_and_following folder:")
open_label.pack()

button = Button(text="Open Directory", command=openDirectory)
button.pack()

label = Label(window, text="")
label.pack()

window.mainloop()

# read the json files and put it into corresponding dataframes
directory = directory_var.get()
followers = pd.read_json(directory + '/followers_1.json')
following = pd.read_json(directory + '/following.json')

with open('followers_and_following/followers_1.json') as data_file:
    data_followers = json.load(data_file)
with open('followers_and_following/following.json') as data_file:
    data_following = json.load(data_file)

df_followers = pd.json_normalize(data_followers, 'string_list_data')
df_following = pd.json_normalize(data_following['relationships_following'], 'string_list_data')

# combine the two dataframes and clean the data
df_combined = pd.merge(df_followers, df_following, on='value', how='outer', suffixes=('_followers', '_following'))
columns_to_remove = ['timestamp_followers', 'timestamp_following']
df_combined = df_combined.drop(columns=columns_to_remove)

# isolate the usernames that are not following you back
df_not_followed = df_combined[df_combined['href_followers'].isna()]
df_not_followed.reset_index(drop=True, inplace=True)
df_not_followed.index = df_not_followed.index + 1
df_not_followed = df_not_followed.drop(columns=['href_followers'])

# save the data to an html file
df_not_followed['href_following'] = df_not_followed['href_following'].apply(lambda x: f'<a href="{x}" target="_blank">{x}</a>')
df_not_followed.to_html('output.html', escape=False)