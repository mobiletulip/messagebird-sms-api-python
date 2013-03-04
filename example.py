"""
=============================================================================
@file: example.py
@author: MessageBird B.V.
@version: v0.1 - 2010-06-29
@requires: This class requires that you have Python 2.x or higher installed

@note: For more information visit http://www.messagebird.com/content/api
=============================================================================
"""

# Import the MessageBird Library which will send the message to our server
from MessageBird import MessageBird

# Set the MessageBird username and password, and create an instance of the SmsCity class
smsApi = MessageBird('username', 'password')

# Set the sender, could be an number (16 numbers) or letters (11 characters)
smsApi.setSender('YourSender')

# Add the destination mobile number.
# This method can be called several times to add have more then one recipient for the same message
smsApi.addDestination('31600000000')

# Set an reference
smsApi.setReference('123456789')

# Send the message to the destination(s)
smsApi.sendSms('This is a test message')

# When using in the console, it will show you what the response was from our server
print 'Response:'
print smsApi.getResponseCode()
print smsApi.getResponseMessage()
print smsApi.getCreditBalance()
