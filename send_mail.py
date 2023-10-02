

# def mail_box(message):
import win32com.client as client
outlook=client.gencache.EnsureDispatch("Outlook.Application")
message=outlook.CreateItem(0)
message.Display()
message.Subject="Mail from Gangadhar"
message.Body="""
********** SUMMARY **********\n
+-----------------+----------------------------------+---------------+
| Ottmar Hitzfeld | Borussia Dortmund, Bayern Munich | 1997 and 2001 |
+-----------------+----------------------------------+---------------+"""
message.Save()
