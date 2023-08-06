# Python client for airt service

## Docs

For full documentation, Please follow the below link:

- <a href="https://docs.airt.ai" target="_blank">https://docs.airt.ai/</a>


## How to install

If you don't have the airt library already installed, please install it using pip.


```console
pip install airt-client
```

## How to use

To access the airt service, you must first create a developer account. Please fill out the signup form below to get one:

- [https://bit.ly/3hbXQLY](https://bit.ly/3hbXQLY)

After successful verification, you will receive an email with the username and password for the developer account.

Once you have the credentials, use them to get an access token by calling `Client.get_token` method. It is necessary to get an access token; otherwise, you won't be able to access all of the airt service's APIs. You can either pass the username, password, and server address as parameters to the `Client.get_token` method or store them in the environment variables **AIRT_SERVICE_USERNAME**, **AIRT_SERVICE_PASSWORD**, and **AIRT_SERVER_URL**

In addition to the regular authentication with credentials, you can also enable multi-factor authentication (MFA) and single sign-on (SSO) for generating tokens.

To help protect your account, we recommend that you enable multi-factor authentication (MFA). MFA provides additional security by requiring you to provide unique verification code (OTP) in addition to your regular sign-in credentials when performing critical operations.

Your account can be configured for MFA in just two easy steps:

1. To begin, you need to enable MFA for your account by calling the `User.enable_mfa` method, which will generate a QR code. You can then 
scan the QR code with an authenticator app, such as Google Authenticator and follow the on-device instructions to finish the setup in your smartphone.

2. Finally, activate MFA for your account by calling `User.activate_mfa` and passing the dynamically generated six-digit verification code from your 
smartphone's authenticator app.

You can also disable MFA for your account at any time by calling the method `User.disable_mfa` method.

Single sign-on (SSO) can be enabled for your account in three simple steps:

1. Enable the SSO for a provider by calling the `User.enable_sso` method with the SSO provider name and an email address. At the moment, 
we only support **"google"** and **"github"** as SSO providers. We intend to support additional SSO providers in future releases.

2. Before you can start generating new tokens with SSO, you must first authenticate with the SSO provider. Call the `Client.get_token` with 
the same SSO provider you have enabled in the step above to generate an SSO authorization URL. Please copy and paste it into your 
preferred browser and complete the authentication process with the SSO provider.

3. After successfully authenticating with the SSO provider, call the `Client.set_sso_token` method to generate a new token and use it automatically 
in all future interactions with the airt server.

For more information, please check:

- [Tutorial](https://docs.airt.ai/Tutorial/) with more elaborate example, and

- [API](https://docs.airt.ai/API/client/Client/) with reference documentation.

Here's a minimal example showing how to use airt services to train a model and make predictions.

In the below example, the username, password, and server address are stored in **AIRT_SERVICE_USERNAME**, **AIRT_SERVICE_PASSWORD**, and **AIRT_SERVER_URL** environment variables.


### 0. Get token


```
#| include: false
# Do not remove "# hide" from this cell. Else this cell will appear in documentation

import os

# setting the environment variable
os.environ["AIRT_SERVICE_USERNAME"] = "johndoe"
os.environ["AIRT_SERVICE_PASSWORD"] = os.environ["AIRT_SERVICE_SUPER_USER_PASSWORD"]
```


```
# Importing necessary libraries
from airt.client import Client, DataSource, DataBlob

# Authenticate
Client.get_token()
```

### 1. Connect data


```
# The input data in this case is a CSV file stored in an AWS S3 bucket. Before
# you can use the data to train a model, it must be uploaded to the airt server.
# Run the following command to upload the data to the airt server for further 
# processing.
data_blob = DataBlob.from_s3(
    uri="s3://test-airt-service/ecommerce_behavior_csv"
)

# Display the upload progress
data_blob.progress_bar()

# Once the upload is complete, run the following command to preprocess and 
# prepare the data for training.
data_source = data_blob.to_datasource(
    file_type="csv",
    index_column="user_id",
    sort_by="event_time"
)

# Display the data preprocessing progress
data_source.progress_bar()

# When the preprocessing is finished, you can run the following command to 
# display the head of the data to ensure everything is fine.
print(data_source.head())
```

    100%|██████████| 1/1 [01:00<00:00, 60.62s/it]
    100%|██████████| 1/1 [00:35<00:00, 35.39s/it]


                              event_time event_type  product_id  \
    user_id                                                       
    10300217   2019-11-06 06:51:52+00:00       view    26300219   
    253299396  2019-11-05 21:25:44+00:00       view     2400724   
    253299396  2019-11-05 21:27:43+00:00       view     2400724   
    272811580  2019-11-05 19:38:48+00:00       view     3601406   
    272811580  2019-11-05 19:40:21+00:00       view     3601406   
    288929779  2019-11-06 05:39:21+00:00       view    15200134   
    288929779  2019-11-06 05:39:34+00:00       view    15200134   
    310768124  2019-11-05 20:25:52+00:00       view     1005106   
    315309190  2019-11-05 23:13:43+00:00       view    31501222   
    339186405  2019-11-06 07:00:32+00:00       view     1005115   
    
                       category_id              category_code  \
    user_id                                                     
    10300217   2053013563424899933                       None   
    253299396  2053013563743667055    appliances.kitchen.hood   
    253299396  2053013563743667055    appliances.kitchen.hood   
    272811580  2053013563810775923  appliances.kitchen.washer   
    272811580  2053013563810775923  appliances.kitchen.washer   
    288929779  2053013553484398879                       None   
    288929779  2053013553484398879                       None   
    310768124  2053013555631882655     electronics.smartphone   
    315309190  2053013558031024687                       None   
    339186405  2053013555631882655     electronics.smartphone   
    
                                   brand    price  \
    user_id                                         
    10300217                     sokolov    40.54   
    253299396                      bosch   246.85   
    253299396                      bosch   246.85   
    272811580                       beko   195.60   
    272811580                       beko   195.60   
    288929779                      racer    55.86   
    288929779                      racer    55.86   
    310768124                      apple  1422.31   
    315309190  dobrusskijfarforovyjzavod   115.18   
    339186405                      apple   915.69   
    
                                       user_session  
    user_id                                          
    10300217   d1fdcbf1-bb1f-434b-8f1a-4b77f29a84a0  
    253299396  b097b84d-cfb8-432c-9ab0-a841bb4d727f  
    253299396  b097b84d-cfb8-432c-9ab0-a841bb4d727f  
    272811580  d18427ab-8f2b-44f7-860d-a26b9510a70b  
    272811580  d18427ab-8f2b-44f7-860d-a26b9510a70b  
    288929779  fc582087-72f8-428a-b65a-c2f45d74dc27  
    288929779  fc582087-72f8-428a-b65a-c2f45d74dc27  
    310768124  79d8406f-4aa3-412c-8605-8be1031e63d6  
    315309190  e3d5a1a4-f8fd-4ac3-acb7-af6ccd1e3fa9  
    339186405  15197c7e-aba0-43b4-9f3a-a815e31ade40  


### 2. Train


```
# We assume that the input data for training a model includes the client_column
# target_column, and timestamp column, which specify the time of an event.
from datetime import timedelta

model = data_source.train(
    client_column="user_id",
    target_column="event_type",
    target="*purchase",
    predict_after=timedelta(hours=3),
)

# Display model training progress
model.progress_bar()

# Once the model training is complete, call the following method to display
# multiple evaluation metrics to evaluate the model's performance.
print(model.evaluate())
```

    100%|██████████| 5/5 [00:00<00:00, 126.62it/s]

                eval
    accuracy   0.985
    recall     0.962
    precision  0.934


    


### 3. Predict


```
# Finally, you can use the trained model to make predictions by calling the
# method below.
predictions = model.predict()

# Display model prediction progress
predictions.progress_bar()

# If the dataset is small enough, you can use the following method to download 
# the prediction results as a pandas DataFrame.
print(predictions.to_pandas().head())
```

    100%|██████████| 3/3 [00:10<00:00,  3.38s/it]

                  Score
    user_id            
    520088904  0.979853
    530496790  0.979157
    561587266  0.979055
    518085591  0.978915
    558856683  0.977960


    

