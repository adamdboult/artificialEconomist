######################
# CONVERT PDF TO TXT #
######################
mkdir -p ./raw_TXT/


#########
# First #
#########
for filename in ./PDF/*.pdf; do
    name=$(basename "$filename")
    nameNoExt=$(basename "$filename" ".pdf")
    echo "Converting $name..."
    pdftotext "./PDF/$name" "./raw_TXT/$nameNoExt.txt"
done

#############
# Do others #
#############
for filename in ./manual_PDF/*.pdf; do
    name=$(basename "$filename")
    nameNoExt=$(basename "$filename" ".pdf")
    echo "Converting $name..."
    pdftotext "./manual_PDF/$name" "./raw_TXT/$nameNoExt.txt"
done

