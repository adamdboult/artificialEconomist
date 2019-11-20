######################
# CONVERT PDF TO TXT #
######################
mkdir -p ./raw_TXT/


#########
# First #
#########
for filename in ./econstor_PDF/*.pdf; do
    name=$(basename "$filename")
    nameNoExt=$(basename "$filename" ".pdf")
    echo "Converting $name..."
    pdftotext "./PDF_econstor/$name" "./TXT_raw/$nameNoExt.txt"
done

#############
# Do others #
#############
for filename in ./PDF_manual/*.pdf; do
    name=$(basename "$filename")
    nameNoExt=$(basename "$filename" ".pdf")
    echo "Converting $name..."
    pdftotext "./PDF_manual/$name" "./TXT_raw/$nameNoExt.txt"
done

