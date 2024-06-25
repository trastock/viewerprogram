import src

if __name__ == "__main__":
    
    s = src.data_setup()
    data = {}
    comp = src.competition("Nyköping Open", "18/7-2024", "Nyköpings Skyttegille", "FR60PR", "6", "20")
    comp.add_relay("18:30")
    comp.add_shooter("Emil", "Alakulju", "Herr", "Nyköping", "", "1")
    comp.add_shooter("Erik", "Alakulju", "Dam", "Nyköping", "", "1")
    comp.add_shooter("Alexander", "Devell", "HJ", "Nyköping", "", "1")
    comp.create_import("C:\\Sius\\SiusData")
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