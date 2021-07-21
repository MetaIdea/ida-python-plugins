#SAGE SOURCE CODE CPP CREATOR BY MJSTRAL aka METAIDEA
#Creates a complete pseudo cpp solution folder with correct cpp/h file and folder structure, names functions and exports them as c decompiled code to the files
#Use on bfme2 rotwk world builder in ida, (alt+F7 and choose this script)

import idaapi
import idautils
import ida_funcs
import idc
import re
import os
import errno

ExportPath = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') + "\\Bfme2RotwkSourceCode\\"

def NameFunctions():
	with open(ExportPath, "wb") as myfile:
		for functionName in idautils.Strings():
			if str(functionName).find("::") != -1 and re.match('^[a-zA-Z0-9_:~]+$',str(functionName)):
				i = 1
				xrefFunctionName = ""
				doChange = True
				for xref in XrefsTo(functionName.ea, 0):
					if i == 1:
						xrefFunctionName = idc.GetFunctionName(xref.frm)
					if xrefFunctionName.find("sub_") == -1 or xrefFunctionName != idc.GetFunctionName(xref.frm) or xrefFunctionName == "":
						doChange = False
						break
					i += 1
				if doChange:
					cleanedFunctionName = str(functionName).replace("~","")
					functionAdress = idaapi.get_func(xref.frm).start_ea
					idc.MakeName(functionAdress, cleanedFunctionName)
					myfile.write(cleanedFunctionName + " " + hex(functionAdress) + "\n")
		myfile.close()

def CreateFunctionList():
	functionNameList = []
	for functionName in idautils.Strings():
		if str(functionName).find("::") != -1 and re.match('^[a-zA-Z0-9_:~]+$',str(functionName)):
			i = 1
			xrefFunctionName = ""
			firstFunctionXref = 0
			doUse = True
			for xref in XrefsTo(functionName.ea, 0):
				if i == 1:
					xrefFunctionName = idc.GetFunctionName(xref.frm)
					firstFunctionXref = xref.frm
				if xrefFunctionName != idc.GetFunctionName(xref.frm):
					doUse = False
					break
				i += 1
			if doUse:
				#myfile.write(str(functionName) + " " + xrefFunctionName + "\n")
				if idaapi.get_func(firstFunctionXref):
					cleanedFunctionName = str(functionName).replace("~","")
					functionAdress = idaapi.get_func(firstFunctionXref).start_ea
					functionNameList.append((functionAdress,cleanedFunctionName))
	return functionNameList
	
def CreateFunctionListAllInlined():
	UseAllInlinedFunctionNames = True
	functionNameList = []
	for functionName in idautils.Strings():
		if str(functionName).find("::") != -1 and re.match('^[a-zA-Z0-9_:~]+$',str(functionName)):
			i = 1
			xrefFunctionName = ""
			functionAdress = 0
			for xref in XrefsTo(functionName.ea, 0):
				if idaapi.get_func(xref.frm) and (functionAdress != idaapi.get_func(xref.frm).start_ea or i == 1):
					functionAdress = idaapi.get_func(xref.frm).start_ea
					cleanedFunctionName = str(functionName).replace("~","")
					functionNameList.append((functionAdress,cleanedFunctionName))
				i += 1
	return functionNameList
	
def CreateSourceFilePathList():
	sourceFilePathList = []
	for filePath in idautils.Strings():
		if (str(filePath).find(".cpp") != -1 or str(filePath).find(".h") != -1) and str(filePath).find("\\") != -1 and str(filePath).find("(") == -1 and str(filePath).find("Invalid call") == -1:
			lastFunctionAdress = 0
			for xref in XrefsTo(filePath.ea, 0):
				if idaapi.get_func(xref.frm):
					functionAdress = idaapi.get_func(xref.frm).start_ea
					if functionAdress != lastFunctionAdress:
						lastFunctionAdress = functionAdress
						filepathFormat = FormatFilepath(str(filePath))
						sourceFilePathList.append((functionAdress,filepathFormat))
	return sourceFilePathList
					
def GetDecompiledFunctionString(functionAdress):
	tempfile = "temp.txt"
	VDRUN_NEWFILE = 0	
	start_keyword = "{:X}".format(functionAdress)  + ")"
	#print(start_keyword)
	end_keyword = "^}" #"// ALL OK"
	idaapi.decompile_many(tempfile, [functionAdress], VDRUN_NEWFILE)
	decompiled_function = ""
	start_found = False
	with open(tempfile, "rt") as myfile:
		for myline in myfile: 
			if start_found:
				decompiled_function += myline
				if re.match(end_keyword,myline): #if myline.find(end_keyword) != -1:
					return decompiled_function
			if myline.find(start_keyword) != -1:
				start_found = True
				
def FormatFilepath(filepath):
	filepath = filepath.replace("e:\\","")
	filepath = filepath.replace("E:\\","")
	filepath = filepath.replace("c:\\","")
	filepath = filepath.replace("C:\\","")
	filepath = filepath.replace("/","\\")
	filepath = ExportPath + filepath
	#print(filepath)
	return filepath
	
def CreateFolderStructure(filename):
	if not os.path.exists(os.path.dirname(filename)):
		try:
			os.makedirs(os.path.dirname(filename))
		except OSError as exc:
			if exc.errno != errno.EEXIST:
				raise
				
