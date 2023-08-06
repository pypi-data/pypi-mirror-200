import aws_credentials
import time

aws_credentials.client.print_atts()
print ()

if aws_credentials.client.update_from_clipboard():
    time.sleep( aws_credentials.client.cfg['SLEEP_SUCCESS'])
else:
    time.sleep( aws_credentials.client.cfg['SLEEP_FAILURE']) 

