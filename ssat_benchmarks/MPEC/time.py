import re
import glob

def extract_runtime(file_path):
    try:
        with open(file_path, 'r') as file:
            sharpSSAT = 0 
            evalSSAT  = 0
            numGen    = 0
            numCheck  = 0
            lowGen    = 0
            lowCheck  = 0
            upGen     = 0
            upCheck   = 0
            overall   = 0
            for line in file:
                match = re.search(r'SSAT LOG: Elapsed time = (\d+(\.\d+)?)', line)
                if match:
                    sharpSSAT = match.group(1)
                    sharpSSAT = int(sharpSSAT) if '.' not in sharpSSAT else float(sharpSSAT)
                match = re.search(r'EVAL LOG: Elapsed time = (\d+(\.\d+)?)', line)
                if match:
                    evalSSAT = match.group(1)
                    evalSSAT = int(evalSSAT) if '.' not in evalSSAT else float(evalSSAT)
                match = re.search(r'GEN LOG: Elapsed time = (\d+(\.\d+)?)', line)
                if match:
                    if numGen == 0:
                        lowGen = match.group(1)
                        lowGen = int(lowGen) if '.' not in lowGen else float(lowGen)
                        numGen = 1 
                    else:
                        upGen = match.group(1)
                        upGen = int(upGen) if '.' not in upGen else float(upGen)
                match = re.search(r'FCHECK LOG: Elapsed time = (\d+(\.\d+)?)', line)
                if match:
                    if numCheck == 0:
                        lowCheck = match.group(1)
                        lowCheck = int(lowCheck) if '.' not in lowCheck else float(lowCheck)
                        numCheck = 1 
                    else:
                        upCheck = match.group(1)
                        upCheck = int(upCheck) if '.' not in upCheck else float(upCheck)
                match = re.search(r'OVERALL LOG: Elapsed time = (\d+(\.\d+)?)', line)
                if match:
                    overall = match.group(1)
                    overall = int(overall) if '.' not in overall else float(overall)
            return sharpSSAT, evalSSAT, lowGen, lowCheck, upGen, upCheck, overall
                    
    except filenotfounderror:
        print(f"file not found: {file_path}")
    except exception as e:
        print(f"an error occurred: {e}")

    return none


def process_all_log_files():
    log_files = glob.glob(f"*.ssat_log")
    print(f"SSAT, eval, lowGen, lowCheck, upGen, upCheck, overall")
    for file_path in log_files:
        sharpSSAT, evalSSAT, lowGen, lowCheck, upGen, upCheck, overall = extract_runtime(file_path)
        if sharpSSAT is not None:
            print(f"{file_path}, {sharpSSAT}, {evalSSAT}, {lowGen}, {lowCheck}, {upGen}, {upCheck}, {overall}")
        else:
            print(f"{file_path}, Satisfying probability not found.")

# Example usage
process_all_log_files()
