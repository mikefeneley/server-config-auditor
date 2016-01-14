
class apache_directive:

    def __init__(self, directive, value, scope, line_num):
       self.__directive = directive
       self.__value = value
       self.__scope = scope
       self.__line_num = line_num
    
    @property
    def directive(self):
    	return self.__directive
    
    @property
    def value(self):
    	return self.__value

    @property
    def score(self):
        return self.__scope

    @property
    def linenum(self):
        return self.__line_num