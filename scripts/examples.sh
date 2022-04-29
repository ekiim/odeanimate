#!/bin/sh
echo "Runing Examples"
REPORT_DIR=html/
mkdir -p ${REPORT_DIR}
ERROR=""
ERROR_FILES=""
while read f ; do 
    echo "== Example: $f"
    coverage run $f
    [[ $? -ne 0 ]] && ERROR="ERROR" && ERROR_FILES="${ERROR_FILES}\n$f"
    coverage html -d ${REPORT_DIR}$(echo $f | sed -e "s/.py//g") \
        --title="Coverage Report"
    echo -e "\n\n==========\n"
done < <(ls -1 examples/*.py )
echo -e "\n\n"
[[ "$ERROR" == "ERROR" ]] \
    && echo -e "Found errors the following files: \n$ERROR_FILES" \
    && exit 1
echo "Done with no errors."
exit 0