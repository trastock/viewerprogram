import src
import numpy as np
import matplotlib.pyplot as plt
import math 

from PyQt6.QtWidgets import QWidget, QApplication, QVBoxLayout, QScrollArea, QSizePolicy, QLabel, QGridLayout, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QFont

import sys

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class My_Window(QWidget):
    def __init__(self, prog):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.canvases = {}
        self.prog = prog
        
        # Create scoreboard table for top half
        self.scoreboard_table = QTableWidget()
        self.scoreboard_table.setColumnCount(3)  # Number of columns
        self.scoreboard_table.setHorizontalHeaderLabels(["Name", "Series Score", "Total Score"])
        """ 
        # Create a placeholder widget for the top half
        self.top_placeholder = QLabel("Top Half Placeholder")
        self.top_placeholder.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        """
        # Set size policy for the table to expand horizontally
        self.scoreboard_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
       
       # Set default column widths (adjust as needed)
        self.scoreboard_table.setColumnWidth(0, 200)  # Name column
        self.scoreboard_table.setColumnWidth(1, 100)  # Total Score column
        self.scoreboard_table.setColumnWidth(2, 400)  # Series Score column
       
       # Set default row height and add spacing between rows
        self.scoreboard_table.verticalHeader().setDefaultSectionSize(50)  # Adjust row height (default is 30)
       
        # Set up a QScrollArea to hold the canvases in a grid
        self.scroll_area = QScrollArea()
        self.scroll_content = QWidget()
        self.scroll_layout = QGridLayout(self.scroll_content)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_content)

         # Add both widgets to the layout with stretch factors
        self.layout.addWidget(self.scoreboard_table, 1)
        self.layout.addWidget(self.scroll_area, 1)
        self.setLayout(self.layout)  # Set the layout once during initialization
        
        self.update_scoreboard()
        self.update_canvas()  # Update canvas when initializing the window
        # Set up a QTimer to call update_canvas periodically
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_canvas)
        self.timer.timeout.connect(self.update_scoreboard)
        self.timer.start(1000)  # Update every 1000 milliseconds (1 second)
        
        self.resizeEvent = self.adjust_sizes
    
    def adjust_sizes(self, event):
        # Calculate font size based on window width
        window_height = self.height()
        window_width = self.width()
        font_size = window_height // 50  # Adjust divisor as needed
        
        # Calculate column widths based on window width
        col_width_name = window_width // 3  # Adjust divisor as needed
        col_width_total = window_width // 3  # Adjust divisor as needed
        col_width_series = window_width // 3  # Adjust divisor as needed
       
        
        self.scoreboard_table.verticalHeader().setDefaultSectionSize(window_height // 19)  # Adjust row height (default is 30)
        
        # Update font for scoreboard table items
        font = QFont()
        font.setPointSize(font_size)
        self.scoreboard_table.setFont(font)
        
        # Update column widths for scoreboard table
        self.scoreboard_table.setColumnWidth(0, col_width_name)
        self.scoreboard_table.setColumnWidth(1, col_width_total)
        self.scoreboard_table.setColumnWidth(2, col_width_series)
        """ 
        # Redraw canvas widgets (if needed)
        for canvas in self.canvases.values():
            canvas.draw()
        """
    def update_scoreboard(self):
        # Populate and sort scoreboard with shooter data
        relay = "1"
        scoreboard_data = []
        for shooter in self.prog.competition.shooters.values():
            score_dict = {
                "Name": f"{shooter.firstname} {shooter.lastname}",
                "Tot": shooter.relays[relay]["result"],
                "NumShots": shooter.relays[relay]["num_shots"],
                "Score": []
            }
            for serie in shooter.relays[relay]["series"]:
                if "Serie" in serie:
                    score_dict["Score"].append(shooter.relays[relay]["series"][serie]["Tot"])
            
            # Calculate average score per shot
            if score_dict["NumShots"] > 0:
                score_dict["AvgScorePerShot"] = score_dict["Tot"] / score_dict["NumShots"]
            else:
                score_dict["AvgScorePerShot"] = 0
            
            scoreboard_data.append(score_dict)
        
        # Sort scoreboard data based on average score per shot
        scoreboard_data.sort(key=lambda x: x["AvgScorePerShot"], reverse=True)
        
        # Clear existing data in the scoreboard
        self.scoreboard_table.setRowCount(0)
        
        # Populate scoreboard table with sorted data
        for row_position, data in enumerate(scoreboard_data):
            self.scoreboard_table.insertRow(row_position)
            
            # Name column
            name_item = QTableWidgetItem(data["Name"])
            self.scoreboard_table.setItem(row_position, 0, name_item)
            
            # Series scores column (Switched with Total score)
            series_scores_str = ", ".join(map(str, data["Score"]))
            series_scores_item = QTableWidgetItem(series_scores_str)
            self.scoreboard_table.setItem(row_position, 1, series_scores_item)
            
            # Total score column (Switched with Series score)
            total_score_item = QTableWidgetItem(str(data["Tot"]))
            self.scoreboard_table.setItem(row_position, 2, total_score_item)

    
    def update_canvas(self):
        if prog.update_competitions():
            #prog.update_competitions()
            #print(self.prog.competition.shooters["100"])
            relay = "1"
            row, col = 0, 0
            max_cols = math.ceil(self.prog.competition.get_number_of_shooters_in_relay(relay)/2)  # Set the maximum number of columns for the grid
            print("Max columns", max_cols)
            for shooter in self.prog.competition.shooters.values():  
                #fig, ax = src.plot(shooter.relays[relay]["series"][shooter.active_serie])
                score_dict = {"Name": shooter.firstname + " " + shooter.lastname, "Tot": shooter.relays[relay]["result"], "Score": []}  # Example scoreboard data
                for serie in shooter.relays[relay]["series"]:
                    if "Serie" in serie:
                        print(serie)
                        score_dict["Score"].append(shooter.relays[relay]["series"][serie]["Tot"])
                fig, ax = src.plot(shooter.relays[relay]["series"][shooter.active_serie], score_dict)
                if not shooter.startnumber in self.canvases.keys():
                    canvas = FigureCanvasQTAgg(fig)
                    canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                    self.canvases[shooter.startnumber] = canvas
                    self.scroll_layout.addWidget(canvas, row, col)
                    
                    col += 1
                    if col >= max_cols:
                        col = 0
                        row += 1
                else:
                    plt.close(self.canvases[shooter.startnumber].figure)
                    self.canvases[shooter.startnumber].figure = fig
                    self.canvases[shooter.startnumber].draw()
                    #self.canvas.draw()
            #print(self.prog.competition.shooters)
            
            self.scroll_content.setLayout(self.scroll_layout)
            self.scroll_content.updateGeometry()
            self.scroll_content.adjustSize()


if __name__ == "__main__":
    logopic = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSMCeGz4Xab3Rxzhs8Hl3bBU9Iafs8FX4PIHg&s"
    sponsorpic = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSvI9l2PnRlWMs5wbvUc-HDNSE7FXth9p83Rg&s"
    
    prog = src.Program()
    
    
    prog.create_competition("Dubbeltest Juli 2024", "20/7-2024", "Nyköpings Skyttegille", 
                           "FR60PR", "6", "20", logopic, sponsorpic, "competitions")
    
    prog.competition.add_shooter("Emil", "Alakulju", "Nyköpings Skyttegille",)
    prog.competition.add_shooter("Erik", "Alakulju", "Södermalm och Liljeholmens Skytteförening")
    prog.competition.add_shooter("Alexander", "Devell", "Nyköping")
    prog.competition.add_shooter("Testshooter 1", "Lastname", "Nyköping")
    prog.competition.add_shooter("Testshooter 2", "Lastname", "Nyköping")
    prog.competition.add_shooter("Testshooter 3", "Lastname", "Nyköping")
    prog.competition.add_shooter("Testshooter 4", "Lastname", "Nyköping")
    prog.competition.add_shooter("Testshooter 5", "Lastname", "Nyköping")
    prog.competition.add_relay("10:00", "")
    prog.competition.add_relay("12:00", "")
    prog.competition.add_shooter_to_relay("100", "FR60PR", "Herr", 0, 0, "1")
    prog.competition.add_shooter_to_relay("100", "FR60PR", "Herr", 0, 0, "2")
    prog.competition.add_shooter_to_relay("101", "FR60PR", "Herr", 0, 0, "1")
    prog.competition.add_shooter_to_relay("101", "FR60PR", "Herr", 0, 0, "2")
    prog.competition.add_shooter_to_relay("102", "FR60PR", "HJ", 0, 0, "1")
    prog.competition.add_shooter_to_relay("102", "FR60PR", "HJ", 0, 0, "2")
    prog.competition.add_shooter_to_relay("103", "FR60PR", "Herr", 0, 0, "1")
    prog.competition.add_shooter_to_relay("104", "FR60PR", "Herr", 0, 0, "1")
    prog.competition.add_shooter_to_relay("105", "FR60PR", "Herr", 0, 0, "1")
    prog.competition.add_shooter_to_relay("106", "FR60PR", "Herr", 0, 0, "1")
    prog.competition.add_shooter_to_relay("107", "FR60PR", "Herr", 0, 0, "1")
    
    prog.competition.create_import(r"C:\Sius\SiusData", False)
    prog.setup_socket()
    
    #prog.create_competition()
    #prog.competition.import_from_hdf5(r"/home/emil/privata_proj/viewerprogram/competitions/Koxängtest.hdf5")
    #prog.competition.export_to_hdf5()
    #prog.competition.create_result("restest.pdf", "relay", "1")    
    
    #comp = src.competition()
    #comp.import_from_hdf5(r"C:\Users\emila\OneDrive - Linköpings universitet\Desktop\Nya skytteprogrammet\viewerprogram\competitions\Dubbeltest Juli 2024_old.hdf5")
    #   print("Test: ")
    #comp.export_to_hdf5()

    
    app = QApplication(sys.argv)
    window = My_Window(prog)
    window.show()
    #prog.competition.shooters["100"]["1"]["series"][prog.competition.shooters["100"].active_serie]
    
    #window.update_canvas()
    sys.exit(app.exec())
    
    while True:
        prog.competition.import_from_hdf5("competitions/Koxängtest.hdf5")
        #prog.competition.export_to_hdf5()
        for shooter in prog.competition.shooters.values(): 
            fig, ax = src.plot(shooter.relays["1"]["series"][shooter.active_serie])
            
            window.canvas = FigureCanvasQTAgg(fig)
        
        input("\nType Ctrl+C to exit. Press Enter to continue...")
        
        sys.exit(app.exec_())
    
    
    """
    try:
        while True:
            if not prog.update_competitions():
                #print("Nytt skott!")
                print(f"Resultat: {str(prog.competition.shooters["100"].relays["1"]["result"])} - {str(prog.competition.shooters["100"].relays["1"]["inner tens"])} *")
                print(f"Raw_shots\n {prog.competition.raw_shots}")
                #input("\nType Ctrl+C to exit. Press Enter to continue...")
            #prog.update_competitions()
            
    except KeyboardInterrupt:
        print("Program stopped by user.")
    """
    
    