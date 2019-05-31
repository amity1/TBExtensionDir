#!/usr/bin/env python3.6

import tkinter
from tkinter import tix
from tkinter import filedialog
from tkinter import messagebox

import os
from os import path

from xml import dom
from xml.dom import minidom

# constants
application_id = '{3550f703-e582-4d05-9a08-453d09bdfdc6}'

class InputVars:
  def __init__(self):
    self.dirName=''
    self.extId=''
    self.extName=''
    self.extVer=''
    self.creator=''
    self.minVer=''
    self.maxVer=''
    self.xulName=''
		
		
class DirectorySelector:
  def unmapEvent(self,evt):
      if(evt.widget==self.dialog):
        openDirButton['state']='active'
        
  def setDirName(self,x):
    # Create the direcory if does not exists, warn if not empty
    if (not path.exists(x)):
      try:
        os.mkdir(x)
      except PermissionError:
        messagebox.showerror('Error',"Cannot create directory: permission denied");
      vars1.dirName=path.realpath(x)
    elif (len(os.listdir(x))):
      ans=messagebox.askyesno('Warning','Directory "' + x + '" is not empty.' + "\nContinue with this directory?")
      if (ans):
          vars1.dirName=path.realpath(x)
    else:
      vars1.dirName=path.realpath(x)
    label2['text']=vars1.dirName
    self.dialog.destroy()

  def __init__(self):
    openDirButton['state']='disabled'
    self.dialog= tix.DirSelectDialog(root,command=self.setDirName);
    self.dialog.bind('<Unmap>',self.unmapEvent)
    self.dialog.popup()

def destroyEvent(evt):
    if (type(evt.widget)==tix.DirSelectDialog):
        print ('Mmmmmmmm')
    print (evt.widget.title());
    
def createRDF(varList):
    try:
        fd=open('install.rdf','w')
    except PermissionError:
        messagebox.showerror('Error','Cannot create \'install.rdf\': permission denied')
        return -1;

    rdfNS = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    emNS = 'http://www.mozilla.org/2004/em-rdf#'
    xmlDom = dom.getDOMImplementation()
    doc=xmlDom.createDocument(rdfNS,"RDF",None)
    elem=doc.documentElement;
    elem.setAttribute('xmlns',rdfNS)
    elem.setAttributeNS(rdfNS,'xmlns:em',emNS)
    desc=doc.createElement('Description')
    desc.setAttribute('about',"urn:mozilla:install-manifest")
    elem.appendChild(desc)
    newChild = doc.createElementNS(emNS,'em:id')
    desc.appendChild(newChild)
    textChild=doc.createTextNode(varList.extId)
    newChild.appendChild(textChild)
    newChild = doc.createElementNS(emNS,'em:name')
    desc.appendChild(newChild)
    textChild=doc.createTextNode(varList.extName)
    newChild.appendChild(textChild)
    newChild = doc.createElementNS(emNS,'em:version')
    desc.appendChild(newChild)
    textChild=doc.createTextNode(varList.extVer)
    newChild.appendChild(textChild)
    newChild = doc.createElementNS(emNS,'em:creator')
    desc.appendChild(newChild) 
    textChild=doc.createTextNode(varList.creator)
    newChild.appendChild(textChild)
    targetAppElem = doc.createElementNS(emNS,'em:targetApplication')
    desc.appendChild(targetAppElem)
    innerDesc=doc.createElement('Description')
    targetAppElem.appendChild(innerDesc)
    newChild = doc.createElementNS(emNS,'em:id')
    innerDesc.appendChild(newChild) 
    textChild=doc.createTextNode(application_id)
    newChild.appendChild(textChild) 
    newChild = doc.createElementNS(emNS,'em:minVersion')
    innerDesc.appendChild(newChild) 
    textChild=doc.createTextNode(varList.minVer)
    newChild.appendChild(textChild)
    newChild = doc.createElementNS(emNS,'em:maxVersion')
    innerDesc.appendChild(newChild) 
    textChild=doc.createTextNode(varList.maxVer)
    newChild.appendChild(textChild)
    print(doc);
    doc.writexml(fd,addindent='    ',newl="\n")
    fd.close()

