package ij.gui;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.*;

public class RoiGroupTable extends Panel {
	
    /**
	 * Implement a table with 2 columns: Roi group number and associated name.
     * This table can be edited to set new names for roi groups
	 */
	private static final long serialVersionUID = 1L;
	private RoiGroupTableModel tableModel;
    
    public RoiGroupTable() {
        super(new GridLayout(0,1)); // 1 column, as many rows as necessary
    	         
        this.tableModel = new RoiGroupTableModel(); 
        final JTable table = new JTable(tableModel);
        table.setPreferredScrollableViewportSize(new Dimension(500, 70));
        table.setFillsViewportHeight(true);
        
        // Handle row selection
        //table.getSelectionModel().addListSelectionListener(new RowListener());
        //table.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
        table.setRowSelectionAllowed(true);


        //Create the scroll pane and add the table to it.
        JScrollPane scrollPane = new JScrollPane(table);
        //ScrollPane scrollPane = new ScrollPane();
        //scrollPane.add(table);
        
        //Add the scroll pane to this panel.
        add(scrollPane);
        
        
        // LABEL PANEL
        JPanel labelPanel = new JPanel(new GridLayout(0,2));
        //Panel labelPanel = new Panel(new GridLayout(0,2));
        //Panel labelPanel = new Panel(); // looks bad when resizing
        
        // Add label 
        JLabel label1 = new JLabel("Group number");
        JLabel label2 = new JLabel("Name");
        labelPanel.add(label1);
        labelPanel.add(label2);
        add(labelPanel);
        
        
        // BUTTON PANNEL
        JPanel buttonPanel = new JPanel(new GridLayout(0,3));
        //Panel buttonPanel = new Panel();

        
        // Add spinner for group number
        SpinnerNumberModel rangeInt = new SpinnerNumberModel(0,0,255,1);
        final JSpinner spinner = new JSpinner(rangeInt); // final needed here for some reason
        buttonPanel.add(spinner);
        
        // Add text field for group name
        final JTextField nameField = new JTextField("new group");
        buttonPanel.add(nameField);
        
        
        // Class defining action of button : Adding a row to table
        class AddButton extends JButton implements ActionListener{
        	
        	public AddButton() {
        		super("Add/Update row");
        		this.addActionListener(this);
        	}
        				 
    		public void actionPerformed(ActionEvent event){
    			
    			// Get group number and name
    			SpinnerNumberModel spinModel = (SpinnerNumberModel) spinner.getModel();
    			int newNumber = spinModel.getNumber().intValue(); 
    			String newGroup = nameField.getText();
    			
    			// Check if group number already in table
    			Vector numbers = tableModel.getColumn(0);
    			int row = numbers.indexOf(newNumber);
    			
    			if ( row==-1 ) {
	    			// new Number not in table -> Add a new row
	    			tableModel.addRow(newNumber, newGroup);
    			}
    			else {
    				// Update existing row
    				tableModel.setValueAt(newGroup, row, 1);
    			}
    		}
        }
        
        // Button "Add Row"
        //JButton buttonAdd = new AddButton();
        buttonPanel.add(new AddButton());
        
        
        // Class defining action of button : Adding a row to table
        class DeleteButton extends JButton implements ActionListener{
        	
        	public DeleteButton() {
        		super("Delete selected row");
        		this.addActionListener(this);
        	}
        				 
    		public void actionPerformed(ActionEvent event){
    			
    			int row = table.getSelectedRow(); // _Had to set Table to final
    			
    			if ( row!=-1 ) tableModel.deleteRow(row);
    		}
        }
        
        buttonPanel.add(new DeleteButton());
                
        
        // Add button panel to main panel
        add(buttonPanel);
        
    }

    /**
     * Create the GUI and show it.  For thread safety,
     * this method should be invoked from the
     * event-dispatching thread.
     */
    public void showTable() {
    	GenericDialog gd = new GenericDialog("Roi-group table");
    	gd.addPanel(this); // Add current table instance to panel
    	gd.showDialog();
    	
    	if ( gd.wasOKed() ) {
	    	Vector<Integer> columnGroups = this.tableModel.getColumn(0);
	    	Vector<String> columnNames   = this.tableModel.getColumn(1); 
	    	
	    	int nRows = this.tableModel.getRowCount();
	    	Map<Integer, String> newMapping = new HashMap<Integer, String>(nRows);
	    	
	    	for (int i=0; i<nRows; i++) {
	    		newMapping.put( columnGroups.get(i) , columnNames.get(i) );
	    	
	    	Roi.setGroupNameMap(newMapping);
	    	}
    	}
    }
    
    public RoiGroupTableModel getTableModel(){ return this.tableModel; }

}
