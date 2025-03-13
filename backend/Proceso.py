import os
import pandas as pd

dataset_path = 'backend/dataset/Entrenamiento/'

def LoadCode():
    data = []
    for root, _, files in os.walk(dataset_path):
        for file in files:
            if file.endswith(".cs") or file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    code = f.read()
                    label = 1 if "CWE" in root else 0
                    data.append((code, label))

    return pd.DataFrame(data, columns=['code', 'label'])

if __name__ == '__main__':
    df = LoadCode()
    df.to_csv('backend/dataset/Codigos.csv', index=False)
    print("Dataset creado y guardado con exito!")