def createChromeManifest(varList):
    ind = varList.extId.index('@')
    firstSegment = varList.extId[0:ind]
    fd=open('chrome.manifest','w')
    fd.write('content	' + firstSegment +"	/content\n")
    fd.write('overlay chrome://messenger/content/messenger.xul ')
    fd.write('chrome://' + firstSegment + '/content/' + varList.xulName + ".xul\n")
    fd.close()

def createXUL(varList):
    filename='content/' + varList.xulName + '.xul'
    fd=open(filename,'w')
    xmlDom = dom.getDOMImplementation()
    xulNS = "http://www.mozilla.org/keymaster/gatekeeper/there.is.only.xul"
    doc=xmlDom.createDocument(xulNS,'overlay',None)
    elem=doc.documentElement
    elem.setAttribute('id','sample')
    elem.setAttribute('xmlns',xulNS)
    textNode=doc.createTextNode('')
    elem.appendChild(textNode)
    doc.writexml(fd,addindent='    ',newl="\n")
    fd.close()

def myMkdir(dirName):
    try:
       os.mkdir(dirName)
    except FileExistsError:
       None

def buildTree(varList):
    os.chdir(varList.dirName)
    createRDF(varList)
    createChromeManifest(varList)
    myMkdir('chrome')
    myMkdir('content')
    createXUL(varList)
    open('content/overlay.js','w').close()
    myMkdir('chrome/locale')
    myMkdir('chrome/skin')
    myMkdir('defaults')
    myMkdir('defaults/preferences')
    
def submitFunc(varList):
    if(varList.dirName==''):
        messagebox.showerror('Error','No directory selected')
        return
    varList.extId=extIdText.get()
    if(varList.extId==''):
        messagebox.showerror('Error','Extension Id is empty')
        return    
    varList.extName=extNameText.get()
    varList.extVer=extVerText.get()
    varList.creator=creatorText.get()
    varList.minVer=minVerText.get()
    varList.maxVer=maxVerText.get()
    varList.xulName=xulNameText.get()

    buildTree(varList)
    messagebox.showinfo('Completed!', 'Completed! Check your new direcory: ' + varList.dirName)
    
#initialize
vars1 = InputVars()
# Start tk
root = tix.Tk()
root.title('TB Extension Tree Creator')
frame=tkinter.Frame(root)
label1=tkinter.Label(frame,text="Directory Location:")
label1.grid(row=0, column=0)
label2=tkinter.Label(frame,text='',width=80,bg='white',anchor=tkinter.W)
label2.grid(row=0, column=1)
openDirButton=tkinter.Button(frame,text='...',command=DirectorySelector)
openDirButton.grid(row=0,column=2,sticky=tkinter.W)
label3=tkinter.Label(frame,text='Extension Id(name@domain):')
label3.grid(row=1, column=0)
extIdText=tkinter.Entry(frame,width=20)
extIdText.grid(row=1, column=1,sticky=tkinter.W)
label4=tkinter.Label(frame,text='Extension Name:')
label4.grid(row=2,column=0)
extNameText=tkinter.Entry(frame,width=20)
extNameText.grid(row=2, column=1,sticky=tkinter.W)
label5=tkinter.Label(frame,text='Ext Version:')
label5.grid(row=3,column=0)
extVerText=tkinter.Entry(frame,width=10)
extVerText.grid(row=3,column=1,sticky=tkinter.W)
label6=tkinter.Label(frame,text='Creator:')
label6.grid(row=4,column=0)
creatorText=tkinter.Entry(frame,width=20)
creatorText.grid(row=4,column=1,sticky=tkinter.W)
label7=tkinter.Label(frame,text='TB Min Version:')
label7.grid(row=5,column=0)
minVerText=tkinter.Entry(frame,width='10')
minVerText.grid(row=5,column=1,sticky=tkinter.W)
label8=tkinter.Label(frame,text='TB Max Version:')
label8.grid(row=6,column=0)
maxVerText=tkinter.Entry(frame,width='10')
maxVerText.grid(row=6,column=1,sticky=tkinter.W)
label9=tkinter.Label(frame,text='XUL Name:')
label9.grid(row=7,column=0)
xulNameText=tkinter.Entry(frame,width=20)
xulNameText.grid(row=7, column=1,sticky=tkinter.W)

frame.pack()
submitButton=tkinter.Button(root,text='Submit',bg='red',fg='blue',
                            command=lambda: submitFunc(vars1))
submitButton.pack(side='bottom');
tkinter.Label(root).pack(side='bottom')
root.mainloop() 
