Quick links
=============

* `General Questions <https://github.com/Kount/kount-ris-python-sdk/wiki/Data-Collector-FAQ-and-Troubleshooting.rst#general>`__ 
* `Iframe <https://github.com/Kount/kount-ris-python-sdk/wiki/Data-Collector-FAQ-and-Troubleshooting.rst#iframe>`__
* `Session Identifier <https://github.com/Kount/kount-ris-python-sdk/wiki/Data-Collector-FAQ-and-Troubleshooting.rst#session-identifier>`__
* `Image <https://github.com/Kount/kount-ris-python-sdk/wiki/Data-Collector-FAQ-and-Troubleshooting.rst#image>`__
* `Troubleshooting <https://github.com/Kount/kount-ris-python-sdk/wiki/Data-Collector-FAQ-and-Troubleshooting.rst#troubleshooting>`__

General:
========

| **Q:** Where do I get the Merchant ID?
| A Sandbox Boarding Information document will be sent following the
  initial kick-off call with the Merchant ID and URLs associated with
  the DC and RIS processes. A separate document for production will be
  sent with the production service URLs once the test transaction have
  been certified.

| **Q:** Why does Kount require a redirect?
| The redirect gathers device information without interfering with the
  order process. The redirect also obfuscates the communication between
  Kount and the customer.

| **Q:** How do I receive a login to the AWC?
| Kount will create the initial administrator user. Once the user has
  been created an automated e-mail will be sent requesting a password
  creation.

| **Q:** Should I send production traffic to the test environment to
  test with?
| Production traffic should not be sent to the test environment due to
  the possibility of skewed scoring from the test orders.

Iframe
======

| **Q:** Where should I place the iframe on my website?
| If multiple forms of payment methods are available, i.e. Credit Card,
  PayPal, Bill Me Later, the iframe should be included on the page where
  the payment method is chosen. If only a single payment method is used,
  i.e. Credit Card, then the iframe should be included on the page where
  the customer inputs their credit card information. 
 
|  :warning:   Place  the iframe only on one page. Do not place the image on multiple form pages on your website.

| **Q:** Are there size restrictions on the iframe?
| Yes, the iframe must be at least 1x1 pixels in size.

| **Q:** Does it matter where the iframe shows up on the web page?
| No, this is left to the merchant to decide.

| **Q:** Why an iframe?
| If a user were to source the page there would be no mention of Kount
  in the source. It also eliminates the possibility of being indexed by
  various search engines or crawlers.

| **Q:** Why are there two files in the iframe?
| The logo.gif file is a fallback in case iframes have been disabled or
  the browser does not support iframes.

| **Q:** Are both the iframe and image required?
| Yes both are required to ensure that a connection is made by the
  customer device.

| **Q:** Why don't I just use the image, we don't have any iframes
  anywhere else on our site.
| The manner in which iframes are handled by browsers provides greater
  insight to Kount.

| **Q:** Why do the .htm and .gif files get interpreted as server side
  code?
| By using .htm and .gif file extensions there is less concern from end
  users that may inspect the source code.

Session Identifier
==================

| **Q:** What does the session identifier do?
| The session identifier is used to join the device data with the order
  data sent by the RIS process. When the RIS process posts data to Kount
  it must use the session identifier that was created when the customer
  initiated the DC HTML.

| **Q:** Does the session identifier need to be unique?
| Yes, the session identifier must be unique over a thirty day time
  period. If there are duplicate session identifiers, device data
  originating from the DC process may be erroneously connected to RIS
  order data.

| **Q:** Are there limitations on the session identifier?
| Yes, it must be alpha-numeric with a minimum of one character and a
  maximum of 32 characters long.

| **Q:** What should I use for the session identifier?
| The merchant determines, as long as the limitation guidelines are
  followed. Many merchants use a portion of the application session that
  is generated when the page is created as the session identifier.

| **Q:** What happens when a user leaves the page after a session
  identifier has been created then returns to finish the order?
| There can be multiple session identifiers created, only the last
  session will be used to join with the RIS transaction.

Image
=====

| **Q:** Does it matter where the image is displayed on the page?
| It is recommended to display the iframe below the fold of the initial
  web page but can be located anywhere on the page.

| **Q:** Why does the merchant need to give Kount the path to an image
  for the redirection?
| Kount must have this path to finish the 302 redirect for the image to
  load. If the path has not been supplied to Kount a broken image icon
  will be displayed on the merchant page.

| **Q:** Does the image need to be accessible via the Internet?
| Yes the image must be publicly available from the Internet.

| **Q:** Why does the path need to be HTTPS?
| If the image is not secure, a notification will appear alerting the
  customer that there are unsecure items on the check out form.

| **Q:** Does it matter what the name of the file is?
| If a customer were to inspect the source of the page there should be
  no indication of interaction from Kount. To alleviate the possibility
  of a merchant's customer questioning the interaction between Kount and
  the merchant do not include any reference to Kount in the file name.

| **Q:** Do you have an example of an image?
| Yes, it can be provided upon request. Please contact your Client
  Success Manager for further details. See example below (Secure
  Payments):

.. figure:: https://raw.githubusercontent.com/wiki/Kount/kount-ris-python-sdk/images/secure-payments.png
   :alt: secure-payments



Troubleshooting
===============

| **Q:** Is the correct Kount URL being used?
| Verify that the correct Kount Data Collector URL is being used, test
  URL or production URL.

| **Q:** Have you provided Kount with the HTTPS URL path to the image?
| If the URL path has not been set there will be a broken image
  displayed on the page.

| **Q:** Is the image available via the Internet?
| Test this by pasting the path of the URL in a browser on an external
  network and verify that the image appears.

| **Q:** Have appropriate DNS entries, NATs, and firewall settings been
  configured correctly?
| Due to the security concerns regarding test environments or production
  environment the merchant's network operations may need to verify that
  proper access is available.

| **Q:** Are the logo.htm and logo.gif files being interpreted as
  server-side code?
| If the files are not interpreted as server-side code, when requested
  the files will serve up the source code instead of performing the
  redirect. This can be tested by pointing the browser directly to the
  logo.htm or logo.gif URLs and verify that the static image appears. If
  source code appears, then the files are not being interpreted
  correctly. This can also be tested via a UNIX wget command.

| **Q:** Does the redirect contain the correct Merchant ID?
| Verify that the redirect Merchant ID is the correct six digit ID
  supplied by Kount.

| **Q:** Is the Session ID created in the DC process the same session ID
  being sent with the RIS post?
| Ensure that the Session ID being created and stored during the DC
  process is the correct one being used in the RIS post to Kount and
  adheres to the session ID requirements.

| **Q:** Only part of the device data is collected, Javascript, Time
  Zone and other details seem to be missing?
| The logo.gif server side script is calling the log.gif instead of the
  logo.htm. See the "Server Side Code Examples" section.

| **Q:** Why do some of the items within the Extended Variables gadget
  not display or display as N/A?
| A fully qualified path must be used within the scr value of the
  iFrame.
