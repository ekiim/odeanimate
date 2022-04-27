#!/bin/sh
echo "Runing Examples"
REPORT_DIR=html/
mkdir -p ${REPORT_DIR}
ERROR=""
ERROR_FILES=""
while read f ; do 
    echo $f
    coverage run $f
    [[ $? -ne 0 ]] && ERROR="ERROR" && ERROR_FILES="${ERROR_FILES}\n$f"
    coverage html -d ${REPORT_DIR}$(echo $f | sed -e "s/.py//g") \
        --title="Coverage Report"
done < <(ls -1 examples/*.py )

echo -e "\n\n"
[[ "$ERROR" == "ERROR" ]] \
    && echo -e "Found errors the following files: \n$ERROR_FILES" \
    && exit 1
exit 0