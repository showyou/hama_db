import sys
import simplejson


def main():
    f = open(sys.argv[1])    
    data = f.read()
    f.close()
    
    jsondata = simplejson.loads(data)
    for key,value in jsondata.iteritems():
        print key, 
        for v in value:
            print v,
        print ""


if __name__ == '__main__':
    main()

