# -*- coding: utf-8 -*-
import time
from celeries import app
from tasks import add, mul, xsum, f

if __name__ == '__main__':

    # r = add.delay(4, 4)
    # print(r.state, r.get())

    r = f.delay('x', 3)
    for i in range(6):
        time.sleep(1)
        print(i+1, 's', r.state)

    r1 = app.AsyncResult(r.id)
    r2 = app.AsyncResult('this-id-does-not-exits')
    print(r.id, r1.state)
    print('this-id-does-not-exits', r2.state)
