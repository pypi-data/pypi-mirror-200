import sys
import time
import logdb
import hashlib


def main():
    client = logdb.Client(sys.argv[1].split(','))

    tags = dict()
    for argv in sys.argv[3:]:
        k, v = argv.split('=')
        tags[k] = v

    chksum = ''
    for r in client.tail(int(sys.argv[2]), tags):
        if 'blob' in r:
            blob = r.pop('blob', b'')
            if blob:
                x = hashlib.md5(blob).hexdigest()
                chksum += x
                y = hashlib.md5(chksum.encode()).hexdigest()
                res = 'log({}) blob({}) seq({}) len({})'.format(
                    y, x, r['seq'], len(blob))
                sys.stderr.write(res + '\n')
        else:
            time.sleep(1)


if '__main__' == __name__:
    main()
