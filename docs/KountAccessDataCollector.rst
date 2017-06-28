Kount Access Data Collector
=========================================

Data Collector
~~~~~~~~~~~~~~

The *Kount Access Data Collector* runs in the background at a sub second
level while the user is logging into the website via a web clients or
browser (see section below) or via a mobile app (**iOS or Android**).
Here are the standard requirements for any Data Collection event.

:information_source:  
  Access Inquiry Service is designed to be used in conjunction with the Data Collection process. The Data Collection process is passive and provides no information back to a merchant independent of the Access Inquiry Service.


Session ID Discussion
~~~~~~~~~~~~~~~~~~~~~

The Session ID is the identifier for the collection event and is
specific to the user's request. You will use the Session ID for
subsequent calls to the API service for device information regarding the
current user's interaction.

-  Data Collector should be run once for each user's session within the
   web browser.
-  Session ID field ``name = sessionId``
-  Session ID values must be exactly 32 character length and must be
   alpha-numeric values ``(0-9, a-z or A-Z)``. Dashes ``(-)`` and
   underscores ``(_)`` are acceptable.
-  Session IDs must be unique per request. They must be unique forever,
   they may not be recycled.
-  Script tag parameter ``value = s`` Example:
   ``s=abcdefg12345abababab123456789012.``

Web Clients or Browser
~~~~~~~~~~~~~~~~~~~~~~

The Data Collector runs on a client's browser and collects a variety of information that helps uniquely identify the device.

Add the ``<script>`` tag and an ``<img>`` tag to the web page where you
want to trigger the ``Data Collection`` to occur.

+---------------+--------------+-----------------------------------------------------+
| Field         | Parameter    | Value                                               |
+===============+==============+=====================================================+
| **merchantId**| ``m``        | six digit Merchant ID number issued by Kount        |
+---------------+--------------+-----------------------------------------------------+
| **sessionId** | ``s``        | 32 character session id; see Session ID Discussion  |
|               |              | above for more information                          |
+---------------+--------------+-----------------------------------------------------+


Below is an example for the sandbox02 environment where the Merchant ID
field ``(m=123456)`` and the Session ID field
``(s=abcdefg12345abababab123456789012)`` are set.

.. code:: html

    <script type='text/javascript' src='https://sandbox02.kaxsdc.com/collect/sdk? m=123456&s=abcdefg12345abababab123456789012'> </script>
    <img src='https://sandbox02.kaxsdc.com/logo.gif?m=123456&s=abcdefg12345abababab123456789012' />

:information_source: 

      The script tag will not affect the UI with its placement. The logo.gif is a 1x1 pixel transparent image served by Kount. This is preset image that is set by Kount within the Data Collection process.

Creating the kaxsdc Class (Responsible for Triggering Data Collection)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Client Collector SDK allows the data collection process to be
triggered by any number of events. The default event is page load. These
events can be configured by adding the kaxsdc class and
``data-event='<event>'`` to an HTML element. The kaxsdc class is
configurable using the Client Collector SDK.

Namespace & ka.ClientSDK Object
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All ``Kount Access JavaScript`` is namespaced under the
``ka JavaScript`` object. To start using the Client Collector SDK,
create a new ClientSDK object: ``var client=new ka.ClientSDK();``

Available methods in the ka.ClientSDK object:

