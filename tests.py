# example usage:
# build all neutral tests (from megamol build directory/tests):
# tests.py ..\examples --generate-neutral-test
# build & install megamol to copy them over
# generate all references (from installed megamol bin dir):
# ..\tests\tests.py ..\tests --generate-reference
# run tests (from installed megamol bin dir):
# ..\tests\tests.py ..\tests

import argparse
import os
import os.path
import pathlib
from PIL import Image
from SSIM_PIL import compare_ssim
import subprocess
from collections import Counter
from report_data import *
from datetime import date

parser = argparse.ArgumentParser(usage="%(prog)s <DIRECTORY>", description="execute test scripts in DIRECTORY")
parser.add_argument('directories', nargs="*")
parser.add_argument('--generate-reference', action='count', help='Generate reference pngs instead of testing against them')
parser.add_argument('--generate-neutral-test', action='count', help='Generate a first basic test (.1) for all found projects. Supply, e.g., the MegaMol build/examples folder as argument to generate a build/tests folder.')
parser.add_argument('--force', action='count', help='force overwriting files')
parser.add_argument('--dry-run', action='count', help='only print actions without performing them')
args = parser.parse_args()

RESULT_NAME = 'result.png'
if os.name == 'nt':
    EXECUTABLE = 'megamol.exe'
    SHELL = False
else: 
    EXECUTABLE = './megamol.sh'
    SHELL = True

IMPORT_PREFIX = '--MM_TEST_IMPORT '
testresults = []
CAPTURE_STDOUT = True
CAPTURE_STDERR = False

ssim_threshold = 0.95
class TestResult:
    testfile: str
    passed: bool
    result: str

def test_to_output(entry_path):
    file_name_only, _ = os.path.splitext(entry_path)
    return file_name_only + ".png", file_name_only + ".stdout", file_name_only + ".stderr", file_name_only + ".failure.png"

def compare_images(reference, result):
    with Image.open(reference) as reference_image:
        with Image.open(result) as result_image:
            ssim_score = compare_ssim(reference_image, result_image, GPU=False)
            return ssim_score

def dump_output(basedir, compl, stdoutname, stderrname, imagename, referencename, tr, reportstring, details = ""):
    if compl != None and not tr.passed:
        if CAPTURE_STDOUT:
            with open(stdoutname, "w") as outfile:
                outfile.write(compl.stdout.decode('utf-8'))
        if CAPTURE_STDERR:
            with open(stderrname, "w") as outfile:
                outfile.write(compl.stderr.decode('utf-8'))
    os.replace(RESULT_NAME, imagename)

    reportstring += f"""
<button class="test coloredblock{' failed' if not tr.passed else ''}">{tr.testfile}: {tr.result}</button>
<div class="testcontent coloredblock">
  <p></p>
  <table width="90%">
    <tr><td width="43%">Reference</td><td width="4%">&nbsp;</td><td width="43%">Result</td></tr>
    <tr><td><img src="{os.path.relpath(referencename, basedir)}" width="100%"/></td><td/><td><img src="{os.path.relpath(imagename, basedir)}" width="100%"/></td></tr>
    <tr><td width="43%">Difference</td><td width="4%">&nbsp;</td><td width="43%"></td></tr>
    <tr><td><div class="img-diff-container">
      <img src="{os.path.relpath(referencename, basedir)}" class="img-diff-reference" />
      <img src="{os.path.relpath(imagename, basedir)}" class="img-diff-result" />
    </div></td></tr>
  </table>
  <button class="coloredblock output">stdout</button>
  <div class="outputcontent">
      <pre>{compl.stdout.decode('utf-8') if compl != None else details}</pre>
  </div>
  <button class="coloredblock output">stderr</button>
  <div class="outputcontent">
      <pre>{compl.stderr.decode('utf-8') if compl != None else "&nbsp;"}</pre>
  </div>
</div>
    """
    return reportstring

if not args.directories:
    print("need at least one input directory")
    exit(1)

if args.generate_neutral_test:
    for directory in args.directories:
        parent = os.path.abspath(os.path.join(directory, os.pardir))
        for subdir, dirs, files in os.walk(directory, topdown=True):
            relpath = os.path.relpath(subdir, parent)
            pp = list(pathlib.Path(relpath).parts)
            pp[0] = "tests"
            pp.insert(1, "projects")
            testfolder = pathlib.Path(os.sep.join(map(str,pp)))
            #print(f"I am in subdir {relpath} of dir {parent} and test files would go to {testfolder}")
            for file in files:
                #print (f"I got file {file} and subdir {subdir}")
                entry = os.path.join(subdir, file)
                if entry.endswith('.lua'):
                    name, _ = os.path.splitext(file)
                    out = os.path.join(parent, testfolder, name + ".1.lua")
                    if args.dry_run:
                        print(f"I would make {out} from {entry}")
                    outpath = os.path.join(parent, testfolder)
                    if not os.path.isdir(outpath):
                        if args.dry_run:
                            print(f"making directory {outpath}")
                        else:
                            os.makedirs(outpath)
                    if not os.path.isfile(out) or args.force:
                        print(f"making neutral test {out}")
                        if not args.dry_run:
                            with open(out, "w") as outfile:
                                outfile.write(f"{IMPORT_PREFIX} {os.path.relpath(entry, os.path.dirname(out))}\n")
                                outfile.write('mmSetGUIVisible(false)\nmmRenderNextFrame()\nmmRenderNextFrame()\nmmScreenshot("result.png")\nmmQuit()\n')
    exit(0)

