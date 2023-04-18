"""
Script to recursively download all bags from the scand archive.
Paths to the rosbags are stored in a csv file.
"""
import csv
import os
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description='Download all bags from scand archive.')
    parser.add_argument('--csv_file', type=str, help='Path to csv file.', default='download_links.csv')
    parser.add_argument('--output_dir', type=str, help='Path to output directory.', default='data/')
    parser.add_argument('--spot_only', action='store_true', help='Only download bags from spot.')
    parser.add_argument('--jackal_only', action='store_true', help='Only download bags from jackal.')
    args = parser.parse_args()
    
    # check if the data/ directory exists and is empty
    if not os.path.exists(args.output_dir):
        print('###############################################')
        print('Creating directory {}.'.format(args.output_dir))
        print('###############################################')
        os.mkdir(args.output_dir)
    else:
        if len(os.listdir(args.output_dir)) > 0:
            print('Directory {} is not empty. Please remove all files and try again.'.format(args.output_dir))
            sys.exit(1)
        

    # download all bags
    with open(args.csv_file, 'r') as f:
        # col1 is the bag number, col2 is the robot name, col3 is the link to the bag that we need to wget
        # wget the rosbag and save it in the output directory with the name <bag_number>_<robot_name>.bag
        reader = csv.reader(f)
        for row in reader:
            bag_number = row[0]
            robot_name = row[1]
            
            # check if we want to download only spot or jackal bags
            if args.spot_only and robot_name != 'spot': continue
            if args.jackal_only and robot_name != 'jackal': continue
            
            bag_link = row[2]
            bag_name = '{}_{}.bag'.format(bag_number, robot_name)
            # download the bag file from the bag_link, wait until the download is complete before moving on
            print('Downloading {} to {}.'.format(bag_link, bag_name))
            os.system('wget -O {} {}'.format(os.path.join(args.output_dir, bag_name), bag_link))
        
if __name__ == '__main__':
    main()