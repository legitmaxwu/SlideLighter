import ConceptMapGenerator
import network
import FirstPDFProcessing
import ProcessPDF


FirstPDFProcessing.CreateJPEGS("test_cal")
links = ["https://i.imgur.com/hdhj414.jpg", "https://i.imgur.com/eRJ6EVw.jpg", "https://i.imgur.com/unf79Cg.jpg", "https://i.imgur.com/Bp4tKwH.jpg", "https://i.imgur.com/7mQ7TOC.jpg", "https://i.imgur.com/Qir2jMM.jpg", "https://i.imgur.com/ntD8iUs.jpg", "https://i.imgur.com/zX8SxAY.jpg", "https://i.imgur.com/VM7fPvW.jpg", "https://i.imgur.com/jO6bjwN.jpg", "https://i.imgur.com/MfL9F1P.jpg"]
ProcessPDF.parse_pdf("../samples/test_cal.pdf")
network.start(links)