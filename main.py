import src
import numpy as np

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
    prog.competition.add_shooter_to_relay("100", "FR60PR", "Herr", "", "1")
    prog.competition.add_shooter_to_relay("100", "FR60PR", "Herr", "", "2")
    prog.competition.add_shooter_to_relay("101", "FR60PR", "Herr", "", "1")
    prog.competition.add_shooter_to_relay("101", "FR60PR", "Herr", "", "2")
    prog.competition.add_shooter_to_relay("102", "FR60PR", "HJ", "", "1")
    prog.competition.add_shooter_to_relay("102", "FR60PR", "HJ", "", "2")
    prog.competition.create_import(r"C:\Sius\SiusData", False)
    prog.setup_socket()
        
    
    #comp = src.competition()
    #comp.import_from_hdf5(r"C:\Users\emila\OneDrive - Linköpings universitet\Desktop\Nya skytteprogrammet\viewerprogram\competitions\Dubbeltest Juli 2024_old.hdf5")
    #   print("Test: ")
    #comp.export_to_hdf5()
    
    
    
    
    try:
        while True:
            prog.update_competitions()
            #comp.export_to_hdf5(data)
            input("\nType Ctrl+C to exit. Press Enter to continue...")
            
    except KeyboardInterrupt:
        print("Program stopped by user.")
    
    