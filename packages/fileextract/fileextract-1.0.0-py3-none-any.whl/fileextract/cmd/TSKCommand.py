from string import Template

class TSKCommand():
    FLS = Template("fls -r -p -o $offset $path")
    FCAT = Template("fcat -o $offset $filePath $imgPath")