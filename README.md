ChatHTN
Combining HTN planning with ChatGPT (LLM)

ChatHTN: author Hector Munoz-Avila
    This code is built on top of pyhop and therefore it is released under the  Apache License, Version 2.0 



compilation order: DOMAINDefinitions, pyhop, openAINewVersion, DOMAIN

For example:

compilation order: logisticsDefinitions, pyhop, openAINewVersion, logistics

To test comment out one of the definitions of the methods in the <domain> file. For instance, comment out the airplaneTransport methods in the logistics module:


pyhop.declare_methods('truckTransport', truckTransportMethod1, truckTransportMethod2, truckTransportMethod3) 
pyhop.declare_methods('airplaneTransport', airplaneTransportMethod1, airplaneTransportMethod2, airplaneTransportMethod3) 
pyhop.declare_methods('transferPackage', transferPackageMethod1, transferPackageMethod2) 

You need a ChatGPT API key. Put the key in openAINewVersion
