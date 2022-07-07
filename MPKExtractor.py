import sys
import glob
import os

# Extracts the file from the MPK file
def extract_file(file_name, file_offset, file_length, mpk_name):
    print("Extracting " + mpk_name + ": " + file_name + " (" + str(file_length) + " bytes)")
    mpkfile = open(mpk_name, "rb")
    mpkfile.seek(file_offset)
    tmp = mpkfile.read(file_length)
    mpkfile.close()
    outfile = open(file_name, "wb")
    outfile.write(tmp)
    outfile.close()

def list_archive_contents(mpkinfo_name):
    file = open(mpkinfo_name, "rb")
    file.read(4) # Skip the first 4 bytes (header)
    num_files = int.from_bytes(file.read(4), "little")
    for x in range(num_files):
        mpk_name = "Engine.mpk"
        name_length = int.from_bytes(file.read(2), "little")
        tmp = file.read(name_length)
        name = "".join(map(chr, tmp))
        file_offset = int.from_bytes(file.read(4), "little")
        file_length = int.from_bytes(file.read(4), "little")
        pak_index = int(int.from_bytes(file.read(4), "little") / 2)
        if(sys.argv[1] == resource_info):
            mpk_name = resource_files[pak_index]
        if(file_length > 0):
            print(mpk_name + ": " + name + ", length: " + str(file_length) + " bytes, offset: " + str(file_offset))

def unpack_archive(mpkinfo_name):
    file = open(mpkinfo_name, "rb")
    file.read(4) # Skip the first 4 bytes (header)
    num_files = int.from_bytes(file.read(4), "little")

    for x in range(num_files):
        mpk_name = "Engine.mpk"
        name_length = int.from_bytes(file.read(2), "little")
        tmp = file.read(name_length)
        name = "".join(map(chr, tmp))
        file_offset = int.from_bytes(file.read(4), "little")
        file_length = int.from_bytes(file.read(4), "little")
        pak_index = int(int.from_bytes(file.read(4), "little") / 2)
        if(sys.argv[1] == resource_info):
            mpk_name = resource_files[pak_index]
        if(file_length > 0):
            try:
                os.makedirs(os.path.dirname(name))
            except FileExistsError:
                pass

            extract_file(name, file_offset, file_length, mpk_name)

if(len(sys.argv) == 0):
    print("Usage: MPKExtractor.py <.mpkinfo> <-x|-l>")
    sys.exit(1)

basename = ""
resource_files = []
resource_info = ""

if(sys.argv[1].lower().endswith(".mpkinfo")):
    # fix mismatching file names for Resource*.mpk
    if(sys.argv[1].lower().startswith("resource")):
        basename = "Resources" 
    else:
        basename = sys.argv[1].split(".")[0]

    mpk_files = glob.glob(basename + "*.mpk")

    resource_files.append(basename + ".mpk")

    for index, x in enumerate(mpk_files):
        if(index > 0):
            resource_files.append(basename + str(index) + '.mpk')    

    resource_info = sys.argv[1]

    if(sys.argv[2] == "-l"):
        list_archive_contents(sys.argv[1])
    elif(sys.argv[2] == "-x"):
        unpack_archive(sys.argv[1])

else:
    print("Usage: MPKExtractor.py <.mpkinfo> <-x|-l>")
    sys.exit(1)
