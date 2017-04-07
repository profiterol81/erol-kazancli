import java.awt.BorderLayout;
import java.awt.EventQueue;

import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.border.EmptyBorder;
import javax.swing.JButton;
import java.awt.event.ActionListener;
import java.io.File;
import java.awt.event.ActionEvent;
import javax.swing.JFileChooser;
import javax.swing.JLabel;
import javax.swing.JOptionPane;

public class PlannerFrame extends JFrame {

	private JPanel contentPane;

	/**
	 * Launch the application.
	 */
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					PlannerFrame frame = new PlannerFrame();
					frame.setLocation(50, 50);
			        frame.setLocationRelativeTo(null);
					frame.setVisible(true);
					frame.setTitle("PAR: Linear Planner");
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}

	/**
	 * Create the frame.
	 */
	public PlannerFrame() {
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(100, 100, 500, 300);
		contentPane = new JPanel();
		contentPane.setBorder(new EmptyBorder(5, 5, 5, 5));
		setContentPane(contentPane);
		contentPane.setLayout(null);
		
		final JLabel lblNewLabel = new JLabel("");
		lblNewLabel.setBounds(171, 77, 273, 16);
		contentPane.add(lblNewLabel);
		
		final JLabel lblNewLabel_1 = new JLabel("");
		lblNewLabel_1.setBounds(171, 175, 273, 16);
		contentPane.add(lblNewLabel_1);
		
		final JLabel lblNewLabel_2 = new JLabel("");
		lblNewLabel_2.setBounds(171, 203, 273, 16);
		contentPane.add(lblNewLabel_2);
		
		final JLabel lblNewLabel_3 = new JLabel("");
		lblNewLabel_3.setBounds(171, 231, 273, 16);
		contentPane.add(lblNewLabel_3);
		
		JButton btnNewButton_1 = new JButton("Start Planner");
		btnNewButton_1.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				String fileName = lblNewLabel.getText();
				if (fileName.equals("")) {
					String message = "Please select a test file before running the planner";
					String title = "Planner: Error";
					JOptionPane.showMessageDialog(getParent(), message, title, JOptionPane.ERROR_MESSAGE);
					return;
				}
				Building a = new Building();
		        a.readConfFile(lblNewLabel.getText());
		        a.start(fileName.replace(".txt", ""));
		        File file = new File(fileName);
		        lblNewLabel_1.setText(file.getName().replace(".txt", "Plan.txt"));
		        lblNewLabel_2.setText(file.getName().replace(".txt", "Goal.txt"));
		        lblNewLabel_3.setText(file.getName().replace(".txt", "States.txt"));
		        
				String message = "Planner finished. Please check output files for result";
				String title = "Planner: Finished";
				JOptionPane.showMessageDialog(getParent(), message, title, JOptionPane.INFORMATION_MESSAGE);
			
			}
		});
		btnNewButton_1.setBounds(50, 128, 150, 29);
		contentPane.add(btnNewButton_1);
		
		JButton btnNewButton = new JButton("Choose File");
		btnNewButton.setBounds(50, 36, 150, 29);
		contentPane.add(btnNewButton);
		
		JLabel lblOutputFiles = new JLabel("Output Files:");
		lblOutputFiles.setBounds(60, 175, 100, 16);
		contentPane.add(lblOutputFiles);
		
		JLabel lblInputFile = new JLabel("Input File:");
		lblInputFile.setBounds(60, 77, 78, 16);
		contentPane.add(lblInputFile);
		
		
		btnNewButton.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				
				JFileChooser fc = new JFileChooser(System.getProperty("user.dir"));

		        fc.setFileSelectionMode(JFileChooser.FILES_ONLY);
		        fc.setMultiSelectionEnabled(false);
				
			    int returnVal = fc.showOpenDialog(PlannerFrame.this);

			    if (returnVal == JFileChooser.APPROVE_OPTION) {
			    	String sourceFile = fc.getSelectedFile().getAbsolutePath();
			    	lblNewLabel.setText(sourceFile); 
			   } 
			}
		});
	}                                              
}
