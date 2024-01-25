import re
import glob

def extract_size(file_path):
    try:
        with open(file_path, 'r') as file:
            sdimacs = 0 
            numNNF  = 0
            lowNNF  = 0
            upNNF  = 0
            numCpog = 0
            lowCpog = 0
            upCpog  = 0
            for line in file:
                match = re.search(r'CHECK: Read CNF file with (\d+) variables and (\d+) clauses', line)
                if match:
                    sdimacs = match.group(2)
                    sdimacs = int(sdimacs) 
                match = re.search(r'Compressed POG has (\d+) nodes, root literal (\d+), and (\d+) defining clauses', line)
                if match:
                    if numNNF == 0:
                        lowNNF = match.group(3)
                        lowNNF = int(lowNNF)
                        numNNF = 1
                    else:
                        upNNF = match.group(3)
                        upNNF = int(upNNF)
                match = re.search(r'defining = (\d+) clauses', line)
                if match:
                    if numCpog == 0:
                        lowCpog = match.group(1)
                        lowCpog = int(lowCpog)
                        numCpog = 1
                    else:
                        upCpog = match.group(1)
                        upCpog = int(upCpog)
            return sdimacs, lowNNF, upNNF, lowCpog, upCpog 
                    
    except filenotfounderror:
        print(f"file not found: {file_path}")
    except exception as e:
        print(f"an error occurred: {e}")

    return none


def process_all_log_files():
    log_files = glob.glob(f"*.ssat_log")
    print(f"file path, sdimacs, lowNNF, upNNF, lowCpog, upCpog")
    for file_path in log_files:
        sdimacs, lowNNF,upNNF, lowCpog, upCpog = extract_size(file_path)
        if sdimacs is not None:
            print(f"{file_path}, {sdimacs}, {lowNNF}, {upNNF}, {lowCpog}, {upCpog}")
        else:
            print(f"{file_path}, Satisfying probability not found.")

# Example usage
process_all_log_files()
