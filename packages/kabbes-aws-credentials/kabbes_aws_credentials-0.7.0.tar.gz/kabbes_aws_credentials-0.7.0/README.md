# aws_credentials
System for quickly importing AWS credentials into Python scripts

[Documentation](https://jameskabbes.github.io/aws_credentials)<br>
[PyPI](https://pypi.org/project/kabbes-aws-credentials)

<br> 

# Installation
`pip install kabbes_aws_credentials`

<br>

# Usage
For more in-depth documentation, read the information provided on the Pages. Or better yet, read the source code.

```python
import aws_credentials
```

```python
role = 'myawsrole'
print ( aws_credentials.Creds[ role ].dict )
```

```
>>> { 'aws_access_key_id': 'XXXXXX', 'aws_secret_access_key': 'XXXXXX' }
```

## Updating AWS Credentials

<br>


**1. Copy credentials in this format to your clipboard**

[aws_role] <br>

aws_access_key_id=XXXXXX <br>

aws_secret_access_key=XXXXXX <br>


**2. Run one of the following**

- ```python -m aws_credentials``` <br>
- ```aws_credentials.update()```

**3. Verify the aws_credentials/aws_creds.txt file is updated**

<br>

# Author
James Kabbes
