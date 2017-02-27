#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys
from xltestview.XLTestViewClientUtil import XLTestViewClientUtil

if xltestServer is None:
    print "No server provided."
    sys.exit(1)

xlt_client = XLTestViewClientUtil.create_XL_TestView_client(xltestServer, username, password)

xlt_client.check_xltestview_version()

test_spec_qualification = xlt_client.get_test_specification_qualification(testSpecificationName)
if test_spec_qualification:
    sys.exit(0)
else:
    sys.exit(1)
