import sys
import simplejson

def read():
    f = open(sys.argv[1])    
    data = f.read()
    f.close()
    
    jsondata = simplejson.loads(data)
    del jsondata["comment"]
   
    return jsondata


def main():
    f = open(sys.argv[1])    
    data = f.read()
    f.close()
    
    jsondata = simplejson.loads(data)
    del jsondata["comment"]
    for key,value in jsondata.iteritems():
        print "key",key,"value",
        for v in value:
            print v,
        print ""
    return jsondata

if __name__ == '__main__':
    main()

