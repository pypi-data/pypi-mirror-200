from parent_class import ParentClass, ParentPluralDict
import py_starter as ps

class AWS_Cred (ParentClass) :

    """Class for storing one instance of a singular AWS Role and its associated credentials
    role: AWS role associated 
    dict: contains each key-value combination for each environment variable and its value
    string: contains a string representation of the dictionary, "key=value"
    """

    BEGIN_ROLE = '['
    END_ROLE = ']'

    _IMP_ATTS = ['role','string','dict']
    _ONE_LINE_ATTS = ['type','role']

    def __init__( self, role = None, dict = {}, string = ''):

        """If initialized with a dict, role must be provided
        if initialized with a string, the role must be contained in [square brackets up to]"""

        ParentClass.__init__( self )

        self.role = role
        self.dict = dict
        self.string = string

        if string != '' and dict == {}:
            self._string_to_dict()
        elif string == '' and dict == {}:
            pass

    def _string_to_dict( self ):

        """turns the dictionary of the creds into a string"""

        role_dict = {}
        for line in self.string.split( '\n' ):

            line = line.strip()
            if line == '':
                continue

            elif self.line_is_role( line ):
                self.role = self.get_role_from_line( line )

            else:
                if self.role != None:
                    key, value = self.get_key_value_from_line( line )
                    role_dict[key] = value

        self.dict = role_dict
        return role_dict

    def get_role_from_line( self, line ):

        """Given [AWS_ROLE-1234], return AWS_ROLE-1234"""

        if self.line_is_role( line ):
            return line[ len(self.BEGIN_ROLE) : -1*len(self.END_ROLE) ]
        return None

    def line_is_role( self, line ):

        """If given a role like [AWS_ROLE-1234], return TRUE"""

        if line[0] == self.BEGIN_ROLE and line[-1] == self.END_ROLE:
            return True
        return False

    def get_key_value_from_line( self, string ):

        """Takes a string, splits by the FIRST equal sign and sets it equal to key, value
        aws_session_token=1234ASDF=B returns ("aws_session_token", "1234ASDF=B") """

        split_by_equal = string.split('=')
        key = split_by_equal[0]

        if len(split_by_equal) > 1:
            value = '='.join( split_by_equal[1:] )
        else:
            value = None

        return key, value


class AWS_Creds (ParentPluralDict) :

    """A class that contains all possible AWS Roles and their respective credentials
    Creds: Dictionary where key is a role and value is an AWS_Cred class instance
    string: string which contains the exported version of the AWS_Creds"""

    def __init__( self, load_from_json=True, dict={} ):
        ParentPluralDict.__init__( self, att='Creds' )
        
        self.dict = dict
        if load_from_json:
            self._import_from_json()

        self._load_Creds()

    def _import_from_json( self ):

        self.dict = self.cfg['access_keys.Path'].read_json_to_dict()

    def export( self ):

        for Cred in self:
            self.dict[ Cred.role ] = Cred.dict

        self._export_to_json()

    def _export_to_json( self ):
        
        self.cfg['access_keys.Path'].write( string = ps.dict_to_json(self.dict) ) 

    def _load_Creds( self ):

        for role in self.dict:
            new_Cred = AWS_Cred( role=role, dict=self.dict[role] )
            self.add_new_Cred( new_Cred )    

    def add_new_Cred( self, new_Cred ):

        """take a new Creds class instance, and add/overwrite the existing credentials"""

        self._add( new_Cred.role, new_Cred )

    def get_Cred_from_role( self, Cred_role ):

        if Cred_role in self.Creds:
            return self.Creds[Cred_role]
        else:
            print ('Could not find role ' + str(Cred_role) + ' in AWS_Creds object')
            return None

    def update_from_clipboard( self ):

        ### Using option 2 from the AWS console
        new_Cred = AWS_Cred( string = ps.paste() )
        new_Cred.print_atts()

        if not new_Cred.role != None:
            print ()
            print ('------------')
            print ('ERROR: Errant AWS selection. Did not find correct format')
            print ('------------')
            print ()
            return False

        self.add_new_Cred( new_Cred )
        self.print_atts()
        print ('Writing merged credentials to ' + str( self.cfg['access_keys.Path'] ))
        self.export()

        print ()
        print ('------------')
        print ('SUCCESS: AWS Credentials successfully updated')
        print ('------------')
        print ()
        return True


