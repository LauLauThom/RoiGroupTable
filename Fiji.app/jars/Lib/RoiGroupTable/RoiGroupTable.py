"""
Define table panels, interactions and button actions 
"""
from javax.swing             import JButton, JTable, JScrollPane, JPanel, JLabel, SpinnerNumberModel, JSpinner, JTextField, JFileChooser
from javax.swing.filechooser import FileNameExtensionFilter
from java.awt       import GridLayout, Panel, Dimension 
from java.awt.event import ActionEvent, ActionListener 
from java.io import File
from ij.gui import GenericDialog, Roi 
from ij import IJ, Prefs
from RoiGroupTableModel import TableModel 
#from RoiGroupTable.RoiGroupTableModel import TableModel # for local tests 
 
class AddButton(JButton, ActionListener):  
	"""Class defining action of button : Adding a row to table"""
 
	def __init__(self, groupTable):  
		super(AddButton, self).__init__("Add row") 
		self.addActionListener(self)  
		self.groupTable = groupTable 
 
 
	def actionPerformed(self, event):  
		 
		# Get group name  
		groupName = self.groupTable.getNameField()   
		   
		# Check if group number already in table   
		tableModel = self.groupTable.tableModel  
		 
		n = tableModel.getRowCount() 
		tableModel.addRow(n+1, groupName) 
		 
  
 

class DeleteButton(JButton, ActionListener):  
	"""Class defining action of button : Adding a row to table"""
	 
	def __init__(self, groupTable):	  
		super(DeleteButton, self).__init__("Delete last row") 
		self.addActionListener(self)  
		self.groupTable = groupTable 
	 
	def actionPerformed(self, event):  
		"""Delete the last row""" 
		tableModel = self.groupTable.tableModel 
		nRows = tableModel.getRowCount() 
		if nRows>0: tableModel.deleteRow(nRows-1) 



class ImportButton(JButton, ActionListener): 
	"""Class defining action of button : importing mappings from a file"""
	
	def __init__(self, groupTable):	 
		super(ImportButton, self).__init__("Import from a file")
		self.addActionListener(self) 
		self.groupTable = groupTable
	
	def actionPerformed(self, event): 
		"""Delete the last row"""

		# Generate a save dialog
		dialog = JFileChooser( Prefs.get("roiGroup.importDir", "") )
		dialog.setSelectedFile( File("roiGroups.txt") )
		dialog.setFileFilter( FileNameExtensionFilter("Text file",["txt"]) )
		output = dialog.showOpenDialog(self.groupTable) # could be None argument too

		if output in [JFileChooser.CANCEL_OPTION, JFileChooser.ERROR_OPTION]: return
		selectedFile = dialog.getSelectedFile()
		directory    = selectedFile.getParent()
		Prefs.set("roiGroup.importDir", directory)
		if not selectedFile.isFile(): return 
		filePath = selectedFile.getPath()
		
		# Read comma-separated group from file
		with open(filePath, "r") as textFile:
			stringGroup = textFile.readline().rstrip()

		# Update table with content of file
		tableModel = self.groupTable.tableModel
		tableModel.setGroupColumn(stringGroup)


class ExportButton(JButton, ActionListener): 
	"""Class defining action of button : exporting mappings to a file"""
	
	def __init__(self, groupTable):	 
		super(ExportButton, self).__init__("Export to a file")
		self.addActionListener(self) 
		self.groupTable = groupTable
	
	def actionPerformed(self, event): 
		"""Delete the last row"""
		
		# Generate a save dialog
		dialog = JFileChooser( Prefs.get("roiGroup.exportDir", "") )
		dialog.setSelectedFile( File("roiGroups.txt") )
		dialog.setFileFilter( FileNameExtensionFilter("Text file",["txt"]) )
		
		output = dialog.showSaveDialog(self.groupTable) # could be argument None too
		
		if output in [JFileChooser.CANCEL_OPTION, JFileChooser.ERROR_OPTION]: return
		selectedFile = dialog.getSelectedFile()
		directory = selectedFile.getParent()
		Prefs.set("roiGroup.exportDir", directory)
		filePath = selectedFile.getPath()
		if not ("." in filePath): filePath += ".txt" # Add extension if missing

		# Write the groupString to the file
		groupString = self.groupTable.tableModel.getGroupString()
		with open(filePath, "w") as textFile: 
			textFile.write(groupString)
			
  
