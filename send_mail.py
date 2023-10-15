

def mail_box(message):
    import win32com.client as client
    import pythoncom
    outlook=client.gencache.EnsureDispatch("Outlook.Application",pythoncom.CoInitialize())
    message=outlook.CreateItem(0)
    message.Display()
    message.Subject="Mail from Arjun"
    message.Body="""Hiii"""
    message.Save()
