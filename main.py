import src
import numpy as np

if __name__ == "__main__":
    """
    s = src.data_setup()
    data = {}
    logopic = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSMCeGz4Xab3Rxzhs8Hl3bBU9Iafs8FX4PIHg&s"
    sponsorpic = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSvI9l2PnRlWMs5wbvUc-HDNSE7FXth9p83Rg&s"
    
    comp = src.competition("Dubbeltest Juli 2024", "20/7-2024", "Nyköpings Skyttegille", 
                           "FR60PR", "6", "20", logopic, sponsorpic, "competitions")
    comp.add_relay("11:00")
    comp.add_shooter("Emil", "Alakulju", "Herr", "Nyköping", "", "1")
    comp.add_shooter("Erik", "Alakulju", "Herr", "Nyköping", "", "1")
    comp.add_shooter("Alexander", "Devell", "HJ", "Nyköping", "", "1")
    comp.export_to_hdf5()
    """
    
    comp = src.competition()
    comp.import_from_hdf5(r"C:\Users\emila\OneDrive - Linköpings universitet\Desktop\Nya skytteprogrammet\viewerprogram\competitions\Dubbeltest Juli 2024_old.hdf5")
    print("Test: ")
    #comp.export_to_hdf5()
    
    """
    
    try:
        while True:
            data = src.update_data(s, data)
            comp.export_to_hdf5(data)
            #input("\nType Ctrl+C to exit. Press Enter to continue...")
            
    except KeyboardInterrupt:
        print("Program stopped by user.")
        s.close()
    
    """