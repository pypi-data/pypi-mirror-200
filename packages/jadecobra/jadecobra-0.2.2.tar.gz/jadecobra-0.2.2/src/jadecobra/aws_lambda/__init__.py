def get_arn(name=None, region=None, account=None):
    return f"arn:aws:lambda:{region}:{account}:function:{name}"