def AdjustFilePathList(filePathList):
	filePathListNew = []
	newFilePath = ""
	for i in range(len(filePathList)):
		newFilePath = filePathList[i][1].replace("Bfme2RotwkSourceCode\\Builds\\BFME2X\\Code\\production\\Code\\","")
		newFilePath = newFilePath.replace("Bfme2RotwkSourceCode\\builds\\bfme2x\\code\\production\\code\\","")
		newFilePath = newFilePath.replace("Bfme2RotwkSourceCode\\dev\\lotr\\bfme2\\production\\code\\","")
		newFilePath = newFilePath.replace("Bfme2RotwkSourceCode\\Source\\","GameEngine\\Source\\")
		newFilePath = newFilePath.replace("Bfme2RotwkSourceCode\\views\\","views\\")
		newFilePath = newFilePath.replace("Bfme2RotwkSourceCode\\..\\wwlib\\","Libraries\\Source\\WWVegas\\wwlib\\")
		newFilePath = newFilePath.replace("Bfme2RotwkSourceCode\\..\\wwmath\\","Libraries\\Source\\WWVegas\\wwmath\\")
		newFilePath = newFilePath.replace("Bfme2RotwkSourceCode\\..\\..\\libraries\\","Libraries\\")
		newFilePath = newFilePath.replace("Bfme2RotwkSourceCode\\..\\..\\gameengine\\","Gameengine\\")	
		newFilePath = newFilePath.replace("Bfme2RotwkSourceCode\\..\\..\\include\\","include\\")	
		newFilePath = newFilePath.replace("Bfme2RotwkSourceCode\\..\\..\\Libraries\\","Libraries\\")
		newFilePath = newFilePath.replace("Bfme2RotwkSourceCode\\..\\..\\Gameengine\\","Gameengine\\")	
		newFilePath = newFilePath.replace("Bfme2RotwkSourceCode\\..\\..\\Include\\","include\\")	
		filePathListNew.append((filePathList[i][0],newFilePath))
		# with open(ExportPath + "output.txt", "a") as myfile:
			# myfile.write(newFilePath + "\n")
			# myfile.close()
	return filePathListNew
		
def CreateSourceFilesAndFunctionNames():
	functionNameList = CreateFunctionList() #CreateFunctionList()
	sourceFilePathList = CreateSourceFilePathList()
	sourceFilePathList = AdjustFilePathList(sourceFilePathList)
	for sourceFilePath in sourceFilePathList:
		CreateFolderStructure(sourceFilePath[1])
		open(sourceFilePath[1], "a").close()
	for functionName in functionNameList:
		for sourceFilePath in sourceFilePathList:
			filename = re.search("[a-zA-Z0-9_]+(.h|.cpp)", sourceFilePath[1]).group()
			if functionName[0] == sourceFilePath[0]:
				print(functionName[1]  + " " + sourceFilePath[1])
				with open(sourceFilePath[1], "a") as myfile:
					myfile.write(functionName[1] + "\n")
					myfile.close()
					break

# def CreateSourceFilesAndFunctionNamesOld():
	# functionNameList = CreateFunctionListAllInlined() #CreateFunctionList()
	# sourceFilePathList = CreateSourceFilePathList()
	# sourceFilePathList = AdjustFilePathList(sourceFilePathList)
	# for sourceFilePath in sourceFilePathList:
		# CreateFolderStructure(sourceFilePath[1])
		# open(sourceFilePath[1], "a").close()
	# for functionName in functionNameList:
		# for sourceFilePath in sourceFilePathList:
			# filename = re.search("[a-zA-Z0-9_]+(.h|.cpp)", sourceFilePath[1]).group()
			# if functionName[0] == sourceFilePath[0]:
				# for sourceFilePathNext in sourceFilePathList:
					# if filename.lower() == re.search("[a-zA-Z0-9_]+(.h|.cpp)", sourceFilePathNext[1]).group().lower():
						# with open(sourceFilePathNext[1], "a") as myfile:
							# myfile.write(functionName[1] + "\n")
							# myfile.close()
							# break
							
def ExportFunctionsToFile():
	for filePath in idautils.Strings():
		if str(filePath).find(".cpp") != -1 or str(filePath).find(".h") != -1 and str(filePath).find("\\"):
			#filename = re.search("[a-zA-Z0-9_]+(.h|.cpp)", str(filePath)).group()
			#print(filename)
			filepathFormat = FormatFilepath(str(filePath))
			CreateFolderStructure(filepathFormat)
			with open(filepathFormat, "wb") as myfile:
				lastFunctionAdress = 0
				for xref in XrefsTo(filePath.ea, 0):
					functionAdress = idaapi.get_func(xref.frm).start_ea #idc.GetFunctionName(xref.frm)
					if functionAdress != lastFunctionAdress:
						functionString = GetDecompiledFunctionString(functionAdress)
						if functionString is not None:
							myfile.write(functionString + "\n\n")
							lastFunctionAdress = functionAdress
						else:
							print("Error: " + "{:X}".format(functionAdress)  + ")" + " " + filepathFormat)
							#idaapi.decompile_many(ExportPath + "error.txt", [functionAdress], 1)
						

CreateSourceFilesAndFunctionNames()

#todo change regex to include all function names for rename
#todo list all function declarations on top of the cpp/h file