# coding=utf-8
#from configparser import SafeConfigParser
import configparser



def get_config(config_file='seq2seq.ini'):
    parser = configparser.ConfigParser()
    parser.read(config_file,encoding="utf-8")
    # get the ints, floats and strings
    _conf_ints = [ (key, int(value)) for key,value in parser.items('ints') ]
    #_conf_floats = [ (key, float(value)) for key,value in parser.items('floats') ]
    _conf_strings = [ (key, str(value)) for key,value in parser.items('strings') ]
    return dict(_conf_ints  + _conf_strings)