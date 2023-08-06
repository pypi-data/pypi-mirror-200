import kabbes_client
import kabbes_menu
import py_starter as ps

class Client( kabbes_menu.Menu ):

    _BASE_DICT = {}

    def __init__( self, dict={}, _OVERRIDE_OPTIONS={} ):

        d = {}
        d.update( Client._BASE_DICT )
        d.update( dict )

        self.Package = kabbes_client.Package( kabbes_menu._Dir, dict=d )
        self.cfg_menu = self.Package.cfg

        cfg_options_node = self.cfg_menu[ kabbes_menu.Menu._OPTIONS_CFG_KEY ]
        cfg_options_node.load_dict( self._OVERRIDE_OPTIONS )
        cfg_options_node.load_dict( _OVERRIDE_OPTIONS )

        kabbes_menu.Menu.__init__( self )
