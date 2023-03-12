import argparse
import csv
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str)
    parser.add_argument('--venmo', type=str, required=False)
    return parser.parse_args()

def parse_csv(file_path, venmo_dict):
    net_dict = {}
    with open(file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            add_net(row, net_dict, venmo_dict)

    print_payments(net_dict)

def parse_venmo(venmo_path, venmo_dict):

    with open(venmo_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            add_venmo(row, venmo_dict)
def add_venmo(row, venmo_dict):
    venmo_dict[row['Prefix'].lower()] = {
        'name': row['Name'],
        'venmo': row['Venmo']
    }

def add_net(row, net_dict, venmo_dict):
    nickname = row['player_nickname'].split()[0]
    name = venmo_dict[nickname.lower()]['venmo'] if nickname.lower() in venmo_dict else nickname
    row_net = int(row['net'])
    net = row_net if name not in net_dict else net_dict[name] + row_net
    net_dict[name] = net

def print_payments(net_dict):
    sorted_dict = sorted(net_dict.items(), key=lambda x:x[1], reverse=True)
    sorted_dict = [list(ele) for ele in sorted_dict]
    # print(sorted_dict)

    winner_index = 0
    loser_index = len(sorted_dict) - 1

    while winner_index < loser_index:
        winner_remaining = sorted_dict[winner_index][1]
        loser_remaining = sorted_dict[loser_index][1]
        winner_to_request = min(winner_remaining, abs(loser_remaining))

        # print amount
        print(sorted_dict[winner_index][0] + ' Request ' + str(winner_to_request/100) + ' From ' + sorted_dict[loser_index][0])

        sorted_dict[winner_index][1] = winner_remaining - winner_to_request
        sorted_dict[loser_index][1] += winner_to_request

        if sorted_dict[winner_index][1] == 0:
            winner_index += 1

        if sorted_dict[loser_index][1] == 0:
            loser_index -= 1

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    args = parse_args()
    venmo_dict = {}
    if args.venmo:
        parse_venmo(args.venmo, venmo_dict)
    parse_csv(args.path, venmo_dict)
