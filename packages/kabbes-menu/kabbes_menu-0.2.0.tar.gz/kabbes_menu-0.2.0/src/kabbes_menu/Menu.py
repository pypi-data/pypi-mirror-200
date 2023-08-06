import kabbes_menu
from parent_class import ParentClass
import py_starter as ps
import functools


def run_wrapper( method ):

    @functools.wraps( method )
    def wrapper( self, *args, **kwargs ):

        self.pre_run()
        output = method( self, *args, **kwargs )
        self.post_run()

        return output

    return wrapper

class Menu( ParentClass ):

    _OVERRIDE_OPTIONS = {}
    _SEARCHABLE_ATTS = []
    _ONE_LINE_ATTS = ['type']
    _OPTIONS_CFG_KEY = 'options'

    def __init__( self ):

        ParentClass.__init__( self )

        self._Children = []
        self.RTI = kabbes_menu.CRTI( self )

    def __len__( self ):
        return len(self._Children)
    def __iter__( self ):
        self.i = -1
        return self
    def __next__( self ):
        self.i += 1
        if self.i < len(self):
            return self._Children[self.i]
        raise StopIteration

    def display( self ):
        return self.print_one_line_atts( print_off = False )

    def do_nothing( self ):
        pass

    def run_Child_user( self ):
        Child = self.get_Child_user()
        if Child != None:
            Child.run()

    def get_Child_user( self ):
        Child = ps.get_selection_from_list( list(self), allow_null=True )
        return Child

    def run_method_user( self ):
        method = input('method: ')
        print ( self.run_method( method ) )

    def run_RTI_choice( self, choice ):
        choice.run()

    def string_found_in_Children( self, string ):

        viable_Children = []
        for att in self._SEARCHABLE_ATTS:
            if string in str( self.get_attr(att) ).lower():
                viable_Children.append( self )
                break

        for Child in self:
            viable_Children.extend( Child.string_found_in_Children( string ) )

        return viable_Children

    @run_wrapper
    def run( self ):

        while True:

            self.print_one_line_atts()
            for i in [ '{i}. {option_view}'.format( i=key, option_view=value[0] ) for key,value in self.cfg_menu[Menu._OPTIONS_CFG_KEY].get_dict().items() ]:
                print (i)
            choice, user_input = self.RTI.get_one_input()

            if choice != None:
                self.run_RTI_choice( choice )
                continue

            if user_input == '':
                break
            
            if user_input in self.cfg_menu[Menu._OPTIONS_CFG_KEY].nodes:
                self.run_method( self.cfg_menu[Menu._OPTIONS_CFG_KEY].nodes[user_input].get_ref_value()[-1] )

        self.exit()

    def pre_run( self ):
        pass

    def post_run( self ):
        pass

    def exit( self ):
        pass


