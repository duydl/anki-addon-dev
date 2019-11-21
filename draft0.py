import sys, os
import sql
# Load Anki library
sys.path.append(r"E:\Users\Radiants\Documents\_Projects\_source\Anki") 
from anki.storage import Collection

# Define the path to the Anki SQLite collection
PROFILE_HOME = os.path.expanduser(r"C:\Users\Radiants\AppData\Roaming\Anki2\2. Scientific English - Natural Science & Technology & Knacks") 
cpath = os.path.join(PROFILE_HOME, "collection.anki2")

# Load the Collection
col = Collection(cpath, log=True) # Entry point to the API

# Use the available methods to list the notes
# Load the Collection
col = Collection(cpath, log=True) # Entry point to the API

# Use the available methods to list the notes
for cid in col.findNotes("Deck:Technology"): 
    note = col.getNote(cid)
    front =  note.fields[0] # "Front" is the first field of these cards
    print(front)