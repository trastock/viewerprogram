import src

if __name__ == "__main__":
    
    s = src.data_setup()
    data = {}
    comp = src.competition("Nyköping Open", "18/7-2024", "Nyköpings Skyttegille", "FR60PR")
    comp.add_shooter("Emil", "Alakulju", "22", "", "1")
    comp.add_shooter("Erik", "Alakulju", "26", "", "3")
    comp.add_shooter("Alexander", "Devell", "17", "", "2")
    
    try:
        while True:
            
            data = src.update_data(s, data)
            comp.export_to_hdf5(data)
            input("\nType Ctrl+C to exit. Press Enter to continue...")
            
    except KeyboardInterrupt:
        print("Program stopped by user.")
        s.close()