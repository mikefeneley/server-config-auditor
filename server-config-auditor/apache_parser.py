import os
import glob

""" ApacheConfParser is used to tokenize config files and couple them
 with relevant information such as file and line number"""
class ApacheConfParser:

    def __init__(self, server_root):
        self.server_root = server_root

    """ Returns a list of DirectiveInfo objects for all parse_objects 
        contained by parse_object. If parse_object is a file, this 
        includes all directives in the file and in files included by
        the file. If parse_object is a directory, it includes all the
        directives of files in the directory and its subdirectories"""
    def parse_apache_conf(self, parse_object):
        directives_list = []

        # Return list of directives contained in files located in
        # directory "parse_object"
        if os.path.isdir(parse_object):
            for root, dirs, files, in os.walk(parse_object):
                for file_object in files:
                    file_path = os.path.join(root, file_object)
                    directives_list += self.parse_apache_conf(file_path)
            return directives_list

        # Return list of all directives in parse_object and those
        # in files included by parse_objectt
        elif os.path.isfile(parse_object):
            conf_file = open(parse_object, "r")

            directives_list = self.preprocess_conf(conf_file)

            for i in range(0, len(directives_list)):
                directive = directives_list[i].get_directive()
                options = directives_list[i].get_options()

                if directive == "Include" or directive == "IncludeOptional":
                    include_option = options[0]
                    include_abspath = os.path.join(
                        self.server_root, include_option)
                    matching_paths = glob.glob(include_abspath)

                    for object_path in matching_paths:
                        directives_list += self.parse_apache_conf(object_path)
            return directives_list
        else:
            return -1


    """ Parse a configuration file and return all directives in a list
        of directive_info objects"""
    def preprocess_conf(self, config_file):

        first_parse = []
        second_parse = []
        third_parse = []

        for line in config_file:
            first_parse.append(line)

        # Combine all multiline directives
        i = 0
        while i < len(first_parse):
            next = i + 1
            line = first_parse[i]
            complete_line = line
            while line[len(line) - 2] == '\\' and next < len(first_parse):
                line = first_parse[next]
                complete_line = complete_line[0:len(complete_line) - 2] + line
                next += 1
            second_parse.append((complete_line, i))
            i = next

        # Tokenize and append directive information
        i = 0
        while i < len(second_parse):
            directive_info = second_parse[i]
            directive = directive_info[0]
            line_num = directive_info[1]
            filtered_directive = directive.replace("\t", " ")
            filtered_directive = filtered_directive.strip("\n ")
            if filtered_directive != "" and filtered_directive[0] != '#':
                tokens = filtered_directive.split()
                directive = tokens[0]
                options = tokens[1:len(tokens)]
                line = DirectiveLine(directive, options)
                info = DirectiveInfo(line, line_num, config_file.name)
                third_parse.append(info)
            i += 1

        return third_parse


""" Directive info holds directive as well as information useful
    for recomendation reporting such as filenames and line numbers"""
class DirectiveInfo:
    def __init__(self, directive_line, line_num, filename):
        self.directive_line = directive_line
        self.line_num = line_num
        self.filename = filename

    def get_directive(self):
        return self.directive_line.directive

    def get_options(self):
        return self.directive_line.options

    def get_line_num(self):
        return self.line_num

    def get_line(self):
        line = list(self.directive_line.options)
        directive = self.get_directive()
        line.insert(0, directive)
        return line

    def get_filename(self):
        return self.filename

    def status(self):
        print self.get_directive(), self.get_options(), self.get_line_num(), self.get_filename()

class DirectiveLine:
    def __init__(self, directive, options):
        self.directive = directive
        self.options = options