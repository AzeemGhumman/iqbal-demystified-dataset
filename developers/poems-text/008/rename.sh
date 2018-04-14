for name in 3_*
do
    newname=8"$(echo "$name" | cut -c2-)"
    # echo "$newname"
    mv "$name" "$newname"
done
