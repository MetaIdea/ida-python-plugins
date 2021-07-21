import idaapi
import idautils
import idc

ExportPath = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') + "\\output.txt"

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
				
NameFunctions()