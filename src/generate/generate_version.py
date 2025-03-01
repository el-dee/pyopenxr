# This script creates an updated version of xr/version.py

import re
import inspect
import xrg

# These variables are filled in by cmake's configure_file process
try:
    pyopenxr_patch = int("@PYOPENXR_VERSION_PATCH_INCREMENTAL@")
except ValueError:
    pyopenxr_patch = 1

try:
    pyopenxr_suffix = "@PYOPENXR_VERSION_SUFFIX@"
except ValueError:
    pyopenxr_suffix = ""

file_string = xrg.get_header_as_string()

# We expect a line in openxr.h like
#   "#define XR_CURRENT_API_VERSION XR_MAKE_VERSION(1, 0, 17)"
version_match = re.search(
    r"define XR_CURRENT_API_VERSION XR_MAKE_VERSION\((\d+), (\d+), (\d+)\)", file_string
)

major = int(version_match.group(1))
minor = int(version_match.group(2))
patch = int(version_match.group(3))
# funny way to merge two different patch numbers
patch2 = 100 * patch + pyopenxr_patch

print("# Warning: this file is automatically generated. Do not edit.\n")
print(
    inspect.cleandoc(
        f'''
    # pyopenxr version is based on openxr version...
    # except the patch number is:
    #   100 * openxr patch number + pyopenxr patch number

    XR_VERSION_MAJOR = {major}
    XR_VERSION_MINOR = {minor}
    XR_VERSION_PATCH = {patch}
    XR_CURRENT_API_VERSION_STRING = "{major}.{minor}.{patch}"

    PYOPENXR_VERSION_MAJOR = {major}
    PYOPENXR_VERSION_MINOR = {minor}
    PYOPENXR_VERSION_PATCH = {patch2}
    PYOPENXR_VERSION_PATCH_INCREMENTAL = {pyopenxr_patch}
    PYOPENXR_VERSION_SUFFIX = "{pyopenxr_suffix}"
    PYOPENXR_VERSION = "{major}.{minor}.{patch2}{pyopenxr_suffix}"


    class Version(object):
        def __init__(self, major: int = 0, minor: int = None, patch: int = None):
            if minor is None and patch is None and major > 0xffff:
                # major argument is actually a packed xr.VersionNumber
                patch = major & 0xffffffff
                minor = (major >> 32) & 0xffff
                major = (major >> 48) & 0xffff
            if minor is None:
                minor = 0
            if patch is None:
                patch = 0
            self.major = major
            self.minor = minor
            self.patch = patch
    
        def number(self) -> int:
            """Packed xr.VersionNumber"""
            return ((self.major & 0xffff) << 48) | ((self.minor & 0xffff) << 32) | (self.patch & 0xffffffff)
    
        def __str__(self):
            return f"{{self.major}}.{{self.minor}}.{{self.patch}}"


    XR_CURRENT_API_VERSION = Version(XR_VERSION_MAJOR, XR_VERSION_MINOR, XR_VERSION_PATCH)
    PYOPENXR_CURRENT_API_VERSION = Version(
        PYOPENXR_VERSION_MAJOR,
        PYOPENXR_VERSION_MINOR,
        PYOPENXR_VERSION_PATCH
    )
    
    
    __version__ = PYOPENXR_VERSION
    
    __all__ = [
        "PYOPENXR_CURRENT_API_VERSION",
        "PYOPENXR_VERSION_MAJOR",
        "PYOPENXR_VERSION_MINOR",
        "PYOPENXR_VERSION_PATCH",
        "PYOPENXR_VERSION_PATCH_INCREMENTAL",
        "PYOPENXR_VERSION_SUFFIX",
        "PYOPENXR_VERSION",
        "Version",
        "XR_CURRENT_API_VERSION",
        "XR_VERSION_MAJOR",
        "XR_VERSION_MINOR",
        "XR_VERSION_PATCH",
    ]
    '''
    )
)
