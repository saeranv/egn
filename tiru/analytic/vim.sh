#!\bash\bin

pytest -p no:warnings --verbose $tirud/analytic/test_analytic.py::test_newton
