This is the repository for MegaMol regression tests.

### Requirements
Regression testing requires Python 3, pillow and SSIM-PIL

### Generation of examples tests
The basic tests rely on the MegaMol examples and on them being enabled in CMake. They can be generated (also incrementally) using the ``tests.py`` script. From a valid build directory, navigate to ``tests/`` and run
```
python tests.py ..\examples --generate-neutral-test
```
The basic tests go into ``tests/projects`` and mirror the directory structure of ``examples``. They have the same name as the example they refer to, but are numbered, so multiple tests can be stored for each example, varying parameters or the like. They will be installed alongside them, and use an internal reference pointing to the corresponding example in the form ``--MM_TEST_IMPORT  ../examples/testspheres.lua`` in the first line. Both files are then executed incrementally, so for the preceding example, the test script will load ``<install_dir>/examples/testspheres.lua`` and then ``<install_dir>/tests/testspheres.1.lua``.



# build all neutral tests (from megamol build directory/tests):
# tests.py ..\examples --generate-neutral-test
# build & install megamol to copy them over
# generate all references (from installed megamol bin dir):
# ..\tests\tests.py ..\tests --generate-reference
# run tests (from installed megamol bin dir):
# ..\tests\tests.py ..\tests