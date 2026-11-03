"""Credit card payoff math for the sx02 Short (shared by the Short and its Manim chart).

Balance $5,000 at the average card rate (ep04: Fed G.19 'all accounts' rate, CC_NOW). Minimum payment: interest + 1% of
the balance, $25 floor (a common card-agreement formula); compared with a fixed $200 a month. Monthly compounding of
APR/12, no new purchases, no fees.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
_argv, sys.argv = sys.argv, [sys.argv[0]]
import ep04_fed as _F  # noqa: E402
sys.argv = _argv

APR = _F.CC_NOW / 100
BAL = 5000.0


def payoff(rule):
    bal, m, paid, path, first = BAL, 0, 0.0, [BAL], None
    while bal > 0.005 and m < 2000:
        i = bal * APR / 12
        p = min(rule(bal, i), bal + i)
        if first is None:
            first = (p, i)
        bal = bal + i - p
        paid += p
        m += 1
        path.append(max(bal, 0))
    return dict(months=m, interest=paid - BAL, path=path, first=first)


MIN = payoff(lambda b, i: max(25.0, i + 0.01 * b))
FIX = payoff(lambda b, i: 200.0)

if __name__ == '__main__':
    out = os.path.join(HERE, 'assets', 'gen', 'sx02', 'payoff.json')
    json.dump({'apr': APR, 'min': MIN, 'fix': FIX}, open(out, 'w'))
    print(f"APR {APR:.4f}  min: {MIN['months']} mo ({MIN['months']/12:.1f} y) interest ${MIN['interest']:,.0f} "
          f"first ${MIN['first'][0]:.2f} (interest ${MIN['first'][1]:.2f})  |  $200: {FIX['months']} mo "
          f"({FIX['months']/12:.1f} y) interest ${FIX['interest']:,.0f}")
