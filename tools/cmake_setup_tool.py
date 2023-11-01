import os.path
import pathlib


# py_generated=directories : finds all directories within a root_dir and its subdirectory
#
# requires: dir=name (subdirectory)
def find_directories(root_dir: str, gen_params: dict, generated_lines: list):
    target_dir = f"{root_dir}/{gen_params['dir']}"
    for d in [d for d in os.listdir(f"{target_dir}") if not os.path.isfile(f"{target_dir}/{d}") if not d.startswith('.')]:
        generated_lines.append(f"{target_dir}/{d}".replace(root_dir+"/", ""))
        gen_params['dir'] += "/"+d
        find_directories(root_dir, gen_params, generated_lines)


# py_generated=files : finds all files within a root_dir and its sub_dir, with optional extensions
#
# requires: dir=name (subdirectory)
# optional: extensions=h|cpp (multiple extensions split by |)
def find_files(root_dir: str, gen_params: dict, generated_lines: list):
    target_dir = f"{root_dir}/{gen_params['dir']}"
    extensions = ()
    if 'extensions' in gen_params:
        extensions = gen_params["extensions"].split("|")
    for f in [f for f in os.listdir(f"{target_dir}") if not f.startswith('.')]:
        if os.path.isfile(f"{target_dir}/{f}"):
            file_extension = f.split('.')[1]
            if len(extensions) > 0:
                if file_extension in extensions:
                    generated_lines.append(f"{target_dir}/{f}".replace(root_dir+"/", ""))
            else:
                generated_lines.append(f"{target_dir}/{f}".replace(root_dir+"/", ""))
        else:
            gen_params['dir'] += "/"+f
            find_files(root_dir, gen_params, generated_lines)


# main parsing method, pass in the path of the CMakeLists.txt file with tags
def update_cmake_file(file_path: str):
    # output lines for file
    out_lines = []

    # open for read
    with open(file_path, 'r') as file:
        in_lines = file.readlines()
        generated_block = False

        # go through each line of the file
        for ln in in_lines:
            ln = ln.replace("\n", "")

            # if we're inside a generated block, ignore the input lines, as these will be overwritten
            if generated_block:
                # check for end of generated block
                if ln.find("/py_generated") >= 0:
                    generated_block = False
                    out_lines.append(ln)
                continue

            # add line to output
            out_lines.append(ln)

            # find generated block by keyword
            i = ln.find(" py_generated")
            if i == -1:
                # not found
                continue

            # we're inside a generated block, generate lines
            generated_block = True
            generated_lines = []

            # parse generation parameters, key/value pairs
            gen_params = {}
            for key_value in ln[i:].strip().split(' '):
                gen_params[key_value[0:key_value.find('=')]] = key_value[key_value.find('=')+1:]

            # invoke the correct generation method
            generated_type = gen_params["py_generated"]

            if generated_type == "directories":
                find_directories(os.path.dirname(file_path), gen_params, generated_lines)
            elif generated_type == "files":
                find_files(os.path.dirname(file_path), gen_params, generated_lines)

            print(f"{file_path} . ln {len(out_lines)} . {ln[i:]}")

            # get indentation
            indent_space = ""
            for s in ln:
                if s == " ":
                    indent_space += " "
                else:
                    break

            # append generated lines to output
            for gen_ln in generated_lines:
                out_lines.append(indent_space + gen_ln)
                print(f"{file_path} . ln {len(out_lines)} . . .  {gen_ln}")

    # replace file contents
    if len(out_lines) > 0:
        with open(file_path, 'w') as file:
            for ln in out_lines:
                file.write(ln + "\n")


# generates cmake include folders, files, assets for juce
# uses tags in the form of
#
# py_generated=type param1=value1 ...
# ...
# /py_generated
#
# to detect where to make changes
# see methods at beginning of file for available tag types
if __name__ == '__main__':
    print("UPDATING")
    print("...")

    # check all CMakeLists.txt files of this repo
    count = 0
    for path in pathlib.Path("../").rglob("CMakeLists.txt"):
        update_cmake_file(path.__str__())
        count += 1

    print("...")
    print(f"DONE, checked {count} CMakeLists.txt files")
