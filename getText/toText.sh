######################
# CONVERT PDF TO TXT #
######################
mkdir -p ./TXT/

for filename in ./PDF/*.pdf; do
    name=$(basename "$filename")
    nameNoExt=$(basename "$filename" ".pdf")
    echo "Converting $name..."
    pdftotext "./PDF/$name" "./TXT/$nameNoExt.txt"
done

###############
# CONCATENATE #
###############
echo "Concatenating..."
cat ./TXT/*.txt > ./merged_file.txt

##############
# CLEAN FILE #
##############
echo "Cleaning..."
grep . ./merged_file.txt > merged_file_clean.txt
iconv -f utf-8 -t ascii//TRANSLIT merged_file_clean.txt > merged_file_clean_2.txt

