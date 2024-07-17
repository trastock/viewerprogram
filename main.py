import src
import numpy as np
import matplotlib.pyplot as plt

from PyQt6.QtWidgets import QWidget, QApplication, QVBoxLayout, QScrollArea, QSizePolicy
from PyQt6.QtCore import QTimer
import sys

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class My_Window(QWidget):
    def __init__(self, prog):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.canvases = {}
        self.prog = prog
        
        # Set up a QScrollArea to hold the canvases
        self.scroll_area = QScrollArea()
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_content)

        self.layout.addWidget(self.scroll_area)
        self.setLayout(self.layout)  # Set the layout once during initialization
        
        self.update_canvas()  # Update canvas when initializing the window
        # Set up a QTimer to call update_canvas periodically
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_canvas)
        self.timer.start(1000)  # Update every 1000 milliseconds (1 second)
    
    def update_canvas(self):
        if prog.update_competitions():
            #prog.update_competitions()
            #print(self.prog.competition.shooters["100"])
            relay = "1"
            print(prog.competition.raw_shots)
            for shooter in self.prog.competition.shooters.values():
                
                fig, ax = src.plot(shooter.relays[relay]["series"][shooter.active_serie])
                if not shooter.startnumber in self.canvases.keys():
                    canvas = FigureCanvasQTAgg(fig)
                    canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                    self.canvases[shooter.startnumber] = canvas
                    self.setLayout(self.layout)
                    
                    self.scroll_layout.addWidget(canvas) 
                else:
                    plt.close(self.canvases[shooter.startnumber].figure)
                    self.canvases[shooter.startnumber].figure = fig
                    self.canvases[shooter.startnumber].draw()
                    
                    #self.canvas.draw()
            #print(self.prog.competition.shooters)
            
            self.scroll_content.setLayout(self.scroll_layout)



if __name__ == "__main__":
    logopic = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSMCeGz4Xab3Rxzhs8Hl3bBU9Iafs8FX4PIHg&s"
    sponsorpic = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSvI9l2PnRlWMs5wbvUc-HDNSE7FXth9p83Rg&s"
    
    prog = src.Program()
    
    
    prog.create_competition("Dubbeltest Juli 2024", "20/7-2024", "Nyköpings Skyttegille", 
                           "FR60PR", "6", "20", logopic, sponsorpic, "competitions")
    
    prog.competition.add_shooter("Emil", "Alakulju", "Nyköpings Skyttegille",)
    prog.competition.add_shooter("Erik", "Alakulju", "Södermalm och Liljeholmens Skytteförening")
    prog.competition.add_shooter("Alexander", "Devell", "Nyköping")
    prog.competition.add_relay("10:00", "")
    prog.competition.add_relay("12:00", "")
    prog.competition.add_shooter_to_relay("100", "FR60PR", "Herr", 0, 0, "1")
    prog.competition.add_shooter_to_relay("100", "FR60PR", "Herr", 0, 0, "2")
    prog.competition.add_shooter_to_relay("101", "FR60PR", "Herr", 0, 0, "1")
    prog.competition.add_shooter_to_relay("101", "FR60PR", "Herr", 0, 0, "2")
    prog.competition.add_shooter_to_relay("102", "FR60PR", "HJ", 0, 0, "1")
    prog.competition.add_shooter_to_relay("102", "FR60PR", "HJ", 0, 0, "2")
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
    
    