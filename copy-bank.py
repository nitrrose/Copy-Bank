from tkinter import *
import pyperclip
import os

def readStored():
    """fetches the stored text to be placed into the GUI

    Returns:
        dict: formatted as idx:[name,raw], the current stored data in 'copybank.txt'
    """

    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'copybank.txt')

    try:
        f = open(file_path, 'r')
        f.close()

    except Exception as e:
        print(f"A <{e}> exception occured!")
        print(f"No such file <{file_path}> exists in the directory!\nCreating file...")

        # create file if not present
        f = open(file_path, 'x')
        f.close()

        print(f"New file <{file_path}> created in the directory!\nBeginning data read...")

    res = {}

    with open(file_path, 'r') as f:
        
        # get stored texts
        lines = f.readlines()

        # add to runtime dict. of stored words
        for text in lines: 
            # splits .txt file lines into readable data
            # format = {idx},{name},{raw}
            data = text.split(',')
            print(f"The current line contains this as data: <{data}>")

            res[int(data[0])] = [data[1],data[2]]
            
        f.close()

    print(f"Data finished reading! The current stored data is <{res}>.")
    return res

def writeContents(contents):
    """write the new contents to file for later use

    Args:
        contents (dict): the dictionary containing the current text to be added to the copybank
    """

    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'copybank.txt')

    with open(file_path, 'w') as f:
        for entry in contents:
            # write data of contents in format {idx},{name},{raw}
            data = contents[entry]
            f.write(f"{entry},{data[0]},{data[1]},\n")
            
        f.close()

def setupGUI(contents, gridW, gridH):
    root = Tk()
    root.geometry('750x150') 
    root.title("CopyBank")

    global nextIdx

    def buttonManager(idx):
        global menu

        menu = Tk()
        menu.geometry('275x75')
        menu.title("Action Selector")

        try:
            selected = contents[idx][0]
        except Exception as e:
            print(f"This text is likely empty! Setting selected to 'empty'...")
            selected = "empty"

        header = Label(menu, text=f"The current selected text is nicknamed '{selected}'.")
        header.pack(side='top')

        copyButton = Button(menu, text=f"Copy this text.", command=lambda:copyFromClicked(idx)).pack(side='top', fill='both')
        #.place(relx=0.25,rely=0.3)

        addButton = Button(menu, text=f"Change this text.", command=lambda:addNewEntry(idx)).pack(side='top', fill='both')
        #.place(relx=0.25,rely=0.6)

        return

    def addNewEntry(idx):
        """handling adding new text to the bank
        """
        global menu
        menu.destroy()

        temp = Tk()
        temp.geometry('200x125')
        temp.title("Change Text")

        # creating temp widgets for the popup
        headerRaw = Label(temp, text="Enter the TEXT to be stored.").pack(side = 'top')

        entryRaw = Entry(temp, width=30)
        entryRaw.pack(side='top')

        headerName = Label(temp, text="Enter the NICKNAME to give the text.").pack(side = 'top')

        entryName = Entry(temp, width=30)
        entryName.pack(side='top')

        # adding to the runtime dict
        def addToDict():
            contents[idx] = [entryName.get(), entryRaw.get()]
            temp.destroy()
            updateButton(idx)

        confirmButton = Button(temp, text='Confirm and Add', command=addToDict).place(relx=0.25,rely=0.7)
        
    # adding stored text into the window as buttons
    # clicking on button copies to clipboard

    copyBoxes = {}

    # initialise buttons from contents
    PADX=(5,0)
    PADY=(2.5,0)

    for row in range(gridH):
        for column in range(gridW):
            # creating new button
            idx = row*gridW + column
            function = lambda idx=idx: buttonManager(idx)

            button = Button(root, text = "Empty", command=function)
            button.grid(row=row, column=column, padx=PADX,pady=PADY)

            copyBoxes[idx] = button

    print(f"All buttons have been initialised. These are the buttons: <{copyBoxes}>")

    
    def updateButton(idx):
        copyBoxes[idx].configure(text=contents[idx][0])

    def copyFromClicked(idx):
        global menu
        try:
            toCopy = contents[idx][1]
        except Exception as e:
            print("This text is likely empty! Setting clipboard to empty...")
            toCopy = ""

        pyperclip.copy(toCopy)

        menu.destroy()

    # update buttons from stored
    print("Now assigning stored data to buttons...")
    for item in contents:
        print(f"Currently updating button at index {item}...")
        updateButton(item)

    return root

def main():
    gridW, gridH = (10,5)                                       # <--- change these values to add more buttons to the GUI to store text.

    curContents =  readStored()

    root = setupGUI(curContents, gridW, gridH)
    root.mainloop()

    print(f"This is the data which will be stored: <{curContents}>")
    print("Storing new data...")

    writeContents(curContents)

    print("Stored. Enjoy!")

if __name__ == "__main__":
    main()