import src

if __name__ == "__main__":
    
    s = src.data_setup()
    data = {}
    while True:
        data = src.update_data(s, data)
        print(data)
    s.close()