import argparse

from trainer import train
from processor import process

def output_result(final_data, output_file):
    with open(output_file, 'w') as file:
        for (word, wf) in final_data:
            print('{} {}'.format(word, wf or '').strip(), file=file)

def main(training_dir, test_file, output_file):
    print('Training...')
    training_data = train(training_dir)

    print('Processing...')
    final_data = process(training_data, test_file)
    
    print('Writing results...')
    output_result(final_data, output_file)

    print('Done.')

parser = argparse.ArgumentParser()
parser.add_argument('training_dir')
parser.add_argument('test_file')
parser.add_argument('output_file')
args = parser.parse_args()

main(args.training_dir, args.test_file, args.output_file)
