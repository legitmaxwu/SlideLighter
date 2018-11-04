import ProcessPDF as Process
import ProcessUser


Process.parse_pdf("../samples/testlist.pdf")
ProcessUser.FindSelectedElements((0.1,0.1,0.5,0.5),1,"test")