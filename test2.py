import h5py


with h5py.File(r"competitions\Dubbeltest Juli 2024.hdf5", "a") as f:
    f.create_dataset("competition_info/relays/Skjutlag 1/relay_number", data = "1")
    f.create_dataset("competition_info/relays/Skjutlag 2/relay_number", data = "2")
