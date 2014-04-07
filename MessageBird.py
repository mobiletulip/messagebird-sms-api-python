"""
=============================================================================
@file: MessageBird.py
@author: MessageBird B.V.
@version: v0.1 - 2010-06-29
@requires: This class requires that you have Python 2.x or higher installed

@note: For more information visit http://www.messagebird.com/content/api
=============================================================================
"""

# For handeling a specific date/time for sending a message
from datetime import \
    datetime

# For reading/parsing the XML response
from xml.dom.minidom import parseString

# For sending and encoding an HTTP POSTS
import httplib
import urllib

class MessageBird:
    """ MessageBird Class which will handle sending messages to the MessageBird website using the MessageBird API """

    GATEWAY_VOICE = 8
    GATEWAY_BASIC = 2
    GATEWAY_BUSINESS = 1
    
    # @var sender: mixed: Can be an number (16 numbers) or an text (11 characters)
    sender = ''

    # @var destination: list: Holds one or more recipients
    destination = []

    # @var reference: integer: The reference to identify delivery reports using this reference and the destinations
    reference = None

    # @var responseType: string: Could be XML, PLAIN or SIMPLE. Determines which kind of response the server will send
    responseType = 'XML'

    # @var timestamp: datetime: Holds the timestamp to schedule a message, instead of sending it now
    timestamp = None

    # @var test: boolean: Set to true when developing. No actual messages will be send
    test = False

    # @var httpResponseStatus: string: Will hold the response status returned by the SMScity server
    httpResponseStatus = ''

    # @var httpResponseReason: string: Will hold the response reason returned by the SMScity server
    httpResponseReason = ''

    # @var httpResponseData: string: Will hold the full response data returned by the SMScity server nothing is parsed from this string
    httpResponseData = ''

    # @var xmlResponseData: documentElement: The XML data parsed by the minidom
    xmlResponseData = None

    # @var replacechars: boolean: Replace non GSM-7 characters by appropriate valid GSM-7 characters
    replacechars = False

    # @var gateway: string: Set the quality of the route that you want to send the message.
    gateway = None

    # @var gatewayId: integer: Change de route over which the message should be send
    gatewayId = None

    def __init__(self, username, password):
        """
        This constructor sets both the username and password
        @param username: string The username of the SMScity account
        @param password: string The password of the SMScity account
        """
        self.username = username
        self.password = password
        self.destination = []


    def addDestination(self, destination):
        """
        Adds an MSISDN to the destination array
        @param destination: integer The destination MSISDN (Mobile number)
        """
        self.destination.append(destination)


    def setReference(self, reference):
        """
        Sets the reference linked to the MSISDN so the correct status can be retrieved later.
        @param reference: integer An unique reference so delivery reports can be linked to the correct message and MSISDN
        """
        self.reference = reference


    def setSender(self, sender):
        """
        Sets the sender. This can be an MSISDN (Mobile number) or an Text.
        When it is only numbers it can be 16 numbers, when it is text, it can only be 11 characters long.
        @param sender: mixed The sender of the message which the recipient will see.
        """
        self.sender = sender


    def setTimestamp(self, scheduleDateTime):
        """
        Sets the date and time when the message should be sent.
        NOTE: Our server uses the CET (UTC +1), CEST (UTC +2), Europe/Amsterdam as time reference
        @param scheduleDateTime: datetime An datetime object with at least year, month, day, hour and minute.
        """
        if isinstance(scheduleDateTime, datetime):
            # Our API needs the timestamp in YearMonthDayHourMinute so we convert it to this format
            self.timestamp = scheduleDateTime.strftime('%Y%m%d%H%M')


    def setResponseType(self, responseType):
        """
        Sets the response type to be used for retrieveing the response in specific manner.
        You can change the response type to anything which is in the API Documentation.
        @param responseType: string Could be XML, PLAIN or SIMPLE (Default: XML)
        """
        self.responseType = responseType


    def setTest(self, testing):
        """
        When defined, then the message is not actually sent or scheduled, so no credits are deducted.
        Validation of the message will take place, and you will also receive a normal response.
        @param testing: boolean: set to TRUE when testing
        """
        self.test = testing

    def setReplacechars(self, replacing):
        """
        When defined, then the message is not actually sent or scheduled, so no credits are deducted.
        Validation of the message will take place, and you will also receive a normal response.
        @param replacing: boolean: Replace non GSM-7 characters by appropriate valid GSM-7 characters
        """
        self.replacechars = replacing

    def setGateway(self, gateway):
        """
        Set the quality of the route that you want to send the message. See the website for more information
        8 = Voice (inclusief vaste nummers), 2 = Basic, 1 =Business+
        @param replacing: boolean: Set the quality of the route that you want to send the message.
        """
        self.gateway = gateway

    def setGatewayId(self, gatewayId):
        """
        The SMS-route that you wish to use. Adjust the quality of the gateway that you wish 
        to use to send the SMS. This setting overrides the "standard quality" that you have 
        set in your account for this message.
        Default possibilities are 239 for basic, 240 for quality and 8 for voice.
        @param replacing: numeric : Change de route over which the message should be send.
        """
        self.gatewayId = gatewayId


    def sendSms(self, message):
        """
        Will actualy send the given message to the destinations given using addDestination()
        @param message: string The message which should be sent to the added destinations.
        """
        # We need all the destinations comma separated
        destinations = ','.join(self.destination)

        # Set the default parameters that needs to be sent
        params = {'username': self.username,
                  'password': self.password,
                  'destination': destinations,
                  'responsetype': self.responseType,
                  'sender': self.sender,
                  'body': message
                 }

        # If there is a reference set, add it to the parameters
        if not self.reference == None:
            params.update({'reference': self.reference})

        # If there is a timestamp set, add it to the parameters
        if not self.timestamp == None:
            params.update({'timestamp': self.timestamp})

        # If testing, add it to the parameters
        if self.test == True:
            params.update({'test': self.test})

        # If not replacing characters, add it to the parameters
        if self.replacechars == False:
            params.update({'replacechars': self.replacechars})

        # If setting the gateway, add it to the parameters
        if self.gateway == 'basic':
            params.update({'gateway': self.GATEWAY_BASIC})
        elif self.gateway == 'business':
            params.update({'gateway': self.GATEWAY_BUSINESS})
        elif self.gateway == 'voice':
            params.update({'gateway': self.GATEWAY_Voice})

        # If setting the gatewayId, add it to the parameters
        if not self.gatewayId == None:
            params.update({'gatewayId': self.gatewayId})

        # urlencode all the paramters
        postParams = urllib.urlencode(params)

        # Set the HTTP Headers
        headers = {'Content-type': 'application/x-www-form-urlencoded'}

        httpConnection = httplib.HTTPConnection('api.messagebird.com')
        httpConnection.request('POST', '/api/sms', postParams, headers)
        httpResponse = httpConnection.getresponse()

        # Read the response data/info
        self.httpResponseStatus = httpResponse.status
        self.httpResponseReason = httpResponse.reason
        self.httpResponseData = httpResponse.read()

        # Close the HTTP connection
        httpConnection.close()

        if self.responseType == 'XML':
            self.xmlResponseData = parseString(self.httpResponseData).documentElement


    def getResponseCode(self):
        """
        Will return the response code which is returned after sending the the message.
        When the responseType is set to XML there can could be more data to be retrieved.
        @return: string The response code
        """
        if not self.xmlResponseData == None:
            responseCodeTag = self.xmlResponseData.getElementsByTagName('responseCode')
            if responseCodeTag.length > 0:
                return responseCodeTag[0].firstChild.data
            else:
                return ''
        else:
            return self.httpResponseData


    def getResponseMessage(self):
        """
        Will return the response message.
        This is only available when using PLAIN or XML, when using SIMPLE, it will return the responseCode
        @return: string The response message
        """
        if not self.xmlResponseData == None:
            responseMessageTag = self.xmlResponseData.getElementsByTagName('responseMessage')
            if responseMessageTag.length > 0:
                return responseMessageTag[0].firstChild.data
            else:
                return ''
        else:
            return self.httpResponseData

