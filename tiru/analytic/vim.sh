#!\bash\bin

pytest -p no:warnings --show-capture=stdout $tirud/analytic/test_analytic.py::test_newton
