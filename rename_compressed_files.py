import os


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Rename processed files")
    parser.add_argument("dir_input", help='Directory with input images')
    parser.add_argument("dir_output", help='Directory with output images')
    args = parser.parse_args()
    # print the passed arguments

    if args.dir_input and args.dir_output:
        # process directory with images
        rootdir = args.dir_input

        for subdir, dirs, files in os.walk(rootdir):
            for file in files:
                full_path_image = os.path.join(subdir, file)
                abs_path_source = os.path.abspath(full_path_image)

                new_path_image = args.dir_output + '\\' + file.replace('_compressed', '')
                print(f'Source:      {abs_path_source}')
                print(f'Destination: {new_path_image}')

                os.rename(abs_path_source, new_path_image)
