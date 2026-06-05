import os

for c in os.listdir('dataset'):
    count = len(os.listdir(f'dataset/{c}'))
    print(f'{c}: {count} frames')