from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    account_name = 'hashimstorage' # Must be replaced by your <storage_account_name>
    account_key = 'xnC9GoVmmXSW8V61jsZTbaMKdu+z8Gz/Iophp2XCvLyXW8SV0IBt32Fz4gMmXPAJ9lZBPspVpNaGYjnAK1e4Ag==' # Must be replaced by your <storage_account_key>
    azure_container = 'media'
    expiration_secs = None

class AzureStaticStorage(AzureStorage):
    account_name = 'hashimstorage' # Must be replaced by your storage_account_name
    account_key = 'gLoEU6id7cNLhXyRFsCapUs1G92bU90mpogL+DIrMzguc3hxvwcU9Ww+w71eMtwJbDZoXFwU/e4s2TU5kyCsIw==' # Must be replaced by your <storage_account_key>
    azure_container = 'static'
    expiration_secs = None