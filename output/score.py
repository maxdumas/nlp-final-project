import argparse

parser = argparse.ArgumentParser()
parser.add_argument('key_file')
parser.add_argument('result_file')
args = parser.parse_args()

correct = incorrect = missing = new = total = all = 0
with open(args.result_file) as result:
    with open(args.key_file) as key:
        while True:
            r_line = result.readline().strip().split()
            k_line = key.readline().strip().split()

            if not r_line or not k_line:
                break
            if r_line[0] != k_line[0]:
                raise Exception('Misalignment at line ' + str(all))

            if len(r_line) == 2:
                r_key = r_line[1]

                if len(k_line) == 2:
                    if k_line[1] == r_key:
                        correct += 1
                    else:
                        print('Line {}: {} ≠ {}'.format(all + 1, r_line, k_line))
                        incorrect += 1
                else:
                    new += 1
                total += 1
            elif len(k_line) == 2:
                missing += 1
                total += 1

            all += 1

print()
print('█ Correct Matches: {}/{} ({}%) [in both, equal]'.format(correct, total, correct * 100 // total))
print('• Incorrect Matches: {}/{} ({}%) [in both but unequal]'.format(incorrect, total, incorrect * 100 // total))
print('▒ New Matches: {}/{} ({}%) [not in key, in result]'.format(new, total, new * 100 // total))
print('░ Missing Matches: {}/{} ({}%) [in key, not in result]'.format(missing, total, missing * 100 // total))
print('{} matches total (in either key or result) out of {} words total ({}%)'.format(total, all, total * 100 // all))
