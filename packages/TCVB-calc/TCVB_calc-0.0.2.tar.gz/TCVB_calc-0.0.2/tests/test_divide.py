import TCVB_calc.calc_main as cc

def test_multiply():
    test_var=cc.Calculator(12)
    test_var.multiply(-3)
    assert test_var.result==-36
    