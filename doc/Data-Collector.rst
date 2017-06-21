| Quick link: * `Data Collector FAQ and Troubleshooting <https://github.com/Kount/kount-ris-python-sdk/wiki/Data-Collector-FAQ-and-Troubleshooting.rst>`__

Feature description
===================

The Data Collector process can be used to obtain data related to the
device initiating the customer transaction. This process is transparent
to the customer and sub second. The data collected is used in
conjunction with the RIS data.


.. figure:: images/data-collector.png
   :alt: data-collector


The following sequence describes the Data Collector process: 
1. Customer browses to merchant order form page containing Data Collector code
2. Customer browser automatically requests redirect on the Data Collector
element
3. Customer browser is redirected to Kount servers 
4. Kount collects device attributes 
5. Kount directs customer browser to display static image hosted by merchant

Requirements
============

1. Port 443 must be available to post and receive data from Kount.
2. Merchant adds code to their checkout process.

   -  HTML iframe:

      -  The iframe should be placed on the order form page where the
         payment method or credit card information is requested, usually
         near the bottom of the page.
      -  Server side code:

         -  The server side code consists of a logo.htm and logo.gif
            server side executable scripts.
         -  The path to the server side code must be a fully qualified
            path.

      -  Code to create a unique session identifier:

         -  When the form page is accessed, a session identifier must be
            created and stored to be used as the session identifier in
            the subsequent RIS post from the merchant to Kount. This
            identifier must be unique for at least 30 days and must be
            unique for every transaction submitted by each unique
            customer. If a single session ID were to be used on multiple
            transactions, those transactions would link together and
            erroneously affect the persona information and score.

3. Merchant supplies static image URL to Kount.

   -  The static image can be an image that is currently being displayed
      on the page or Kount can provide an image if desired.
   -  If the path or image requires change by the merchant subsequent to
      moving into production, Kount must be notified of the new path or
      filename to avoid possible failure.

Sample code
===========

Although a bit ancient (.jsp lol), the following code example
demonstrates how to code for the data collector. Additional details can
be found in the `Data Collector FAQ and Troubleshooting <https://github.com/Kount/kount-ris-python-sdk/wiki/Data-Collector-FAQ-and-Troubleshooting.rst>`__ page.

 |   :warning: 
    All of the code presented here is for example purposes
    only. Any production implementation performed by the customer should
    follow all internal code quality standards of the customer's
    organization including security review.

.. code:: html

    <!-- 
      HTML iframe example
      Requirements - The iframe has a minimum width=1 and height=1
    -->
     
    <iframe width=1 height=1 frameborder=0 scrolling=no src='https://MERCHANT_URL/logo.htm?m=merchantId&s=sessionId'>
        <img width=1 height=1 src='https://MERCHANT_URL/logo.gif?m=merchantId&s=sessionId'>
    </iframe>

Phone-to-Web order submissions
==============================

When a merchant submits phone orders via the same web page interface as
a customer, the data regarding the merchant's device is being sent to
Kount, not the customer's device data. This will cause order linking to
occur and in time will elevate the score of all orders associated with
the persona.

| :warning: 
    Linking will also occur if the browser session ID is used
    as the transaction session ID and multiple orders are submitted from
    within the same browser session without closing the browser. To
    avoid this type of linking, the browser session ID could be
    incremented appending the UNIX timestamp, choose a different
    methodology for creating the session ID, or agents must close the
    browser between orders to ensure a new session has been created.

There are two different methods for receiving phone orders.

1. If the customer service agents navigate to a separate order entry
   page that does not collect iframe data: Call Center/Phone Orders will
   be posted as a Mode=P; hard code the IP address specifically to
   10.0.0.1 and provide the phone number within the ANID field (if no
   phone number is available, pass 0123456789 hard coded).
2. If the customer service agents navigate to the same page as the
   customer (iframe data is collected): don't perform the redirect to
   the Kount Data Collector service, just post Call Center Orders as a
   Mode=Q; hard code the IP address specifically to 10.0.0.1.

In any of the above circumstances, if the email address is not provided
to the agents, the agents will need to input noemail@Kount.com as the
email address in order to prevent linking.
