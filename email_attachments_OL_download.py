#!/usr/bin/env python
# coding: utf-8

# In[1]:


import imaplib
import base64
import os
import email
import imap_tools
from imap_tools import MailBox


# In[56]:


#typ, data = mail.search(None, '(SINCE "01-Jan-2021")')


# In[1]:


import win32com.client
import os
from datetime import datetime, timedelta


# In[12]:


outlook = win32com.client.Dispatch('outlook.application')
mapi = outlook.GetNamespace("MAPI")
#for account in mapi.Accounts:
#    print(account.DeliveryStore.DisplayName)


# In[13]:


inbox = mapi.GetDefaultFolder(6)


# In[14]:


messages = inbox.Items
received_dt = datetime.now() - timedelta(days=7)
received_dt = received_dt.strftime('%m/%d/%Y %H:%M %p')
messages = messages.Restrict("[ReceivedTime] >= '" + received_dt + "'")
messages = messages.Restrict("[SenderEmailAddress] = 'XXXX@gmail.com'")
messages = messages.Restrict("[Subject] = '[EXTERNAL] Fwd: Expense Report'")


# In[49]:


outputDir = r"\\BLRESGANALXXXX\XXXXX\attachment_download"

#mydir = os.path.join(outputDir,datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
#os.makedirs(mydir)
#date=datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
try:
    for message in list(messages):
        try:
            s = message.sender
            for attachment in message.Attachments:
                attachment.SaveASFile(os.path.join(outputDir,attachment.FileName))
                print(f"attachment {attachment.FileName} from {s} saved")
        except Exception as e:
            print("error when saving the attachment:" + str(e))
except Exception as e:
    print("error when processing emails messages:" + str(e))

