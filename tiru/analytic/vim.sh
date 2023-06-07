#!\bash\bin

pytest -p no:warnings --verbose --tb=short \
    $tirud/analytic/test_analytic.py::test_newton
