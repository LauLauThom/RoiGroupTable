from javax.swing import JTable, JScrollPane, JButton
from java.awt.event import ActionEvent, ActionListener
from java.awt import *
from ij.gui import Roi, GenericDialog


class RoiGroupTable(Panel):
    """
    Implement a table with 2 columns: Roi group number and associated name.
    self table can be edited to set  names for roi groups
    """
    
    def __init__(self):
        
        #super(GridLayout(0,1)) # 1 column, as many rows as necessary
        super(RoiGroupTable, self).__init__(GridLayout(0,1)) # 1 column, as many rows as necessary
        #super()
        #self.setLayout(GridLayout(0,1))
        
        ### Table Panel ###
        # Prepare table data
        headers = ["Group number", "Name"]
        listNames = Roi.getGroupNames().split(",") # groupNames is a list then
        dataRows = [ [item[0]+1, item[1]] for item in enumerate(listNames)] # +1 since the group actually start at 1
        #print dataRows

        # Make the table pane
        table = JTable(dataRows, headers)
        #table.setPreferredScrollableViewportSize( Dimension(500, 70) )
        #table.setFillsViewportHeight(true)
              

        # Create the scroll pane and add the table to it.
        tablePane =  JScrollPane(table)
        #tablePane = ScrollPane()
        #tablePane.add(table)
        
        # Add the scrollpane to the main panel.
        self.add(tablePane)

    
    def showTable(self):
        """
        Create the GUI and show it.  For thread safety,
        self method should be invoked from the
        event-dispatching thread.
        """
        gd = GenericDialog("Roi-group table")
        gd.addPanel(self) # Add current table instance (a subclass of Panel to gd panel)
        gd.showDialog()
        
if __name__ in ['__builtin__', '__main__']:
    
    table = RoiGroupTable()
    table.showTable()
    
    # once table closed, check new name mapping
    #print Roi.getGroupNameMap()