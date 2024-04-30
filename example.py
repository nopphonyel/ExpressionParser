import random
import math
from expression_parser import SimpleParser

test_eval = [
    "(กะเพราไข่ดาว*2)*50/100",
    "random_var/(-2.00)"
]


def randomness():
    r = random.randint(0, 1000)
    return math.sin(r * 0.01 * math.pi)


expb = SimpleParser()
expb.define(var_name='a', callback=lambda: 3)
random_var = randomness()
expb.define(var_name='random_var', callback=randomness)
expb.define(var_name="กะเพราไข่ดาว", callback=lambda: 60)

for expression in test_eval:
    print(expression)
    expb_eval_res = expb.eval(expression)
    print("expb: %f" % expb_eval_res)

# eval('('*1000 + '1' + ')'*1000)
