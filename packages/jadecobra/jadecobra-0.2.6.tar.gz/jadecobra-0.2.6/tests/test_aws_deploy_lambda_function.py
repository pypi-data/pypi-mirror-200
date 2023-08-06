import jadecobra.aws_lambda.deploy.deploy_lambda_function
import jadecobra.toolkit

class TestAwsDeployLambdaFunction(jadecobra.toolkit.TestCase):

    def test_deploy_lambda_function(self):
        with self.assertRaises(TypeError):
            jadecobra.aws_lambda.deploy.deploy_lambda_function.LambdaFunction(
                function_name='bob_function'
            )

    def test_deploy_lambda_function_attributes(self):
        self.assert_attributes_equal(
            jadecobra.aws_lambda.deploy.deploy_lambda_function.LambdaFunction,
            [
                '__class__',
                '__delattr__',
                '__dict__',
                '__dir__',
                '__doc__',
                '__eq__',
                '__format__',
                '__ge__',
                '__getattribute__',
                '__gt__',
                '__hash__',
                '__init__',
                '__init_subclass__',
                '__le__',
                '__lt__',
                '__module__',
                '__ne__',
                '__new__',
                '__reduce__',
                '__reduce_ex__',
                '__repr__',
                '__setattr__',
                '__sizeof__',
                '__str__',
                '__subclasshook__',
                '__weakref__',
                'delete_directory',
                'delete_zipfile',
                'delimiter',
                'directory',
                'package_code',
                'python_filename',
                's3_key',
                'update_lambda_code',
                'upload_to_s3',
                'zip_filename'
            ]
        )