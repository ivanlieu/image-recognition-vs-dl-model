import tkinter as tk
import UI_v1

def main():

    # initialize tkinter 
    root = tk.Tk()
    root.title('Image Identification')
    root.geometry("700x920")

    # model file path
    filePathModel = 'best_model_acc_2convL_2FCL_9178.pt'

    # create tkinter window object
    mainWindow = UI_v1.UIWindow(root, filePathModel)

    root.mainloop()

main()



