import idaapi
import idautils
import idc
import re
import ida_funcs
import os

ExportPath = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') + "\\Source\\"

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
						

	
ExportFunctionsToFile()