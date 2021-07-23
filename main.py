# This is a sample Python script.
import re
import os


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Line:
    def __init__(self, line_num, keyword, indentation, expected, value):
        self.line_num = line_num
        self.keyword = keyword
        self.indentation = indentation
        self.expected = expected
        self.value = value

def getListOfFiles(dirName):
    listOfFile = os.listdir(dirName)
    allFiles = list()
    for entry in listOfFile:
        fullPath = os.path.join(dirName, entry)
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
    onlyjava = list()
    for dir in allFiles:
        if dir.__contains__(".java"):
            onlyjava.append(dir)

    return onlyjava

def read_file(filename):
    file = open(filename, 'r', encoding='utf-8')
    Lines = file.readlines()
    return Lines

def parse_file(Lines):
    count = 0
    objects = list()
    for line in Lines:
        count += 1
        if line.__contains__("assertEquals("):
            objects.append(Line(count-1, "isEqualTo", len(re.findall(r"^ *", line)[0]),
                                re.sub(r"^ ", "", (re.findall(r"\(.*,", line)[0]).replace('(', '', 1).replace(',', '', 1)),
                                re.sub(r"\)$", "", re.findall(r",.*\)", line)[0].replace(',', '', 1))))
        elif line.__contains__("assertNotEquals("):
            objects.append(Line(count - 1, "isNotEqualTo", len(re.findall(r"^ *", line)[0]),
                                re.sub(r"^ ", "", (re.findall(r"\(.*,", line)[0]).replace('(', '', 1).replace(',', '', 1)),
                                re.sub(r"\)$", "", re.findall(r",.*\)", line)[0].replace(',', '', 1))))
            # variables[0] = count
            # variables[1] = "isEqualTo"
            # variables[2] = len(re.findall(r"^ *", line)[0])
            # variables[3] = (re.findall(r"\(.*,", line)[0]).replace('(', '').replace(',', '')
            # variables[4] = re.sub(r"\)$", "", re.findall(r",.*\)", line)[0].replace(',', ''))
            # lines_var += variables
        elif line.__contains__("assertTrue("):
            objects.append(Line(count-1, "isTrue", len(re.findall(r"^ *", line)[0]),
                                "True",
                                re.sub(r"^\(", '', re.sub(r"\)$", "", re.findall(r"\(.*\)", line)[0]))))
        elif line.__contains__("assertFalse("):
            objects.append(Line(count-1, "isFalse", len(re.findall(r"^ *", line)[0]),
                                "False",
                                re.sub(r"^\(", '', re.sub(r"\)$", "", re.findall(r"\(.*\)", line)[0]))))
        elif line.__contains__("assertNull("):
            objects.append(Line(count-1, "isNull", len(re.findall(r"^ *", line)[0]),
                                "Null",
                                re.sub(r"^\(", '', re.sub(r"\)$", "", re.findall(r"\(.*\)", line)[0]))))
        elif line.__contains__("assertNotNull("):
            objects.append(Line(count-1, "isNotNull", len(re.findall(r"^ *", line)[0]),
                                "NotNull",
                                re.sub(r"^\(", '', re.sub(r"\)$", "", re.findall(r"\(.*\)", line)[0]))))
    return objects

class new_line:
    def __init__(self, line, line_num):
        self.line = line
        self.line_num = line_num

def remove_junit(lines):
    have_imported = False
    new_lines = list()
    for line in lines:
        if line.__contains__("import static org.junit.jupiter.api.Assertions"):
            if not have_imported:
                new_lines.append("import static org.assertj.core.api.Assertions.assertThat;\n")
                have_imported = True
        else:
            new_lines.append(line)
    return new_lines



def create_line(lines):
    new_lines= list()
    for line in lines:
        if line.keyword == "isEqualTo":
            new_lines.append(new_line(
                line.indentation * ' ' + 'assertThat(' + re.sub(r"^ ", "", line.value) + ').' + line.keyword + '(' + line.expected + ');' + '\n',
                line.line_num))
        elif line.keyword == "isNotEqualTo":
            new_lines.append(new_line(
                line.indentation * ' ' + 'assertThat(' + line.value + ').' + line.keyword + '(' + line.expected + ');' + '\n',
                line.line_num))
        elif line.keyword == "isTrue":
            new_lines.append(new_line(
                line.indentation * ' ' + 'assertThat(' + line.value + ').' + line.keyword + '();' + '\n',
                line.line_num))
        elif line.keyword == "isFalse":
            new_lines.append(new_line(
                line.indentation * ' ' + 'assertThat(' + line.value + ').' + line.keyword + '();' + '\n',
                line.line_num))
        elif line.keyword == "isNull":
            new_lines.append(new_line(
                line.indentation * ' ' + 'assertThat(' + line.value + ').' + line.keyword + '();' + '\n',
                line.line_num))
        elif line.keyword == "isNotNull":
            new_lines.append(new_line(
                line.indentation * ' ' + 'assertThat(' + line.value + ').' + line.keyword + '();' + '\n',
                line.line_num))
    return new_lines

def write_file(filename, lines):
    file = open(filename, 'w', encoding='utf-8')
    for line in lines:
        file.write(line)
    file.close()

def main():
    do_loop = True
    while do_loop == True:
        single_file = True
        want_single = input('Would you like to assertjify multiple files? ')
        if want_single == 'y' or want_single == 'Y' or want_single == 'yes' or want_single == 'Yes':
            single_file = False
        else:
            single_file = True
        if not single_file:
            base_path = input('Please input the base path of files to be assertjified: ')
            all_files = getListOfFiles(base_path)
            for file in all_files:
                try:
                    in_lines = read_file(file)
                    removed_imports = remove_junit(in_lines)
                    lines = parse_file(removed_imports)
                    repl_lines = create_line(lines)
                    for line in repl_lines:
                        removed_imports[line.line_num] = line.line
                    write_file(file, removed_imports)
                    print(f"{bcolors.OKGREEN}Assertjified "+ file + bcolors.ENDC)
                except:
                    print(f"{bcolors.FAIL}Failed to assertjify file \"" + file + f"\" . Most likely an assertion spans multiple lines an I am not smart enough to deal with it :P{bcolors.ENDC}")
        else:
            in_file = input('Please input the file to be assertjified: ')
            try:
                in_lines = read_file(in_file)
                removed_imports = remove_junit(in_lines)
                lines = parse_file(removed_imports)
                repl_lines = create_line(lines)
                for line in repl_lines:
                    removed_imports[line.line_num] = line.line
                write_file(in_file, removed_imports)
            except:
                print(f"{bcolors.FAIL}Failed to assertjify the file. Most likely an assertion spans multiple lines an I am not smart enough to deal with it :P{bcolors.ENDC}")
        want_loop = input('Do you want to assertjify another file? y/n')
        if want_loop == 'y' or want_loop == 'Y' or want_loop == 'yes' or want_loop == 'Yes':
            do_loop = True
        else:
            do_loop = False

    print(f"{bcolors.OKCYAN}Done assertjifying files. Have a nice day! :){bcolors.ENDC}");

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