num_found_tests = 0

for directory in args.directories:
    report_string = report_top
    report_string += f"""
<h2>MegaMol regression test report:{directory} {date.today()}</h2>
<p>
SSIM Threshold <input type="number" step="0.01" name="SSIM_Threshold" value="0.98">
</p>
    """
    report_path = os.path.join(directory, "report.html")
    for subdir, dirs, files in os.walk(directory, topdown=True):
        for file in files:
            entry = os.path.join(subdir, file)
            if entry.endswith('.lua'):
                with open(entry) as infile:
                    lines = infile.readlines()
                    deps = []
                    for line in lines:
                        if line.startswith(IMPORT_PREFIX):
                            dep = line[len(IMPORT_PREFIX):].strip()
                            #print(f"state: dir {directory} subdir {subdir} dep {dep}")
                            deps.append(os.path.abspath(os.path.join(subdir, dep).replace("\\","/")))
                            #print(f"found test for {deps}: {entry}")
                    commandline = f"{EXECUTABLE} --nogui " + ' '.join(deps) + ' ' + entry
                    refname, stdoutname, stderrname, imgname = test_to_output(entry)
                    if args.dry_run:
                        print(f"would exec: {commandline}")
                        print(f"would expect same result as {refname}, stdout {stdoutname}, stderr {stderrname}")
                        continue
                    if os.path.isfile(RESULT_NAME):
                        os.remove(RESULT_NAME)
                    if os.path.isfile(imgname):
                        os.remove(imgname)
                    if os.path.isfile(report_path):
                        os.remove(report_path)
                    if CAPTURE_STDOUT and os.path.isfile(stdoutname):
                        os.remove(stdoutname)
                    if CAPTURE_STDERR and os.path.isfile(stderrname):
                        os.remove(stderrname)
                    if args.generate_reference and not args.force and os.path.isfile(refname):
                        print(f"skipping test {entry}.")
                        continue
                    print(f"running test {entry}... ", end='')
                    num_found_tests = num_found_tests + 1
                    tr = TestResult()
                    tr.testfile=entry
                    tr.passed=True
                    try:
                        compl = subprocess.run(commandline, capture_output=True, check=True, shell=SHELL)
                        if args.generate_reference:
                            try:
                                if args.force:
                                    os.replace(RESULT_NAME, refname)
                                else:
                                    os.rename(RESULT_NAME, refname)
                                print('generated reference')
                            except OSError as exception:
                                print(f'could not move {RESULT_NAME} to {refname}: {exception}')
                        else:
                            if not os.path.isfile(RESULT_NAME):
                                print('failed')
                                tr.passed = False
                                tr.result = "no output generated"
                                testresults.append(tr)
                                continue
                            if not os.path.isfile(refname):
                                print('failed')
                                tr.passed = False
                                tr.result = "missing reference image"
                                testresults.append(tr)
                                continue
                            try:
                                ssim = compare_images(refname, RESULT_NAME)
                                tr.result = f'SSIM = {ssim}'
                                if ssim > ssim_threshold:
                                    print(f'passed ({ssim})')
                                else:
                                    print(f'failed ({ssim})')
                                    tr.passed = False
                                report_string = dump_output(directory, compl, stdoutname, stderrname, imgname, refname, tr, report_string)
                                testresults.append(tr)

                            except Exception as exception:
                                tr.result = exception
                                tr.passed = False
                                testresults.append(tr)
                                print(f'unexpected exception: {exception}')
                                report_string = dump_output(directory, compl, stdoutname, stderrname, imgname, refname, tr, report_string)


                    except subprocess.CalledProcessError as exception:
                        print(f"failed running command line '{commandline}'':")
                        print(f"{exception}")
                        print(f"{exception.stdout.decode('utf-8')}")
                        tr.passed = False
                        tr.result = "program exception"
                        testresults.append(tr)
                        report_string = dump_output(directory, None, stdoutname, stderrname, imgname, refname, tr, report_string, exception.stdout.decode('utf-8'))
                        #exit(1)
    report_string += report_bottom
    if not args.generate_reference and not args.dry_run:
        with open(report_path, "w", encoding="utf-8") as reportfile:
            reportfile.write(report_string)


if args.generate_reference or args.dry_run:
    exit(0)

num_passed_tests = 0
if len(testresults) > 0:
    print("\nRecap:")
    for tr in testresults:
        print(f'{tr.testfile}: {"passed" if tr.passed else "failed"}, {tr.result}')
        if tr.passed:
            num_passed_tests = num_passed_tests + 1
    histo = Counter(tr.result for tr in testresults if tr.passed==False)
    for k,v in histo.items():
        print(f"{k}: {v}")
    print(f"\nSummary: {num_passed_tests}/{num_found_tests} tests passed")
else:
    print("no tests found.")
