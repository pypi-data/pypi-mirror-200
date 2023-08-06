To run the python tests, do `make check` in the top contur directory.


How to update the reference data
================================

If the regressions tests are failing because of a change which means
the reference data need updating, here's how to do that.

For the single yoda file regression
-----------------------------------

In the `tests/sources/tmp` is a folder `single` and file `Summary.txt`

`Summary.txt` is the target for the theory regression test. Update `single_yoda_theory.txt` in `sources`
(base file for theory regression) to be this file. (note change the name of `Summary.txt`
to `single_yoda_theory.txt`).

For the non-theory regression, in the `single` folder, you will see another `Summary.txt` file.
This is the target for the non-theory single yoda regression. Update `single_yoda_run.txt` in `sources`
(base result) with this file (again, note the rename).

For the grid runs
-----------------

By default the targets for these are deleted at the end of our tests, so use `make check-keep` instead of `make check` to stop this.

After this you will have a `tmp` folder in the tests folder after your run.

This folder will contain `contur.map` (target results for non-theory run) and `contur_theory.map`
(target results for theory run). You can then update the base map files in the `sources` folder to be
these target files.

Likewise, for the yodastream test:

```
tests/sources/tmp/yodastream_results.pkl tests/sources/yodastream_results_dict.pkl
```

Contur export
-------------
Currently this exports the existing source `contur.map`, so you need to separately update `contur.csv` after having rerun with the above updates.
