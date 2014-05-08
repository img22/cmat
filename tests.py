from PersonalData import PdfPersonalData, ImgPersonalData

pd = PdfPersonalData('cmat-test/pdf-test.pdf')
imgPd = ImgPersonalData('cmat-test/face-test.pdf')
imgPd.pdata.blurAll()