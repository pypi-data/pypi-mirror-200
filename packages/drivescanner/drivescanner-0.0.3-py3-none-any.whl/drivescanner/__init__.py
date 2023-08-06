# the xlrd version (1.2.0) used in Textractplus is unable to handle .xlsx files with the standard settings, below code fixes that problem
# source: https://stackoverflow.com/questions/64264563/attributeerror-elementtree-object-has-no-attribute-getiterator-when-trying
import xlrd
xlrd.xlsx.ensure_elementtree_imported(False, None)
xlrd.xlsx.Element_has_iter = True

from drivescanner.file_index import *
from drivescanner.scan import *
from drivescanner.evaluate import *