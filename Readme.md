This is the repository for MegaMol regression tests.

### Requirements
Regression testing requires Python 3, pillow and SSIM-PIL

### Generation of examples tests
The basic tests rely on the MegaMol examples and on them being enabled in CMake. They can be generated (also incrementally) using the ``tests.py`` script. From a valid build directory, navigate to ``tests/`` and run
```
python tests.py ..\examples --generate-neutral-test
```
The basic tests go into ``tests/projects`` and mirror the directory structure of ``examples``. They have the same name as the example they refer to, but are numbered, so multiple tests can be stored for each example, varying parameters or the like. They will be installed alongside them, and use an internal reference pointing to the corresponding example in the form ``--MM_TEST_IMPORT  ../examples/testspheres.lua`` in the first line. Both files are then executed incrementally, so for the preceding example, the test script will load ``<install_dir>/examples/testspheres.lua`` and then ``<install_dir>/tests/projects/testspheres.1.lua``. Note that the path separator will depend on the OS you generate the test on, but will be automatically translated to the current OS when the test is executed.

### Generation of reference images
Build & install MegaMol, this will install the tests as well.
Change to your installation/bin directory and use
```
python ..\tests\tests.py ..\tests --generate-reference
```
to generate the reference images. They will be placed next to the installed tests. Check them and move the correct ones to the correct place in ```build/tests/projects```, where you can stage and commit them.

### Running tests
Build & install MegaMol, this will install the tests as well.
Change to your installation/bin directory and use
```
python ..\tests\tests.py ..\tests
```
This will output individual results and a summary.
