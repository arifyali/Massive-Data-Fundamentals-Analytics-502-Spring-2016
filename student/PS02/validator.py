#!/usr/bin/env python
#
# validate student submission


import sys,zipfile,os,os.path

required = ["answer.txt"]
required += ["report%d.py" % i for i in range(1,5)]
required += ["report%d.txt" % i for i in range(1,5)]
optional = []
optional += ["join%d.py" % i for i in range(1,5)]
optional += ["join%d.txt" % i for i in range(1,5)]

from subprocess import Popen,PIPE,call

def build_zip(fname):
    required_missing = 0
    print("Building {0}".format(fname))
    z = zipfile.ZipFile(fname,"w",zipfile.ZIP_DEFLATED)
    for fn in required+optional:
        if os.path.exists(fn):
            print("Adding {0}...".format(fn))
            z.write(fn)
        else:
            if fn in required:
                msg = "REQUIRED FILE "
                required_missing += 1
            else:
                msg = ""
            print("{0}Not found {1}...".format(msg,fn))
            
    z.close()
    print("Done!\n\n")
    call(['ls','-l',fname])
    print("\n")
    call(['unzip','-l',fname])
    if required_missing > 0:
        print("\n*** REQUIRED FILES MISSING: {0} ***".format(required_missing))
    exit(0)


def validate_file(z,fname,fbase,hook):
    import py_compile
    # Get the file contents
    contents = z.open(fname).read()


    # Unpack if the file is python or if we have a hook
    # If python file, see if it compiles
    if fbase.endswith(".py") or hook:
        fnew = "unpack/"+fbase
        with open(fnew,"w") as fb:
            fb.write(contents)

    # Verify python correctness if it is a python file
    if fbase.endswith(".py"):
        try:
            py_compile.compile(fnew)
        except py_compile.PyCompileError as e:
            print("Compile error: "+str(e))
            errors += 1

    # If this is a text file, complain if it is RTF
    if fname.endswith(".txt") and contents.startswith(r"{\rtf"):
        print("*** {0} is a RTF file; it should be a text file".format(fname))
        errors += 1

    if hook:
        hook(fbase,fnew)


def validate(zfile,hook=None):
    try:
        os.mkdir("unpack")
    except OSError as e:
        pass
    required_count = 0
    optional_count = 0
    errors = 0
    print("Validating {0} ...\n".format(zfile))
    z = zipfile.ZipFile(zfile)
    for p in ('required','optional','unwanted'):
        for f in z.filelist:
            fname = f.orig_filename
            fbase = os.path.basename(fname)
            if fbase in required and p=='required':
                print("Required file {0} present.".format(fbase))
                required.remove(fbase)
                validate_file(z,fname,fbase,hook)
                continue
            if fbase in optional and p=='optional':
                print("Optional file: {0} present.".format(fbase))
                optional.remove(fbase)
                validate_file(z,fname,fbase,hook)
                continue
            if p=='unwanted':
                print("Unwanted file: {0}".format(fname))
                errors += 1

    print("")
    if required:
        print("MISSING REQUIRED FILES: "+" ".join(required))
        errors += len(required)
    if optional:
        print("MISSING OPTIONAL FILES: "+" ".join(optional))
    if errors:
        print("TOTAL ERRORS: {0}".format(errors))
    return(errors)


if __name__=="__main__":

    fname = PS+".zip"           # default file name
    if len(sys.argv)>1:
        if sys.argv[1]=="--zip":
            build_zip(fname)
        fname = sys.argv[1]
    code = validate(fname)
    exit(code)

