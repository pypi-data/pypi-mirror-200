import TCVB_calc.calc_main as cc

def test_end_to_end():
    test_var=cc.Calculator(1)
    test_var.add(90)
    test_var.reset()
    test_var.subtract(-25.0)
    test_var.multiply(1.0)
    test_var.divide(5.0)
    test_var.multiply(25.0)
    test_var.n_root(3.0)
    assert test_var.result==5.0