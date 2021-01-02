import os
import argparse

parser = argparse.ArgumentParser(description='Process Gender')
parser.add_argument('--g', required=True, default='man', type=str,help='Gender')

args = parser.parse_args()

file_path = 'data/{}face'.foramt(args.g[0])
file_names = os.listdir(file_path)

i = 0
for name in file_names:
    src = os.path.join(file_path, name)
    dst = os.path.join(file_path, '{}_{}.jpg'.format(args.g, i))
    os.rename(src, dst)
    i += 1