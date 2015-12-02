# IRTTAE
Interactive Real-Time Timed Automata Engine
by Christopher Hannon: 

##########################
#  channon@hawk.iit.edu  #
##########################

     ./verifier.py Path_to_state_config init_state user_defined_py_funcions(continous) t/v(input method) final state log_file


dependencies: python 2.7, pyttsx, pywapi

install pyttsx: `pip install pyttsx`

install pip: `apt-get install -y python-pip`

install pywapi (for test) `wget https://launchpad.net/python-weather-api/trunk/0.3.8/+download/pywapi-0.3.8.tar.gz`

untar file. Run `python setup.py build` then `python setup.py install`
(uses weather api)

The purpose of this program is to interactively emulate a timed automata through interactive variable enty and vocal (siri-like) program. The program can recieve state information updates manually, as well as programmatically.