+----------------------------+----------------------------------------------------------------+
| Method                     | Description                                                    |
+============================+================================================================+
| **className**              | Sets the class to be used by ``autoLoadEvents()``              |
+----------------------------+----------------------------------------------------------------+
| **autoLoadEvents()**       | Automatically load events to trigger the data collection       |
|                            | process. This will wire all elements with a class equal to the |
|                            | property className that also have a data-event attribute.      |
|                            | After the first event fires and the data collection process    |
|                            | begins, no further events will have an effect.                 |
+----------------------------+----------------------------------------------------------------+
| **collectData()**          | Manually initiates the data collection process instead of      |
|                            | waiting for an event to be loaded using the autoLoadEvents()   |
|                            | method.                                                        |
+----------------------------+----------------------------------------------------------------+
| **setupCallback(config)**  |A client programmable callback system that allows the client    |
|                            |to execute custom code at certain points in the data            |
|                            |collection process. This method allows a merchant to add a      |
|                            |callback function to be called at a specified life-cycle hook.  |
|                            |A merchant can pass a JavaScript object containing one or more  |
|                            |life cycle hooks with a function pointer or an anonymous        |
|                            |function to be executed. List of hooks (in order of firing):    |
|                            | * ``collect-begin`` - Triggers when the collection starts.     |
|                            | * ``collect-end`` - Triggers when the collection ends. When    |
|                            |executed, the callback function is passed a JavaScript object   |
|                            |containing the following properties:                            |
|                            | * ``MercSessId`` - The merchant provided session.              |
|                            | * ``MerchantId`` - The merchant Id.                            |
+----------------------------+----------------------------------------------------------------+


Code Example:
^^^^^^^^^^^^^

This code will fire an alert when the process reaches the
``collect-begin`` hook

.. code:: html

    <html>
       .
       .
       .
       <body class='kaxsdc' data-event='load'>
          .
          .
          .
          <script type='text/javascript'>
            var client=new ka.ClientSDK();
            client.setupCallback(
                {
                    // fires when collection has finished
                    'collect-end':
                        function(params) {
                            // enable login button
                            loginButton = document.getElementById('login_button');
                            loginButton.removeAttribute('disabled');
                            // now user can login and navigate away from the page
                        },
                    // fires when collection has started
                    'collect-begin':
                        function(params) {
                            // add hidden form element to post session id
                            var loginForm = document.forms['loginForm'];
                            var input = document.createElement('input');
                            input.type = 'hidden';
                            input.name = 'kaId';
                            input.value = params['MercSessId'];
                            loginForm.appendChild(input);
                        }
                }
            );
            // The auto load looks for the default, an element with the 'kaxsdc' class and
            // data-event equal to a DOM event (load in this case). Data collection begins
            // when that event fires on that element--immediately in this example
            client.autoLoadEvents();
          </script>
       </body>
    </html>

Alternative Integration Example
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For maximum efficiency in data collection, initiating data collection
when the body loads is best. However, if your use-case demands that data
collection is initiated by a different event, then this example may be
helpful.

.. code:: html

    <html>
        <body>
            <button class='mycustomclass' data-event='click'>Click Me!</button>
          <script type='text/javascript'>
            var client=new ka.ClientSDK();
            // notice the use of the custom class
            client.className = 'mycustomclass';
            client.autoLoadEvents();
          </script>
        </body>
    </html>

Another Optional Example to use if you would rather not wait, then just call collectData()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: html

    <html>
        <body>
          <script type='text/javascript'>
            var client=new ka.ClientSDK();
            client.setupCallback(
                {
                    // fires when collection has finished
                    'collect-end':
                        function(params) {
                        location.href = 'http: //example.com/loginpage';
                        }
                }
            );
            client.collectData();
          </script>
        </body>
    </html>

SDK for Native Mobile Apps (iOS and Android)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The implementation of the Client Collector is somewhat different for
native Mobile Apps. Kount has a native Mobile SDK for both iOS and 
Android which is compatible with both the Kount Complete and Kount
Access products. By using the native Mobile SDK, along with a Merchant
ID, Session ID, and custom URL for posting, native mobile apps can take
advantage of the added capabilities from these native SDKs. These native
Mobile SDKs collect more data and increase the reliability of more
consistent fingerprint across the life of a device.

The Data Collector SDK for Android provides a java jar file which can be
used to perform Device Collection interaction with Kount for native
Android applications.

-  For Android implementations see the `Android SDK Guide <http://kount.github.io/mobile-client/android.html>`_
-  For iOS implementation see the `iOS SDK Guide <http://kount.github.io/mobile-client/ios.html>`_

:information_source:
      
       The Access Inquiry Service is designed to be used in conjunction with the Data Collection process. The Data Collection process is passive and provides no information back to a merchant independent of the Access Inquiry Service.