class Table(Panel):  
	"""
	Implement a table with 2 columns: Roi group number and associated name.  
	The table exposes the  
	- tableModel: the raw data 
	- table: a JTable which takes care of the visualization/interactions (clicks...)  
	"""
	  
	def __init__(self):  
		  
		super(Table, self).__init__(GridLayout(0,1)) # 1 column, as many rows as necessary 
		  
		self.tableModel = TableModel() 
		self.table = JTable(self.tableModel)  
		self.table.setPreferredScrollableViewportSize( Dimension(500, 100) )  
		self.table.setFillsViewportHeight(True)  
		  
		# Handle row selection  
		#table.getSelectionModel().addListSelectionListener( RowListener())  
		#table.setSelectionMode(ListSelectionModel.SINGLE_SELECTION)  
		self.table.setRowSelectionAllowed(True)  
  
  
		#Create the scroll pane and add the table to it.  
		scrollPane = JScrollPane(self.table)  
		#ScrollPane scrollPane =  ScrollPane()  
		#scrollPane.add(table)  
		  
		#Add the scroll pane to self panel.  
		self.add(scrollPane)  
		  
		  
		# LABEL PANEL  
		labelPanel = JPanel( GridLayout(0,1) ) 
		#Panel labelPanel =  Panel( GridLayout(0,2))  
		#Panel labelPanel =  Panel() # looks bad when resizing  
		  
		# Add label   
		labelName = JLabel("Name")  
		labelPanel.add(labelName)  
		self.add(labelPanel)  
		  
		  
		# BUTTON PANNEL  
		buttonPanel = JPanel( GridLayout(0,2) )  
		#Panel buttonPanel =  Panel()  
		  
		  
		# Add text field for group name  
		self.groupField = JTextField("new group")  
		buttonPanel.add(self.groupField)  
		 
		 
		# Button "Add Row"  
		#JButton buttonAdd =  AddButton()  
		buttonPanel.add( AddButton(self) )  
		buttonPanel.add( JLabel() ) # empty JLabel to fill the blank
		buttonPanel.add( DeleteButton(self) )  
		buttonPanel.add( ImportButton(self) ) 
		buttonPanel.add( ExportButton(self) )
		  
		# Finally add button panel to main panel  
		self.add(buttonPanel)  
 
 
	def getNameField(self): 
		"""Read the current state of the group name""" 
		return self.groupField.getText() 
		 
		  
	def showTable(self):  
		"""
		Add the main panel to a GenericDialog and show it 
		"""
		gd = GenericDialog("Roi-group table")  
		gd.addPanel(self) # Add current table instance to panel  
		gd.addMessage("""If you use this plugin, please cite: 
		
		Laurent Thomas. (2020, November 18). 
		LauLauThom/RoiGroupTable: ImageJ/Fiji RoiGroup Table (Version 1.0)
		Zenodo. http://doi.org/10.5281/zenodo.4279049""")
		gd.addHelp(r"https://github.com/LauLauThom/RoiGroupTable")
		gd.showDialog()  
		  
		if gd.wasOKed():  
			# Update ImageJ Roi group names mapping 
			stringGroup = self.tableModel.getGroupString()
			Roi.setGroupNames(stringGroup)  
	 
	 
	 
	def getTableModel(self):  
		return self.tableModel 
 
 
if __name__ in ['__builtin__', '__main__']: 
	"""
	Initialize a RoiGroupTable and show it. 
	"""
	table = Table() 
	 
	table.showTable()