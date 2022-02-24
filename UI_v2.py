import tkinter as tk
import math
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import cnnModel_v1

class UIWindow():
    def __init__(self, rootWindow, modelFPath):
        """Initializes needed tracking variables and tkinter objects to create the GUI."""
        #values of interest to potentially modify/counters
        self.count = 1 
        self.labelList = ['t-shirt/top', 'pants/trouser', 'pullover/sweater', 'dress', 'coat/jacket', 'sandal/open-toe shoes', 'shirt/button up shirt', 'sport/casual shoes', 'bag/purse', 'ankle boots']
        self.changeSpeed = 20   # iteration change speed in milliseconds
        self.increment = -10     # increment rate in decimal color units (+ve for brightening, -ve for darkening)
        self.correctAnswer = True   # tracks if user choice was correct
        self.correctAnsColor = '#69e514'    # hex color
        self.wrongAnsColor = '#f71b1b'      # hex color
        self.windowBGColor = '#f0f0f0'      # hex color
        self.blackColor = '#000000'         # hex color
        self.radiansTextCounter = 0.0
        self.radiansBarCounter = 0.0
        self.oldUserPercent = 0.0

        # initialize cnn model
        self.cnnModel = cnnModel_v1.cnnEvalModel(modelFPath)
        self.cnnModel.runModel(self.count)

        # initialize score tracking vars
        self.iterationNum = 0.0
        self.userCorrect = 0.0
        self.cpuCorrect = 0.0
        self.userCorrectPercent = 0.0
        self.cpuCorrectPercent = 0.0

        # create frames for tkinter window
        self.imageFrame = tk.Frame(rootWindow, bg = 'black', width = 700, height = 500) # frame for matplotlib figure for image
        self.imageSubFrame = tk.Frame(self.imageFrame, bg = 'black', width = 700, height = 500)
        self.paddingFrame = tk.Frame(rootWindow, width = 700, height = 6)
        self.lastCorrectFrame = tk.Frame(rootWindow, width = 700, height = 38) # frame for label listing correct choice for the last image
        self.topRowButtonFrame = tk.Frame(rootWindow, width = 700, height = 75) # frame for top row of buttons
        self.botRowButtonFrame = tk.Frame(rootWindow,  width = 700, height = 75) # frame for bottom row of buttons
        self.userScoreFrame = tk.Frame(rootWindow, width = 700, height = 75) # frame for user score
        self.cpuScoreFrame = tk.Frame(rootWindow, width = 700, height = 75) # frame for cpu score
        self.padding2Frame = tk.Frame(rootWindow, width = 700, height = 15)
        self.infoFrame = tk.Frame(rootWindow, width = 700, height = 30) # frame for info at bottom of window

        # create subframes for userScoreFrame
        self.userScorePaddingFrame = tk.Frame(self.userScoreFrame, width = 22, height = 75) # subframe for adjusting layout
        self.userScoreDescriptorFrame = tk.Frame(self.userScoreFrame, bg = 'purple', width = 135, height = 75) # subframe for user score descriptor
        self.userScoreBarFrame = tk.Frame(self.userScoreFrame, bg='white', width = 425, height = 75) # subframe for user score bar
        self.userScorePercentFrame = tk.Frame(self.userScoreFrame, bg = 'purple', width = 125, height = 75) # subframe for user score %

        # create subframes for cpuScoreFrame
        self.cpuScorePaddingFrame = tk.Frame(self.cpuScoreFrame, width = 22, height = 75) # subframe for adjusting layout
        self.cpuScoreDescriptorFrame = tk.Frame(self.cpuScoreFrame, bg = 'cyan', width = 135, height = 75) # subframe for cpu score descriptor
        self.cpuScoreBarFrame = tk.Frame(self.cpuScoreFrame, bg='white', width = 425, height = 75) # subframe for cpu score bar
        self.cpuScorePercentFrame = tk.Frame(self.cpuScoreFrame, bg = 'cyan', width = 125, height = 75) # subframe for cpu score %

        # create font class for labels
        self.scoreFont = ('Consolas', 15, 'bold')
        self.percentFont = ('Helvetica', 20, 'bold')
        self.lastCorrectFont = ('Consolas', 10)
        self.consolasSize9 = ('Consolas', 9)

        # create fmnist data image
        self.cnnModel.runImagePlotData()
        self.fig = plt.figure(figsize=(5, 5.5))
        self.imgPlot = plt.imshow(self.cnnModel.imgOut, cmap = 'gray')
        self.imageCanvas = FigureCanvasTkAgg(self.fig, master = self.imageSubFrame)
        self.imageCanvas.draw()
        self.imageCanvas.get_tk_widget().pack(side = 'top', fill = 'both')

        # create the last correct choice label
        self.lastCorrectLabelStatic = tk.Label(self.lastCorrectFrame, anchor = 'center', bd = 0, font = self.lastCorrectFont, text = '   Correct clothing from last image: ')
        self.lastCorrectLabelVar = tk.Label(self.lastCorrectFrame, anchor = 'center', bd = 0, font = self.lastCorrectFont, text = '')

        # create buttons 
        self.buttons0 = tk.Button(self.topRowButtonFrame, height=2, width=12, font = self.consolasSize9, text='T-shirt/top', command=lambda : self.updateTkinter(0))
        self.buttons1 = tk.Button(self.topRowButtonFrame, height=2, width=12, font = self.consolasSize9, text='Pants/\ntrouser', command=lambda : self.updateTkinter(1))
        self.buttons2 = tk.Button(self.topRowButtonFrame, height=2, width=12, font = self.consolasSize9, text='Pullover/\nSweater', command=lambda : self.updateTkinter(2))
        self.buttons3 = tk.Button(self.topRowButtonFrame, height=2, width=12, font = self.consolasSize9, text='Dress', command=lambda : self.updateTkinter(3))
        self.buttons4 = tk.Button(self.topRowButtonFrame, height=2, width=12, font = self.consolasSize9, text='Coat/\nJacket', command=lambda : self.updateTkinter(4))
        self.buttons5 = tk.Button(self.botRowButtonFrame, height=2, width=12, font = self.consolasSize9, text='Sandal/\nOpen-toe', command=lambda : self.updateTkinter(5))
        self.buttons6 = tk.Button(self.botRowButtonFrame, height=2, width=12, font = self.consolasSize9, text='Shirt/\nButton-up', command=lambda : self.updateTkinter(6))
        self.buttons7 = tk.Button(self.botRowButtonFrame, height=2, width=12, font = self.consolasSize9, text='Sport/Casual\nShoes', command=lambda : self.updateTkinter(7))
        self.buttons8 = tk.Button(self.botRowButtonFrame, height=2, width=12, font = self.consolasSize9, text='Bag/Purse', command=lambda : self.updateTkinter(8))
        self.buttons9 = tk.Button(self.botRowButtonFrame, height=2, width=12, font = self.consolasSize9, text='Ankle Boots', command=lambda : self.updateTkinter(9))

        # create descriptor and score % labels
        self.userScoreLabel = tk.Label(self.userScoreDescriptorFrame, anchor = 'center', bd = 0, font = self.scoreFont, text = 'Your Score', width = 11)
        self.userScorePercentLabel = tk.Label(self.userScorePercentFrame, anchor = 'center', bd = 0, font = self.percentFont, text = '00.00%', width = 7)
        self.cpuScoreLabel = tk.Label(self.cpuScoreDescriptorFrame, anchor = 'center', bd = 0, font = self.scoreFont, text = 'Deep\nLearning\nModel', width = 11)
        self.cpuScorePercentLabel = tk.Label(self.cpuScorePercentFrame, anchor = 'center', bd = 0, font = self.percentFont, text = '00.00%', width = 7)

        # create canvas for user and cpu score bar
        self.userScoreCanvas = tk.Canvas(self.userScoreBarFrame, width = 420, height = 75)
        self.cpuScoreCanvas = tk.Canvas(self.cpuScoreBarFrame, width = 420, height = 75)

        # create the score bars in the canvas
        self.userBlackBar = self.userScoreCanvas.create_rectangle(0, 21, 5, 57, fill = 'black')
        self.userColourBar = self.userScoreCanvas.create_rectangle(5, 21, 10, 57, fill = '#f0f0f0', outline = '#f0f0f0')
        self.cpuScoreBar = self.cpuScoreCanvas.create_rectangle(0, 21, 5, 57, fill = 'black')

        # create labels for info at bottom of window
        self.userInfoStaticLabel = tk.Label(self.infoFrame, anchor = 'center', bd = 0, font = self.lastCorrectFont, text = '   Correct images: ', width = 20)
        self.userInfoDynamicLabel = tk.Label(self.infoFrame, anchor = 'center', bd = 0, font = self.lastCorrectFont, text = '0', width = 4)
        self.cpuInfoStaticLabel = tk.Label(self.infoFrame, anchor = 'center', bd = 0, font = self.lastCorrectFont, text = '\t  DL model correct images: ', width = 37)
        self.cpuInfoDynamicLabel = tk.Label(self.infoFrame, anchor = 'center', bd = 0, font = self.lastCorrectFont, text = '0', width = 4)
        self.numImagesInfoStaticLabel = tk.Label(self.infoFrame, anchor = 'center', bd = 0, font = self.lastCorrectFont, text = '\t Total images: ', width = 25)
        self.numImagesInfoDynamicLabel = tk.Label(self.infoFrame, anchor = 'center', bd = 0, font = self.lastCorrectFont, text = '0', width = 4)

        # pack frames
        self.imageFrame.pack(side = 'top', fill = 'both')
        self.imageSubFrame.pack(side = 'top', fill = 'both')
        self.paddingFrame.pack(side = 'top', fill = 'both')
        self.lastCorrectFrame.pack(side = 'top', fill = 'both')
        self.topRowButtonFrame.pack(side = 'top', fill = 'both')
        self.botRowButtonFrame.pack(side = 'top', fill = 'both')
        self.userScoreFrame.pack(side = 'top', fill = 'both')
        self.cpuScoreFrame.pack(side = 'top', fill = 'both')
        self.padding2Frame.pack(side = 'top', fill = 'both')
        self.infoFrame.pack(side = 'top', fill = 'both')

        # pack buttons
        self.buttons0.pack(side = 'left', padx = 40, pady = 15)
        self.buttons1.pack(side = 'left', padx = 0, pady = 15)
        self.buttons2.pack(side = 'left', padx = 40, pady = 15)
        self.buttons3.pack(side = 'left', padx = 0, pady = 15)
        self.buttons4.pack(side = 'left', padx = 40, pady = 15)
        self.buttons5.pack(side = 'left', padx = 40, pady = 15)
        self.buttons6.pack(side = 'left', padx = 0, pady = 15)
        self.buttons7.pack(side = 'left', padx = 40, pady = 15)
        self.buttons8.pack(side = 'left', padx = 0, pady = 15)
        self.buttons9.pack(side = 'left', padx = 40, pady = 15)

        # pack subframes
        self.userScorePaddingFrame.pack(side = 'left')
        self.userScoreDescriptorFrame.pack(side = 'left')
        self.userScoreBarFrame.pack(side = 'left')
        self.userScorePercentFrame.pack(side = 'left')

        self.cpuScorePaddingFrame.pack(side = 'left')
        self.cpuScoreDescriptorFrame.pack(side = 'left')
        self.cpuScoreBarFrame.pack(side = 'left')
        self.cpuScorePercentFrame.pack(side = 'left')

        # pack canvas
        self.userScoreCanvas.pack(side = 'left', fill = 'both')
        self.cpuScoreCanvas.pack(side='left', fill = 'both')

        # pack labels
        self.userScoreLabel.pack(side = 'right')
        self.userScorePercentLabel.pack(side = 'right')
        self.cpuScoreLabel.pack(side = 'right')
        self.cpuScorePercentLabel.pack(side = 'right')
        self.lastCorrectLabelStatic.pack(side = 'left')
        self.lastCorrectLabelVar.pack(side = 'left')
        self.userInfoStaticLabel.pack(side = 'left')
        self.userInfoDynamicLabel.pack(side = 'left')
        self.cpuInfoStaticLabel.pack(side = 'left')
        self.cpuInfoDynamicLabel.pack(side = 'left')
        self.numImagesInfoStaticLabel.pack(side = 'left')
        self.numImagesInfoDynamicLabel.pack(side = 'left')

    def drawTensorImage(self):
        """Removes the current image and creates a new greyscale matplotlib plot from a denormalized tensor
        that is packed to a new tkinter subframe."""

        # destroy previous figure
        self.imageSubFrame.destroy()

        # remake image subframe
        self.imageSubFrame = tk.Frame(self.imageFrame, bg = 'black', width = 700, height = 500)

        # clear old figure
        plt.close(self.fig)

        # create new figure and plot
        self.fig = plt.figure(figsize=(5, 5.5))
        self.imgPlot = plt.imshow(self.cnnModel.imgOut, cmap = 'gray')

        self.imageCanvas = FigureCanvasTkAgg(self.fig, master = self.imageSubFrame)
        self.imageCanvas.draw()
        self.imageCanvas.get_tk_widget().pack(side = 'top', fill = 'both')
        self.imageSubFrame.pack(side = 'top', fill = 'both')

    def calcCorrectPercent(self, correctCountVar):
        """Calculates a percent that is divided by the total number of iterations.
            Accepts correctCountVar as a integer/float
            Returns correctPercent as a float"""

        correctPercent = correctCountVar / self.iterationNum * 100

        return correctPercent

    def updateScoreStrVar(self, scorePercent):
        """Takes a percent value and converts it to a string rounded to 2 decimal places.
            Accepts scorePercent as a float
            Returns tempScoreString as a string."""

        if scorePercent > 100:      # deal with edge cases
            tempScoreString = '100.00%'
        elif scorePercent <= 0:     # deal with edge cases
            tempScoreString = '0.00%'
        else:
            tempScoreString = str(round(scorePercent, 2)) + '%'

        return tempScoreString

    def updateScoreBarPixel(self, scorePercent):
        """Takes a percent value and calculates the width of a score bar for tkinter canvas rectangle (for cpu score bar)
            Accepts scorePercent as a float
            Returns tempScoreWidth as an integer."""

        if scorePercent > 100:      # deal with edge cases
            tempScoreWidth = 410
        elif scorePercent < 0.5:    # deal with edge cases
            tempScoreWidth = 5
        else:
            tempScoreWidth = round(scorePercent / 100 * 410)

        return tempScoreWidth

    def updateScoreBarPosition(self, scorePercent, oldScorePercent):
        """Calculates x positions for tkinter canvas rectangles based on changes in score percent (for user score bar)
            Accepts scorePercent as a float
                    oldScorePercent as a float
            Returns scoreBlackBarX2Pos as an integer
                    scoreColourBarX2Pos as an integer
                    significantChange as a boolean"""

        if scorePercent > 100:      # deal with edge cases
            scoreWidthDefault = 410
        elif scorePercent < (100 / 410):    # deal with edge cases
            scoreWidthDefault = 1
        else:
            scoreWidthDefault = round(scorePercent / 100 * 410)

        if abs(scorePercent - oldScorePercent) >= (100 / 410):      # check for change in percent between old and new percent
            significantChange = True 

            if scorePercent > oldScorePercent:       # check if score has increased/decreased
                scoreBlackBarX2Pos = round(oldScorePercent / 100 * 410)
                scoreColourBarX2Pos = round(scorePercent / 100 * 410)
            else:
                scoreBlackBarX2Pos = round(scorePercent / 100 * 410)
                scoreColourBarX2Pos = round(oldScorePercent / 100 * 410)

        else:       # assigns x-position values if score percentage stays at 100% or 0%
            significantChange = False
            scoreBlackBarX2Pos = scoreWidthDefault
            scoreColourBarX2Pos = scoreWidthDefault + 1

        return scoreBlackBarX2Pos, scoreColourBarX2Pos, significantChange

    def incrementHexVal(self, hexStr, increment):
        """Changes an input hex value by a step value of increment
            Accepts hexStr as a string in format '#FFFFFF'
                    increment as an integer
            Returns newHexStr as a string in format '#FFFFFF'"""

        # deconstruct hex to red green blue
        rgbVal = [''] * 3
        rgbVal[0] = hexStr[1:3]     # red
        rgbVal[1] = hexStr[3:5]     # green
        rgbVal[2] = hexStr[5:]      # blue

        for i in range(3):
            if rgbVal[i] == '00':   # check if value already 0
                
                continue
            
            # convert hex to int
            rgbVal[i] = int(rgbVal[i], 16)

            if rgbVal[i] < 26:      # verify valid rgb value
                rgbVal[i] = '00'
            elif rgbVal[i] > 255:
                rgbVal[i] = 'ff'
            else:
                rgbVal[i] += increment
                rgbVal[i] = hex(rgbVal[i])
                rgbVal[i] = rgbVal[i][2:]   # remove the '0x' prefix in returned hex() method string

        newHexStr = '#' + rgbVal[0] + rgbVal[1] + rgbVal[2]

        return newHexStr

    def cosineHexVal(self, hexStr, radians):
        """Multiplies a normalized hex color value with a cosine function.
            Accepts hexStr as a string in format '#FFFFFF'
                    radians as a float
            Returns newHexStr as a string in format '#FFFFFF'"""

        # deconstruct hex to red green blue
        rgbValue = [''] * 3
        rgbValue[0] = hexStr[1:3]     # red
        rgbValue[1] = hexStr[3:5]     # green
        rgbValue[2] = hexStr[5:]      # blue
        for i in range(3):
            if rgbValue[i] == '00':   # check if value already 0
                
                continue

            # convert hex to int
            rgbValue[i] = int(rgbValue[i], 16)

            if round(rgbValue[i] * (math.cos(radians) + 1) / 2) < 26:      # verify valid rgb value
                rgbValue[i] = '00'
            elif rgbValue[i] > 255:
                rgbValue[i] = 'ff'
            else:
                rgbValue[i] = round(rgbValue[i] * (math.cos(radians) + 1) / 2)
                rgbValue[i] = hex(rgbValue[i])
                rgbValue[i] = rgbValue[i][2:]   # remove the '0x' prefix in returned hex() method string

        newHexStr = '#' + rgbValue[0] + rgbValue[1] + rgbValue[2]

        return newHexStr

    def advCosineHexVal(self, hexStr, endHexStr, radians):
        """Uses a cosine function normalized to be non-negative that is multiplied with the 
        difference between two corresponding hex string values. This is summed with hexStr 
        and returns as a combined hex string value.
            Accepts hexStr as a string in format '#FFFFFF'
                    radians as a float in radians for cos()
                    endHexStr as a string in format '#FFFFFF'
            Returns newHexStr as a string in format '#FFFFFF'"""

        # deconstruct hexStr to red green blue
        hexStrRGB = [''] * 3
        hexStrRGB[0] = hexStr[1:3]     # red
        hexStrRGB[1] = hexStr[3:5]     # green
        hexStrRGB[2] = hexStr[5:]      # blue

        # deconstruct endHexStr to red green blue
        endHexStrRGB = [''] * 3
        endHexStrRGB[0] = endHexStr[1:3]     # red
        endHexStrRGB[1] = endHexStr[3:5]     # green
        endHexStrRGB[2] = endHexStr[5:]      # blue
        tempRGB = [0] * 3

        for i in range(3):
            # convert hex to int
            hexStrRGB[i] = int(hexStrRGB[i], 16)
            endHexStrRGB[i] = int(endHexStrRGB[i], 16)

            # do the cosine magic
            tempRGB[i] = round(hexStrRGB[i] + (endHexStrRGB[i] - hexStrRGB[i]) * (math.cos(radians) + 1) / 2)

            # convert back to hex
            tempRGB[i] = hex(tempRGB[i])

            if len(tempRGB[i]) == 3:    # check if hex conversion results in single digit hex value
                tempRGB[i] = tempRGB[i].replace('0x', '0x0')
            tempRGB[i] = tempRGB[i][2:] # remove '0x' prefix

        newHexStr = '#' + tempRGB[0] + tempRGB[1] + tempRGB[2]

        return newHexStr

    def userScorePercentColorFade(self, startHexVal, increment):
        """Increments hex colour value of self.userScorePercentLabel to change to black in a gradient.
           Accepts startHexVal as a string in format '#FFFFFF'
                   increment as an integer/float if calling functions incrementHexVal/cosineHexVal"""

        # extract individual hex values
        red = startHexVal[1:3]
        green = startHexVal[3:5]

        if (red != '00') or green != '00': 
            newHexVal = self.cosineHexVal(startHexVal, increment)
            self.radiansTextCounter += math.pi/75     # comment when using self.incrementHexVal -- denominator controls num of iterations needed
            self.userScorePercentLabel['fg'] = newHexVal
            # self.userScorePercentLabel.after(self.changeSpeed, lambda : self.userScorePercentColorFade(newHexVal, increment)) # comment when using self.cosineHexVal()
            self.userScorePercentLabel.after(self.changeSpeed, lambda : self.userScorePercentColorFade(newHexVal, self.radiansTextCounter)) # comment when using self.incrementHexVal()
        else:
            return

    def userScoreBarColorFade(self, startHexValz, endHexValz, incrementz):
        """Increments hex colour value of self.userScorePercentLabel to change from the starting hex value color
        to the end hex color as a gradient.
           Accepts startHexVal as a string in format '#FFFFFF'
                   increment as an integer/float if calling functions incrementHexVal/advCosineHexVal
                   endHexValz as a string in format #FFFFFF"""

        if startHexValz.upper() != endHexValz.upper(): 
            newHexVal = self.advCosineHexVal(startHexValz, endHexValz, incrementz)
            self.radiansBarCounter += math.pi/75     # comment when using self.incrementHexVal -- denominator controls num of iterations needed
            self.userScoreCanvas.itemconfig(self.userColourBar, fill = newHexVal, outline = newHexVal)
            # self.userScorePercentLabel.after(self.changeSpeed, lambda : self.userScorePercentColorFade(newHexVal, increment)) # comment when using self.advCosineHexVal()
            self.userScoreCanvas.after(self.changeSpeed, lambda : self.userScoreBarColorFade(newHexVal, endHexValz, self.radiansBarCounter)) # comment when using self.incrementHexVal()
        else:
            return

    def updateTkinter(self, userChoice):
        """Accepts userChoice as an integer"""
        self.iterationNum += 1

        # get user and cpu predictions
        correctChoice = self.cnnModel.labels
        cpuChoice = self.cnnModel.pred

        print(self.labelList[correctChoice])

        # check if user and cpu made correct choice
        if userChoice == correctChoice:
            self.userCorrect += 1
            self.correctChoice = True
        else:
            self.correctChoice = False

        if cpuChoice == correctChoice:
            self.cpuCorrect += 1

        # change color of self.userScorePercentLabel on right (green) or wrong (red) choice
        if self.correctChoice:
            self.userScorePercentLabel['fg'] = self.correctAnsColor
            # self.userScorePercentColorFade(self.correctAnsColor, self.increment) # uncomment if using self.incrementHexVal()
            self.radiansTextCounter = 0                                                   # uncomment if using self.cosineHexVal()
            self.userScorePercentColorFade(self.correctAnsColor, self.radiansTextCounter) # uncomment if using self.cosineHexVal()
        else:
            self.userScorePercentLabel['fg'] = self.wrongAnsColor
            # self.userScorePercentColorFade(self.wrongAnsColor, self.increment) # uncomment if using self.incrementHexVal()
            self.radiansTextCounter = 0                                               # uncomment if using self.cosineHexVal()
            self.userScorePercentColorFade(self.wrongAnsColor, self.radiansTextCounter) # uncomment if using self.cosineHexVal()

        # update self.infoFrame labels
        self.userInfoDynamicLabel['text'] = str(int(self.userCorrect))
        self.cpuInfoDynamicLabel['text'] = str(int(self.cpuCorrect))
        self.numImagesInfoDynamicLabel['text'] = str(int(self.iterationNum))

        # re-calculate user and cpu correct percentages
        self.userCorrectPercent = self.userCorrect / self.iterationNum * 100
        self.cpuCorrectPercent = self.cpuCorrect / self.iterationNum * 100

        # update correct percentages
        self.userScorePercentLabel['text'] = self.updateScoreStrVar(self.userCorrectPercent)
        self.cpuScorePercentLabel['text'] = self.updateScoreStrVar(self.cpuCorrectPercent)

        # re-calculate score bar pixel width for user and cpu
        newUserBlackBarX2Pos, newUserColorX2Pos, significantChanges = self.updateScoreBarPosition(self.userCorrectPercent, self.oldUserPercent)
        self.userScoreCanvas.coords(self.userBlackBar, 0, 21, newUserBlackBarX2Pos, 57)
        self.userScoreCanvas.coords(self.userColourBar, newUserBlackBarX2Pos, 21, newUserColorX2Pos, 57)
        self.cpuScoreCanvas.coords(self.cpuScoreBar, 0, 21, self.updateScoreBarPixel(self.cpuCorrectPercent), 57)
        self.oldUserPercent = self.userCorrectPercent
        print(self.userScoreCanvas.coords(self.userBlackBar))
        print(self.userScoreCanvas.coords(self.userColourBar))

        # change color of self.userColorBar on right (green) or wrong (red) choice
        if significantChanges:
            if self.correctChoice:
                self.userScoreCanvas.itemconfig(self.userColourBar, fill = self.correctAnsColor, outline = self.correctAnsColor)
                self.radiansBarCounter = math.pi
                self.userScoreBarColorFade(self.correctAnsColor, self.blackColor, self.radiansBarCounter)
            else:
                self.userScoreCanvas.itemconfig(self.userColourBar, fill = self.wrongAnsColor, outline = self.wrongAnsColor)
                self.radiansBarCounter = math.pi 
                self.userScoreBarColorFade(self.wrongAnsColor, self.windowBGColor, self.radiansBarCounter)

        # update lastCorrectLabelVar with the correct choice for the image
        self.lastCorrectLabelVar['text'] = ' ' + self.labelList[self.cnnModel.labels]

        # update model and image for next iteration
        self.count += 1
        self.cnnModel.runModel(self.count)
        self.cnnModel.runImagePlotData()
        self.drawTensorImage()
