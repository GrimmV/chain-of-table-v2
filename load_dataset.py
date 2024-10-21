import json

def load_dataset(
    dataset_path,
    first_n=-1,
):
    dataset = []
    if first_n != -1:
        all_lines = []
        for line in open(dataset_path):
            all_lines.append(line)
            if len(all_lines) >= first_n: break
    else:
        all_lines = open(dataset_path).readlines()
    for i, line in enumerate(all_lines):
        info = json.loads(line)
        dataset.append(info)
    return dataset