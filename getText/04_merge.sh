###############
# CONCATENATE #
###############
echo "Concatenating..."
cat ./clean_TXT/*.txt > ./merged_file.txt

##############
# CLEAN FILE #
##############
echo "Cleaning..."
grep . ./merged_file.txt > merged_file_clean.txt
iconv -f utf-8 -t ascii//TRANSLIT merged_file_clean.txt > merged_file_clean_2.txt

