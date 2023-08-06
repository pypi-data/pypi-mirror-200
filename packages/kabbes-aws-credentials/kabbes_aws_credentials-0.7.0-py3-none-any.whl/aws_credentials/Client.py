import kabbes_client
import aws_credentials

class Client( aws_credentials.AWS_Creds ):

    _BASE_DICT = {}

    def __init__( self, dict={} ):

        d = {}
        d.update( Client._BASE_DICT )
        d.update( dict )

        self.Package = kabbes_client.Package( aws_credentials._Dir, dict=d )
        self.cfg = self.Package.cfg

        if not self.cfg['access_keys.Path'].exists():
            self.cfg['access_keys.Path'].write( string ='{}',override=True )

        aws_credentials.AWS_Creds.__init__( self )

