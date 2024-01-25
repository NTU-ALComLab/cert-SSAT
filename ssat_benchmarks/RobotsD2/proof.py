import re
import glob

def extract_satisfying_probability(file_path):
    try:
        with open(file_path, 'r') as file:
            probability = '-1'
            sharpSSAT = 0 
            evalSSAT  = 0
            lowGen    = 0
            lowCheck  = 0
            upGen     = 0
            upCheck   = 0
            overall   = 0
            for line in file:
                match = re.search(r'# satisfying probability = (\d+(\.\d+)?)', line)
                if match:
                    probability = match.group(1)
                    probability = int(probability) if '.' not in probability else float(probability)
                match = re.search(r'SSAT OUTCOME: normal', line)
                if match:
                    sharpSSAT = 1 
                match = re.search(r'EVAL OUTCOME: normal', line)
                if match:
                    evalSSAT = 1 
                match = re.search(r'GEN OUTCOME: normal', line)
                if match:
                    if lowGen == 0:
                        lowGen = 1 
                    else:
                        upGen = 1
                match = re.search(r'FCHECK OUTCOME: normal', line)
                if match:
                    if lowCheck == 0:
                        lowCheck = 1 
                    else:
                        upCheck = 1
                match = re.search(r'OVERALL OUTCOME: normal', line)
                if match:
                    overall = 1 
            return probability, sharpSSAT, evalSSAT, lowGen, lowCheck, upGen, upCheck, overall
                    
    except filenotfounderror:
        print(f"file not found: {file_path}")
    except exception as e:
        print(f"an error occurred: {e}")

    return none


def process_all_log_files():
    log_files = glob.glob(f"*.ssat_log")
    print(f"prob,  SSAT, eval, lowGen, lowCheck, upGen, upCheck, overall")
    for file_path in log_files:
        probability, sharpSSAT, evalSSAT, lowGen, lowCheck, upGen, upCheck, overall = extract_satisfying_probability(file_path)
        if probability is not None:
            print(f"{file_path},  {probability},  {sharpSSAT}, {evalSSAT}, {lowGen}, {lowCheck}, {upGen}, {upCheck}, {overall}")
        else:
            print(f"{file_path}, Satisfying probability not found.")

# Example usage
process_all_log_files()
